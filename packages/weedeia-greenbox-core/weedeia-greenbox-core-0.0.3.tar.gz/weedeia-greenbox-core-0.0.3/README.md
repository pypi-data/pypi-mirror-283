### Development

```shell
python -m venv env
pip install fastapi uvicorn #rpi.gpio only is supported

fastapi main.py
```

### Publish new version

First, update version in setup.py

```shell
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
