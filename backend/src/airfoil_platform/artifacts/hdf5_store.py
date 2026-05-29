"""HDF5 artifact storage for aerodynamic field data."""

import os
import numpy as np
import h5py

from airfoil_platform.artifacts.artifact_registry import (
    artifact_file_path,
    write_sidecar,
    build_metadata,
    read_sidecar,
)


def write_hdf5_artifact(
    artifact_id: str,
    coordinates: np.ndarray,
    pressure: np.ndarray,
    velocity: np.ndarray,
) -> str:
    """
    Write an HDF5 aerodynamic field artifact and its JSON sidecar.
    Returns the HDF5 file path.
    """
    file_path = artifact_file_path("aerodynamic", artifact_id, "h5")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with h5py.File(file_path, "w") as f:
        f.create_dataset("/coordinates", data=coordinates)
        f.create_dataset("/fields/pressure", data=pressure)
        f.create_dataset("/fields/velocity", data=velocity)

    meta = build_metadata(
        artifact_id=artifact_id,
        format="hdf5",
        role="aerodynamic_field",
        file_path=file_path,
        datasets={
            "coordinates": "/coordinates",
            "pressure_field": "/fields/pressure",
            "velocity_field": "/fields/velocity",
        },
    )
    write_sidecar(artifact_id, "aerodynamic", meta)

    return file_path


def read_hdf5_datasets(artifact_id: str):
    """Return (coordinates, pressure, velocity) arrays from an HDF5 artifact."""
    file_path = artifact_file_path("aerodynamic", artifact_id, "h5")
    with h5py.File(file_path, "r") as f:
        coords = f["/coordinates"][:]
        pressure = f["/fields/pressure"][:]
        velocity = f["/fields/velocity"][:]
    return coords, pressure, velocity


def get_hdf5_metadata(artifact_id: str):
    """Read HDF5 artifact metadata from its JSON sidecar."""
    return read_sidecar("aerodynamic", artifact_id)
