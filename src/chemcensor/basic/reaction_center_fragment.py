from dataclasses import dataclass
from functools import cached_property

from rdkit import Chem

from .utils import drop_atom_maps


@dataclass(frozen=True)
class ReactionCenterFragment:
    """Represents a reaction center fragment as an RDKit query molecule.

    :param fr_mol: RDKit molecule object representing the fragment.
    """

    fr_mol: Chem.Mol

    @cached_property
    def atom_mapped_smiles(self) -> str:
        """Return the atom-mapped SMILES string for the fragment.

        :return: Atom-mapped SMILES representation of the fragment.
        :rtype: str
        """
        return Chem.MolToSmiles(self.fr_mol, ignoreAtomMapNumbers=False)

    @cached_property
    def smiles(self) -> str:
        """Return the SMILES string for the fragment.

        :return: SMILES representation of the fragment.
        :rtype: str
        :raises ValueError: If the fragment cannot be converted to SMILES.
        """
        # drop atom maps from the fragment
        fr_mol = drop_atom_maps(self.fr_mol)
        smiles = Chem.MolToSmiles(fr_mol)
        if not smiles:
            raise ValueError("Failed to convert reaction center fragment to SMILES")
        return smiles

    @cached_property
    def mapped_components(self) -> tuple[tuple[str, frozenset[int]], ...]:
        """Extract unmapped SMILES and atom-map numbers for each disconnected component.

        Uses ``GetMolFrags`` to split the fragment molecule into individual
        connected components.  For each component returns a pair of:

        * unmapped canonical SMILES (via ``drop_atom_maps`` + ``MolToSmiles``);
        * frozenset of atom-map numbers present in that component.

        The unmapped SMILES here is an intermediate value — final
        canonicalization (``MolFromSmarts`` round-trip) happens in
        :pyattr:`ReactionCenter.reaction_center_components`.

        :return: Tuple of ``(unmapped_smiles, atom_map_numbers)`` pairs.
        :rtype: tuple[tuple[str, frozenset[int]], ...]
        """
        frags = Chem.GetMolFrags(self.fr_mol, asMols=True, sanitizeFrags=False)
        result: list[tuple[str, frozenset[int]]] = []
        for frag in frags:
            unmapped = Chem.MolToSmiles(drop_atom_maps(frag))
            if not unmapped:
                continue
            maps = frozenset(
                a.GetAtomMapNum() for a in frag.GetAtoms() if a.GetAtomMapNum() != 0
            )
            result.append((unmapped, maps))
        return tuple(result)

    def __repr__(self) -> str:
        return f"ReactionCenterFragment(smiles='{self.smiles}')"

    def __str__(self) -> str:
        return self.smiles
