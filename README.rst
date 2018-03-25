CheesyPi
========

Control panel for intelligent fridge used to age cheese.

Pre-requisites
--------------

Tested on Arch Linux and on Debian Jessie

* python version 3.6 with virtualenv

Setup
-----

```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Running
-------

```
source venv/bin/activate
./run.py
```

The server will be running on port 8000 by default.

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-tornado`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-tornado`: https://github.com/hkage/cookiecutter-tornado
