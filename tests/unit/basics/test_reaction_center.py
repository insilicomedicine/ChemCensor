from dataclasses import dataclass
from functools import cached_property

import pytest

from chemcensor.basic import Reaction
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.extraction.extractor import Extractor
from chemcensor.processing.orphan_remover import OrphanRemover
from chemcensor.processing.reaction_processor import ReactionProcessor
from chemcensor.processing.transform_creator import TransformCreator


def process_mapped_reaction_for_rc_extraction(mapped_rxn: str) -> Reaction:
    """
    Strip unmapped fragments (solvents, salts, ...) and build ``reaction_transform``
    like production.

    Pipeline: OrphanRemover -> TransformCreator.
    """
    mapped_rxn = mapped_rxn.strip()
    reaction = Reaction(reaction_smiles=mapped_rxn, mapped_reaction_smiles=mapped_rxn)
    return ReactionProcessor(
        processors=(
            OrphanRemover(),
            TransformCreator(),
        )
    ).process(reaction)


@dataclass(frozen=True)
class ReactionCenterTestCase:
    id: str
    reaction_mapped_smiles: str
    expected_rc_components: dict[ReactionCenterType, tuple[str, ...]]
    expected_rc_is_composite: dict[ReactionCenterType, bool]

    @cached_property
    def processed_reaction(self) -> Reaction:
        reaction = process_mapped_reaction_for_rc_extraction(
            self.reaction_mapped_smiles
        )
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        return ext.extract_rc(reaction)


