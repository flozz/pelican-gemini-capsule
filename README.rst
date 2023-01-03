Pelican Gemini Capsule Plugin
=============================

|GitHub| |License| |Discord| |Github Actions| |Black|

Pelican Gemini Capsule is a Pelican plugin to generate Gemini capsules. Only
works with articles in reStructuredText formats.

**This project is currently work in progress.**


Requirements
------------

* Python >= 3.7
* rst2gemtext_


Installation
------------

TODO


Usage
-----

Once Pelican Gemini Capsule installed, simply add it to you Pelican configuration:

.. code-block:: python

    PLUGINS = [
        "pelican_gemini_capsule",
    ]


Contributing
------------

Questions
~~~~~~~~~

If you have any question, you can:

* `Open an issue <https://github.com/flozz/pelican-gemini-capsule/issues>`_ on GitHub
* `Ask on Discord <https://discord.gg/P77sWhuSs4>`_ (I am not always available to chat, but I try to answer to everyone)


Bugs
~~~~

Please `open an issue <https://github.com/flozz/pelican-gemini-capsule/issues>`_ on GitHub with as much information as possible if you found a bug:

* Your operating system / Linux distribution (and its version)
* How you installed the software
* All the logs and message outputted by the software
* etc.

If the issue is about the outputted Gemtext (wrong markup, unsupported reStructuredText feature,...), please report the bug to the rst2gemtext_ project.


Pull requests
~~~~~~~~~~~~~

Please consider `filing a bug <https://github.com/flozz/pelican-gemini-capsule/issues>`_ before starting to work on a new feature; it will allow us to discuss the best way to do it. It is obviously unnecessary if you just want to fix a typo or small errors in the code.

Please note that your code must follow the coding style defined by the `pep8 <https://pep8.org>`_ and pass tests. `Black <https://black.readthedocs.io/en/stable>`_ and `Flake8 <https://flake8.pycqa.org/en/latest>`_ are used on this project to enforce the coding style.


Check codding style
~~~~~~~~~~~~~~~~~~~

You must install `Nox <https://nox.thea.codes/>`__ first::

    pip3 install nox

Then you can check for lint error::

    nox --session lint

You can also fix coding style errors automatically with::

    nox -s black_fix


Support this project
--------------------

Want to support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__
* `💵️ Give me a tip on PayPal <https://www.paypal.me/0xflozz>`__
* `❤️ Sponsor me on GitHub <https://github.com/sponsors/flozz>`__


Changelog
---------

TODO


.. _rst2gemtext: https://github.com/flozz/rst2gemtext

.. |GitHub| image:: https://img.shields.io/github/stars/flozz/pelican-gemini-capsule?label=GitHub&logo=github
   :target: https://github.com/flozz/pelican-gemini-capsule

.. |License| image:: https://img.shields.io/github/license/flozz/pelican-gemini-capsule
   :target: https://github.com/flozz/pelican-gemini-capsule/blob/master/COPYING

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Github Actions| image:: https://github.com/flozz/pelican-gemini-capsule/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/pelican-gemini-capsule/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable
