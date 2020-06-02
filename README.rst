==============================================
Preperation Plugin for FESOM Mesh Partitioning
==============================================

This plugin contains functionality to prepare files for the mesh partioner
after the Triangle program has run.

Usage
-----

From the command line::

    $ mesh_part_prep <PATH_TO_MESH_FOLDER>

From an ``esm_tools`` script (as a plugin, which you can include in your recipe as ``mesh_part_prep``):

.. code-block:: yaml

    general:
        # Turn on the plugin (seperate from actually loading it):
        mesh_part_prep: True

    fesom:
        # Specify the raw mesh directory:
        mesh_dir: /some/path/to/mesh/dir
