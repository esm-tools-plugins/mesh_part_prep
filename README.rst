==============================================
Preperation Plugin for FESOM Mesh Partitioning
==============================================

.. image:: https://readthedocs.org/projects/mesh-part-prep/badge/?version=latest
    :target: https://mesh-part-prep.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/github/license/pgierz/mesh_part_prep   
    :alt: GitHub

This plugin contains functionality to prepare files for the mesh partioner
after the Triangle program has run.

Usage
-----

From the command line::

    $ mesh_part_prep <PATH_TO_MESH_FOLDER>

From an ``esm_tools`` script (as a plugin, which you can include in your recipe as ``mesh_part_prep`` and ``mesh_part_finish``):

.. code-block:: yaml

    general:
        # Turn on the plugin (seperate from actually loading it):
        mesh_part_prep: True
        # Turn on copying the mesh to a desired location after completion
        mesh_part_finish: True

    fesom_mesh_part:
        # Specify the raw mesh directory:
        mesh_dir: /some/path/to/mesh/dir
        # Where the finished, paritioned mesh should be placed:
        result_mesh_dir: /some/path/where/the/finished/mesh/should/be
