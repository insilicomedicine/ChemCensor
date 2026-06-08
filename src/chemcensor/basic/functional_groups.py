from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import cached_property

import numpy as np
from frozendict import frozendict
from numpy.typing import NDArray
from rdkit import Chem

from .errors.functional_group_errors import FunctionalGroupsInitializationError
from .errors.functional_group_errors import InvalidDataTypesError
from .errors.functional_group_errors import InvalidSMARTSStringError
from .errors.functional_group_errors import MissingRequiredKeysError
from .molecule import Molecule
from .utils import smarts_to_pattern_fingerprint


class FunctionalGroupClass(Enum):
    GENERAL = 0
    SEAR = 1
    SKIP = 2
    EXPANDABLE = 3


@dataclass(frozen=True)
class FunctionalGroup:
    """
    Initialize a FunctionalGroup object.
    :param idx: Functional group index;
    :type idx: int
    :param name: Functional group name;
    :type name: str
    :param ui_name: Functional group user-friendly name;
    :type ui_name: str
    :param smarts: Functional group SMARTS string;
    :type smarts: str
    :param fg_class: Functional group class;
    :type fg_class: FunctionalGroupClass
    """

    idx: int
    name: str
    ui_name: str
    smarts: str
    fg_class: FunctionalGroupClass

    @cached_property
    def pattern(self) -> Chem.Mol:
        """
        Create and cache the RDKit Mol pattern from the SMARTS string.
        :return: RDKit Mol pattern object.
        :rtype: Chem.Mol
        :raises: ValueError if the SMARTS string is invalid.
        """
        pattern = Chem.MolFromSmarts(self.smarts)
        if pattern is None:
            raise InvalidSMARTSStringError(self.smarts)
        return pattern

    @classmethod
    def from_dict(
        cls, fg_group_data: frozendict[str, int | str | FunctionalGroupClass]
    ) -> FunctionalGroup:
        """
        Create a FunctionalGroup object from a dictionary.
        :param fg_group_data: Dictionary containing the functional group data;
        :type fg_group_data: frozendict[str, int | str | FunctionalGroupClass]
        :return: FunctionalGroup object.
        :rtype: FunctionalGroup
        :raises: MissingRequiredKeysError if required keys are missing.
        """
        if (idx := fg_group_data.get("idx")) is None:
            raise MissingRequiredKeysError({"idx"})
        if not isinstance(idx, int):
            raise InvalidDataTypesError(type(idx), "idx", int)
        if (name := fg_group_data.get("name")) is None:
            raise MissingRequiredKeysError({"name"})
        if not isinstance(name, str):
            raise InvalidDataTypesError(type(name), "name", str)
        if (ui_name := fg_group_data.get("ui_name")) is None:
            raise MissingRequiredKeysError({"ui_name"})
        if not isinstance(ui_name, str):
            raise InvalidDataTypesError(type(ui_name), "ui_name", str)
        if (smarts := fg_group_data.get("smarts")) is None:
            raise MissingRequiredKeysError({"smarts"})
        if not isinstance(smarts, str):
            raise InvalidDataTypesError(type(smarts), "smarts", str)
        if (fg_class := fg_group_data.get("fg_class")) is None:
            raise MissingRequiredKeysError({"fg_class"})
        if not isinstance(fg_class, FunctionalGroupClass):
            raise InvalidDataTypesError(
                type(fg_class), "fg_class", FunctionalGroupClass
            )

        return cls(
            idx=int(idx),
            name=str(name),
            ui_name=str(ui_name),
            smarts=str(smarts),
            fg_class=fg_class,
        )


@dataclass(frozen=True)
class MatchedGroup:
    """
    Class representing a matched functional group along with the matching sites.
    """

    functional_group: FunctionalGroup
    matching_sets: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, unsafe_hash=True)
class FunctionalGroups:
    """
    Class representing a collection of functional groups and allows to
    efficiently identify them in a molecule.
    """

    known_groups: tuple[FunctionalGroup, ...]
    fps_bits_collection: NDArray[np.uint8]
    fp_length: int = 2048

    @cached_property
    def num_groups(self) -> int:
        """Number of functional groups in this collection."""
        return len(self.known_groups)

    @classmethod
    def from_tuple(
        cls,
        functional_groups: tuple[
            frozendict[str, int | str | FunctionalGroupClass], ...
        ],
        fp_length: int = 2048,
    ) -> FunctionalGroups:
        """
        Initialize a FunctionalGroups collection.

        :param functional_groups: List of functional group dictionaries;
        :type functional_groups: tuple[frozendict[str, int | str
            | FunctionalGroupClass], ...]
        :param fp_length: Fingerprint length;
        :type fp_length: int
        :raises FunctionalGroupsInitializationError: If initialization fails
        """
        try:
            known_groups_tuple = tuple(
                FunctionalGroup.from_dict(fg) for fg in functional_groups
            )
        except MissingRequiredKeysError as e:
            raise FunctionalGroupsInitializationError() from e

        try:
            fps = np.array(
                [
                    smarts_to_pattern_fingerprint(fg.pattern, fp_length)
                    for fg in known_groups_tuple
                ]
            )
        except InvalidSMARTSStringError as e:
            raise FunctionalGroupsInitializationError() from e

        return cls(
            known_groups=known_groups_tuple,
            fps_bits_collection=fps,
            fp_length=fp_length,
        )

    def identify_functional_groups(self, mol: Molecule) -> tuple[MatchedGroup, ...]:
        """
        Identifies the functional groups in a molecule.
        :param mol: molecule to identify functional groups in;
        :type mol: Molecule
        :return: tuple of matched functional groups;
        """
        mol_fingerprint = smarts_to_pattern_fingerprint(
            mol.canonical_rdmol, self.fp_length
        )

        matching_fg_mask = np.all(self.fps_bits_collection <= mol_fingerprint, axis=1)
        selected_local_indices = np.nonzero(matching_fg_mask)[0]
        matched_groups: tuple[MatchedGroup, ...] = ()
        for idx in selected_local_indices:
            group = self.known_groups[idx]
            matches = mol.canonical_rdmol.GetSubstructMatches(
                group.pattern,
                uniquify=False,  # allow multiple matches for the same functional group
            )
            if matches:
                matched_group = MatchedGroup(
                    functional_group=group,
                    matching_sets=matches,
                )
                matched_groups += (matched_group,)

        return matched_groups
