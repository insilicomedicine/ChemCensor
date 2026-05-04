from collections.abc import Mapping

from rdkit import Chem

from ..basic import MoleculeStereoSpecification
from ..basic import ReactionTransform


SYNTHETIC_IMPLICIT_STEREO_SLOT_ID_BASE = 10_000


def bond_key(a: int, b: int) -> tuple[int, int]:
    """Canonical undirected bond key: ``(min, max)`` of two atom indices.

    :param a: Atom index of the first atom
    :type a: int
    :param b: Atom index of the second atom
    :type b: int
    :return: Canonical undirected bond key
    :rtype: tuple[int, int]
    """
    return (a, b) if a < b else (b, a)


def permutation_parity(items: tuple[int, ...]) -> int:
    """Return parity of the local substituent ordering.

    We rely on RDKit returning atom neighbors in the same stereo-defining order
    that is used by the atom's raw tetrahedral tag. The local ids themselves do
    not carry stereochemical meaning; they only define a deterministic canonical
    order against which the current RDKit neighbor order can be compared.

    :param items: Ordered tuple of unique comparable ids.
    :type items: tuple[int, ...]
    :return: 0 for even parity, 1 for odd parity.
    :rtype: int

    Example:
        (4, 7, 10, 10004) -> sorted order (4, 7, 10, 10004) -> parity 0
        (7, 4, 10, 10004) -> one swap relative to sorted order -> parity 1
        (7, 10, 4, 10004) -> two swaps relative to sorted order -> parity 0
    """
    inversions = 0

    for i, left in enumerate(items):
        for right in items[i + 1 :]:
            if left > right:
                inversions += 1
    return inversions % 2


def get_center_neighbor_ids(
    mol: Chem.Mol,
    atom_idx: int,
    product_center_idx: int,
    idx_map: Mapping[int, int | None] | None = None,
) -> tuple[int, int, int, int]:
    """Return four stereo-defining neighbor ids for a tetrahedral center
    in product index space.

    When RDKit exposes only three explicit neighbors, the fourth slot is a
    synthetic implicit id.

    :param mol: RDKit molecule containing the center.
    :type mol: Chem.Mol
    :param atom_idx: Atom index of the stereocenter in *mol*.
    :type atom_idx: int
    :param product_center_idx: Product index of the center (used for the
        synthetic implicit slot).
    :type product_center_idx: int
    :param idx_map: Optional mapping from *mol* atom indices to product index
        space. ``None`` means *mol* is already the product (identity mapping).
    :type idx_map: Mapping[int, int | None] | None
    :return: Four stereo-defining neighbor ids
    :rtype: tuple[int, int, int, int]

    Example:
        If the center is atom ``10`` in molecule ``mol`` and the product center
        index is ``4``, this helper returns ``(10, 11, 12, 10004)``.
    """
    atom = mol.GetAtomWithIdx(atom_idx)
    if idx_map is None:
        neighbor_ids = tuple(n.GetIdx() for n in atom.GetNeighbors())
    else:
        neighbor_ids = tuple(idx_map[n.GetIdx()] for n in atom.GetNeighbors())

    if len(neighbor_ids) == 3:
        neighbor_ids = (
            *neighbor_ids,
            SYNTHETIC_IMPLICIT_STEREO_SLOT_ID_BASE + product_center_idx,
        )
    if len(neighbor_ids) != 4:
        raise ValueError(
            "Stereocenter does not have four stereo-defining substituent slots."
        )

    return (neighbor_ids[0], neighbor_ids[1], neighbor_ids[2], neighbor_ids[3])


def mapped_tetrahedral_center_matches(
    transform: ReactionTransform,
    product_atom_idx: int,
    reactant_idx: int,
    reactant_atom_idx: int,
) -> bool:
    """Check whether one mapped static tetrahedral center is preserved.

    The comparison uses local product-space ids for the four stereo-defining
    substituent slots plus raw RDKit chiral tags. For the same underlying
    geometry, a parity flip must coincide with a raw CW/CCW tag flip.

    :param transform: Reaction transform with atom mappings.
    :type transform: ReactionTransform
    :param product_atom_idx: Product atom index of the stereocenter.
    :type product_atom_idx: int
    :param reactant_idx: Reactant index mapped to the product center.
    :type reactant_idx: int
    :param reactant_atom_idx: Reactant atom index of the stereocenter.
    :type reactant_atom_idx: int
    :return: ``True`` if the mapped static center is preserved.
    :rtype: bool

    Example:
        If product and reactant expose the same four local ids but their
        neighbor order differs by one swap, the raw RDKit chiral tags must also
        be opposite. If parity flips but the raw tags stay equal, this helper
        returns ``False``.
    """
    product_mol = transform.product.canonical_rdmol
    reactant_mol = transform.reactants[reactant_idx].canonical_rdmol

    product_neighbor_ids = get_center_neighbor_ids(
        mol=product_mol,
        atom_idx=product_atom_idx,
        product_center_idx=product_atom_idx,
    )
    reactant_neighbor_ids = get_center_neighbor_ids(
        mol=reactant_mol,
        atom_idx=reactant_atom_idx,
        product_center_idx=product_atom_idx,
        idx_map=transform.Rp_map[reactant_idx],
    )

    parity_matches = permutation_parity(product_neighbor_ids) == permutation_parity(
        items=reactant_neighbor_ids
    )
    product_atom = product_mol.GetAtomWithIdx(product_atom_idx)
    reactant_atom = reactant_mol.GetAtomWithIdx(reactant_atom_idx)
    tag_matches = product_atom.GetChiralTag() == reactant_atom.GetChiralTag()
    return parity_matches == tag_matches


