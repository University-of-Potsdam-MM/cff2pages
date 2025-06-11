Usage
=====

Command Line Interface
----------------------

To convert a ``Citation.cff`` file into an HTML page, run:

.. code-block:: bash

   cff2pages [-h] [-i [INPUT]] [-o [OUTPUT]]

Options:
  - ``-h, --help``: Show help message and exit.
  - ``-i [INPUT], --input [INPUT]``: Path to the input CFF file. Default: ``./CITATION.cff``
  - ``-o [OUTPUT], --output [OUTPUT]``: Path to the output file. Default: ``public/citation.html``

Installation
------------

.. code-block:: bash

   pip install cff2pages

Basic Example
-------------

.. code-block:: bash

   cd your_project_directory
   cff2pages

By default, the HTML output is saved to ``public/citation.html``.
