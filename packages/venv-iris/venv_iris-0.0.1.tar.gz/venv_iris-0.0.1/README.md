# venv-iris

This module is an extension of the virtual environment module in Python. 

It is designed to be used with the Iris dataplatfrom.

It brings the following features:
- Automatic binding of the virtual environment to the Iris dataplatform
- Automatic unbinding of the virtual environment from the Iris dataplatform

Limitation:
- the binding and unbinding is only available for the whole instance of IRIS. It is not possible to bind and unbind a virtual environment to a specific project/namespace.

## Installation

```bash
pip install venv-iris
```

## Usage 

For creating a virtual environment with the Iris dataplatform, use the following command:

### Unix

```bash
python3 -m venv-iris .venv-iris
source .venv-iris/bin/activate
```

### Windows

```ps1
python -m venv-iris .venv-iris
.venv-iris\Scripts\Activate.ps1
```

Then if you want to install a package, you can use the following command:

```bash
pip install <package>
```

To bind the virtual environment to the Iris dataplatform, use the following command:

```bash
bind
```

To unbind the virtual environment from the Iris dataplatform, use the following command:

```bash
unbind
```

To deactivate the virtual environment, use the following command:

```bash
deactivate
```

### Options

- `--isc-package-installdir` to specify the instance of IRIS to bind to. By default, it will use the instance of IRIS that is running on the same machine if the environment variable `ISC_PACKAGE_INSTALLDIR` is set.

```bash
python3 -m venv-iris .venv-iris --isc-package-installdir /usr/irissys
```

## Use case example

I want to install the package `requests` in a virtual environment that is binded to the Iris dataplatform.

Like this I will have the same experience as if I was using the Iris dataplatform directly from an IRIS instance.

```bash
python3 -m venv-iris .venv-iris
source .venv-iris/bin/activate
pip install requests
bind
```

Optionally, you can use the `iris` package to interact with the Iris dataplatform directly from the virtual environment.

```bash
python3
>>> import iris
>>> iris.system.version.GetVersion()
'IRIS for UNIX (Apple Silicon) 2024.2.0 (Build 311U) Tue Feb  8 2024 14:00:00 EST'
```

Now run an IRIS Terminal and you will be able to import the `requests` package.

```bash
iris session iris
USER>do ##class(%SYS.Python).Shell()

Python 3.11.8 (main, Feb  6 2024, 21:21:21) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type quit() or Ctrl-D to exit this shell.
>>> import requests
>>>
```

Now if you unbind the virtual environment, you will not be able to import the `requests` package anymore.

```bash
unbind
```

```bash
iris session
USER>do ##class(%SYS.Python).Shell()

Python 3.11.8 (main, Feb  6 2024, 21:21:21) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type quit() or Ctrl-D to exit this shell.
>>> import requests
Traceback (most recent call last):
  File "<input>", line 1, in <module>
ModuleNotFoundError: No module named 'requests'
>>>
```

## Benefits

- You can use any package available on PyPI
- You can use any version of Python
- You can use any version of the package
- You can develop your code locally and then deploy it on the Iris dataplatform
- You can use `import iris` in your code to interact with the Iris as if you were using the Iris dataplatform directly from an IRIS instance
- You can share the same instance of IRIS for multiple projects without having conflicts between the packages