def get_static_assigned_atom_centers(
    stereo_spec: MoleculeStereoSpecification,
    reacting_atoms: tuple[int, ...] | None,
) -> frozenset[int]:
    """Return assigned atom stereocenters outside the reaction center.

    Assigned non-bridgehead and bridgehead stereocenters are both relevant for
    static validation. A center is considered static only when its atom index is
    not part of the detected reacting atoms.

    :param stereo_spec: Molecule stereo specification.
    :type stereo_spec: MoleculeStereoSpecification
    :param reacting_atoms: Atom indices marked dynamic by edit detection.
    :type reacting_atoms: tuple[int, ...] | None
    :return: Assigned static atom stereocenters.
    :rtype: frozenset[int]

    Example:
        If assigned centers are ``(3, 8, 11)`` and reacting atoms are
        ``(8, 9)``, this helper returns ``frozenset({3, 11})``.
    """
    reacting_atom_set = set(reacting_atoms or ())
    assigned_atoms = (
        stereo_spec.assigned_atom_centers + stereo_spec.assigned_bridgehead_atom_centers
    )
    return frozenset(
        atom_idx for atom_idx in assigned_atoms if atom_idx not in reacting_atom_set
    )


def get_static_assigned_bond_centers(
    stereo_spec: MoleculeStereoSpecification,
    reacting_atoms: tuple[int, ...] | None,
) -> frozenset[tuple[int, int]]:
    """Return assigned bond stereocenters outside the reaction center.

    A double bond is considered static only when neither of its end atoms is in
    the detected reaction center.

    :param stereo_spec: Molecule stereo specification.
    :type stereo_spec: MoleculeStereoSpecification
    :param reacting_atoms: Atom indices marked dynamic by edit detection.
    :type reacting_atoms: tuple[int, ...] | None
    :return: Assigned static bond stereocenters.
    :rtype: frozenset[tuple[int, int]]

    Example:
        If assigned bonds are ``((7, 3), (10, 11))`` and atom ``10`` is
        reacting, this helper returns ``frozenset({(3, 7)})``.
    """
    reacting_atom_set = set(reacting_atoms or ())
    return frozenset(
        bond_key(atom_idx_a, atom_idx_b)
        for atom_idx_a, atom_idx_b in stereo_spec.assigned_bond_centers
        if atom_idx_a not in reacting_atom_set and atom_idx_b not in reacting_atom_set
    )


