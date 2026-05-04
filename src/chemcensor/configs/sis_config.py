from dataclasses import dataclass


@dataclass(slots=True)
class SisConfig:
    """Parameters for `SisAnnotator`.

    :ivar max_simultaneous_atom_stereo_resolutions: Max tetrahedral centers that may
        resolve ``?`` → ``R/S`` in one step and still count as atom-level SIS.
    :ivar max_simultaneous_alkene_stereo_resolutions: Max double bonds that may
        resolve enumerable E/Z in one step and still count as alkene-level SIS.
    """

    max_simultaneous_atom_stereo_resolutions: int = 2
    max_simultaneous_alkene_stereo_resolutions: int = 1


sis_config = SisConfig()
