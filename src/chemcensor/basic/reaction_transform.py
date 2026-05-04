from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from frozendict import frozendict

from .errors.reaction_transform_errors import ProductMissingAtomMapError
from .errors.reaction_transform_errors import ReactantsMissingAtomMapError
from .molecule import Molecule
from .utils import detect_product_atom_change
from .utils import translate_atom_map


@dataclass(frozen=True)
class ReactionTransform:
    """
    ReactionTransform class represents a reaction transform with
    reactants, product, and atom mappings.
    """

    reactants: tuple[Molecule, ...]
    product: Molecule
    pR_map: frozendict[int, tuple[int, ...] | None]
    Rp_map: tuple[frozendict[int, int | None], ...]
    p_reacting_atoms: tuple[int, ...] | None = None
    R_reacting_atoms: tuple[tuple[int, ...], ...] | None = None

    @property
    def has_reacting_atoms(self) -> bool:
        """True if edit-detection found product atoms that differ from reactants:
        including fragment attach, fragment detach, and property change
        (except for the stereotags).
        """
        return bool(self.p_reacting_atoms)

    @classmethod
    def from_reaction_smiles(cls, reaction_smiles: str) -> ReactionTransform:
        """Create ReactionTransform from reaction SMILES.

        :param reaction_smiles: Reaction SMILES
        :type reaction_smiles: str

        :return: ReactionTransform
        :rtype: ReactionTransform
        """
        R_smi_str, _, p_smi = reaction_smiles.split(">")
        R_smi_list = R_smi_str.split(".")

        # convert atom mapped smiles Molecule
        R = tuple(Molecule.from_atom_mapped_smiles(r_smi) for r_smi in R_smi_list)
        p = Molecule.from_atom_mapped_smiles(p_smi)

        # extract atom_map_num -> atom_idx maps for reactants and products
        p_map = p.atom_map
        if p_map is None or not any(p_map.values()):
            raise ProductMissingAtomMapError(reaction_smiles)

        R_maps = tuple(r.atom_map for r in R)
        if all(m is None or not any(m.values()) for m in R_maps):
            raise ReactantsMissingAtomMapError(reaction_smiles)

        amn_p_map = {
            atom_map_num: atom_idx
            for atom_idx, atom_map_num in p_map.items()
            if atom_map_num is not None
        }
        amn_R_map = {
            atom_map_num: (r_idx, atom_idx)
            for r_idx, r_map in enumerate(R_maps)
            if r_map is not None
            for atom_idx, atom_map_num in r_map.items()
            if atom_map_num is not None
        }

        # generate pR and Rp maps from atom maps and atom map number maps
        pR_map = translate_atom_map(p_map, amn_R_map, None)
        Rp_map = tuple(
            translate_atom_map(r_map, amn_p_map, None)
            for r_map in R_maps
            if r_map is not None
        )

        # init transform without reacting atom indices
        T = ReactionTransform(
            reactants=R,
            product=p,
            pR_map=pR_map,
            Rp_map=Rp_map,
        )

        # deduce reacting atom indices using edit detection and assign to the transform
        p_reacting_atoms = tuple(
            atom_idx
            for atom_idx in range(p.num_atoms)
            if detect_product_atom_change(T, atom_idx)
        )

        R_reacting_atoms = tuple(
            tuple(
                atom_idx
                for atom_idx in range(r.num_atoms)
                if (rp_map[atom_idx] is None or rp_map[atom_idx] in p_reacting_atoms)
            )
            for r, rp_map in zip(T.reactants, T.Rp_map)
        )

        return replace(
            T,
            p_reacting_atoms=p_reacting_atoms,
            R_reacting_atoms=R_reacting_atoms,
        )