def mapped_double_bond_stereo_matches(
    transform: ReactionTransform,
    product_atom_idx_a: int,
    product_atom_idx_b: int,
) -> bool:
    """Check whether one mapped static alkene center is preserved.

    Compares product and reactant bond stereo by projecting both sides into
    product index space. A side "flip" (RDKit chose the opposite stereo-defining
    substituent) inverts the raw E/Z label; two flips restore it.

    :param transform: Reaction transform with atom mappings.
    :type transform: ReactionTransform
    :param product_atom_idx_a: One product atom of the double bond.
    :type product_atom_idx_a: int
    :param product_atom_idx_b: The other product atom of the double bond.
    :type product_atom_idx_b: int
    :return: ``True`` if the mapped static bond stereocenter is preserved.
    :rtype: bool
    """
    product_mol = transform.product.canonical_rdmol
    product_bond = product_mol.GetBondBetweenAtoms(
        product_atom_idx_a,
        product_atom_idx_b,
    )

    product_begin = product_bond.GetBeginAtomIdx()
    product_end = product_bond.GetEndAtomIdx()

    begin_mapping = transform.pR_map.get(product_begin)
    end_mapping = transform.pR_map.get(product_end)
    if begin_mapping is None or end_mapping is None:  # unreachable; narrowing for mypy
        return False
    reactant_idx, reactant_begin = begin_mapping
    _, reactant_end = end_mapping

    reactant_mol = transform.reactants[reactant_idx].canonical_rdmol
    reactant_bond = reactant_mol.GetBondBetweenAtoms(reactant_begin, reactant_end)
    idx_map = transform.Rp_map[reactant_idx]

    product_stereo_atoms = tuple(product_bond.GetStereoAtoms())
    reactant_stereo_atoms = tuple(reactant_bond.GetStereoAtoms())

    # Re-orient the reactant stereo atoms so that "begin" and "end" mean the
    # same alkene side on both molecules.
    if reactant_bond.GetBeginAtomIdx() == reactant_begin:
        reactant_begin_stereo_atom = reactant_stereo_atoms[0]
        reactant_end_stereo_atom = reactant_stereo_atoms[1]
    else:
        reactant_begin_stereo_atom = reactant_stereo_atoms[1]
        reactant_end_stereo_atom = reactant_stereo_atoms[0]

    # A single side flip in RDKit's chosen stereo-defining substituents flips
    # the raw E/Z label; two flips restore it.
    begin_flip = product_stereo_atoms[0] != idx_map[reactant_begin_stereo_atom]
    end_flip = product_stereo_atoms[1] != idx_map[reactant_end_stereo_atom]

    stereo_matches = product_bond.GetStereo() == reactant_bond.GetStereo()
    return stereo_matches == (begin_flip == end_flip)


def confirm_center_consistency_in_static_part(
    transform: ReactionTransform,
    product_static_assigned_atom_centers: frozenset[int],
    reactants_static_assigned_atom_centers: tuple[frozenset[int], ...],
    reactants_pseudoasymmetric_atom_centers: tuple[frozenset[int], ...],
) -> bool:
    """Confirm that atom stereocenters in the static part are preserved.

    Both inputs already contain only assigned static stereocenters. The
    validator must prove that every assigned static reactant center is still
    present as an assigned static product center and that each such mapped pair
    passes :func:`mapped_tetrahedral_center_matches`.

    Product-only assigned centers are still treated as inconsistent by default.
    The only exception is a mapped reactant center already classified as
    pseudoasymmetric ``r/s`` in :class:`MoleculeStereoSpecification`. A
    pseudoasymmetric reactant center can legitimately become an ordinary
    uppercase ``R/S`` center after a remote change elsewhere in the molecule,
    and that transition should not be counted as a static stereo mismatch. By
    contrast, reactant ``?`` -> product ``R/S`` belongs to SIS only when there
    are no dynamic atoms; if the reaction reaches this validator, such a
    transition is inconsistent.

    :param transform: Reaction transform with atom mappings.
    :type transform: ReactionTransform
    :param product_static_assigned_atom_centers: Assigned static product atom
        stereocenters.
    :type product_static_assigned_atom_centers: frozenset[int]
    :param reactants_static_assigned_atom_centers: Assigned static reactant
        atom stereocenters grouped by reactant.
    :type reactants_static_assigned_atom_centers: tuple[frozenset[int], ...]
    :param reactants_pseudoasymmetric_atom_centers: Reactant pseudoasymmetric
        atom centers grouped by reactant.
    :type reactants_pseudoasymmetric_atom_centers: tuple[frozenset[int], ...]
    :return: ``True`` if all static atom stereocenters are preserved.
    :rtype: bool

    Example:
        If product static centers map to reactant centers
        ``{(0, 5), (0, 9)}`` and the same two reactant centers map back into
        the product static set, the helper returns ``True`` only when both
        mapped pairs also pass the local tetrahedral comparison.
    """
    expected_reactant_centers: set[tuple[int, int]] = set()
    for reactant_idx, reactant_atom_centers in enumerate(
        reactants_static_assigned_atom_centers
    ):
        for reactant_atom_idx in reactant_atom_centers:
            mapped_product_idx = transform.Rp_map[reactant_idx][reactant_atom_idx]
            if mapped_product_idx not in product_static_assigned_atom_centers:
                return False
            expected_reactant_centers.add((reactant_idx, reactant_atom_idx))

    for product_atom_idx in product_static_assigned_atom_centers:
        mapping = transform.pR_map.get(product_atom_idx)
        if mapping is None:  # unreachable; narrowing for mypy
            return False
        reactant_idx, reactant_atom_idx = mapping
        if (
            reactant_atom_idx
            not in reactants_static_assigned_atom_centers[reactant_idx]
        ):
            if (
                reactant_atom_idx
                in reactants_pseudoasymmetric_atom_centers[reactant_idx]
            ):
                continue
            return False

        if not mapped_tetrahedral_center_matches(
            transform=transform,
            product_atom_idx=product_atom_idx,
            reactant_idx=reactant_idx,
            reactant_atom_idx=reactant_atom_idx,
        ):
            return False

        if (reactant_idx, reactant_atom_idx) not in expected_reactant_centers:
            return False
        expected_reactant_centers.discard((reactant_idx, reactant_atom_idx))

    return len(expected_reactant_centers) == 0


