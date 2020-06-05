"""
There is also a esm-tools plugin to prepare files for the FESOM Mesh Generator.

This consists of two parts, first to prepare the ``aux3d.out`` file, and
secondly to move the resulting mesh files into a common directory.

In your recipe, you can include the following elements after the installation:

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 3,22

    compute:
            recipe:
                    - "mesh_part_prep"
                    - "_create_setup_folders"
                    - "_create_component_folders"
                    - "initialize_experiment_logfile"
                    - "_write_finalized_config"
                    - "copy_tools_to_thisrun"
                    - "_copy_preliminary_files_from_experiment_to_thisrun"
                    - "_show_simulation_info"
                    - "copy_files_to_thisrun"
                    - "modify_namelists"
                    - "modify_files"
                    - "create_new_files"
                    - "prepare_coupler_files"
                    - "add_batch_hostfile"
                    - "copy_files_to_work"
                    - "write_simple_runscript"
                    - "report_missing_files"
                    - "database_entry"
                    - "submit"
                    - "mesh_part_finish"


You configuration should include the following to set up the plugin correctly:

.. code-block:: yaml

    general:
        mesh_part_prep: True
        mesh_part_finish: True
    
    fesom_mesh_part:
        mesh_dir: /path/to/your/Triangle/output/dir 
        result_mesh_dir: /some/path
        part: 288 # For example, you could set a different partitioning here

"""

import errno
import os
import shutil

import mesh_part_prep


def copy_and_overwrite(from_path, to_path):
    """
    Removes to path and copies over from path
    """
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    return shutil.copytree(from_path, to_path)


def cp(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def deep_dict_update(d, mesh_dir, new_mesh_dir):
    for key in list(d):
        old_value = d[key]
        if isinstance(old_value, dict):
            deep_dict_update(old_value, mesh_dir, new_mesh_dir)
        if isinstance(old_value, str):
            if mesh_dir in old_value:
                new_value = old_value.replace(mesh_dir, new_mesh_dir)
                d[key] = new_value
        if isinstance(old_value, list) or isinstance(old_value, tuple):
            new_value = []
            for item in old_value:
                if isinstance(item, str):
                    new_value.append(item.replace(mesh_dir, new_mesh_dir))
                else:
                    new_value.append(item)
            d[key] = new_value


def esm_mesh_part_prep(config):
    """
    Runs a pre-process script for the mesh partioner to generate 3D information
    """
    if config.get("general", {}).get("mesh_part_prep", False):
        mesh_dir = config["fesom_mesh_part"]["mesh_dir"]
        # Copy the mesh files to the actual input directory and reassign
        new_mesh_dir = copy_and_overwrite(
            mesh_dir, config["fesom_mesh_part"]["experiment_input_dir"]
        )
        # Make sure all the "original" mesh files come from the new copy:
        deep_dict_update(config, mesh_dir, new_mesh_dir)
        # Make sure the namelist.config thinks the mesh is in the work dir
        config["fesom_mesh_part"]["namelist_changes"]["namelist.config"]["paths"][
            "MeshPath"
        ] = config["general"]["thisrun_work_dir"]

        # PG: I don't like this:
        # Recreate the all-files-to-copy
        self = config["general"]["jobclass"]
        self.all_files_to_copy = self.assemble_file_lists(config, self.relevant_files)

        rm = mesh_part_prep.RawMesh(path=new_mesh_dir)
        rm.process()
    return config


def esm_mesh_part_finish(config):
    """
    Finishes up a mesh by copying the paritioned mesh into a folder
    """
    if config.get("general", {}).get("mesh_part_finish", False):
        result_mesh_dir = config["fesom_mesh_part"]["result_mesh_dir"]
        work_dir = config["fesom_mesh_part"]["thisrun_work_dir"]
        part = str(config["fesom_mesh_part"].get("part", 288))
        file_list = [
            "aux3d.out",
            "edge_tri.out",
            "edgenum.out",
            "edges.out",
            "elem2d.out",
            "elvls.out",
            "nlvls.out",
            "nod2d.out",
        ]
        for f in file_list:
            cp(work_dir + "/" + f, result_mesh_dir + "/" + f)
        cp(work_dir + "/dist_" + part, result_mesh_dir)
    return config
