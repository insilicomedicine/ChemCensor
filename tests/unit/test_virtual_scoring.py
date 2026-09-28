from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np

from chemcensor.basic import ReactionCenterType
from chemcensor.chemcensor import _fg_coverage_by_real_and_virtual
from chemcensor.chemcensor import ChemCensor
from chemcensor.chemcensor import ScoreResult
from chemcensor.configs.chemcensor_config import ChemCensorConfig
from chemcensor.configs.scoring_configs import ScoringConfig
from chemcensor.db import DBManager
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH


def _sig(*bits: int) -> np.ndarray:
    arr = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
    for i, bit in enumerate(bits):
        arr[i] = bit
    return arr


class TestFgCoverageByRealAndVirtual:
    def test_all_bits_in_real(self):
        rc = _sig(1, 1, 0)
        real = _sig(1, 1, 1)
        assert _fg_coverage_by_real_and_virtual(rc, real, None) == (True, 2, 0)

    def test_missing_bits_filled_by_virtual(self):
        rc = _sig(1, 1, 0)
        real = _sig(1, 0, 0)
        virt = _sig(0, 1, 0)
        assert _fg_coverage_by_real_and_virtual(rc, real, virt) == (True, 2, 1)

    def test_missing_bits_absent_from_virtual(self):
        rc = _sig(1, 1, 0)
        real = _sig(1, 0, 0)
        virt = _sig(0, 0, 1)
        assert _fg_coverage_by_real_and_virtual(rc, real, virt) == (False, 2, 0)

    def test_virtual_only(self):
        rc = _sig(0, 1, 0)
        virt = _sig(0, 1, 1)
        assert _fg_coverage_by_real_and_virtual(rc, None, virt) == (True, 1, 1)

    def test_neither_covers(self):
        rc = _sig(1, 0, 0)
        assert _fg_coverage_by_real_and_virtual(rc, None, None) == (False, 1, 0)