def confirm_bond_stereo_consistency_in_static_part(
    transform: ReactionTransform,
    product_static_assigned_bond_centers: frozenset[tuple[int, int]],
    reactants_static_assigned_bond_centers: tuple[frozenset[tuple[int, int]], ...],
) -> bool:
    """Confirm that bond stereocenters in the static part are preserved.

    For alkenes we compare the two stereo-defining sides in product index
    space. The comparison is analogous to the tetrahedral case:
    first verify that product and reactant describe the same local
    substituent sets on both alkene atoms, then reconcile that local
    correspondence with RDKit's raw bond stereo assignment.

    The crucial complication for alkenes is that RDKit can choose the other
    stereo-defining substituent on one side after canonicalization or after
    a substituent priority change near the double bond. In that situation,
    the absolute E/Z label flips even though the local alkene geometry is
    still the same. A flip on both sides restores the original label.

    Example::

        product sides:   left=(4, H), right=(7, 9)
        reactant sides:  left=(4, H), right=(7, 9)
        same chosen substituents on both sides -> no side flips

        product sides:   left=(4, H), right=(7, 9)
        reactant sides:  left=(4, H), right=(7, 9)
        choose 4 vs H on the left -> one side flip -> raw E/Z label flips

        product sides:   left=(4, H), right=(7, 9)
        reactant sides:  left=(4, H), right=(7, 9)
        choose 4 vs H on the left and 7 vs 9 on the right
        -> two side flips -> raw E/Z label is restored

    :param transform: Reaction transform with atom mappings.
    :type transform: ReactionTransform
    :param product_static_assigned_bond_centers: Assigned static product
        bond stereocenters.
    :type product_static_assigned_bond_centers: frozenset[tuple[int, int]]
    :param reactants_static_assigned_bond_centers: Assigned static reactant
        bond stereocenters grouped by reactant.
    :type reactants_static_assigned_bond_centers:
        tuple[frozenset[tuple[int, int]], ...]
    :return: ``True`` if all static bond stereocenters are preserved.
    :rtype: bool

    Example:
        If product static bonds map to reactant bonds
        ``{(0, 7, 9), (0, 12, 14)}``, this helper returns ``True`` only when
        the same reactant bond set maps back into the product static set and
        each mapped alkene also passes :func:`mapped_double_bond_stereo_matches`.
    """
    expected_reactant_bonds: set[tuple[int, int, int]] = set()
    for reactant_idx, reactant_bond_centers in enumerate(
        reactants_static_assigned_bond_centers
    ):
        for reactant_atom_idx_a, reactant_atom_idx_b in reactant_bond_centers:
            product_atom_idx_a = transform.Rp_map[reactant_idx][reactant_atom_idx_a]
            product_atom_idx_b = transform.Rp_map[reactant_idx][reactant_atom_idx_b]
            # unreachable; narrowing for mypy
            if product_atom_idx_a is None or product_atom_idx_b is None:
                return False

            product_bond_key = bond_key(product_atom_idx_a, product_atom_idx_b)
            if product_bond_key not in product_static_assigned_bond_centers:
                return False

            expected_reactant_bonds.add(
                (reactant_idx, reactant_atom_idx_a, reactant_atom_idx_b)
            )

    for (
        product_atom_idx_a,
        product_atom_idx_b,
    ) in product_static_assigned_bond_centers:
        mapping_a = transform.pR_map.get(product_atom_idx_a)
        mapping_b = transform.pR_map.get(product_atom_idx_b)
        if mapping_a is None or mapping_b is None:  # unreachable; narrowing for mypy
            return False

        reactant_idx, reactant_atom_idx_a = mapping_a
        _, reactant_atom_idx_b = mapping_b

        reactant_bond_key = bond_key(reactant_atom_idx_a, reactant_atom_idx_b)
        if (
            reactant_bond_key
            not in reactants_static_assigned_bond_centers[reactant_idx]
        ):
            return False

        if not mapped_double_bond_stereo_matches(
            transform=transform,
            product_atom_idx_a=product_atom_idx_a,
            product_atom_idx_b=product_atom_idx_b,
        ):
            return False

        expected_reactant_bonds.discard(
            (reactant_idx, reactant_bond_key[0], reactant_bond_key[1])
        )

    return len(expected_reactant_bonds) == 0
