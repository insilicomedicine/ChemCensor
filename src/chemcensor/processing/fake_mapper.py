from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import replace
from typing import Any

from frozendict import frozendict
from rdkit import Chem

from ..basic import Reaction
from ..basic.errors.molecule_errors import InvalidSMILESError
from ..basic.molecule import Molecule
from .base import process_batch as _process_batch
from .errors.mapper_errors import MapperError

ATOM_MAPS_META_KEY = "atom_maps"


def _normalize_atom_map(m: Mapping[Any, int]) -> frozendict[int, int]:
    """Coerce atom-index map keys and values to ``int`` and return a frozen dict.

    :param m: Atom index to map number (keys may be int-like non-ints).
    :type m: Mapping[Any, int]

    :return: Immutable map with integer keys and values.
    :rtype: frozendict[int, int]
    """
    out: dict[int, int] = {}
    for k, v in m.items():
        ki = int(k) if not isinstance(k, int) else k
        out[ki] = int(v)
    return frozendict(out)


def _validate_atom_indices(fragment_smiles: str, maps: frozendict[int, int]) -> None:
    """Ensure every mapped atom index exists on the parsed fragment.

    :param fragment_smiles: Unmapped SMILES for one reaction fragment.
    :type fragment_smiles: str
    :param maps: Atom index to map number for that fragment.
    :type maps: frozendict[int, int]

    :raises InvalidSMILESError: If ``fragment_smiles`` does not parse.
    :raises MapperError: If any atom index is out of range for the fragment.
    """
    mol = Chem.MolFromSmiles(fragment_smiles)
    if mol is None:
        raise InvalidSMILESError(fragment_smiles)
    n = mol.GetNumAtoms()
    for idx in maps:
        if idx < 0 or idx >= n:
            raise MapperError(
                reaction_smiles=fragment_smiles,
                msg=f"Atom index {idx} out of range for fragment with {n} atoms",
            )


def _fragment_to_mapped_smiles(
    fragment_smiles: str, atom_idx_to_map: Mapping[Any, int]
) -> str:
    """Attach atom map numbers to a fragment and return canonical mapped SMILES.

    :param fragment_smiles: Unmapped SMILES for one dot-separated fragment.
    :type fragment_smiles: str
    :param atom_idx_to_map: RDKit atom index to map number for that fragment.
    :type atom_idx_to_map: Mapping[Any, int]

    :return: Canonical atom-mapped SMILES for the fragment.
    :rtype: str

    :raises MapperError: On invalid SMILES, out-of-range indices, or mapping failure.
    """
    maps = _normalize_atom_map(atom_idx_to_map)
    _validate_atom_indices(fragment_smiles, maps)
    try:
        mol = Molecule(fragment_smiles, atom_map_from_dict=maps)
        return mol.atom_mapped_canonical_smiles
    except InvalidSMILESError as e:
        raise MapperError(
            reaction_smiles=fragment_smiles,
            msg=str(e),
        ) from e


def _parse_payload(
    reaction_smiles: str, payload: Any
) -> tuple[tuple[Mapping[Any, int], ...], Mapping[Any, int]]:
    """Validate and unpack ``fake_mapper_atom_maps`` payload from reaction meta.

    :param reaction_smiles: Raw reaction SMILES (included in error messages).
    :type reaction_smiles: str
    :param payload: Value at ``meta[ATOM_MAPS_META_KEY]``.
    :type payload: Any

    :return: Per-reactant map sequence and product-side map.
    :rtype: tuple[tuple[Mapping[Any, int], ...], Mapping[Any, int]]

    :raises MapperError: If structure, keys, or value types are invalid.
    """
    if not isinstance(payload, Mapping):
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg=(
                f"meta[{ATOM_MAPS_META_KEY!r}] must be a mapping "
                f"with 'reactants' and 'product' keys"
            ),
        )
    try:
        reactants_maps = payload["reactants"]
        product_map = payload["product"]
    except KeyError as e:
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg=(f"meta[{ATOM_MAPS_META_KEY!r}] missing key {e!r}"),
        ) from e
    if not isinstance(reactants_maps, Sequence) or isinstance(
        reactants_maps,
        (str, bytes),
    ):
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg=(
                f"meta['{ATOM_MAPS_META_KEY}']['reactants'] must be a sequence "
                "of per-fragment maps"
            ),
        )
    if not isinstance(product_map, Mapping):
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg=(
                f"meta['{ATOM_MAPS_META_KEY}']['product'] must be a mapping from "
                "atom index to map number"
            ),
        )
    return tuple(reactants_maps), product_map


