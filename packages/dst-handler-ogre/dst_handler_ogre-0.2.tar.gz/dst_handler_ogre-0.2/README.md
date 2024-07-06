# dst-handler

Installation steps:
- ``python -m pip install –-user –-upgrade setuptools wheel``
- ``python setup.py sdist bdist_wheel``
- ``pip install -e .`` (install the lib locally)
- ``pip install twine`` (twine is used for uploading the package)
- ``python -m twine upload — repository testpypi dist/*`` (the package must first be uploaded in the testpypi env)
- ``pip uninstall dst-handler-ogre`` (uninstall the package)
- ``pip install -i https://test.pypi.org/dst-handler-ogre/ dst-handler-ogre==0.0.1`` (verify if you can install it through the testpypi env)
- ``python -m twine upload dist/*`` (publish it to the main pypi env)
- ``pip install dst-handler-ogre``

TestPyPi auth:
- username: ``__token__``
- password: [``AWS secret {{testpypi}}``](https://eu-central-1.console.aws.amazon.com/secretsmanager/secret?name=testpypi&region=eu-central-1)

PyPi auth:
- username: ``__token__``
- password: [``AWS secret {{pypi}}``](https://eu-central-1.console.aws.amazon.com/secretsmanager/secret?name=pypi&region=eu-central-1)
