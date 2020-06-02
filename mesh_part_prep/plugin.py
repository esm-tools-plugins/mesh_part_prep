import mesh_part_prep


def esm_mesh_part_prep(config):
    if config.get("general", {}).get("mesh_part_prep", False):
        mesh_dir = config["fesom"]["mesh_dir"]
        rm = mesh_part_prep.RawMesh(path=mesh_dir)
        rm.process()
    return config
