#!/usr/bin/env python3
"""
The Python module allows you to prepare a Triangle output for use with the mesh partitioner.

A minimal example::

    >>> from mesh_part_prep import RawMesh
    >>> path = "/some/path/with/a/triangle/output"
    >>> rm = RawMesh(path)
    >>> rm.process()
"""
import logging
import pathlib

logger = logging.getLogger("mesh_part_prep")


class MeshPartPrepError(Exception):
    """Raise this when prepping the raw mesh fails"""


class RawMesh(object):
    """A representation of the raw mesh (after Triangle, before MeshPart)"""

    def __init__(self, path):
        self.dir = pathlib.Path(path)
        self.processed = False
        logger.debug(f"RawMesh built for {self.dir}")

    def process(self):
        """Processes files to generate a partitioned FESOM-2.0 mesh using the METIS mesh partitioner from a standard Triangle output"""
        try:
            self._prep_depths()
            self._check_required_mesh_part_files()
            self.processed = True
        except Exception as e:
            m = getattr(e, "message", repr(e))
            raise MeshPartPrepError(f"oops: {m}")

    def _check_required_mesh_part_files(self):
        """Asserts that files required to run the mesh partitioner are in place"""
        for file_ in ["aux3d.out", "elem2d.out", "nod2d.out", "nodhn.out"]:
            req_file = self.dir / pathlib.Path(file_)
            try:
                assert req_file.is_file()
            except AssertionError:
                raise MeshPartPrepError(f"{req_file.name} does not exist!")
            logger.debug(f"{req_file} in place")

    def _prep_depths(self):
        """Prepends depth information from the nodhn file to create aux3d file"""
        with open(self.dir / pathlib.Path("nodhn.out"), "r") as depths_file:
            prev_depths = depths_file.readlines()
            logger.debug(f"{depths_file} loaded!")

        number_levels = 48
        depths = [
            0.0,
            -5.0,
            -10.0,
            -20.0,
            -30.0,
            -40.0,
            -50.0,
            -60.0,
            -70.0,
            -80.0,
            -90.0,
            -100.0,
            -115.0,
            -135.0,
            -160.0,
            -190.0,
            -230.0,
            -280.0,
            -340.0,
            -410.0,
            -490.0,
            -580.0,
            -680.0,
            -790.0,
            -910.0,
            -1040.0,
            -1180.0,
            -1330.0,
            -1500.0,
            -1700.0,
            -1920.0,
            -2150.0,
            -2400.0,
            -2650.0,
            -2900.0,
            -3150.0,
            -3400.0,
            -3650.0,
            -3900.0,
            -4150.0,
            -4400.0,
            -4650.0,
            -4900.0,
            -5150.0,
            -5400.0,
            -5650.0,
            -6000.0,
            -6250.0,
        ]
        with open(self.dir / pathlib.Path("aux3d.out"), "w") as depths_file:
            depths_file.write(str(number_levels))
            depths_file.write("\n")
            for depth in depths:
                depths_file.write(str(depth))
                depths_file.write("\n")
            for depth in prev_depths:
                depths_file.write(depth)
            logger.debug(f"{depths_file} generated")

    def __repr__(self):
        return f"{self.__class.__name__}('{self.dir}')"
