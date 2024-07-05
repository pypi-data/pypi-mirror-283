## overload the EnvBuilder class to :
# the root folder will be prefixed the env $ISC_PACKAGE_INSTALLDIR
# 1. make the default folders of the virtual environment to be:
#    1.1 bin : $ISC_PACKAGE_INSTALLDIR/bin
#    1.2 lib : $ISC_PACKAGE_INSTALLDIR/mgr/python
#    1.3 include : $ISC_PACKAGE_INSTALLDIR/bin
# 2. change the default interpreter to $ISC_PACKAGE_INSTALLDIR/bin/irispython

import logging
import os
import shutil
import subprocess
import sys
import sysconfig
import types

from venv import EnvBuilder

CORE_VENV_DEPS = ('pip', 'setuptools')
logger = logging.getLogger(__name__)

class IrisEnvBuilder(EnvBuilder):

    use_irispython: bool = False
    isc_package_installdir: str

    def __init__(self, system_site_packages=False, clear=False,
                 symlinks=False, upgrade=False, with_pip=False, prompt=None,
                 upgrade_deps=False, isc_package_installdir=None, use_irispython=False):
        super().__init__(system_site_packages=system_site_packages, clear=clear,
                         symlinks=symlinks, upgrade=upgrade, with_pip=with_pip,
                         prompt=prompt, upgrade_deps=upgrade_deps)
        self.isc_package_installdir = None
        self.use_irispython = use_irispython
        # raise an error if the $ISC_PACKAGE_INSTALLDIR is not set in env 
        # or not present in kwargs
        if 'ISC_PACKAGE_INSTALLDIR' in os.environ:
            self.isc_package_installdir = os.environ['ISC_PACKAGE_INSTALLDIR']
        elif isc_package_installdir:
            self.isc_package_installdir = isc_package_installdir
        else:
            raise ValueError('The $ISC_PACKAGE_INSTALLDIR is not set in env or not present in args')

    # force sys._base_executable to be the irispython interpreter
    def ensure_directories(self, env_dir):
        """
        Create the directories for the environment.

        Returns a context object which holds paths in the environment,
        for use by subsequent logic.
        """

        def create_if_needed(d):
            if not os.path.exists(d):
                os.makedirs(d)
            elif os.path.islink(d) or os.path.isfile(d):
                raise ValueError('Unable to create directory %r' % d)

        if os.path.exists(env_dir) and self.clear:
            self.clear_directory(env_dir)
        context = types.SimpleNamespace()
        context.env_dir = env_dir
        context.env_name = os.path.split(env_dir)[1]
        prompt = self.prompt if self.prompt is not None else context.env_name
        context.prompt = '(%s) ' % prompt
        create_if_needed(env_dir)

        executable = sys._base_executable
        # change the default interpreter to irispython if use_irispython is True
        if self.use_irispython:
            if os.name != 'nt':
                executable = os.path.join(self.isc_package_installdir, 'bin', 'irispython')
            else:
                executable = os.path.join(self.isc_package_installdir, 'bin', 'irispython.exe')
        
        dirname, exename = os.path.split(os.path.abspath(executable))
        context.executable = executable
        context.python_dir = dirname
        context.python_exe = exename
        if sys.platform == 'win32':
            binname = 'Scripts'
            incpath = 'Include'
            libpath = os.path.join(env_dir, 'Lib', 'site-packages')
        else:
            binname = 'bin'
            incpath = 'include'
            libpath = os.path.join(env_dir, 'lib',
                                   'python%d.%d' % sys.version_info[:2],
                                   'site-packages')
        context.inc_path = path = os.path.join(env_dir, incpath)
        create_if_needed(path)
        create_if_needed(libpath)
        # Issue 21197: create lib64 as a symlink to lib on 64-bit non-OS X POSIX
        if ((sys.maxsize > 2**32) and (os.name == 'posix') and
            (sys.platform != 'darwin')):
            link_path = os.path.join(env_dir, 'lib64')
            if not os.path.exists(link_path):   # Issue #21643
                os.symlink('lib', link_path)
        context.bin_path = binpath = os.path.join(env_dir, binname)
        context.bin_name = binname
        context.env_exe = os.path.join(binpath, exename)
        create_if_needed(binpath)
        # Assign and update the command to use when launching the newly created
        # environment, in case it isn't simply the executable script (e.g. bpo-45337)
        context.env_exec_cmd = context.env_exe
        if sys.platform == 'win32':
            # bpo-45337: Fix up env_exec_cmd to account for file system redirections.
            # Some redirects only apply to CreateFile and not CreateProcess
            real_env_exe = os.path.realpath(context.env_exe)
            if os.path.normcase(real_env_exe) != os.path.normcase(context.env_exe):
                logger.warning('Actual environment location may have moved due to '
                               'redirects, links or junctions.\n'
                               '  Requested location: "%s"\n'
                               '  Actual location:    "%s"',
                               context.env_exe, real_env_exe)
                context.env_exec_cmd = real_env_exe
        return context

    # override the setup_python method to support the irispython interpreter
    def setup_python(self, context):
        """
        Set up a Python executable in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        binpath = context.bin_path
        path = context.env_exe
        copier = self.symlink_or_copy
        dirname = context.python_dir
        if os.name != 'nt':
            copier(context.executable, path)
            if not os.path.islink(path):
                os.chmod(path, 0o755)
            for suffix in ('python', 'python3', f'python3.{sys.version_info[1]}','irispython'):
                path = os.path.join(binpath, suffix)
                if not os.path.exists(path):
                    # Issue 18807: make copies if
                    # symlinks are not wanted
                    copier(context.env_exe, path, relative_symlinks_ok=True)
                    if not os.path.islink(path):
                        os.chmod(path, 0o755)
        else:
            if self.symlinks:
                # For symlinking, we need a complete copy of the root directory
                # If symlinks fail, you'll get unnecessary copies of files, but
                # we assume that if you've opted into symlinks on Windows then
                # you know what you're doing.
                suffixes = [
                    f for f in os.listdir(dirname) if
                    os.path.normcase(os.path.splitext(f)[1]) in ('.exe', '.dll')
                ]
                if sysconfig.is_python_build(True):
                    suffixes = [
                        f for f in suffixes if
                        os.path.normcase(f).startswith(('python', 'vcruntime'))
                    ]
            else:
                suffixes = {'python.exe', 'python_d.exe', 'pythonw.exe', 'pythonw_d.exe','irispython.exe'}
                base_exe = os.path.basename(context.env_exe)
                suffixes.add(base_exe)

            for suffix in suffixes:
                src = os.path.join(dirname, suffix)
                if os.path.lexists(src):
                    copier(src, os.path.join(binpath, suffix))

            if sysconfig.is_python_build(True):
                # copy init.tcl
                for root, dirs, files in os.walk(context.python_dir):
                    if 'init.tcl' in files:
                        tcldir = os.path.basename(root)
                        tcldir = os.path.join(context.env_dir, 'Lib', tcldir)
                        if not os.path.exists(tcldir):
                            os.makedirs(tcldir)
                        src = os.path.join(root, 'init.tcl')
                        dst = os.path.join(tcldir, 'init.tcl')
                        shutil.copyfile(src, dst)
                        break


    def setup_scripts(self, context):
        """
        Set up scripts into the created environment from a directory.

        This method installs the default scripts into the environment
        being created. You can prevent the default installation by overriding
        this method if you really need to, or if you need to specify
        a different location for the scripts to install. By default, the
        'scripts' directory in the venv package is used as the source of
        scripts to install.
        """
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, 'scripts')
        self.install_scripts(context, path)

    def replace_variables(self, text, context):
        """
        Replace variable placeholders in script text with context-specific
        variables.

        Return the text passed in , but with variables replaced.

        :param text: The text in which to replace placeholder variables.
        :param context: The information for the environment creation request
                        being processed.
        """
        text = text.replace('__VENV_DIR__', context.env_dir)
        text = text.replace('__VENV_NAME__', context.env_name)
        text = text.replace('__VENV_PROMPT__', context.prompt)
        text = text.replace('__VENV_BIN_NAME__', context.bin_name)
        text = text.replace('__VENV_PYTHON__', context.env_exe)
        text = text.replace('__VENV_ISC_PACKAGE_INSTALLDIR__', self.isc_package_installdir)

        return text
    
    def post_setup(self, context: types.SimpleNamespace) -> types.NoneType:
        """
        Perform any final steps to complete the environment setup.

        :param context: The information for the environment creation request
                        being processed.
        """
        # install the core dependencies
        if not self.use_irispython:
            cmd = [context.env_exec_cmd, '-m', 'pip', 'install', 'git+https://github.com/grongierisc/iris-embedded-python-wrapper']
            subprocess.check_call(cmd)

def main(args=None):
    compatible = True
    if sys.version_info < (3, 3):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with Python >= 3.3')
    else:
        import argparse

        parser = argparse.ArgumentParser(prog=__name__,
                                         description='Creates virtual Python '
                                                     'environments in one or '
                                                     'more target '
                                                     'directories.',
                                         epilog='Once an environment has been '
                                                'created, you may wish to '
                                                'activate it, e.g. by '
                                                'sourcing an activate script '
                                                'in its bin directory.')
        parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                            help='A directory to create the environment in.')
        parser.add_argument('--system-site-packages', default=False,
                            action='store_true', dest='system_site',
                            help='Give the virtual environment access to the '
                                 'system site-packages dir.')
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--symlinks', default=use_symlinks,
                           action='store_true', dest='symlinks',
                           help='Try to use symlinks rather than copies, '
                                'when symlinks are not the default for '
                                'the platform.')
        group.add_argument('--copies', default=not use_symlinks,
                           action='store_false', dest='symlinks',
                           help='Try to use copies rather than symlinks, '
                                'even when symlinks are the default for '
                                'the platform.')
        parser.add_argument('--clear', default=False, action='store_true',
                            dest='clear', help='Delete the contents of the '
                                               'environment directory if it '
                                               'already exists, before '
                                               'environment creation.')
        parser.add_argument('--upgrade', default=False, action='store_true',
                            dest='upgrade', help='Upgrade the environment '
                                               'directory to use this version '
                                               'of Python, assuming Python '
                                               'has been upgraded in-place.')
        parser.add_argument('--without-pip', dest='with_pip',
                            default=True, action='store_false',
                            help='Skips installing or upgrading pip in the '
                                 'virtual environment (pip is bootstrapped '
                                 'by default)')
        parser.add_argument('--prompt',
                            help='Provides an alternative prompt prefix for '
                                 'this environment.')
        parser.add_argument('--upgrade-deps', default=False, action='store_true',
                            dest='upgrade_deps',
                            help='Upgrade core dependencies: {} to the latest '
                                 'version in PyPI'.format(
                                 ' '.join(CORE_VENV_DEPS)))
        # add the isc_package_installdir argument
        parser.add_argument('--isc-package-installdir', default=os.environ.get('ISC_PACKAGE_INSTALLDIR', None),
                            dest='isc_package_installdir',
                            help='The InterSystems IRIS package install directory')
        # add the use_irispython argument
        parser.add_argument('--use-irispython', default=False, action='store_true',
                            dest='use_irispython',
                            help='Use the irispython interpreter')
        options = parser.parse_args(args)
        if options.upgrade and options.clear:
            raise ValueError('you cannot supply --upgrade and --clear together.')
        builder = IrisEnvBuilder(system_site_packages=options.system_site,
                             clear=options.clear,
                             symlinks=options.symlinks,
                             upgrade=options.upgrade,
                             with_pip=options.with_pip,
                             prompt=options.prompt,
                             upgrade_deps=options.upgrade_deps,
                             isc_package_installdir=options.isc_package_installdir,
                             use_irispython=options.use_irispython)
        for d in options.dirs:
            builder.create(d)

if __name__ == '__main__':
    rc = 1
    try:
        main(['.venv-iris', '--isc-package-installdir', '/opt/intersystems/iris/'])
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)

