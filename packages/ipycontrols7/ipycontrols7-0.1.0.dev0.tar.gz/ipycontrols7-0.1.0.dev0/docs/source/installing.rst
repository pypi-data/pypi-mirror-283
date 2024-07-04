
.. _installation:

Installation
============


The simplest way to install ipycontrols7 is via pip::

    pip install ipycontrols7

or via conda::

    conda install ipycontrols7


If you installed via pip, and notebook version < 5.3, you will also have to
install / configure the front-end extension as well. If you are using classic
notebook (as opposed to Jupyterlab), run::

    jupyter nbextension install [--sys-prefix / --user / --system] --py ipycontrols7

    jupyter nbextension enable [--sys-prefix / --user / --system] --py ipycontrols7

with the `appropriate flag`_. If you are using Jupyterlab, install the extension
with::

    jupyter labextension install ipycontrols7

If you are installing using conda, these commands should be unnecessary, but If
you need to run them the commands should be the same (just make sure you choose the
`--sys-prefix` flag).


.. links

.. _`appropriate flag`: https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html#installing-and-enabling-extensions
