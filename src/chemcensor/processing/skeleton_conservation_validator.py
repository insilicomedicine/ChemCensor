from collections.abc import Iterable
from collections.abc import Sequence
from typing import NamedTuple

from rdkit import Chem

from ..basic import Reaction
from .base import process_batch as _process_batch
from .errors.skeleton_conservation_validator_errors import (
    SkeletonConservationValidatorEmptyTransformError,
)
from .errors.skeleton_conservation_validator_errors import (
    SkeletonConservationValidatorTruncatedCarbonChainError,
)

_CARBON_ATOMIC_NUM = 6


class _UnmappedComponent(NamedTuple):
    """A connected component of unmapped atoms and its screening flags.

    :ivar atoms: Atom indices making up the component.
    :ivar is_pure_carbon: ``True`` when every atom is carbon.
    :ivar attached_to_carbon: ``True`` when the component is bonded to the
        retained (mapped) skeleton through at least one carbon atom, i.e. across
        a broken carbon-carbon bond.
    :ivar attached_via_double_bond_to_carbon: ``True`` when at least one
        attachment to a retained carbon is a double bond (terminal / exocyclic
        ``=CH2`` lost in C=C → C=O cleavage).
    """

    atoms: frozenset[int]
    is_pure_carbon: bool
    attached_to_carbon: bool
    attached_via_double_bond_to_carbon: bool


def _explore_unmapped_component(
    rdmol: Chem.Mol,
    start: int,
    unmapped: set[int],
    visited: set[int],
) -> _UnmappedComponent:
    """Explore the connected component of unmapped atoms containing ``start``.

    Purity and skeleton-attachment are gathered in the same pass. ``visited`` is
    updated on push so each atom is expanded exactly once.

    :param rdmol: Molecule being inspected.
    :param start: Seed atom index (unmapped, not yet visited).
    :param unmapped: All unmapped atom indices in ``rdmol``.
    :param visited: Atoms already assigned to a component; mutated in place.
    :return: The component together with its screening flags.
    :rtype: _UnmappedComponent
    """
    component: list[int] = [start]
    visited.add(start)
    is_pure_carbon = True
    attached_to_carbon = False
    attached_via_double_bond_to_carbon = False

    stack = [start]
    while stack:
        atom_idx = stack.pop()
        atom = rdmol.GetAtomWithIdx(atom_idx)
        if atom.GetAtomicNum() != _CARBON_ATOMIC_NUM:
            is_pure_carbon = False

        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor_idx not in unmapped:
                # neighbor belongs to the retained skeleton (an attachment point)
                if neighbor.GetAtomicNum() == _CARBON_ATOMIC_NUM:
                    attached_to_carbon = True
                    bond = rdmol.GetBondBetweenAtoms(atom_idx, neighbor_idx)
                    if bond is not None and bond.GetBondType() == Chem.BondType.DOUBLE:
                        attached_via_double_bond_to_carbon = True
                continue
            if neighbor_idx in visited:
                continue
            visited.add(neighbor_idx)
            component.append(neighbor_idx)
            stack.append(neighbor_idx)

    return _UnmappedComponent(
        atoms=frozenset(component),
        is_pure_carbon=is_pure_carbon,
        attached_to_carbon=attached_to_carbon,
        attached_via_double_bond_to_carbon=attached_via_double_bond_to_carbon,
    )


def _is_terminal_methylene_cleavage(component: _UnmappedComponent) -> bool:
    """Return whether *component* is a single ``=CH2`` lost across a C=C bond.

    Oxidative cleavage of a terminal / exocyclic methylene to a carbonyl leaves
    exactly one unmapped carbon that was double-bonded to the retained skeleton.
    That is legitimate chemistry, unlike silent homolog drift of a singly bonded
    alkyl carbon (ethyl ether → methyl ether).

    :param component: Explored unmapped component.
    :type component: _UnmappedComponent
    :return: ``True`` when the component should not be flagged.
    :rtype: bool
    """
    return len(component.atoms) == 1 and component.attached_via_double_bond_to_carbon


def find_truncated_carbon_fragments(
    rdmol: Chem.Mol,
    unmapped_indices: Iterable[int],
    max_fragment_size: int | None,
) -> list[frozenset[int]]:
    """Return connected components of unmapped atoms that look like a silently
    truncated carbon chain.

    A component qualifies when all of the following hold:

    * every atom in the component is carbon (a pure-hydrocarbon fragment);
    * the component is attached to the retained (mapped) skeleton, i.e. at least
      one of its atoms has a neighbor outside the component;
    * at least one such attachment neighbor is a carbon (the broken bond is a
      carbon-carbon bond, not a carbon-heteroatom bond as in legitimate O-/N-
      dealkylation);
    * the component is not a single carbon double-bonded to the skeleton
      (terminal / exocyclic ``=CH2`` lost in C=C → C=O cleavage);
    * the component is not larger than ``max_fragment_size`` (when set).

    Neighbors outside the component are always mapped atoms: any adjacent
    unmapped atom would belong to the same connected component.

    :param rdmol: Molecule whose unmapped atoms are inspected.
    :type rdmol: Chem.Mol
    :param unmapped_indices: Atom indices with no counterpart on the other side
        of the reaction (deleted reactant atoms or added product atoms).
    :type unmapped_indices: Iterable[int]
    :param max_fragment_size: Maximum number of atoms a flagged component may
        contain. ``None`` disables the size cap.
    :type max_fragment_size: int | None
    :return: Suspicious pure-hydrocarbon components (as frozensets of indices).
    :rtype: list[frozenset[int]]
    """
    unmapped = set(unmapped_indices)
    visited: set[int] = set()
    suspicious: list[frozenset[int]] = []

    for start in unmapped:
        if start in visited:
            continue

        component = _explore_unmapped_component(
            rdmol=rdmol,
            start=start,
            unmapped=unmapped,
            visited=visited,
        )

        if not component.is_pure_carbon or not component.attached_to_carbon:
            continue
        if _is_terminal_methylene_cleavage(component):
            continue
        if max_fragment_size is not None and len(component.atoms) > max_fragment_size:
            continue

        suspicious.append(component.atoms)

    return suspicious


