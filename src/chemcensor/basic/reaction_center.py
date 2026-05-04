from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from enum import IntEnum
from functools import cached_property
from functools import partial

import numpy as np

from ..rules.functional_groups import FG_SIGNATURE_LENGTH
from .reaction_center_fragment import ReactionCenterFragment
from .utils import canonicalize_smiles


class ReactionCenterType(IntEnum):
    """Type of reaction center by context width.

    RC1: only reacting atoms and their neighbors (base).
    RC2, RC3, RC4: extended context (more neighbors/rings).
    """

    RC1 = 1
    RC2 = 2
    RC3 = 3
    RC4 = 4


@dataclass(frozen=True)
class ReactionCenter:
    """Represents a reaction center with its type and signature.

    :param center_type: Type/level of the reaction center (ReactionCenterType).
    :param product_fragment: Fragment of the product molecule.
    :param reactant_fragments: Fragments of the reactant molecules.
    :param product_indices: Atom indices in the product molecule that belong to the
        reacting fragment. Functional group matches intersecting these indices are
        excluded from the signature.
    :param reactant_indices: Per-reactant atom indices that belong to the reacting
        fragment. Each element corresponds to one reactant molecule of the transform.
        Functional group matches intersecting these indices are excluded.
    :param fg_signature: Binary vector indicating which functional groups are present
        in the reaction environment (excluding the reacting fragment). Defaults to
        an all-zero vector of length ``FG_SIGNATURE_LENGTH``.
    """

    center_type: ReactionCenterType
    product_fragment: ReactionCenterFragment
    reactant_fragments: tuple[ReactionCenterFragment, ...]
    product_indices: frozenset[int] = frozenset()
    reactant_indices: tuple[frozenset[int], ...] = ()
    fg_signature: np.ndarray = field(
        default_factory=partial(np.zeros, FG_SIGNATURE_LENGTH, dtype=np.uint8)
    )

    @cached_property
    def reaction_center_smiles(self) -> str:
        """Build canonical reaction SMILES from all fragment components.

        Merges unique component SMILES from all reactant and product fragments,
        then canonicalizes both sides via :pyfunc:`canonicalize_smiles`
        (``MolFromSmarts`` → ``MolToSmiles`` round-trip).

        Format: ``reactant_components>>product_components``

        :return: Canonical reaction center SMILES string.
        :rtype: str
        """
        # join full fragment SMILES (not components-as-set) to preserve
        # duplicates when the same substructure appears in multiple fragments
        reactants_smiles = ".".join(frag.smiles for frag in self.reactant_fragments)
        product_smiles = self.product_fragment.smiles

        r_canonical = canonicalize_smiles(reactants_smiles)
        p_canonical = canonicalize_smiles(product_smiles)

        return f"{r_canonical}>>{p_canonical}"

    @cached_property
    def reaction_center_components(self) -> tuple[str, ...]:
        """Split the reaction center into individual simple components.

        Each component is a ``reactant(s)>>product(s)`` SMILES representing
        one "simple" reaction center — determined by overlapping atom-map
        numbers between reactant and product fragments.  Reactant pieces
        are distinguished by their atom-map sets (not only unmapped SMILES),
        so two stoichiometric copies of the same reagent stay separate.
        Product pieces that touch the same reactant map set
        merge on the right-hand side (``"."``-joined, then canonicalized),
        e.g. carbonate opening to two ``CO`` fragments.  Several reactant
        pieces matching one product fragment appear on the left as
        ``r1.r2`` (dot-joined).

        Canonicalization is identical to :pyattr:`reaction_center_smiles`
        (``canonicalize_smiles``), so the same sub-reaction extracted from
        a single-component reaction will match the one extracted from
        a multi-component reaction.

        Falls back to the full :pyattr:`reaction_center_smiles` if no
        atom-map-based pairing can be established.

        The tuple order follows the first-seen order of product
        pieces (not a separate global sort): each side
        is still canonicalized via :pyfunc:`canonicalize_smiles`.

        :return: Tuple of canonical ``R>>P`` SMILES strings.
        :rtype: tuple[str, ...]
        """
        r_parts = [
            part for frag in self.reactant_fragments for part in frag.mapped_components
        ]
        p_parts = self.product_fragment.mapped_components

        # Group key: frozenset of each matched reactant component's atom-map set.
        groups: defaultdict[frozenset[frozenset[int]], list[str]] = defaultdict(list)
        r_order_by_key: dict[frozenset[frozenset[int]], tuple[str, ...]] = {}
        key_order: list[frozenset[frozenset[int]]] = []

        for p_smi, p_maps in p_parts:
            if not p_maps:
                continue
            matched_entries = [
                (r_smi, r_maps) for r_smi, r_maps in r_parts if r_maps & p_maps
            ]
            if not matched_entries:
                continue
            key = frozenset(r_maps for _, r_maps in matched_entries)
            if key not in r_order_by_key:
                r_order_by_key[key] = tuple(r_smi for r_smi, _ in matched_entries)
                key_order.append(key)
            groups[key].append(p_smi)

        if not key_order:
            return (self.reaction_center_smiles,)

        out: tuple[str, ...] = ()
        for key in key_order:
            r_canonical = canonicalize_smiles(".".join(r_order_by_key[key]))
            p_canonical = canonicalize_smiles(".".join(groups[key]))
            out += (f"{r_canonical}>>{p_canonical}",)

        return out if out else (self.reaction_center_smiles,)

    @cached_property
    def is_reaction_center_composite(self) -> bool:
        """Check if the reaction center is composite
        (multi-site reaction center), i.e.
        it has more than one unique component.

        A composite reaction center consists of multiple
        independent transformations happening simultaneously
        (e.g., Boc + Cbz deprotection). Each individual transformation
        is a simple reaction center (component).

        :return: True if the reaction center is composite, False otherwise.
        :rtype: bool
        """
        return len(self.reaction_center_components) > 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReactionCenter):
            return NotImplemented
        return self.reaction_center_smiles == other.reaction_center_smiles

    def __hash__(self) -> int:
        return hash((self.reaction_center_smiles,))