def build_mapped_reaction_smiles_from_meta(
    reaction_smiles: str,
    reactant_maps: Sequence[Mapping[Any, int]],
    product_map: Mapping[Any, int],
) -> str:
    """Build atom-mapped reaction SMILES from unmapped ``reaction_smiles`` and maps.

    Atom indices are RDKit ``MolFromSmiles`` indices for each dot-separated
    fragment, matching :class:`~chemcensor.basic.molecule.Molecule` input order.

    :param reaction_smiles: Unmapped reaction SMILES with ``>>`` separator.
    :type reaction_smiles: str
    :param reactant_maps: One atom-index map per dot-separated reactant fragment.
    :type reactant_maps: Sequence[Mapping[Any, int]]
    :param product_map: Atom index to map number for the product side.
    :type product_map: Mapping[Any, int]

    :return: Full atom-mapped reaction SMILES.
    :rtype: str

    :raises MapperError: If format, fragment counts, or mapping steps fail.
    """
    if ">>" not in reaction_smiles:
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg="Reaction SMILES must contain '>>'",
        )
    reactants_str, product_str = reaction_smiles.split(">>", maxsplit=1)
    reactant_frags = reactants_str.split(".") if reactants_str else []
    if len(reactant_frags) != len(reactant_maps):
        raise MapperError(
            reaction_smiles=reaction_smiles,
            msg=(
                f"meta['{ATOM_MAPS_META_KEY}']['reactants'] has length "
                f"{len(reactant_maps)} "
                f"but reaction has {len(reactant_frags)} reactant fragment(s)"
            ),
        )
    mapped_rx = [
        _fragment_to_mapped_smiles(frag, amap)
        for frag, amap in zip(reactant_frags, reactant_maps)
    ]
    mapped_prod = _fragment_to_mapped_smiles(product_str, product_map)
    return f"{'.'.join(mapped_rx)}>>{mapped_prod}"


class FakeMapper:
    """Applies atom mapping from :attr:`~chemcensor.basic.reaction.Reaction.meta`.

    Expects ``reaction.meta[ATOM_MAPS_META_KEY]`` to be a mapping::

        {
            "reactants": ( {atom_idx: map_num, ...}, ... ),
            "product": {atom_idx: map_num, ...},
        }

    There is one ``reactants`` entry per dot-separated reactant fragment.
    Fragment order follows ``reaction_smiles`` on each side of ``>>``.
    """

    def process(self, reaction: Reaction) -> Reaction:
        """Set ``mapped_reaction_smiles`` from meta-driven atom maps.

        :param reaction: Reaction with ``meta[ATOM_MAPS_META_KEY]`` populated.
        :type reaction: Reaction

        :return: Reaction with ``mapped_reaction_smiles`` set; dummies unchanged.
        :rtype: Reaction

        :raises MapperError: If meta is missing, invalid, or mapping fails.
        """
        if reaction.dummy:
            return reaction
        try:
            payload = reaction.meta[ATOM_MAPS_META_KEY]
        except KeyError as e:
            raise MapperError(
                reaction_smiles=reaction.reaction_smiles,
                msg=f"Missing meta[{ATOM_MAPS_META_KEY!r}] for FakeMapper",
            ) from e
        reactant_maps, product_map = _parse_payload(reaction.reaction_smiles, payload)
        mapped = build_mapped_reaction_smiles_from_meta(
            reaction.reaction_smiles,
            reactant_maps,
            product_map,
        )
        return replace(reaction, mapped_reaction_smiles=mapped)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Map a batch of reactions; dummies unchanged, failures become ``SENTINEL``.

        :param reactions: Reactions to map (batch size preserved).
        :type reactions: Sequence[Reaction]

        :return: Mapped reactions in the same order; failed slots are ``SENTINEL``.
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