class SkeletonConservationValidator:
    """Reject reactions where a carbon skeleton is silently truncated or grown.

    Some records carry data-extraction artifacts such as an ethyl ether that
    "becomes" a methyl ether (``CCOC...`` -> ``COC...``): the carbon-oxygen bond
    is preserved, yet the alkyl chain loses a carbon with no leaving group,
    reagent, or product to account for it. After atom mapping such a carbon is
    an unmapped atom that remains attached to the retained skeleton through a
    broken carbon-carbon bond.

    This validator flags those cases while leaving legitimate chemistry intact:

    * O-/N-dealkylation break a carbon-heteroatom bond (attachment neighbor is
      not carbon), so they are not flagged;
    * protecting-group removal (Boc, Cbz, esters) deletes fragments that contain
      heteroatoms, so they are not pure-hydrocarbon components;
    * unmapped spectator/reagent molecules are separate components with no bond
      to the retained skeleton (and are already dropped by ``OrphanRemover``);
    * terminal / exocyclic ``=CH2`` lost across a C=C bond (oxidative cleavage
      to a carbonyl) is a single carbon double-bonded to the skeleton, so it is
      not flagged.

    By default only deletions (reactant side) are checked, because adding a
    pure-hydrocarbon fragment across a carbon-carbon bond is common, legitimate
    chemistry (alkylation, arylation, C-C couplings). Enable ``check_additions``
    to also flag unmapped carbon fragments appearing on the product side.
    """

    def __init__(
        self,
        max_fragment_size: int | None = None,
        check_additions: bool = False,
    ) -> None:
        """Initialize the validator.

        :param max_fragment_size: Optional cap on the size of a flagged
            pure-hydrocarbon component. ``None`` (the default) flags a truncated
            carbon chain of any length, since data-extraction errors are not
            limited to short "homolog drift" (methyl/ethyl/propyl) and also occur
            in long chains. Set an integer only to deliberately restrict the
            check to small fragments.
        :type max_fragment_size: int | None
        :param check_additions: When ``True``, also flag unmapped carbon
            fragments added on the product side. Off by default to avoid
            flagging legitimate C-C bond-forming reactions.
        :type check_additions: bool
        """
        self.max_fragment_size = max_fragment_size
        self.check_additions = check_additions

    def process(self, reaction: Reaction) -> Reaction:
        """Validate carbon-skeleton conservation and return the reaction on success.

        :param reaction: Reaction to validate.
        :type reaction: Reaction
        :return: The same reaction instance if validation succeeds.
        :rtype: Reaction
        :raises SkeletonConservationValidatorEmptyTransformError: If
            ``reaction.reaction_transform`` is missing.
        :raises SkeletonConservationValidatorTruncatedCarbonChainError: If a
            pure-hydrocarbon fragment is deleted from (or, with
            ``check_additions``, added to) the retained skeleton across a broken
            carbon-carbon bond.
        """
        transform = reaction.reaction_transform
        if transform is None:
            raise SkeletonConservationValidatorEmptyTransformError()

        reaction_smiles = reaction.processed_reaction_smiles or reaction.reaction_smiles

        # Deletions: unmapped atoms of each reactant (no product counterpart).
        for reactant, rp_map in zip(transform.reactants, transform.Rp_map):
            rdmol = reactant.canonical_rdmol
            unmapped = [
                idx for idx in range(rdmol.GetNumAtoms()) if rp_map[idx] is None
            ]
            if find_truncated_carbon_fragments(rdmol, unmapped, self.max_fragment_size):
                raise SkeletonConservationValidatorTruncatedCarbonChainError(
                    reaction_smiles=reaction_smiles, side="reactant"
                )

        # Additions: unmapped atoms of the product (no reactant counterpart).
        if self.check_additions:
            rdmol = transform.product.canonical_rdmol
            unmapped = [
                idx
                for idx in range(rdmol.GetNumAtoms())
                if transform.pR_map[idx] is None
            ]
            if find_truncated_carbon_fragments(rdmol, unmapped, self.max_fragment_size):
                raise SkeletonConservationValidatorTruncatedCarbonChainError(
                    reaction_smiles=reaction_smiles, side="product"
                )

        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Validate a batch of reactions.

        :param reactions: Batch of reactions to validate.
        :type reactions: Sequence[Reaction]
        :return: Validated reactions in the original order.
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
