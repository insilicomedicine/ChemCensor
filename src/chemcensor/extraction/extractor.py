from __future__ import annotations

from dataclasses import replace

from frozendict import frozendict
from rdkit import Chem

from ..basic import Reaction
from ..basic import ReactionCenter
from ..basic import ReactionCenterFragment
from ..basic import ReactionCenterType
from ..basic import ReactionTransform
from ..configs.reaction_center_extraction_configs import BASE_CONFIG
from ..configs.reaction_center_extraction_configs import ExtractionConfig
from ..configs.reaction_center_extraction_configs import LINEAR_CONFIGS
from ..configs.reaction_center_extraction_configs import RING_CONFIGS
from .errors.extractor_errors import MissingReactingAtomsError
from .errors.extractor_errors import MissingReactionTransformError
from .molecule_fragment_extractor import MolecularFragmentExtractor
from .utils import find_symmetric_matches
from .utils import is_ring_atoms_within_indices


MAX_FRAGS_FOR_SYMMETRIC_EXPANSION = 5


class Extractor:
    """Extracts reaction centers from reactions."""

    def __init__(
        self, max_center_type: ReactionCenterType = ReactionCenterType.RC4
    ) -> None:
        """
        Initialize extractor with maximum center type.

        :param max_center_type: Maximum center type to extract (RC1–RC4).
        :type max_center_type: ReactionCenterType
        """
        self.max_center_type = max_center_type

    def _extract_single_rc(
        self,
        config: ExtractionConfig,
        T: ReactionTransform,
        skip_symmetric_expansion: bool = False,
    ) -> ReactionCenter:
        """
        Extract a single reaction center for the given config.

        :param config: Extraction configuration.
        :type config: ExtractionConfig
        :param T: Reaction transform with reacting atoms set.
        :type T: ReactionTransform
        :param skip_symmetric_expansion: Whether to skip symmetric expansion.
        :type skip_symmetric_expansion: bool

        :return: Extracted reaction center.
        :rtype: ReactionCenter
        """
        if (not T.p_reacting_atoms) or (not T.R_reacting_atoms):
            raise MissingReactingAtomsError()

        fragment_extractor = MolecularFragmentExtractor(config)

        # Extract product fragment
        product_fr_mol, product_indices = fragment_extractor.extract_fragment(
            mol=T.product,
            atom_indices=list(T.p_reacting_atoms),
        )
        product_fragment = ReactionCenterFragment(fr_mol=product_fr_mol)

        # Extract reactant fragments
        reactant_fragments: list[ReactionCenterFragment] = []
        reactants_indices: list[list[int]] = []

        for i, reactant in enumerate(T.reactants):
            reactant_fr_mol, reactant_indices = fragment_extractor.extract_fragment(
                mol=reactant,
                atom_indices=list(T.R_reacting_atoms[i]),
            )

            if not skip_symmetric_expansion:
                self._expand_symmetric_indices(
                    reactant.canonical_rdmol,
                    reactant_fr_mol,
                    reactant_indices,
                    product_indices,
                    T.Rp_map[i],
                )

            reactant_fragments.append(ReactionCenterFragment(fr_mol=reactant_fr_mol))
            reactants_indices.append(reactant_indices)

        return ReactionCenter(
            center_type=config.center_type,
            product_fragment=product_fragment,
            reactant_fragments=tuple(reactant_fragments),
            product_indices=frozenset(product_indices),
            reactant_indices=tuple(frozenset(indices) for indices in reactants_indices),
        )

    @staticmethod
    def _expand_symmetric_indices(
        rdmol: Chem.Mol,
        fragment: Chem.Mol,
        reactant_indices: list[int],
        product_indices: list[int],
        rp_map: frozendict[int, int | None],
    ) -> None:
        """Add indices from asymmetric substructure matches in-place.

        If *rdmol* has non-equivalent matches for *fragment* that differ
        from *reactant_indices*, both the reactant and the mapped product
        indices are extended accordingly.

        :param rdmol: Full reactant molecule.
        :param fragment: Extracted fragment molecule.
        :param reactant_indices: Reactant indices to extend (mutated).
        :param product_indices: Product indices to extend (mutated).
        :param rp_map: Reactant→product atom-index mapping.
        """
        reactant_set = set(reactant_indices)
        for sub in find_symmetric_matches(rdmol, fragment):
            if set(sub) == reactant_set:
                continue
            reactant_indices.extend(sub)
            product_indices.extend(
                mapped for idx in sub if (mapped := rp_map[idx]) is not None
            )

    def _has_too_many_base_fragments(self, T: ReactionTransform) -> bool:
        """Check whether the BASE_CONFIG product fragment has too many parts.

        When the product fragment consists of more than
        ``_MAX_FRAGS_FOR_SYMMETRIC_EXPANSION`` disconnected components,
        substructure matching in :meth:`_expand_symmetric_indices` becomes
        prohibitively expensive, so it should be skipped.

        :param T: Reaction transform with reacting atoms set.
        :type T: ReactionTransform
        :return: *True* if symmetric expansion should be skipped.
        :rtype: bool
        """
        if T.p_reacting_atoms is None:
            return False
        fragment_extractor = MolecularFragmentExtractor(BASE_CONFIG)
        product_fr_mol, _ = fragment_extractor.extract_fragment(
            mol=T.product,
            atom_indices=list(T.p_reacting_atoms),
        )
        n_frags = len(Chem.GetMolFrags(product_fr_mol))
        return n_frags > MAX_FRAGS_FOR_SYMMETRIC_EXPANSION

    @staticmethod
    def _has_ring_atoms_in_rc(
        T: ReactionTransform,
        rc: ReactionCenter,
    ) -> bool:
        """Check if the reaction center contains any ring atoms.

        :param T: Reaction transform.
        :type T: ReactionTransform
        :param rc: Reaction center.
        :type rc: ReactionCenter

        :return: True if the reaction center contains ring atoms, False otherwise.
        :rtype: bool
        """
        if is_ring_atoms_within_indices(
            T.product.canonical_rdmol, list(rc.product_indices)
        ):
            return True

        for i, r_indices in enumerate(rc.reactant_indices):
            if is_ring_atoms_within_indices(
                T.reactants[i].canonical_rdmol, list(r_indices)
            ):
                return True

        return False

    def _select_additional_configs(
        self, has_ring_atoms: bool
    ) -> tuple[ExtractionConfig, ...]:
        """Select configs for center types 2+ based on ring presence.

        :param has_ring_atoms: Whether the reaction center contains ring atoms.
        :type has_ring_atoms: bool

        :return: Tuple of ExtractionConfig objects.
        :rtype: tuple[ExtractionConfig, ...]
        """
        source = RING_CONFIGS if has_ring_atoms else LINEAR_CONFIGS
        return tuple(c for c in source if c.center_type <= self.max_center_type)

    def extract_rc(self, reaction: Reaction) -> Reaction:
        """
        Extract reaction centers from reaction.

        :param reaction: Reaction with reaction_transform set.
        :type reaction: Reaction
        :return: Reaction with populated reaction_centers.
        :rtype: Reaction
        :raises MissingReactionTransformError: If reaction_transform is not set.
        """
        T = reaction.reaction_transform
        if T is None:
            raise MissingReactionTransformError()

        skip_symmetric = self._has_too_many_base_fragments(T)

        # Extract base reaction center (type 1)
        base_rc = self._extract_single_rc(
            config=BASE_CONFIG,
            T=T,
            skip_symmetric_expansion=skip_symmetric,
        )
        reaction_centers: dict[ReactionCenterType, ReactionCenter] = {
            base_rc.center_type: base_rc
        }

        if self.max_center_type == ReactionCenterType.RC1:
            return replace(reaction, reaction_centers=frozendict(reaction_centers))

        # Choose ring-aware or linear configs based on base RC
        has_ring_atoms = self._has_ring_atoms_in_rc(T, base_rc)
        additional_configs = self._select_additional_configs(has_ring_atoms)

        for config in additional_configs:
            rc = self._extract_single_rc(
                config=config,
                T=T,
                skip_symmetric_expansion=skip_symmetric,
            )
            if rc not in reaction_centers.values():
                reaction_centers[rc.center_type] = rc

        return replace(reaction, reaction_centers=frozendict(reaction_centers))