_REACTION_CENTER_TEST_CASES: list[ReactionCenterTestCase] = [
    ReactionCenterTestCase(
        id="tricomponent_reaction_1",
        reaction_mapped_smiles=(
            "[CH3:1][CH:2]([CH3:3])[CH2:4][OH:5].[NH2:12][C@@H:13]1[CH2:14][CH2:15]"
            "[CH2:16][CH2:17][C@H:18]1[OH:19].[O:11]=[C:10](O)[c:9]1[cH:8][n:7][c:6]"
            "(Cl)[c:21](Br)[cH:20]1.OB(O)[c:22]1[cH:23][cH:24][c:25]([Cl:26])"
            "[cH:27][cH:28]1>>[CH3:1][CH:2]([CH3:3])[CH2:4][O:5][c:6]1[n:7]"
            "[cH:8][c:9]([C:10](=[O:11])[NH:12][C@@H:13]2[CH2:14][CH2:15][CH2:16]"
            "[CH2:17][C@H:18]2[OH:19])[cH:20][c:21]1-[c:22]1[cH:23][cH:24][c:25]"
            "([Cl:26])[cH:27][cH:28]1"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "CO.cc(Br)c(n)Cl.cc(c)B(O)O>>COc(n)c(c)-c(c)c",
                "CN.cC(O)=O>>CNC(c)=O",
            ),
            ReactionCenterType.RC2: (
                "CO.N[C@@H]1CCCC[C@H]1O.OB(O)c1ccccc1.OC(=O)c1cnc(Cl)c(Br)c1>>"
                "COc1ncc(C(=O)N[C@@H]2CCCC[C@H]2O)cc1-c1ccccc1",
            ),
            ReactionCenterType.RC4: (
                "CO.N[C@@H]1CCCC[C@H]1O.OB(O)c1ccc(Cl)cc1."
                "OC(=O)c1cnc(Cl)c(Br)c1>>COc1ncc(C(=O)N[C@@H]2CCCC[C@H]2O)"
                "cc1-c1ccc(Cl)cc1",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: False,
            ReactionCenterType.RC4: False,
        },
    ),
    ReactionCenterTestCase(
        id="tricomponent_reaction_2",
        reaction_mapped_smiles=(
            "[CH2:1]=[CH:2][C:3](=[O:4])Cl.CC(C)(C)OC(=O)[N:5]1[CH2:6][CH2:7][CH:8]"
            "([CH2:9][NH2:10])[CH2:31][CH2:32]1.CC1(C)OB([c:18]2[cH:19][cH:20][c:21]"
            "([NH:22][c:23]3[cH:24][cH:25][cH:26][cH:27][cH:28]3)[cH:29][cH:30]2)OC1(C)"
            "C.[NH2:16][c:15]1[n:14][cH:13][n:12][c:11](Cl)[c:17]1Cl>>"
            "[CH2:1]=[CH:2][C:3](=[O:4])[N:5]1[CH2:6][CH2:7][CH:8]([CH2:9][NH:10][c:11]"
            "2[n:12][cH:13][n:14][c:15]([NH2:16])[c:17]2-[c:18]2[cH:19][cH:20][c:21]"
            "([NH:22][c:23]3[cH:24][cH:25][cH:26][cH:27][cH:28]3)[cH:29][cH:30]2)"
            "[CH2:31][CH2:32]1"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "CC(=O)Cl.CN(C)C(=O)OC(C)(C)C>>CC(=O)N(C)C",
                "CC1(C)OB(c(c)c)OC1(C)C.CN.cc(Cl)c(n)Cl>>CNc(n)c(c)-c(c)c",
            ),
            ReactionCenterType.RC2: (
                "CC(=O)Cl.CC(C)(C)OC(=O)N1CCC(CN)CC1.CC1(C)OB(c2ccccc2)OC1(C)C."
                "Clc1cncnc1Cl>>CC(=O)N1CCC(CNc2ncncc2-c2ccccc2)CC1",
            ),
            ReactionCenterType.RC4: (
                "CC(=O)Cl.CC(C)(C)OC(=O)N1CCC(CN)CC1.CC1(C)OB(c2ccc(N)cc2)OC1"
                "(C)C.Nc1ncnc(Cl)c1Cl>>CC(=O)N1CCC(CNc2ncnc(N)c2-c2ccc(N)cc2)CC1",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: False,
            ReactionCenterType.RC4: False,
        },
    ),
    ReactionCenterTestCase(
        id="tricomponent_reaction_3",
        reaction_mapped_smiles=(
            "[CH3:1][CH2:2][c:3]1[cH:4][c:5]2[c:6](=[O:7])[nH:8][c:20](=[O:21])[n:22]("
            "[CH2:23][c:24]3[cH:25][cH:26][c:27](-[c:28]4[cH:29][c:30]([F:31])[cH:32]"
            "[cH:33][c:34]4[C:35]#[N:40])[cH:41][cH:42]3)[c:43]2[s:44]1.CN(C)C=O."
            "[CH3:17][O:16][c:15]1[cH:14][cH:13][c:12]([C:10](=[O:11])[CH2:9]Br)[cH:19]"
            "[cH:18]1.CS(C)=O.ClC(Cl)Cl.[O:39]=[C:38]([O-])O.[Cl-].[H-].[NH3+:36][OH:37"
            "].[Na+]>>[CH3:1][CH2:2][c:3]1[cH:4][c:5]2[c:6](=[O:7])[n:8]([CH2:9][C:10]"
            "(=[O:11])[c:12]3[cH:13][cH:14][c:15]([O:16][CH3:17])[cH:18][cH:19]3)[c:20]"
            "(=[O:21])[n:22]([CH2:23][c:24]3[cH:25][cH:26][c:27](-[c:28]4[cH:29][c:30]"
            "([F:31])[cH:32][cH:33][c:34]4-[c:35]4[n:36][o:37][c:38](=[O:39])[nH:40]4)"
            "[cH:41][cH:42]3)[c:43]2[s:44]1"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "O=CCBr.O=c[nH]c=O>>O=CCn(c=O)c=O",
                "NO.OC(O)=O.cC#N>>c-c1noc(=O)[nH]1",
            ),
            ReactionCenterType.RC2: (
                "O=CCBr.O=c1ccnc(=O)[nH]1>>O=CCn1c(=O)ccnc1=O",
                "N#Cc1ccccc1.NO.OC(O)=O>>O=c1[nH]c(-c2ccccc2)no1",
            ),
            ReactionCenterType.RC3: (
                "O=CCBr.O=c1nc2sccc2c(=O)[nH]1>>O=CCn1c(=O)nc2sccc2c1=O",
                "N#Cc1ccccc1.NO.OC(O)=O>>O=c1[nH]c(-c2ccccc2)no1",
            ),
            ReactionCenterType.RC4: (
                "Cc1cc2c(=O)[nH]c(=O)n(C)c2s1.O=CCBr>>Cc1cc2c(=O)n(CC=O)c(=O)n(C)c2s1",
                "NO.OC(O)=O.c-c1cc(F)ccc1C#N>>c-c1cc(F)ccc1-c1noc(=O)[nH]1",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: True,
            ReactionCenterType.RC3: True,
            ReactionCenterType.RC4: True,
        },
    ),
    ReactionCenterTestCase(
        id="double_boc_removal",
        reaction_mapped_smiles=(
            "CC(C)(C)OC(=O)[N:3]1[CH2:2][CH2:1][N:6](C(=O)OC(C)(C)C)[CH2:5][CH2:4]1>>"
            "[CH2:1]1[CH2:2][NH:3][CH2:4][CH2:5][NH:6]1"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "CN(C)C(=O)OC(C)(C)C>>CNC",
                "CN(C)C(=O)OC(C)(C)C>>CNC",
            ),
            ReactionCenterType.RC2: (
                "CC(C)(C)OC(=O)N1CCN(C(=O)OC(C)(C)C)CC1>>C1CNCCN1",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: False,
        },
    ),
    ReactionCenterTestCase(
        id="boc_and_cbz_removal",
        reaction_mapped_smiles=(
            "CC(C)(C)OC(=O)[NH:1][CH2:2][CH2:3][NH:4]C(=O)OCc1ccccc1>>"
            "[NH2:1][CH2:2][CH2:3][NH2:4]"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "CNC(=O)OC(C)(C)C>>CN",
                "CNC(=O)OCc1ccccc1>>CN",
            ),
            ReactionCenterType.RC2: ("CC(C)(C)OC(=O)NCCNC(=O)OCc1ccccc1>>NCCN",),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: False,
        },
    ),
    ReactionCenterTestCase(
        id="clucose_full_acetylation",
        reaction_mapped_smiles=(
            "Cl[C:24]([CH3:25])=[O:26].Cl[C:28]([CH3:29])=[O:30]."
            "Cl[C:18]([CH3:19])=[O:20].Cl[C:13]([CH3:14])=[O:15]."
            "Cl[C:8]([CH3:9])=[O:10].Cl[C:2]([CH3:1])=[O:3]."
            "[OH:4][CH2:5][CH:6]([OH:7])[CH:11]([OH:12])[CH:16]([OH:17])"
            "[CH:21]([CH2:22][OH:23])[OH:27]>>"
            "[CH3:1][C:2](=[O:3])[O:4][CH2:5][CH:6]([O:7][C:8]([CH3:9])=[O:10])"
            "[CH:11]([O:12][C:13]([CH3:14])=[O:15])[CH:16]([O:17][C:18]([CH3:19])="
            "[O:20])[CH:21]([CH2:22][O:23][C:24]([CH3:25])=[O:26])[O:27][C:28]"
            "([CH3:29])=[O:30]"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: (
                "CC(=O)Cl.CO>>COC(C)=O",
                "CC(=O)Cl.CO>>COC(C)=O",
                "CC(=O)Cl.CO>>COC(C)=O",
                "CC(=O)Cl.CO>>COC(C)=O",
                "CC(=O)Cl.CO>>COC(C)=O",
                "CC(=O)Cl.CO>>COC(C)=O",
            ),
            ReactionCenterType.RC2: (
                "CC(=O)Cl.CC(=O)Cl.CC(=O)Cl.CC(=O)Cl.CC(=O)Cl.CC(=O)Cl.OCC(O)C(O)C(O)C"
                "(O)CO>>CC(=O)OCC(OC(C)=O)C(OC(C)=O)C(OC(C)=O)C(COC(C)=O)OC(C)=O",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: False,
        },
    ),
    ReactionCenterTestCase(
        id="acid_deprotonation",
        reaction_mapped_smiles=("[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[O-:3]"),
        expected_rc_components={
            ReactionCenterType.RC1: ("OC=O>>OC=O",),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: False,
        },
    ),
    ReactionCenterTestCase(
        id="acid_deprotonation_with_metal",
        reaction_mapped_smiles=("[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[O:3][Na:4]"),
        expected_rc_components={
            ReactionCenterType.RC1: ("OC=O>>O=C[O][Na]",),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: False,
        },
    ),
    ReactionCenterTestCase(
        id="one_component_complex_reaction",
        reaction_mapped_smiles=(
            "O=C([O:37]1)[O:36][CH2:35][C@@H:34]1[C@H:32]([C@@H:31]2[O:38][C:5]([C:3]"
            "([O:2][CH3:1])=[O:4])=[CH:6][C@H:7]([NH:8][C:9]([NH:18][C:19]([O:21]"
            "[C:22]([CH3:24])([CH3:23])[CH3:25])=[O:20])=[N:10][C:11]([O:13][C:14]"
            "([CH3:16])([CH3:15])[CH3:17])=[O:12])[C@H:26]2[NH:27][C:28]([CH3:29])="
            "[O:30])[OH:33]>>[CH3:1][O:2][C:3]([C:5]3=[CH:6][C@@H:7]([C@H:26]([C@@H:31]"
            "([O:38]3)[C@@H:32]([C@@H:34]([CH2:35][OH:36])[OH:37])[OH:33])[NH:27][C:28]"
            "([CH3:29])=[O:30])[NH:8][C:9]([NH:18][C:19]([O:21][C:22]([CH3:24])"
            "([CH3:25])[CH3:23])=[O:20])=[N:10][C:11]([O:13][C:14]([CH3:16])"
            "([CH3:17])[CH3:15])=[O:12])=[O:4]"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: ("COC(=O)OC>>CO.CO",),
            ReactionCenterType.RC2: ("C[C@H]1COC(=O)O1>>C[C@H](O)CO",),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: False,
            ReactionCenterType.RC2: False,
        },
    ),
    ReactionCenterTestCase(
        id="one_component_complex_reaction_2",
        reaction_mapped_smiles=(
            "O=C([O:4]1)[O:3][CH2:2][C@@H:1]1[C@H:7]([C@@H:8]2[O:5][C:27]([C:29]([O:30]"
            "[CH3:31])=[O:28])=[CH:26][C@H:25]([NH:24][C:23]([NH:21][C:20]([O:18][C:17]"
            "([CH3:15])([CH3:16])[CH3:14])=[O:19])=[N:22]C(OC(C)(C)C)=O)[C@H:13]2"
            "[NH:12][C:11]([CH3:10])=[O:9])[OH:6]>>[CH3:31][O:30][C:29]([C:27]3="
            "[CH:26][C@@H:25]([C@H:13]([C@@H:8]([O:5]3)[C@@H:7]([C@@H:1]([CH2:2]"
            "[OH:3])[OH:4])[OH:6])[NH:12][C:11]([CH3:10])=[O:9])[NH:24][C:23]"
            "([NH:21][C:20]([O:18][C:17]([CH3:15])([CH3:14])[CH3:16])=[O:19])"
            "=[NH:22])=[O:28]"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: ("CC(C)(C)OC(=O)N=C>>C=N", "COC(=O)OC>>CO.CO"),
            ReactionCenterType.RC2: (
                "CC(C)(C)OC(=O)N=C>>C=N",
                "C[C@H]1COC(=O)O1>>C[C@H](O)CO",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: True,
        },
    ),
    ReactionCenterTestCase(
        id="one_component_complex_reaction_2_inverted",
        reaction_mapped_smiles=(
            "[CH3:31][O:30][C:29]([C:27]3=[CH:26][C@@H:25]([C@H:13]([C@@H:8]([O:5]3)"
            "[C@@H:7]([C@@H:1]([CH2:2][OH:3])[OH:4])[OH:6])[NH:12][C:11]([CH3:10])="
            "[O:9])[NH:24][C:23]([NH:21][C:20]([O:18][C:17]([CH3:15])([CH3:14])"
            "[CH3:16])=[O:19])=[NH:22])=[O:28]>>O=C([O:4]1)[O:3][CH2:2][C@@H:1]1"
            "[C@H:7]([C@@H:8]2[O:5][C:27]([C:29]([O:30][CH3:31])=[O:28])=[CH:26]"
            "[C@H:25]([NH:24][C:23]([NH:21][C:20]([O:18][C:17]([CH3:15])([CH3:16])"
            "[CH3:14])=[O:19])=[N:22]C(OC(C)(C)C)=O)[C@H:13]2[NH:12][C:11]"
            "([CH3:10])=[O:9])[OH:6]"
        ),
        expected_rc_components={
            ReactionCenterType.RC1: ("C=N>>CC(C)(C)OC(=O)N=C", "CO.CO>>COC(=O)OC"),
            ReactionCenterType.RC2: (
                "C=N>>CC(C)(C)OC(=O)N=C",
                "C[C@H](O)CO>>C[C@H]1COC(=O)O1",
            ),
        },
        expected_rc_is_composite={
            ReactionCenterType.RC1: True,
            ReactionCenterType.RC2: True,
        },
    ),
]


@pytest.mark.parametrize(
    "test_case",
    _REACTION_CENTER_TEST_CASES,
    ids=[tc.id for tc in _REACTION_CENTER_TEST_CASES],
)
def test_reaction_center_number(test_case: ReactionCenterTestCase) -> None:
    assert len(test_case.processed_reaction.reaction_centers) == len(
        test_case.expected_rc_components
    )


@pytest.mark.parametrize(
    "test_case",
    _REACTION_CENTER_TEST_CASES,
    ids=[tc.id for tc in _REACTION_CENTER_TEST_CASES],
)
def test_reaction_center_components(test_case: ReactionCenterTestCase) -> None:
    reaction = test_case.processed_reaction
    for rc_type, expected_components in test_case.expected_rc_components.items():
        rc = reaction.reaction_centers[rc_type]
        assert rc.reaction_center_components == expected_components
        expected_composite = test_case.expected_rc_is_composite[rc_type]
        assert rc.is_reaction_center_composite == expected_composite
