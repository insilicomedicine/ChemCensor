from __future__ import annotations

import copy
from functools import cached_property
from typing import Optional
from typing import Union

from frozendict import frozendict
from rdkit import Chem

from .errors.molecule_errors import InvalidSMILESError
from .utils import drop_atom_maps
from .utils import extract_atom_map
from .utils import translate_atom_map


class Molecule:
    """
    Molecule class represents a molecule with a canonical SMILES
    string and a canonical RDKit molecule.
    """

    _cano_smiles: str
    _inv_cano_map: frozendict[int, int]
    _cano_mol: Chem.Mol
    _atom_map: Optional[frozendict[int, int | None]]

    def __init__(
        self,
        mol: Union[str, Chem.Mol],
        atom_map_from_dict: Optional[frozendict[int, int | None]] = None,
        disable_internal_atom_map: bool = False,
    ):
        """
        Initialize a Molecule object.
        :param mol: Molecule SMILES string or RDKit molecule;
        :type mol: str or Chem.Mol;
        :param atom_map_from_dict: Dictionary of atom map numbers to atom indices;
        :type atom_map_from_dict: Optional[frozendict[int, int | None]];
        :param disable_internal_atom_map: Disable internal atom map;
        :type disable_internal_atom_map: bool;
        """
        if isinstance(mol, Chem.Mol):
            init_mol = mol
        else:
            init_mol = Chem.MolFromSmiles(mol)

        if init_mol is None:
            raise InvalidSMILESError(mol)

        # calculate canonical smiles
        cano_smiles = Chem.MolToSmiles(init_mol, ignoreAtomMapNumbers=True)
        # calculate mapping from canonical form to the input form
        cano_indices = list(
            map(int, init_mol.GetProp("_smilesAtomOutputOrder")[1:-1].split(","))
        )
        self._inv_cano_map = frozendict(
            {i: cano_indices[i] for i in range(len(cano_indices))}
        )
        # recalculate smiles and init canonical rdmol
        tmp_mol = Chem.MolFromSmiles(cano_smiles)
        if tmp_mol is None:
            raise InvalidSMILESError(cano_smiles)

        self._cano_smiles = Chem.MolToSmiles(tmp_mol, ignoreAtomMapNumbers=True)
        self._cano_mol = Chem.MolFromSmiles(self._cano_smiles)

        if disable_internal_atom_map:
            self._atom_map = None
        elif atom_map_from_dict is not None:
            self._atom_map = translate_atom_map(self._inv_cano_map, atom_map_from_dict)
        else:
            self._atom_map = frozendict(
                {i: i + 1 for i in range(init_mol.GetNumAtoms())}
            )

    def copy(self, atom_map_dict: frozendict[int, int]) -> Molecule:
        """
        Copy a Molecule object with atom mappings.
        :param atom_map_dict: Dictionary of atom map numbers to atom indices;
        :type atom_map_dict: frozendict[int, int];
        :return: Molecule object;
        :rtype: Molecule;
        """
        return Molecule(
            mol=self.canonical_smiles,
            atom_map_from_dict=atom_map_dict,
            disable_internal_atom_map=False,
        )

    @property
    def canonical_smiles(self) -> str:
        """
        Get the canonical SMILES string of the molecule.
        :return: Canonical SMILES string;
        :rtype: str;
        """
        return self._cano_smiles

    @property
    def canonical_rdmol(self) -> Chem.Mol:
        """
        Get the canonical RDKit molecule of the molecule.
        :return: Canonical RDKit molecule;
        :rtype: Chem.Mol;
        """
        return self._cano_mol

    @cached_property
    def num_atoms(self) -> int:
        """
        Get the number of atoms in the molecule.
        :return: Number of atoms;
        :rtype: int;
        """
        return self._cano_mol.GetNumAtoms()

    @property
    def atom_map(self) -> Optional[frozendict[int, int | None]]:
        """
        Get the atom map of the molecule.
        :return: Atom map;
        :rtype: Optional[frozendict[int, int | None]];
        """
        return self._atom_map

    @cached_property
    def atom_mapped_canonical_smiles(self) -> str:
        """
        Get the atom-mapped canonical SMILES string of the molecule.
        :return: Atom-mapped canonical SMILES string;
        :rtype: str;
        """
        if self.atom_map is None:
            raise ValueError("Atom map is not set")
        rdmol = copy.deepcopy(self.canonical_rdmol)
        for atom in rdmol.GetAtoms():
            atom_map_num = self.atom_map[atom.GetIdx()] if self.atom_map else None
            atom.SetAtomMapNum(atom_map_num if atom_map_num else 0)
        return Chem.MolToSmiles(rdmol, ignoreAtomMapNumbers=True)

    @cached_property
    def atom_mapped_canonical_rdmol(self) -> Chem.Mol:
        """
        Get the atom-mapped canonical RDKit molecule of the molecule.
        :return: Atom-mapped canonical RDKit molecule;
        :rtype: Chem.Mol;
        """
        return Chem.MolFromSmiles(self.atom_mapped_canonical_smiles)

    @staticmethod
    def from_atom_mapped_rdmol(rdmol: Chem.Mol) -> Molecule:
        """
        Create a Molecule object from an atom-mapped RDKit molecule.
        :param rdmol: RDKit molecule;
        :type rdmol: Chem.Mol;
        :return: Molecule object;
        :rtype: Molecule;
        """
        return Molecule(
            drop_atom_maps(rdmol), atom_map_from_dict=extract_atom_map(rdmol)
        )

    @staticmethod
    def from_atom_mapped_smiles(smiles: str) -> Molecule:
        """
        Create a Molecule object from an atom-mapped SMILES string.
        :param smiles: SMILES string;
        :type smiles: str;
        :return: Molecule object;
        :rtype: Molecule;
        """
        rdmol = Chem.MolFromSmiles(smiles)
        if rdmol is None:
            raise InvalidSMILESError(smiles)
        return Molecule.from_atom_mapped_rdmol(rdmol)

    def __hash__(self) -> int:
        return hash(self.canonical_smiles)

    def __eq__(self, mol) -> bool:
        return self.canonical_smiles == mol.canonical_smiles
