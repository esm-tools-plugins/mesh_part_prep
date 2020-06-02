"""A esm-tools plugin to prepare files for the FESOM Mesh Generator"""

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
        config["fesom_mesh_part"]["mesh_dir"] = new_mesh_dir
        config["fesom_mesh_part"]["namelist_changes"]["namelist.config"]["paths"][
            "MeshPath"
        ] = new_mesh_dir
        for key in list(config["fesom_mesh_part"]):
            old_value = config["fesom_mesh_part"][key]
            if isinstance(key, str):
                if mesh_dir in old_value:
                    new_value = old_value.replace(mesh_dir, new_mesh_dir)
                    config["fesom_mesh_part"][key] = new_value

        rm = mesh_part_prep.RawMesh(path=new_mesh_dir)
        rm.process()
    return config