class TestScoreCentersVirtual:
    def _censor_with_db(self, db: DBManager) -> ChemCensor:
        return ChemCensor(
            manager=db,
            config=ChemCensorConfig(find_exact_match=False, max_center_type=1),
            processor=MagicMock(),
        )

    def test_virtual_only_center_scores_lc1(self):
        db = DBManager()
        fg = _sig(1, 0, 0)
        db.add_reaction_center("rc1", fg, is_virtual=True)
        censor = self._censor_with_db(db)

        rc = MagicMock()
        rc.reaction_center_smiles = "rc1"
        rc.fg_signature = fg
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {ReactionCenterType.RC1: rc}

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_1_scoring.value,
            without_functional_groups=ScoringConfig.lc_1_scoring.value,
            all_fgs_precedents_are_real=False,
            total_number_of_fgs=1,
            number_of_fgs_covered_by_virtual_precedents=1,
            all_center_precedents_are_real=False,
        )

    def test_real_partial_fg_completed_by_virtual(self):
        db = DBManager()
        db.add_reaction_center("rc1", _sig(1, 0, 0), is_virtual=False)
        db.add_reaction_center("rc1", _sig(0, 1, 0), is_virtual=True)
        censor = self._censor_with_db(db)

        rc = MagicMock()
        rc.reaction_center_smiles = "rc1"
        rc.fg_signature = _sig(1, 1, 0)
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {ReactionCenterType.RC1: rc}

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_1_scoring.value,
            without_functional_groups=ScoringConfig.lc_1_scoring.value,
            all_fgs_precedents_are_real=False,
            total_number_of_fgs=2,
            number_of_fgs_covered_by_virtual_precedents=1,
            # Real row exists — center presence is real even if FG bits
            # needed virtual fill-in.
            all_center_precedents_are_real=True,
        )

    def test_missing_fg_bits_break_with_fg_but_keep_without(self):
        db = DBManager()
        db.add_reaction_center("rc1", _sig(1, 0, 0), is_virtual=False)
        censor = self._censor_with_db(db)

        rc = MagicMock()
        rc.reaction_center_smiles = "rc1"
        rc.fg_signature = _sig(1, 1, 0)
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {ReactionCenterType.RC1: rc}

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.default_reaction_scoring.value,
            without_functional_groups=ScoringConfig.lc_1_scoring.value,
            # FG check failed with no virtual fill-in accepted.
            all_fgs_precedents_are_real=True,
            total_number_of_fgs=2,
            number_of_fgs_covered_by_virtual_precedents=0,
            all_center_precedents_are_real=True,
        )

    def test_plain_scoring_stops_after_both_chains_fail_but_trace_continues(self):
        censor = self._censor_with_db(DBManager())
        rc1 = MagicMock(
            reaction_center_smiles="absent-rc1",
            fg_signature=_sig(1, 0, 0),
        )
        rc2 = MagicMock(
            reaction_center_smiles="absent-rc2",
            fg_signature=_sig(1, 0, 0),
        )
        reaction = MagicMock(
            canonical_smiles="A>>B",
            reaction_smiles="A>>B",
            is_sear_reaction=False,
            reaction_centers={
                ReactionCenterType.RC1: rc1,
                ReactionCenterType.RC2: rc2,
            },
        )

        with patch.object(
            censor,
            "_reference_fg_pair_for_center_scoring",
            wraps=censor._reference_fg_pair_for_center_scoring,
        ) as lookup:
            censor._score_centers(reaction)
            assert lookup.call_count == 1

            lookup.reset_mock()
            trace = censor._trace_centers(
                reaction,
                canonical_smiles="A>>B",
                include_precedents=True,
            )

        assert lookup.call_count == 2
        assert [center.center_type for center in trace.centers] == [
            ReactionCenterType.RC1,
            ReactionCenterType.RC2,
        ]

    def test_counters_come_from_outermost_passing_center(self):
        """Nested centers must not sum overlapping FGs into the counters."""
        db = DBManager()
        db.add_reaction_center("rc1", _sig(1, 0, 0), is_virtual=False)
        db.add_reaction_center("rc2", _sig(1, 1, 0), is_virtual=False)
        db.add_reaction_center("rc2", _sig(0, 0, 1), is_virtual=True)
        censor = ChemCensor(
            manager=db,
            config=ChemCensorConfig(find_exact_match=False, max_center_type=2),
            processor=MagicMock(),
        )

        rc1 = MagicMock()
        rc1.reaction_center_smiles = "rc1"
        rc1.fg_signature = _sig(1, 0, 0)
        rc2 = MagicMock()
        rc2.reaction_center_smiles = "rc2"
        # 3 FGs on RC2; one needs virtual — counters must be 3 / 1,
        # not 1+3 / 0+1 from summing RC1 and RC2.
        rc2.fg_signature = _sig(1, 1, 1)
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {
            ReactionCenterType.RC1: rc1,
            ReactionCenterType.RC2: rc2,
        }

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_2_scoring.value,
            without_functional_groups=ScoringConfig.lc_2_scoring.value,
            all_fgs_precedents_are_real=False,
            total_number_of_fgs=3,
            number_of_fgs_covered_by_virtual_precedents=1,
            all_center_precedents_are_real=True,
        )

    def test_prefix_virtual_fill_in_kept_when_outer_center_is_real(self):
        """Inner virtual fill-in must keep the flag False even if RC2 is all-real.

        ``score_with_fg`` reaches lc_2 only because RC1 passed via virtual
        precedents; counters still describe the outermost (real) center.
        """
        db = DBManager()
        db.add_reaction_center("rc1", _sig(1, 0, 0), is_virtual=False)
        db.add_reaction_center("rc1", _sig(0, 1, 0), is_virtual=True)
        db.add_reaction_center("rc2", _sig(1, 1, 1), is_virtual=False)
        censor = ChemCensor(
            manager=db,
            config=ChemCensorConfig(find_exact_match=False, max_center_type=2),
            processor=MagicMock(),
        )

        rc1 = MagicMock()
        rc1.reaction_center_smiles = "rc1"
        rc1.fg_signature = _sig(1, 1, 0)
        rc2 = MagicMock()
        rc2.reaction_center_smiles = "rc2"
        rc2.fg_signature = _sig(1, 1, 1)
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {
            ReactionCenterType.RC1: rc1,
            ReactionCenterType.RC2: rc2,
        }

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_2_scoring.value,
            without_functional_groups=ScoringConfig.lc_2_scoring.value,
            all_fgs_precedents_are_real=False,
            total_number_of_fgs=3,
            number_of_fgs_covered_by_virtual_precedents=0,
            all_center_precedents_are_real=True,
        )

    def test_exact_match_on_virtual_reaction_keeps_real_fg_flag(self):
        """Exact match skips center/FG loops — vacuous precedent flags."""
        db = DBManager()
        db.add_reaction("canon>>smiles", "doc", is_virtual=True, source="7")
        censor = ChemCensor(
            manager=db,
            config=ChemCensorConfig(find_exact_match=True),
            processor=MagicMock(),
        )
        reaction = MagicMock()
        reaction.dummy = False
        reaction.is_sis_reaction = False
        reaction.canonical_smiles = "canon>>smiles"

        result = censor.evaluate_processed(reaction)
        assert result == ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
        assert result.all_fgs_precedents_are_real is True
        assert result.all_center_precedents_are_real is True

    def test_real_only_center_marks_all_fgs_precedents_real(self):
        db = DBManager()
        fg = _sig(1, 0, 0)
        db.add_reaction_center("rc1", fg, is_virtual=False)
        censor = self._censor_with_db(db)

        rc = MagicMock()
        rc.reaction_center_smiles = "rc1"
        rc.fg_signature = fg
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {ReactionCenterType.RC1: rc}

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_1_scoring.value,
            without_functional_groups=ScoringConfig.lc_1_scoring.value,
            all_fgs_precedents_are_real=True,
            total_number_of_fgs=1,
            number_of_fgs_covered_by_virtual_precedents=0,
            all_center_precedents_are_real=True,
        )

    def test_virtual_only_center_marks_all_center_precedents_not_real(self):
        db = DBManager()
        fg = _sig(1, 0, 0)
        db.add_reaction_center("rc1", fg, is_virtual=True)
        censor = self._censor_with_db(db)

        rc = MagicMock()
        rc.reaction_center_smiles = "rc1"
        rc.fg_signature = fg
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {ReactionCenterType.RC1: rc}

        result = censor._score_centers(reaction)
        assert result.all_center_precedents_are_real is False
        assert result.without_functional_groups == ScoringConfig.lc_1_scoring.value

    def test_prefix_virtual_only_center_kept_when_outer_center_is_real(self):
        """Inner virtual-only presence must keep the flag False even if RC2 is real.

        ``score_without_fg`` reaches lc_2 only because RC1 was present (as a
        virtual row); the center-precedent flag ANDs over that whole prefix.
        """
        db = DBManager()
        db.add_reaction_center("rc1", _sig(1, 0, 0), is_virtual=True)
        db.add_reaction_center("rc2", _sig(1, 1, 1), is_virtual=False)
        censor = ChemCensor(
            manager=db,
            config=ChemCensorConfig(find_exact_match=False, max_center_type=2),
            processor=MagicMock(),
        )

        rc1 = MagicMock()
        rc1.reaction_center_smiles = "rc1"
        rc1.fg_signature = _sig(1, 0, 0)
        rc2 = MagicMock()
        rc2.reaction_center_smiles = "rc2"
        rc2.fg_signature = _sig(1, 1, 1)
        reaction = MagicMock()
        reaction.is_sear_reaction = False
        reaction.reaction_centers = {
            ReactionCenterType.RC1: rc1,
            ReactionCenterType.RC2: rc2,
        }

        result = censor._score_centers(reaction)
        assert result == ScoreResult(
            with_functional_groups=ScoringConfig.lc_2_scoring.value,
            without_functional_groups=ScoringConfig.lc_2_scoring.value,
            all_fgs_precedents_are_real=False,
            total_number_of_fgs=3,
            number_of_fgs_covered_by_virtual_precedents=0,
            all_center_precedents_are_real=False,
        )
