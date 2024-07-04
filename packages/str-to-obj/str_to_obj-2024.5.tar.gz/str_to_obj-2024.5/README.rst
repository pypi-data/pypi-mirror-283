..
   Copyright CNRS/Inria/UniCA
   Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
   SEE COPYRIGHT NOTICE BELOW

.. |PROJECT_NAME|      replace:: Str-to-Obj
.. |SHORT_DESCRIPTION| replace:: Convert strings to Python objects guided by (potentially annotated) type hints

.. |PYPI_NAME_LITERAL| replace:: ``str-to-obj``
.. |PYPI_PROJECT_URL|  replace:: https://pypi.org/project/str-to-obj/
.. _PYPI_PROJECT_URL:  https://pypi.org/project/str-to-obj/

.. |DOCUMENTATION_URL| replace:: https://src.koda.cnrs.fr/eric.debreuve/str-to-obj/-/wikis/home
.. _DOCUMENTATION_URL: https://src.koda.cnrs.fr/eric.debreuve/str-to-obj/-/wikis/home



===================================
|PROJECT_NAME|: |SHORT_DESCRIPTION|
===================================



Installation
============

This project is published
on the `Python Package Index (PyPI) <https://pypi.org/>`_
at: |PYPI_PROJECT_URL|_.
It should be installable from Python distribution platforms or Integrated Development Environments (IDEs).
Otherwise, it can be installed from a command console using `pip <https://pip.pypa.io/>`_:

..
   - For all users, after acquiring administrative rights:
       - First installation: ``pip install`` |PYPI_NAME_LITERAL|
       - Installation update: ``pip install --upgrade`` |PYPI_NAME_LITERAL|
   - For the current user (no administrative rights required):
       - First installation: ``pip install --user`` |PYPI_NAME_LITERAL|
       - Installation update: ``pip install --user --upgrade`` |PYPI_NAME_LITERAL|

+--------------+-------------------------------------------------------+----------------------------------------------------------+
|              | For all users (after acquiring administrative rights) | For the current user (no administrative rights required) |
+==============+=======================================================+==========================================================+
| Installation | ``pip install`` |PYPI_NAME_LITERAL|                   | ``pip install --user`` |PYPI_NAME_LITERAL|               |
+--------------+-------------------------------------------------------+----------------------------------------------------------+
| Update       | ``pip install --upgrade`` |PYPI_NAME_LITERAL|         | ``pip install --user --upgrade`` |PYPI_NAME_LITERAL|     |
+--------------+-------------------------------------------------------+----------------------------------------------------------+



Documentation
=============

The documentation is available at |DOCUMENTATION_URL|_.



Acknowledgments
===============

The project is developed with `PyCharm Community <https://www.jetbrains.com/pycharm/>`_.

The development relies on several open-source packages
(see ``install_requires`` in ``setup.py``, if present; otherwise ``import`` statements should be searched for).

The code is formatted by `Black <https://github.com/psf/black/>`_, *The Uncompromising Code Formatter*.

The imports are ordered by `isort <https://github.com/timothycrosley/isort/>`_... *your imports, so you don't have to*.



..
   COPYRIGHT NOTICE

   This software is governed by the CeCILL  license under French law and
   abiding by the rules of distribution of free software.  You can  use,
   modify and/ or redistribute the software under the terms of the CeCILL
   license as circulated by CEA, CNRS and INRIA at the following URL
   "http://www.cecill.info".

   As a counterpart to the access to the source code and  rights to copy,
   modify and redistribute granted by the license, users are provided only
   with a limited warranty  and the software's author,  the holder of the
   economic rights,  and the successive licensors  have only  limited
   liability.

   In this respect, the user's attention is drawn to the risks associated
   with loading,  using,  modifying and/or developing or reproducing the
   software by the user in light of its specific status of free software,
   that may mean  that it is complicated to manipulate,  and  that  also
   therefore means  that it is reserved for developers  and  experienced
   professionals having in-depth computer knowledge. Users are therefore
   encouraged to load and test the software's suitability as regards their
   requirements in conditions enabling the security of their systems and/or
   data to be ensured and,  more generally, to use and operate it in the
   same conditions as regards security.

   The fact that you are presently reading this means that you have had
   knowledge of the CeCILL license and that you accept its terms.

   SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

   This software is being developed by Eric Debreuve, a CNRS employee and
   member of team Morpheme.
   Team Morpheme is a joint team between Inria, CNRS, and UniCA.
   It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
   I3S, and Laboratory iBV.

   CNRS: https://www.cnrs.fr/index.php/en
   Inria: https://www.inria.fr/en/
   UniCA: https://univ-cotedazur.eu/
   Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
   I3S: https://www.i3s.unice.fr/en/
   iBV: http://ibv.unice.fr/
   Team Morpheme: https://team.inria.fr/morpheme/
