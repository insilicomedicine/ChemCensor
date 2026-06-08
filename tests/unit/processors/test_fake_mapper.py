import pytest
from frozendict import frozendict

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.mapper_errors import MapperError
from chemcensor.processing.fake_mapper import ATOM_MAPS_META_KEY
from chemcensor.processing.fake_mapper import FakeMapper
from chemcensor.processing.utils import prepare_fake_mapper_meta_from_mapped_rxn


@pytest.fixture
def fake_mapper():
    return FakeMapper()


def _meta(atom_maps: dict) -> frozendict[str, object]:
    return frozendict({ATOM_MAPS_META_KEY: atom_maps})


def test_process_symmetric_mapping(fake_mapper):
    reaction = Reaction(
        reaction_smiles="CC>>CC",
        meta=_meta({"reactants": ({0: 1, 1: 2},), "product": {0: 1, 1: 2}}),
    )
    out = fake_mapper.process(reaction)
    assert ">>" in out.mapped_reaction_smiles
    assert out.reaction_smiles == reaction.reaction_smiles
    mapped = out.mapped_reaction_smiles
    assert "[CH3:1]" in mapped or "[C:1]" in mapped


def test_process_two_reactant_fragments(fake_mapper):
    reaction = Reaction(
        reaction_smiles="C.C>>CC",
        meta=_meta(
            {
                "reactants": ({0: 1}, {0: 2}),
                "product": {0: 1, 1: 2},
            }
        ),
    )
    out = fake_mapper.process(reaction)
    assert out.mapped_reaction_smiles.count(">>") == 1
    assert ":1]" in out.mapped_reaction_smiles and ":2]" in out.mapped_reaction_smiles


def test_process_roundtrip_from_precomputed_mapped_rxn(fake_mapper):
    test_rxn = (
        "CNc1ncnc2c1CCNC2.Cc1cc(-c2cc(Sc3ccc(O)cc3)ccc2CO)c(C)n1CCC#N>>"
        "CNc1ncnc2c1CCN(Cc1ccc(Sc3ccc(O)cc3)cc1-c1cc(C)n(CCC#N)c1C)C2"
    )
    mapped_rxn = (
        "[CH3:1][NH:2][c:3]1[n:4][cH:5][n:6][c:7]2[c:8]1[CH2:9][CH2:10]"
        "[NH:11][CH2:38]2.[CH3:30][c:29]1[cH:28][c:27](-[c:26]2[cH:25][c:16]"
        "([S:17][c:18]3[cH:19][cH:20][c:21]([OH:22])[cH:23][cH:24]3)[cH:15]"
        "[cH:14][c:13]2[CH2:12]O)[c:36]([CH3:37])[n:31]1[CH2:32][CH2:33]"
        "[C:34]#[N:35]>>[CH3:1][NH:2][c:3]1[n:4][cH:5][n:6][c:7]2[c:8]1"
        "[CH2:9][CH2:10][N:11]([CH2:12][c:13]1[cH:14][cH:15][c:16]([S:17]"
        "[c:18]3[cH:19][cH:20][c:21]([OH:22])[cH:23][cH:24]3)[cH:25][c:26]1-"
        "[c:27]1[cH:28][c:29]([CH3:30])[n:31]([CH2:32][CH2:33][C:34]#[N:35])"
        "[c:36]1[CH3:37])[CH2:38]2"
    )
    meta = prepare_fake_mapper_meta_from_mapped_rxn(mapped_rxn)
    reaction = Reaction(reaction_smiles=test_rxn, meta=frozendict(meta))
    out = fake_mapper.process(reaction)
    assert out.mapped_reaction_smiles == mapped_rxn


def test_process_accepts_string_keys_for_atom_indices(fake_mapper):
    reaction = Reaction(
        reaction_smiles="CO>>CO",
        meta=_meta({"reactants": ({"0": 1, "1": 2},), "product": {"0": 1, "1": 2}}),
    )
    out = fake_mapper.process(reaction)
    assert out.mapped_reaction_smiles


def test_process_raises_when_meta_key_missing(fake_mapper):
    reaction = Reaction(reaction_smiles="CC>>CC")
    with pytest.raises(MapperError, match="atom_maps"):
        fake_mapper.process(reaction)


def test_process_raises_on_wrong_number_of_reactant_maps(fake_mapper):
    reaction = Reaction(
        reaction_smiles="C.C>>CC",
        meta=_meta({"reactants": ({0: 1},), "product": {0: 1, 1: 2}}),
    )
    with pytest.raises(MapperError, match="fragment"):
        fake_mapper.process(reaction)


def test_process_raises_on_atom_index_out_of_range(fake_mapper):
    reaction = Reaction(
        reaction_smiles="C>>C",
        meta=_meta({"reactants": ({0: 1, 1: 99},), "product": {0: 1}}),
    )
    with pytest.raises(MapperError, match="out of range"):
        fake_mapper.process(reaction)


def test_process_batch_passes_dummy_and_replaces_failure_with_sentinel(fake_mapper):
    good = Reaction(
        reaction_smiles="CC>>CC",
        meta=_meta({"reactants": ({0: 1, 1: 2},), "product": {0: 1, 1: 2}}),
    )
    bad = Reaction(reaction_smiles="CC>>CC")
    batch = [good, SENTINEL, bad]
    results = fake_mapper.process_batch(batch)
    assert not results[0].dummy
    assert results[1] is SENTINEL
    assert results[2].dummy


def test_dummy_reaction_unchanged(fake_mapper):
    r = SENTINEL
    assert fake_mapper.process(r) is r
