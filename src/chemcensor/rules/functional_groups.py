from frozendict import frozendict

from ..basic.functional_groups import FunctionalGroupClass
from ..basic.functional_groups import FunctionalGroups

FUNCTIONAL_GROUPS: tuple[frozendict[str, int | str | FunctionalGroupClass], ...] = (
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 0,
            "name": "1,2,4-oxadiazol-5(4H)-one [nH]",
            "ui_name": "Hetarene #25",
            "smarts": "[c]1[nH0][o][c](=[O])[nH1]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 1,
            "name": "1,2,4-oxadiazol-5(4H)-one [nH0]",
            "ui_name": "Hetarene #26",
            "smarts": "[c]1[nH0][o][c](=[O])[nH0]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 2,
            "name": "2-bromo-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl bromide #1",
            "smarts": "[c$(*1caa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 3,
            "name": "2-bromo-azole",
            "ui_name": "(Het)aryl bromide #2",
            "smarts": "[c$(*1naa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 4,
            "name": "2-chloro- pyrimidine and 2-chloro-imidazole",
            "ui_name": "(Het)aryl chloride #1",
            "smarts": "[n][c]([n])[Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 5,
            "name": "2-chloro-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl chloride #2",
            "smarts": "[c$(*1caa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 6,
            "name": "2-chloro-azole",
            "ui_name": "(Het)aryl chloride #3",
            "smarts": "[c$(*1naa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 7,
            "name": "2-Hydroxypyridine nc[O,S]H",
            "ui_name": "Aromatic (thio)amide #1",
            "smarts": "[c$(*n)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 8,
            "name": "2-iodo-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl iodide #1",
            "smarts": "[c$(*1caa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 9,
            "name": "2-iodo-azole",
            "ui_name": "(Het)aryl iodide #2",
            "smarts": "[c$(*1naa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 10,
            "name": "2-nitro- pyrimidine and 2-nitro-imidazole",
            "ui_name": "Nitro #1",
            "smarts": "[n][c]([n])[N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 11,
            "name": "2-OTf-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl triflate #1",
            "smarts": "[c$(*1caa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 12,
            "name": "2-OTf-azole",
            "ui_name": "(Het)aryl triflate #2",
            "smarts": "[c$(*1naa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 13,
            "name": "2-Pyridone [O,S]=[#6][n-] activated",
            "ui_name": "Aromatic (thio)amide #2",
            "smarts": "[O,S]=[c][n-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 14,
            "name": "2-Pyridone [O,S]=[#6][n][Me] activated",
            "ui_name": "Aromatic (thio)amide #4",
            "smarts": "[O,S]=[c][n][Li,K,Mg,Na,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 15,
            "name": "2-Pyridone [O,S]=[#6][nh]",
            "ui_name": "Aromatic (thio)amide #3",
            "smarts": "[O,S]=[c][nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 16,
            "name": "2,4-EWG Aryl bromide",
            "ui_name": "(Het)aryl bromide #3",
            "smarts": "[Br][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 17,
            "name": "2,4-EWG Aryl chloride",
            "ui_name": "(Het)aryl chloride #4",
            "smarts": "[Cl][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 18,
            "name": "2,4-EWG Aryl fluoride",
            "ui_name": "(Het)aryl fluoride #1",
            "smarts": "[F][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 19,
            "name": "2,4-EWG Aryl iodide",
            "ui_name": "(Het)aryl iodide #3",
            "smarts": "[I][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 20,
            "name": "2,4-EWG Aryl sulfonate",
            "ui_name": "Sulfonate #2",
            "smarts": "[O]([S](=[O])(=[O])[#6!$(*[F])])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 21,
            "name": "2,4-EWG Aryl triflate",
            "ui_name": "(Het)aryl triflate #3",
            "smarts": "[O]([S](=[O])(=[O])[#6]([F])([F])[F])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 22,
            "name": "3-bromo-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl bromide #4",
            "smarts": "[c$(*1ca[!c]c1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 23,
            "name": "3-chloro-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl chloride #5",
            "smarts": "[c$(*1ca[!c]c1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 24,
            "name": "3-iodo-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl iodide #4",
            "smarts": "[c$(*1ca[!c]c1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 25,
            "name": "3-OTf-(pyrrole, thiophene, furan)",
            "ui_name": "(Het)aryl triflate #4",
            "smarts": "[c$(*1ca[!c]c1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 26,
            "name": "4-Hydroxypyridine",
            "ui_name": "(Het)aryl-(S,O)H #1",
            "smarts": "[c$(*:1:a:a:n:a:a:1)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 27,
            "name": "4-Pyridone [O,S]=[#6]aa[n-] activated",
            "ui_name": "Hetarene #33",
            "smarts": "[c]1(=[O,S])aa[n-]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 28,
            "name": "4-Pyridone [O,S]=[#6]aa[n][Me] activated",
            "ui_name": "Hetarene #34",
            "smarts": "[c]1(=[O,S])aa[n]([Li,K,Mg,Na,Zn])aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 29,
            "name": "4-Pyridone [O,S]=[#6]aa[nh]",
            "ui_name": "Hetarene #35",
            "smarts": "[c]1(=[O,S])aa[nh]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 30,
            "name": "a-[Br] bromo-carbonyle",
            "ui_name": "Carbonyl #4",
            "smarts": "[Br][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 31,
            "name": "a-[C-] aldehyde anion (type I)",
            "ui_name": "CH-anion #23",
            "smarts": "[C;X3&-1][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 32,
            "name": "a-[C-] amide anion",
            "ui_name": "CH-anion #12",
            "smarts": "[C;X3&-1][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 33,
            "name": "a-[C-] carboxylic ester and acid anion",
            "ui_name": "CH-anion #11",
            "smarts": "[C;X3&-1][C](=[O])[O;h,$(*[#6!$(*[C]=[O,S,N])])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 34,
            "name": "a-[C-] Common template anion",
            "ui_name": "CH-anion #10",
            "smarts": "[C;X3&-1][C,S,N,P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 35,
            "name": "a-[C-] dithiane anion",
            "ui_name": "Dithiane #2",
            "smarts": "[S][C-;X3][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 36,
            "name": "a-[C-] ketone anion",
            "ui_name": "CH-anion #9",
            "smarts": "[C;X3&-1][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 37,
            "name": "a-[C-] nitrile derivatives anion (form I)",
            "ui_name": "CH-anion #8",
            "smarts": "[C;X3&-1][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 38,
            "name": "a-[C-] nitrile enolate derivatives (form II)",
            "ui_name": "Nitrile enolate #1",
            "smarts": "[C]=[C]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 39,
            "name": "a-[C-] nitro derivatives anion",
            "ui_name": "CH-anion #7",
            "smarts": "[C;X3&-1][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 40,
            "name": "a-[C-] phosphonate and phosphine oxide anion",
            "ui_name": "CH-anion #6",
            "smarts": "[C;X3&-1][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 41,
            "name": "a-[C-] sulfo derivatives anion",
            "ui_name": "CH-anion #5",
            "smarts": "[C;X3&-1][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 42,
            "name": "a-[C-] thioamide, thioester anion",
            "ui_name": "CH-anion #22",
            "smarts": "[C;X3&-1][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 43,
            "name": "a-[C-][Me] aldehyde anion (type I)",
            "ui_name": "CH-anion #21",
            "smarts": "[CX4$(*[C;X3&h]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 44,
            "name": "a-[C-][Me] amide anion",
            "ui_name": "CH-anion #20",
            "smarts": "[CX4$(*[C](=[O])[#7])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 45,
            "name": "a-[C-][Me] carboxylic ester and acid anion",
            "ui_name": "CH-anion #19",
            "smarts": "[CX4$(*[C](=[O])[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 46,
            "name": "a-[C-][Me] ketone anion",
            "ui_name": "CH-anion #18",
            "smarts": "[CX4$(*[C](=[O])[#6])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 47,
            "name": "a-[C-][Me] nitrile derivatives anion (form I)",
            "ui_name": "CH-anion #17",
            "smarts": "[CX4$(*[C]#[N])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 48,
            "name": "a-[C-][Me] nitro derivatives anion",
            "ui_name": "CH-anion #16",
            "smarts": "[CX4$(*[N+](=[O])[O-])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 49,
            "name": "a-[C-][Me] phosphonate and phosphine oxide anion",
            "ui_name": "CH-anion #15",
            "smarts": "[CX4$(*[P]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 50,
            "name": "a-[C-][Me] sulfo derivatives anion",
            "ui_name": "CH-anion #14",
            "smarts": "[CX4$(*[S]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 51,
            "name": "a-[C-][Me] thioamide, thioester anion",
            "ui_name": "CH-anion #13",
            "smarts": "[CX4$(*[C](=[S])[#7,#8])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 52,
            "name": "a-[Ch] aldehyde",
            "ui_name": "CH-acid #14",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 53,
            "name": "a-[Ch] allyl derivatives",
            "ui_name": "CH-acid #13",
            "smarts": "[C]=[C][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 54,
            "name": "a-[Ch] amide",
            "ui_name": "CH-acid #12",
            "smarts": "[C;X4&h][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 55,
            "name": "a-[Ch] ammoium salt",
            "ui_name": "CH-acid #11",
            "smarts": "[C;X4&h][#7;h0&+1&!$(*=O)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 56,
            "name": "a-[Ch] arenes",
            "ui_name": "CH-acid #10",
            "smarts": "[c][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 57,
            "name": "a-[Ch] carboxylic acid",
            "ui_name": "CH-acid #9",
            "smarts": "[C;X4&h][C](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 58,
            "name": "a-[Ch] carboxylic ester",
            "ui_name": "CH-acid #8",
            "smarts": "[C;X4&h][C](=[O])[OH0][#6!$(*=[O,S,N,P])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 59,
            "name": "a-[Ch] Imine =N[Ch]",
            "ui_name": "CH-acid #7",
            "smarts": "[C;X4&h][N]=[C;$(*[#6])&!$(*-[!#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 60,
            "name": "a-[Ch] ketone",
            "ui_name": "CH-acid #6",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 61,
            "name": "a-[Ch] nitrile",
            "ui_name": "CH-acid #5",
            "smarts": "[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 62,
            "name": "a-[Ch] nitro derivatives",
            "ui_name": "CH-acid #4",
            "smarts": "[C;X4&h][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 63,
            "name": "a-[Ch] phosponate and phosphine oxide",
            "ui_name": "CH-acid #16",
            "smarts": "[C;X4&h][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 64,
            "name": "a-[Ch] sulfo derivatives",
            "ui_name": "CH-acid #15",
            "smarts": "[C;X4&h][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 65,
            "name": "a-[Ch] thioamide, thioester",
            "ui_name": "CH-acid #3",
            "smarts": "[C;X4&h][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 66,
            "name": "a-[Cl] chloro-carbonyle",
            "ui_name": "Carbonyl #2",
            "smarts": "[Cl][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 67,
            "name": "a-[I] Iodo-carbonyle",
            "ui_name": "Carbonyl #5",
            "smarts": "[I][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 68,
            "name": "a-[N2] diazo-carbonyle",
            "ui_name": "Carbonyl #6",
            "smarts": "[N-1]=[N+1]=[CX3][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 69,
            "name": "a-Carboxylic group C(#[N])[C]COOH (type II)",
            "ui_name": "Carboxyl(ate) #1",
            "smarts": "[C](#[N])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 70,
            "name": "a-Carboxylic group C(=O)[C]COOH (type I)",
            "ui_name": "Carboxyl(ate) #2",
            "smarts": "[C](=[O])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 71,
            "name": "a-sulfonate-carbonyle",
            "ui_name": "Carbonyl #1",
            "smarts": "[C](=[O])[C;X4&h][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 72,
            "name": "Acetale and Ketale O-[CX4]-O",
            "ui_name": "Acetale and ketale #1",
            "smarts": "[#6][O]-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 73,
            "name": "Acetic anhydride (mixed) C(=O)OC(=O)",
            "ui_name": "Anhydride #1",
            "smarts": "[#6][C](=[O])[O][C](=[O])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 74,
            "name": "Alcohol [Ch][C][Oh] (type III)",
            "ui_name": "Alcohol #10",
            "smarts": "[C;X4&h][C;X4&!$(*[#7])&!$(*([O])[O])&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 75,
            "name": "Alcohol [C](=[O])[Ch][C][Oh]",
            "ui_name": "Alcohol #9",
            "smarts": "[O]=[CX3][CX4h][CX4][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 76,
            "name": "Alcohol C-[Oh] (primary)",
            "ui_name": "Alcohol #1",
            "smarts": "[C;X4H2&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 77,
            "name": "Alcohol C-[Oh] (secondary)",
            "ui_name": "Alcohol #3",
            "smarts": "[C;X4H1&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 78,
            "name": "Alcohol C-[Oh] (tertiary)",
            "ui_name": "Alcohol #6",
            "smarts": "[C;X4H0&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 79,
            "name": "Alcohol OH (OBn) ( benzyl type I) secondary",
            "ui_name": "Alcohol #4",
            "smarts": "[CX4][CX4H1]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 80,
            "name": "Alcohol OH (OBn) ( benzyl type I) tertiary",
            "ui_name": "Alcohol #7",
            "smarts": "[CX4][CX4H0]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 81,
            "name": "Alcohol OH (OBn) ( benzyl type II) primary",
            "ui_name": "Alcohol #2",
            "smarts": "[CX4H2]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 82,
            "name": "Alcohol OH (OBn) ( benzyl type II) secondary",
            "ui_name": "Alcohol #5",
            "smarts": "[CX4H1]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 83,
            "name": "Alcohol OH (OBn) ( benzyl type II) tertiary",
            "ui_name": "Alcohol #8",
            "smarts": "[CX4H0]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 84,
            "name": "Alcoholate C-[O-]",
            "ui_name": "Alcoholate #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 85,
            "name": "Alcoholate C-[O][Me]",
            "ui_name": "Alcoholate #2",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 86,
            "name": "Aldehyde [Ch][OH1][OH1] and H2O",
            "ui_name": "Geminal diol #1",
            "smarts": "[#6][CX4h][OH1][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 87,
            "name": "Aldehyde [Ch]=[O]",
            "ui_name": "Carbonyl #3",
            "smarts": "[CX3z1h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 88,
            "name": "Aldoxime  [#6][Ch](=[N][Oh]) (type I)",
            "ui_name": "Aldoxime #1",
            "smarts": "[#6][Ch](=[N][Oh])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 89,
            "name": "Aldoxime  [#6][Ch](=[N][Oh0]) (type II)",
            "ui_name": "Aldoxime #2",
            "smarts": "[#6][Ch](=[N][Oh0])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 90,
            "name": "Aldoxime anions [N][O-]",
            "ui_name": "Aldoxime #3",
            "smarts": "[#6][Ch]=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 91,
            "name": "Aldoxime anions [N][O][Me]",
            "ui_name": "Aldoxime #4",
            "smarts": "[#6][Ch]=[N][O][Na,K,Li,Cu,Mg,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 92,
            "name": "Alkenyl bromide",
            "ui_name": "Alkenyl bromide #1",
            "smarts": "[C]=[C][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 93,
            "name": "Alkenyl chloride",
            "ui_name": "Alkenyl chloride #1",
            "smarts": "[C]=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 94,
            "name": "Alkenyl halide, mesylate, tosylate",
            "ui_name": "Alkenyl (pseudo)halide #1",
            "smarts": "[C]=[C][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 95,
            "name": "Alkenyl iodide",
            "ui_name": "Alkenyl iodide #1",
            "smarts": "[C]=[C][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 96,
            "name": "Alkenyl sulfonate",
            "ui_name": "Sulfonate #1",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 97,
            "name": "Alkenyl triflate",
            "ui_name": "Alkenyl triflate #1",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 98,
            "name": "Alkyl bromide (primary)",
            "ui_name": "Primary alkyl bromide #1",
            "smarts": "[CX4H2][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 99,
            "name": "Alkyl bromide (secondary)",
            "ui_name": "Secondary alkyl bromide #1",
            "smarts": "[CX4H1][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 100,
            "name": "Alkyl bromide (tertiary)",
            "ui_name": "Tertiary alkyl bromide #1",
            "smarts": "[CX4H0][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 101,
            "name": "Alkyl chloride (primary)",
            "ui_name": "Primary alkyl chloride #1",
            "smarts": "[CX4H2][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 102,
            "name": "Alkyl chloride (secondary)",
            "ui_name": "Secondary alkyl chloride #1",
            "smarts": "[CX4H1][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 103,
            "name": "Alkyl chloride (tertiary)",
            "ui_name": "Tertiary alkyl chloride #1",
            "smarts": "[CX4H0][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 104,
            "name": "Alkyl iodide (primary)",
            "ui_name": "Primary alkyl iodide #1",
            "smarts": "[CX4H2][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 105,
            "name": "Alkyl iodide (secondary)",
            "ui_name": "Secondary alkyl iodide #1",
            "smarts": "[CX4H1][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 106,
            "name": "Alkyl iodide (tertiary)",
            "ui_name": "Tertiary alkyl iodide #1",
            "smarts": "[CX4H0][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 107,
            "name": "alkyl sulfinate [#6][Sv4](=[O])[O]",
            "ui_name": "Sulfinate #1",
            "smarts": "[#6][Sv4](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 108,
            "name": "Alkyl sulfonate (primary)",
            "ui_name": "Sulfonate #4",
            "smarts": "[CX4H2][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 109,
            "name": "Alkyl sulfonate (secondary)",
            "ui_name": "Sulfonate #8",
            "smarts": "[CX4H1][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 110,
            "name": "Alkyl sulfonate (tertiary)",
            "ui_name": "Sulfonate #9",
            "smarts": "[CX4H0][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 111,
            "name": "Alkyne (terminal [C]#[Ch])",
            "ui_name": "Alkyne #1",
            "smarts": "[C]#[Ch]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 112,
            "name": "Alkyne (triple bond C#C)",
            "ui_name": "Alkyne #2",
            "smarts": "[C]#[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 113,
            "name": "Alkyne (triple bond C#C) small cycles",
            "ui_name": "Alkyne #6",
            "smarts": "[C;r3,r4,r5,r6]#[C;r3,r4,r5,r6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 114,
            "name": "Alkyne activated",
            "ui_name": "Alkyne #3",
            "smarts": "[C]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 115,
            "name": "Alkyne Metallorganic C#C[Me] (type I)",
            "ui_name": "Alkyne #4",
            "smarts": "[C]#[C][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 116,
            "name": "Alkyne Metallorganic C#C[Me] (type II)",
            "ui_name": "Alkyne #5",
            "smarts": "[C]#[C][Cu,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 117,
            "name": "Amide [Nh]",
            "ui_name": "Amide #1",
            "smarts": "[CX3z2](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 118,
            "name": "Amide [Nh0]",
            "ui_name": "Amide #2",
            "smarts": "[CX3z2](=[O])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 119,
            "name": "Amide anion (Activated [N-])",
            "ui_name": "Amide #3",
            "smarts": "[CX3z2](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 120,
            "name": "Amide anion (Activated N-Me bond)",
            "ui_name": "Amide #4",
            "smarts": "[CX3z2](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 121,
            "name": "Amidine [#6]C(=N)[N-] (activated)",
            "ui_name": "Amidine #1",
            "smarts": "[#6][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 122,
            "name": "Amidine [#6]C(=N)[N][Me] (activated)",
            "ui_name": "Amidine #2",
            "smarts": "[#6][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 123,
            "name": "Amidine [#6]C(=N)[Nh]",
            "ui_name": "Amidine #3",
            "smarts": "[#6][C!R](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 124,
            "name": "Amidine [#6]C(=N)[Nh] cyclic",
            "ui_name": "Amidine #4",
            "smarts": "[#6][CR](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 125,
            "name": "Aminal non-cyclic [Nh][CX4][Nh]",
            "ui_name": "(Hemi)aminal #1",
            "smarts": "[N&h&R0&$(*[CX4][#7])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 126,
            "name": "Amine aliphatic (primary) C-NH2",
            "ui_name": "Primary amine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 127,
            "name": "Amine aliphatic (secondary) C-NH-C",
            "ui_name": "Secondary amine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H1][C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 128,
            "name": "Amine aliphatic (tertiary) C-N(-C)-C",
            "ui_name": "Tertiary alkylamine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H0]([C;X4&!$(*=[C,N,O,S])])[C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 129,
            "name": "Amine anion [#6][N-]",
            "ui_name": "Amine anion #1",
            "smarts": "[#6;!$(*=[O,S,N])][N;!$(*[!#6])&!$(*[C]=[O,S,N])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 130,
            "name": "Amine anion [#6][N-][Me]",
            "ui_name": "Amine anion #2",
            "smarts": "[#6;!$(*=[O,S,N])][N;z1&!$(*[C]=[O,S,N])&+0][Li,Na,K,Cu,Mg,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 131,
            "name": "Amine aromatic (primary) c-NH2",
            "ui_name": "Amine #1",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 132,
            "name": "Amine aromatic (primary) c-NH2 (tautomeric form)",
            "ui_name": "Amine #2",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 133,
            "name": "Amine aromatic (secondary, aliphatic) c-NH-[C]",
            "ui_name": "Amine #3",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 134,
            "name": "Amine aromatic (secondary, aliphatic) c-NH-[C] (tautomeric form)",
            "ui_name": "Amine #4",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 135,
            "name": "Amine aromatic (secondary, aromatic) c-NH-c",
            "ui_name": "Amine #5",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 136,
            "name": "Amine aromatic (secondary, aromatic) c-NH-c (tautomeric form)",
            "ui_name": "Amine #6",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 137,
            "name": "Amine aromatic (tertiary) c-N(-[#6])-[#6]",
            "ui_name": "Amine #7",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])])[#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 138,
            "name": "Amine oxide",
            "ui_name": "Amine oxide #1",
            "smarts": "[NX4z+1][Oz-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 139,
            "name": "Amine poor electronic (primary) c-NH2",
            "ui_name": "Amine #8",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 140,
            "name": "Amine poor electronic (primary) c-NH2 (tautomeric form)",
            "ui_name": "Amine #9",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 141,
            "name": "Amine poor electronic (secondary, aliphatic) c-NH-[C]",
            "ui_name": "Amine #10",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 142,
            "name": "Amine poor electronic (secondary, aliphatic) c-NH-[C] (tautomeric form)",
            "ui_name": "Amine #11",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 143,
            "name": "Amine poor electronic (secondary, aromatic) c-NH-[c,CX3]",
            "ui_name": "Amine #12",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 144,
            "name": "Amine poor electronic (secondary, aromatic) c-NH-[c,CX3] (tautomeric form)",
            "ui_name": "Amine #13",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 145,
            "name": "Amine poor electronic (secondary, poor) c-NH-c",
            "ui_name": "Amine #14",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 146,
            "name": "Amine poor electronic (secondary, poor) c-NH-c (tautomeric form)",
            "ui_name": "Amine #15",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 147,
            "name": "Amine poor electronic (tertinary) c-N(-[#6])-[#6]",
            "ui_name": "Amine #16",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6!$(*=[O,S,N])])[#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 148,
            "name": "Aminoacetal and aminoketal N-[CX4]-O",
            "ui_name": "Aminoacetal and aminoketal #1",
            "smarts": "[#6][NH0]([#6])-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 149,
            "name": "Ammonium Salts [N+] (alkyl)",
            "ui_name": "Ammonium #1",
            "smarts": "[CX4][N+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 150,
            "name": "Ammonium Salts [Nh+]",
            "ui_name": "Ammonium #2",
            "smarts": "[#6!$(*=[O,S,N])][Nh+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 151,
            "name": "Anhydride (mixed) C(=O)O[N,S](=O) type I",
            "ui_name": "Anhydride #2",
            "smarts": "[#6][C](=[O])[O][S,N](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 152,
            "name": "Anhydride (mixed) C(=O)O[P](=O) type II",
            "ui_name": "Anhydride #3",
            "smarts": "[#6][C](=[O])[O][P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 153,
            "name": "Anhydride C(=O)OC(=O)",
            "ui_name": "Anhydride #4",
            "smarts": "[#6][C](=[O])[O][C!$(*[CH3])](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 154,
            "name": "Arenes [ch] (meta-EDG) Type I",
            "ui_name": "Arene [ch] #1",
            "smarts": "[ch]:1:[c]:[c$(*[OH0,N!$(*=O),SX2])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 155,
            "name": "Arenes [ch] (meta-EDG) Type II",
            "ui_name": "Arene [ch] #2",
            "smarts": "[ch]:1:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 156,
            "name": "Arenes [ch] (meta-EDG) Type III",
            "ui_name": "Arene [ch] #3",
            "smarts": "[ch]:1:[c]:[c$(*[O;+0H1,-1H0])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 157,
            "name": "Arenes [ch] (meta-EDG) Type IV",
            "ui_name": "Arene [ch] #4",
            "smarts": "[ch]:1:[c]:[c$(*(a)(a)a)]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 158,
            "name": "Arenes [ch] (meta-EDG) Type V",
            "ui_name": "Arene [ch] #5",
            "smarts": "[ch]:1:[c]:[c$(*[CX4])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 159,
            "name": "Arenes [ch] (meta-EWG)",
            "ui_name": "Arene [ch] #6",
            "smarts": "[ch]:1:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 160,
            "name": "Arenes [ch] (ortho-EDG) Type I",
            "ui_name": "Arene [ch] #7",
            "smarts": "[cr6h]:[c$(*[OX2H0z0])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 161,
            "name": "Arenes [ch] (ortho-EDG) Type II",
            "ui_name": "Arene [ch] #8",
            "smarts": "[cr6h]:[c$(*[F,Cl,Br,I])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 162,
            "name": "Arenes [ch] (ortho-EDG) Type III",
            "ui_name": "Arene [ch] #9",
            "smarts": "[cr6h]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 163,
            "name": "Arenes [ch] (ortho-EDG) Type IV",
            "ui_name": "Arene [ch] #10",
            "smarts": "[cr6h]:[c$(*(a)(a)a)]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 164,
            "name": "Arenes [ch] (ortho-EDG) Type V",
            "ui_name": "Arene [ch] #11",
            "smarts": "[cr6h]:[c;$(*[CX4z0]),$(*[CX4z1][O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 165,
            "name": "Arenes [ch] (ortho-EDG) Type VI",
            "ui_name": "Arene [ch] #12",
            "smarts": "[cr6h]:[c$(*[NX3!$(*=O),SX2])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 166,
            "name": "Arenes [ch] (ortho-EWG)",
            "ui_name": "Arene [ch] #13",
            "smarts": "[cr6h]:[c$(*[N$(*=O),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 167,
            "name": "Arenes [ch] (ortho-EWG) Type II",
            "ui_name": "Arene [ch] #14",
            "smarts": "[cr6h]:[c$(*[C]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 168,
            "name": "Arenes [ch] (para-EDG) Type I",
            "ui_name": "Arene [ch] #15",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[OX2H0z0,N!$(*=O),SX2])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 169,
            "name": "Arenes [ch] (para-EDG) Type II",
            "ui_name": "Arene [ch] #16",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 170,
            "name": "Arenes [ch] (para-EDG) Type III",
            "ui_name": "Arene [ch] #17",
            "smarts": "[ch]:1:[c]:[c]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 171,
            "name": "Arenes [ch] (para-EDG) Type IV",
            "ui_name": "Arene [ch] #18",
            "smarts": "[ch]:1:[c]:[c]:[c$(*(a)(a)a)]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 172,
            "name": "Arenes [ch] (para-EDG) Type V",
            "ui_name": "Arene [ch] #19",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[CX4])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 173,
            "name": "Arenes [ch] (para-EWG)",
            "ui_name": "Arene [ch] #20",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 174,
            "name": "Arenes [ch] 5-memb 2nd pos 2 rings",
            "ui_name": "Arene [ch] #21",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[a!$([nX2])]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 175,
            "name": "Benzoimidazole [ch] 5-memb",
            "ui_name": "Hetarene #28",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[nX2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 176,
            "name": "Arenes activated [c-]",
            "ui_name": "Arene [c-] #1",
            "smarts": "[c-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 177,
            "name": "Arenes activated metallorganic [c][Me] (type I)",
            "ui_name": "Arene [c-] #2",
            "smarts": "[c][Li,Mg,Na,K]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 178,
            "name": "Arenes activated metallorganic [c][Me] (type II)",
            "ui_name": "Arene [c-] #3",
            "smarts": "[c][Sn,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 179,
            "name": "Aryl bromide",
            "ui_name": "(Het)aryl bromide #5",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 180,
            "name": "5-bromo pyrimidine",
            "ui_name": "(Het)aryl bromide #6",
            "smarts": "[cr6$(*1cncnc1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 181,
            "name": "Aryl carboxylic group [c]COOH",
            "ui_name": "Carboxyl(ate) #10",
            "smarts": "[c][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 182,
            "name": "Aryl chloride",
            "ui_name": "(Het)aryl chloride #6",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 183,
            "name": "Aryl fluoride",
            "ui_name": "(Het)aryl fluoride #2",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 184,
            "name": "Aryl halide and sulfanate",
            "ui_name": "(Het)aryl (pseudo)halide #3",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 185,
            "name": "Aryl iodide",
            "ui_name": "(Het)aryl iodide #5",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 186,
            "name": "Aryl sulfonate",
            "ui_name": "Sulfonate #3",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 187,
            "name": "Aryl triflate",
            "ui_name": "(Het)aryl triflate #5",
            "smarts": "[cr6!$(*[n])&!$(*1aanaa1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 188,
            "name": "Azide [C,c][N3]",
            "ui_name": "Azide #1",
            "smarts": "[#6][N]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 189,
            "name": "Azole (thiazole, oxazole, imidazole and other) [n:]",
            "ui_name": "Hetarene #32",
            "smarts": "[n,s,o]:1:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 190,
            "name": "Benzofuran [ch] 3rd pos",
            "ui_name": "Hetarene #27",
            "smarts": "[ch]:1:[a]:[o]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 191,
            "name": "Benzothiophene [ch] 3rd pos",
            "ui_name": "Hetarene #29",
            "smarts": "[ch]:1:[a]:[s]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 192,
            "name": "Benzoyl O,N ([O,N]Bz)",
            "ui_name": "Bz-PG #1",
            "smarts": "[#6,#7,#8][O,#7][C](=[O])[c]:1:[cH1]:[cH1]:[cH1]:[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 193,
            "name": "Benzyl O,N ([O,N]Bn)",
            "ui_name": "Bn-PG #1",
            "smarts": "[#6,#7,#8][O,#7][CX4H2][c]:1:[c;H1,$(*OC)]:c:[c;H1,$(*OC),$(*[F,Cl,Br])]:c:[c;H1,$(*OC)]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 194,
            "name": "Boc-protection",
            "ui_name": "Boc-PG #2",
            "smarts": "[#7][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 195,
            "name": "Boc-protection [Nh]",
            "ui_name": "Boc-PG #1",
            "smarts": "[Nh][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 196,
            "name": "Boron acid",
            "ui_name": "Boron #4",
            "smarts": "[#6][B]([Oh])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 197,
            "name": "Boron derivates",
            "ui_name": "Boron #3",
            "smarts": "[#6][BH0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 198,
            "name": "Boron derivates [Bh]",
            "ui_name": "Boron #2",
            "smarts": "[#6][Bh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 199,
            "name": "Boron pinocolate",
            "ui_name": "Boron #1",
            "smarts": "[#6][B]1[O][C](C)(C)[C](C)(C)[O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 200,
            "name": "C-enamine C=C[N] cyclic",
            "ui_name": "Enamine #9",
            "smarts": "[C]=[C;r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 201,
            "name": "C-enamine C=C[N] non-cyclic",
            "ui_name": "Enamine #10",
            "smarts": "[C]=[C!r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 202,
            "name": "C-Halogenanhydride [C](=[O])[Hal]",
            "ui_name": "Acyl halide #1",
            "smarts": "[C](=[O])[Br,Cl,I,F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 203,
            "name": "C-nitro derivatives",
            "ui_name": "Nitro #2",
            "smarts": "[C]=[N+]([O-])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 204,
            "name": "C-O activated",
            "ui_name": "Oxonium #1",
            "smarts": "[CX4][O+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 205,
            "name": "Carbamate  [O][C](=[O])[Nh0]",
            "ui_name": "Carbamate #1",
            "smarts": "[OH0][C](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 206,
            "name": "Carbamate [O][C](=[O])[Nh]",
            "ui_name": "Carbamate #3",
            "smarts": "[OH0][C](=[O])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 207,
            "name": "Carbamate anion (Activated [N-])",
            "ui_name": "Carbamate #4",
            "smarts": "[O!$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 208,
            "name": "Carbamate anion (Activated [N][Me])",
            "ui_name": "Carbamate #5",
            "smarts": "[O][C](=[O])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 209,
            "name": "Carbamate Boc anion (Activated [N-])",
            "ui_name": "Carbamate #2",
            "smarts": "[O$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 210,
            "name": "Carbocation [C+]",
            "ui_name": "Carbenium #1",
            "smarts": "[C;X3&+1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 211,
            "name": "Carbodiimide",
            "ui_name": "Carbodiimide #1",
            "smarts": "[#6][N]=[C]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 212,
            "name": "Carbonate (4-nitrophenyl) [O][C](=[O])O[C6H4][NO2]",
            "ui_name": "Carboxyl(ate) #12",
            "smarts": "[#6][O][CX3](=[O])[O]c1ccc([N+1]([O-])=[O])cc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 213,
            "name": "Carbonate (vinyl) [O][C](=[O])O[CH1]=[CH2]",
            "ui_name": "Carboxyl(ate) #14",
            "smarts": "[#6][O][CX3](=[O])[O][CH1]=[CH2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 214,
            "name": "Carbonate and thiocarbonate [O,S][C](=[O,S])[O,S]",
            "ui_name": "Carboxyl(ate) #13",
            "smarts": "[#8,#16][#6](=[O,S])[#8,#16]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 215,
            "name": "Carboxylate [C][C](=[O])[O-]",
            "ui_name": "Carboxyl(ate) #3",
            "smarts": "[#6,#7][C](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 216,
            "name": "Carboxylate [C][C](=[O])[O][Me]",
            "ui_name": "Carboxyl(ate) #4",
            "smarts": "[#6,#7][C](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 217,
            "name": "Carboxylic acid [C](=[O])[Oh]",
            "ui_name": "Carboxyl(ate) #5",
            "smarts": "[CX3z2](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 218,
            "name": "Carboxylic ester (ethyl) COOEt",
            "ui_name": "Carboxyl(ate) #6",
            "smarts": "[CX3z2](=[O])[O][CH2][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 219,
            "name": "Carboxylic ester (methyl) COOCH3",
            "ui_name": "Carboxyl(ate) #7",
            "smarts": "[CX3z2&$(*[#6&+0])&!$(*[CX3]=[CX3][O][Na,K,Li,Mg,Zn])&!$(*[CX3]=[CX3][O-1])](=[O])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 220,
            "name": "Carboxylic ester COOR (ordinary)",
            "ui_name": "Carboxyl(ate) #8",
            "smarts": "[CX3z2](=[O])[O;!$(*[CH2][CH3])&!$(*[CH3])][#6;!$(*=[O,S,N])&!$(*([#6])([#6])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 221,
            "name": "Carboxylic ester COOR (tert-butyl)",
            "ui_name": "Carboxyl(ate) #9",
            "smarts": "[CX3z2](=[O])[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 222,
            "name": "Di-carbonyl derivatives (type I) Malonic derivatives",
            "ui_name": "Dicarbonyl #1",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 223,
            "name": "Di-carbonyl derivatives (type I) Malonic derivatives (activated)",
            "ui_name": "Dicarbonyl #2",
            "smarts": "[C,S,N,P](=[O])[C;X3&-1][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 224,
            "name": "Di-carbonyl derivatives (type II) Malonic derivatives",
            "ui_name": "Dicarbonyl #3",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 225,
            "name": "Di-nitrile derivatives (Malonic derivatives)",
            "ui_name": "Dinitrile #1",
            "smarts": "[C](#[N])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 226,
            "name": "Diazirine",
            "ui_name": "Diazirine #1",
            "smarts": "[CX4]1[N]=[N]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 227,
            "name": "Diazo compound (type I, aliphatic)",
            "ui_name": "Diazo #1",
            "smarts": "[C][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 228,
            "name": "Diazo compound (type I, aromatic)",
            "ui_name": "Diazo #2",
            "smarts": "[c][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 229,
            "name": "Diazo compounds",
            "ui_name": "Diazo #3",
            "smarts": "[C]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 230,
            "name": "Diazo compounds (type II) (diazene or diimide or diimine)",
            "ui_name": "Diazo #4",
            "smarts": "[#6][N]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 231,
            "name": "Diazo compounds anion (type III)",
            "ui_name": "Diazo #5",
            "smarts": "[C-]-[N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 232,
            "name": "Dimethylacetale protecting group",
            "ui_name": "DMA-PG #1",
            "smarts": "[CX4z2]([O][CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 233,
            "name": "Dioxalane",
            "ui_name": "Dioxalane #1",
            "smarts": "[CX4]1[O][CH2][O][CX4]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 234,
            "name": "Disulfide activated S-[S-]",
            "ui_name": "Disulfide #2",
            "smarts": "[Sv2][Sv2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 235,
            "name": "Disulfide activated S-[S][Me]",
            "ui_name": "Disulfide #3",
            "smarts": "[Sv2][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 236,
            "name": "Disulfide S-[Sh]",
            "ui_name": "Disulfide #1",
            "smarts": "[Sv2][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 237,
            "name": "Dithiane S-[Ch]-S",
            "ui_name": "Dithiane #1",
            "smarts": "[S][C;X4&h][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 238,
            "name": "Double bond",
            "ui_name": "Alkene #1",
            "smarts": "[CX3!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]=[CX3!$(*(=[CX3][a])[a])&!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 239,
            "name": "Double bond (allen)",
            "ui_name": "Allene #1",
            "smarts": "[C]=[C]=[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 240,
            "name": "Double bond (isolated)",
            "ui_name": "Alkene #2",
            "smarts": "[a][CX3]=[CX3][a]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 241,
            "name": "Enamine C=C-[Nh]",
            "ui_name": "Enamine #5",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 242,
            "name": "Enamine C=C-[Nh] (conjugated)",
            "ui_name": "Enamine #4",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 243,
            "name": "Enamine C=C-[Nh] Acylated",
            "ui_name": "Enamine #3",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3h$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 244,
            "name": "Enamine C=C-[NH0]",
            "ui_name": "Enamine #8",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 245,
            "name": "Enamine C=C-[NH0] (conjugated)",
            "ui_name": "Enamine #7",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 246,
            "name": "Enamine C=C-[NH0] Acylated",
            "ui_name": "Enamine #6",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3H0$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 247,
            "name": "Enamine C=C[N-]",
            "ui_name": "Enamine #2",
            "smarts": "[C]=[C][NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 248,
            "name": "Enamine C=C[N][Me]",
            "ui_name": "Enamine #1",
            "smarts": "[C]=[C][NX3][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 249,
            "name": "Enol C=C-[Oh] (conjugated)",
            "ui_name": "Enol #2",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 250,
            "name": "Enol C=C-[Oh] (non-conjugated)",
            "ui_name": "Enol #1",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 251,
            "name": "Enol silyl ether C=C[O][Si]",
            "ui_name": "Silyl #11",
            "smarts": "[CX3]=[CX3][O][#14]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 252,
            "name": "Enolate C=C[O-]",
            "ui_name": "Enolate #4",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 253,
            "name": "Enolate C=C[O-] (conjugated)",
            "ui_name": "Enolate #3",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 254,
            "name": "Enolate C=C[O][Me]",
            "ui_name": "Enolate #2",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 255,
            "name": "Enolate C=C[O][Me] (conjugated)",
            "ui_name": "Enolate #1",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 256,
            "name": "Epoxide",
            "ui_name": "Epoxide #1",
            "smarts": "[CX4]1[CX4][O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 257,
            "name": "Ether",
            "ui_name": "Ether #1",
            "smarts": "[C;X4&!$(*=[O,S,N])&!$(*([O])[O,S,N])][O][#6;!$(*=[O,S,N])&!$(*([O])[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 258,
            "name": "Ether (di-phenyl)",
            "ui_name": "Ether #2",
            "smarts": "[c!$(*=[O,S,N])][O][c!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 259,
            "name": "EWG aryl ortho- (tosylate,mesylate and so on)",
            "ui_name": "(Het)aryl (pseudo)halide #2",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 260,
            "name": "EWG aryl ortho- bromide",
            "ui_name": "(Het)aryl bromide #12",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 261,
            "name": "EWG aryl ortho- chloride",
            "ui_name": "(Het)aryl chloride #11",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 262,
            "name": "EWG aryl ortho- fluoride",
            "ui_name": "(Het)aryl fluoride #7",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 263,
            "name": "EWG aryl ortho- iodide",
            "ui_name": "(Het)aryl iodide #6",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 264,
            "name": "EWG aryl ortho- triflate",
            "ui_name": "(Het)aryl triflate #6",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 265,
            "name": "EWG aryl para-  (tosylate,mesylate and so on)",
            "ui_name": "(Het)aryl (pseudo)halide #1",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 266,
            "name": "EWG aryl para- bromide",
            "ui_name": "(Het)aryl bromide #11",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 267,
            "name": "EWG aryl para- chloride",
            "ui_name": "(Het)aryl chloride #12",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 268,
            "name": "EWG aryl para- fluoride",
            "ui_name": "(Het)aryl fluoride #6",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 269,
            "name": "EWG aryl para- iodide",
            "ui_name": "(Het)aryl iodide #7",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 270,
            "name": "EWG aryl para- triflate",
            "ui_name": "(Het)aryl triflate #7",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 271,
            "name": "Fluorene [Ch]",
            "ui_name": "Fluorene #1",
            "smarts": "[Ch]1[c][c][c][c]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 272,
            "name": "Fmoc group",
            "ui_name": "Fmoc-PG #1",
            "smarts": "c:1:c:c:c2:c(:c:1)C(c:3:c2:c:c:c:c:3)COC(=O)[#7;X3&!$(*=[O])][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 273,
            "name": "Formic acid amide [Ch]=[O]",
            "ui_name": "Amide #5",
            "smarts": "[#7][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 274,
            "name": "Formic acid ester [Ch]=O",
            "ui_name": "Carboxyl(ate) #11",
            "smarts": "[O][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 275,
            "name": "Fukuyama-Mitsunobu intermediate",
            "ui_name": "Oxaphosphonium #1",
            "smarts": "[CX4][O+]=[P]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 276,
            "name": "Furan",
            "ui_name": "Hetarene #1",
            "smarts": "o:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 277,
            "name": "Furan [ch]  2nd pos",
            "ui_name": "Hetarene #2",
            "smarts": "[ch]:1:[o]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 278,
            "name": "Furan [ch]  3rd pos",
            "ui_name": "Hetarene #3",
            "smarts": "[ch]:1:[a]:[o]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 279,
            "name": "Guanidine (=Nh)",
            "ui_name": "Guanidine #6",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](-[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 280,
            "name": "Guanidine (=Nh) deactivated",
            "ui_name": "Guanidine #5",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](-[NX3])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 281,
            "name": "Guanidine NC(=N)[N-] activated",
            "ui_name": "Guanidine #4",
            "smarts": "[N][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 282,
            "name": "Guanidine NC(=N)[N][Me] activated",
            "ui_name": "Guanidine #3",
            "smarts": "[N][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 283,
            "name": "Guanidine NC(=N)[Nh]",
            "ui_name": "Guanidine #2",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](=[N])[NX3h!$(*([C]=[N])[C,S,N]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 284,
            "name": "Guanidine NC(=N)[Nh] deactivated",
            "ui_name": "Guanidine #1",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](=[N])[NX3h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 285,
            "name": "Hemiaminal non-cyclic [N][CX4][Oh]",
            "ui_name": "(Hemi)aminal #2",
            "smarts": "[OH1][CX4][#7!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 286,
            "name": "Hemiaminal non-cyclic [Nh][CX4][O]",
            "ui_name": "(Hemi)aminal #3",
            "smarts": "[N&h&R0&$(*[CX4][O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 287,
            "name": "Hydrazide from aldehyde  [C][C](=[N][Nh0])[C] (type II)",
            "ui_name": "N-N #9",
            "smarts": "[#6][Ch](=[N][Nh0$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 288,
            "name": "Hydrazide from aldehyde  [C][Ch](=[N][Nh]) (type I)",
            "ui_name": "N-N #8",
            "smarts": "[#6][Ch](=[N][Nh$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 289,
            "name": "Hydrazide from ketone  [C][C](=[N][Nh])[C] (type I)",
            "ui_name": "N-N #6",
            "smarts": "[#6][C](=[N][Nh$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 290,
            "name": "Hydrazide from ketone  [C][C](=[N][Nh0])[C] (type II)",
            "ui_name": "N-N #7",
            "smarts": "[#6][C](=[N][Nh0$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 291,
            "name": "Hydrazine, hydrazide and hydrazone [N][Nh]",
            "ui_name": "N-N #5",
            "smarts": "[NX3!$(*=[O])][NX3h!$(*=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 292,
            "name": "Hydrazone from aldehyde  [C][C](=[N][Nh0]) (type II)",
            "ui_name": "N-N #4",
            "smarts": "[#6][Ch](=[N][Nh0!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 293,
            "name": "Hydrazone from aldehyde  [C][Ch](=[N][Nh]) (type I)",
            "ui_name": "N-N #3",
            "smarts": "[#6][Ch](=[N][Nh!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 294,
            "name": "Hydrazone from ketone  [C][C](=[N][Nh])[C] (type I)",
            "ui_name": "N-N #1",
            "smarts": "[#6][C](=[N][Nh!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 295,
            "name": "Hydrazone from ketone  [C][C](=[N][Nh0])[C] (type II)",
            "ui_name": "N-N #2",
            "smarts": "[#6][C](=[N][Nh0!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 296,
            "name": "Hydroxamic acid C(=O)[N][Oh]",
            "ui_name": "N-O #7",
            "smarts": "[#6][C](=[O])[N][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 297,
            "name": "Hydroxamic acid C(=O)[Nh][O]",
            "ui_name": "N-O #6",
            "smarts": "[#6][C](=[O])[Nh][O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 298,
            "name": "Hydroxylamine [N][Oh]",
            "ui_name": "N-O #5",
            "smarts": "[#7;X3&!$(*[C]=[O])&!$(*=[O])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 299,
            "name": "Hydroxylamine [Nh][O]",
            "ui_name": "N-O #3",
            "smarts": "[#7h;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 300,
            "name": "Hydroxylamine [Nh0][Oh0]",
            "ui_name": "N-O #4",
            "smarts": "[#7h0;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 301,
            "name": "Hydroxylamine anions [N][O-]",
            "ui_name": "N-O #2",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 302,
            "name": "Hydroxylamine anions [N][O][Me]",
            "ui_name": "N-O #1",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 303,
            "name": "Imidate [#6][C](=[N][C])[O][C]",
            "ui_name": "Imidate #1",
            "smarts": "[#6][C](=[NH0][#6])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 304,
            "name": "Imidazole [ch] 4th pos",
            "ui_name": "Hetarene #5",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 305,
            "name": "Imidazole [ch] 5th pos",
            "ui_name": "Hetarene #4",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 306,
            "name": "Imidazole [nh]",
            "ui_name": "Hetarene #6",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:c:n:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 307,
            "name": "Imidazolium",
            "ui_name": "Hetarene #36",
            "smarts": "[n;$(*-[#6])&+1]:1:[ch]:[n$(*[C])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 308,
            "name": "Imide anion (Activated [N-])",
            "ui_name": "Imide #1",
            "smarts": "[#6][C](=[O])[N-][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 309,
            "name": "Imide C(=O)[Nh]C(=O)",
            "ui_name": "Imide #2",
            "smarts": "[C](=[O])[Nh][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 310,
            "name": "Imine [#6][C](=[N][#6])[#6] (ketone)",
            "ui_name": "C=N #6",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 311,
            "name": "Imine [#6][Ch](=[N][#6]) (aldehyde)",
            "ui_name": "C=N #5",
            "smarts": "[#6][Ch](=[N][#6,S])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 312,
            "name": "Imine, oxyme [#6][C](=[N])[#6] (ketone)",
            "ui_name": "C=N #3",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 313,
            "name": "Imine, oxyme [#6][C](=[N+])[#6] activated (ketone)",
            "ui_name": "C=N #4",
            "smarts": "[#6][C](=[N+][#6,S,O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 314,
            "name": "Imine, oxyme [#6][C]=[N] (aldehyde)",
            "ui_name": "C=N #1",
            "smarts": "[#6][Ch]=[N][#6,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 315,
            "name": "Imine, oxyme [#6][C]=[N+] activated (aldehyde)",
            "ui_name": "C=N #2",
            "smarts": "[#6][Ch]=[N+][#6,S,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 316,
            "name": "Indole",
            "ui_name": "Hetarene #7",
            "smarts": "n:1:[cR2]:[cR2]:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 317,
            "name": "Indole [ch] 3rd pos",
            "ui_name": "Hetarene #8",
            "smarts": "[ch]:1:[a]:[nX3]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 318,
            "name": "Isocyanate and Isothiocyanate R-N=C=O,S",
            "ui_name": "Iso(thio)cyanate #1",
            "smarts": "[N$(*([#6])=[C])]=[C]=[O,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 319,
            "name": "Isocyanide (Isonitrile) R-[N+]#[C-]",
            "ui_name": "Isocyanide #1",
            "smarts": "[N+1&$(*([#6])#[C])]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 320,
            "name": "Ketene [C]=[C]=[O]",
            "ui_name": "Ketene #1",
            "smarts": "[C]=[C]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 321,
            "name": "Ketone [C]=[O]",
            "ui_name": "Carbonyl #7",
            "smarts": "[#6!$(*[Na,K,Li,Mg,Zn,Sn])][C!$([C;r5,r6](=[O])([c])[c])](=[O])[#6!$(*[Na,K,Li,Mg,Zn,Sn])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 322,
            "name": "Anthraquinone [C]=[O]",
            "ui_name": "Quinone #1",
            "smarts": "[c][C;r5,r6](=[O])[c]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 323,
            "name": "Ketone [C]=[O] and H2O",
            "ui_name": "Geminal diol #2",
            "smarts": "[#6][CX4]([OH1])([OH1])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 324,
            "name": "Ketoxime  [#6][C](=[N][Oh])[#6] (type I)",
            "ui_name": "C=N #9",
            "smarts": "[#6][C](=[N][Oh])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 325,
            "name": "Ketoxime  [#6][C](=[N][Oh0])[#6] (type II)",
            "ui_name": "C=N #10",
            "smarts": "[#6][C](=[N][Oh0])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 326,
            "name": "Ketoxime anions [N][O-]",
            "ui_name": "C=N #8",
            "smarts": "[#6][C]([#6])=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 327,
            "name": "Ketoxime anions [N][O][Me]",
            "ui_name": "C=N #7",
            "smarts": "[#6][C]([#6])=[N][O][Na,K,Mg,Li,Cu,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 328,
            "name": "Metallorganic aliphatic (type I)",
            "ui_name": "Metal-organic compound #5",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 329,
            "name": "Metallorganic aliphatic (type II)",
            "ui_name": "Metal-organic compound #4",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 330,
            "name": "Metallorganic alkene (type I)",
            "ui_name": "Metal-organic compound #3",
            "smarts": "[CX3]=[CX3][Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 331,
            "name": "Metallorganic alkene (type II)",
            "ui_name": "Metal-organic compound #2",
            "smarts": "[CX3]=[CX3][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 332,
            "name": "Metallorganic sp2 (lithium and magnesium)",
            "ui_name": "Metal-organic compound #1",
            "smarts": "[CX3,c][Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 333,
            "name": "Michael acceptor [C,N,S](=[O])[C]#[C][C,N,S]=[O] (type VIII)",
            "ui_name": "Michael acceptor #10",
            "smarts": "[C,N,S](=[O])[C]#[C][C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 334,
            "name": "Michael acceptor [C]#[C][C;X3&!$(*[!#6])](=[O]) (type X)",
            "ui_name": "Michael acceptor #9",
            "smarts": "[C!$(*[O,N])]#[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 335,
            "name": "Michael acceptor [C]#[C][C](=[O,N,S])[O,N,S] (type IX) ",
            "ui_name": "Michael acceptor #8",
            "smarts": "[C!$(*[O,N])]#[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 336,
            "name": "Michael acceptor [C]=[C]([C,N,S]=[O])[C,N,S]=[O] (type VI)",
            "ui_name": "Michael acceptor #7",
            "smarts": "[C!$(*[O,N])]=[C]([C,N,S]=[O])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 337,
            "name": "Michael acceptor [C]=[C]([C]#[N])[C,N,S]=[O] (type VII)",
            "ui_name": "Michael acceptor #6",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 338,
            "name": "Michael acceptor [C]=[C]([C]#[N])[C]#[N] (type III)",
            "ui_name": "Michael acceptor #5",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 339,
            "name": "Michael acceptor [C]=[C][C;X3&!$(*[!#6])](=[O]) (type II)",
            "ui_name": "Michael acceptor #4",
            "smarts": "[C!$(*[O,N])]=[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 340,
            "name": "Michael acceptor [C]=[C][C](=[O,N,S])[O,N,S] (type I) ",
            "ui_name": "Michael acceptor #2",
            "smarts": "[C!$(*[O,N])]=[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 341,
            "name": "Michael acceptor [C]=[C][C]#[N] (type IV)",
            "ui_name": "Michael acceptor #3",
            "smarts": "[C!$(*[O,N])]=[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 342,
            "name": "Michael acceptor [C]=[C][N,S,P]=[O,N] (type V)",
            "ui_name": "Michael acceptor #1",
            "smarts": "[C!$(*[O,N])]=[C][N,S,P]=[O,N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 343,
            "name": "MOM protecting group",
            "ui_name": "MOM-PG #1",
            "smarts": "[#6!$(*=[O,S,N])][O][CH2][O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 344,
            "name": "Nitrile C#N (aliphatic)",
            "ui_name": "Nitrile #2",
            "smarts": "[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 345,
            "name": "Nitrile C#N (aromatic)",
            "ui_name": "Nitrile #1",
            "smarts": "[c][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 346,
            "name": "Nitrile oxide",
            "ui_name": "N-oxide #1",
            "smarts": "[C]#[N+][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 347,
            "name": "Nitro compounds",
            "ui_name": "Nitro #3",
            "smarts": "[#6][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 348,
            "name": "Nitroso derivatives",
            "ui_name": "Nitroso #1",
            "smarts": "[#6h0][NX2]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 349,
            "name": "o-Alkyl pyridine (PyCH)",
            "ui_name": "CH-acid #1",
            "smarts": "[C;X4&h][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 350,
            "name": "o-Alkyl pyridine anione Py[C-]",
            "ui_name": "CH-anion #3",
            "smarts": "[C;X3&-1][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 351,
            "name": "o-Alkyl pyridine anione Py[C][Me]",
            "ui_name": "CH-anion #4",
            "smarts": "[Li,K,Na,Mg][C;X4][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 352,
            "name": "O-Tetrahydropyrane protection (OTHP)",
            "ui_name": "THP-PG #1",
            "smarts": "[Ch2]1[O][Ch]([O,#7][#6])[Ch2][Ch2][Ch2]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 353,
            "name": "p-Alkyl pyridine (PyCH)",
            "ui_name": "CH-acid #2",
            "smarts": "[C;X4&h][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 354,
            "name": "p-Alkyl pyridine anione Py[C-]",
            "ui_name": "CH-anion #1",
            "smarts": "[C;X3&-1][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 355,
            "name": "p-Alkyl pyridine anione Py[C][Me]",
            "ui_name": "CH-anion #2",
            "smarts": "[Li,K,Na,Mg][CX4][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 356,
            "name": "P-anhydride [O]=[P][O][P]=[O]",
            "ui_name": "P-compound #8",
            "smarts": "[O]=[P][O][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 357,
            "name": "P-Halogenanhydride [P][Hal]",
            "ui_name": "P-Hal #1",
            "smarts": "[P][Cl,Br,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 358,
            "name": "Peroxide [O][Oh]",
            "ui_name": "Peroxide #1",
            "smarts": "[O][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 359,
            "name": "Peroxy anions [N,O][O][Me]",
            "ui_name": "Peroxide #2",
            "smarts": "[O][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 360,
            "name": "Peroxy anions [O][O-]",
            "ui_name": "Peroxide #3",
            "smarts": "[O][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 361,
            "name": "phenol c-[Oh]",
            "ui_name": "Phenol #1",
            "smarts": "[c;!$(*n)&!$(*:1:a:a:n:a:a:1)][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 362,
            "name": "phenolate c-[O-]",
            "ui_name": "Phenolate #2",
            "smarts": "[c][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 363,
            "name": "phenolate c-[O][Me]",
            "ui_name": "Phenolate #1",
            "smarts": "[c][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 364,
            "name": "Phenyldimethylsilane group (C)",
            "ui_name": "Silyl #13",
            "smarts": "[#6][#14]([CH3])([CH3])c1ccccc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 365,
            "name": "Phosphine and phosphane [#6]-P",
            "ui_name": "P-compound #7",
            "smarts": "[#6][P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 366,
            "name": "Phosphine and phosphane [Ch]",
            "ui_name": "P-compound #6",
            "smarts": "[P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 367,
            "name": "Phosphite, Phosphinite,Phosphonite [O]-P",
            "ui_name": "P-compound #5",
            "smarts": "[O][P;X3&!$(*([!#6,!O])[!#6,!O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 368,
            "name": "Phosphonate anion",
            "ui_name": "P-compound #4",
            "smarts": "[P](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 369,
            "name": "Phosphonate anion [Me]",
            "ui_name": "P-compound #3",
            "smarts": "[P](=[O])[OH0][Na,K,Cu,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 370,
            "name": "Phosphonium salts [P+][C;X4&h] Wittig",
            "ui_name": "P-compound #2",
            "smarts": "[P+][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 371,
            "name": "Phosphoric acid",
            "ui_name": "P-compound #1",
            "smarts": "[P](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 372,
            "name": "PMB protecting group",
            "ui_name": "PMB-PG #2",
            "smarts": "[#6,#7,#8][O,#7][CH2][c]:1:[cH1]:[cH1]:[c]([O][CH3]):[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 373,
            "name": "PMB protecting group (common)",
            "ui_name": "PMB-PG #1",
            "smarts": "[#6,#7,#8][O,#7][C;R0&X4&h]c:1:c:c:[c]([O][C]):c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 374,
            "name": "Pyranone group",
            "ui_name": "Hetarene #20",
            "smarts": "[O]=[c]1[c][c!$(*[O,N])][o][c!$(*[O,N])][c]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 375,
            "name": "Pyrazole [ch] 4th pos",
            "ui_name": "Hetarene #23",
            "smarts": "[ch]:1:[!n]:[nX3]:[nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 376,
            "name": "Pyrazole [ch] 5th pos",
            "ui_name": "Hetarene #22",
            "smarts": "[ch]:1:[nX3]:[nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 377,
            "name": "Pyrazole [n-] activated",
            "ui_name": "Hetarene #21",
            "smarts": "[n;-1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 378,
            "name": "Pyrazole [nh]",
            "ui_name": "Hetarene #19",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 379,
            "name": "Pyridine",
            "ui_name": "Hetarene #18",
            "smarts": "[c,n]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 380,
            "name": "Pyridine oxide [n+1][O-]",
            "ui_name": "N-oxide #2",
            "smarts": "[nr6&+1][O-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 381,
            "name": "Pyridinyl bromide (2-pos)",
            "ui_name": "(Het)aryl bromide #10",
            "smarts": "[c$(*1nacac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 382,
            "name": "Pyridinyl bromide (4-pos)",
            "ui_name": "(Het)aryl bromide #9",
            "smarts": "[c$(*1canac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 383,
            "name": "Pyridinyl chloride (2-pos)",
            "ui_name": "(Het)aryl chloride #7",
            "smarts": "[c$(*1nacac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 384,
            "name": "Pyridinyl chloride (4-pos)",
            "ui_name": "(Het)aryl chloride #8",
            "smarts": "[c$(*1canac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 385,
            "name": "Pyridinyl fluoride",
            "ui_name": "(Het)aryl fluoride #5",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 386,
            "name": "Pyridinyl iodide (2-pos)",
            "ui_name": "(Het)aryl iodide #11",
            "smarts": "[c$(*1nacac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 387,
            "name": "Pyridinyl iodide (4-pos)",
            "ui_name": "(Het)aryl iodide #10",
            "smarts": "[c$(*1canac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 388,
            "name": "Pyridinyl sulfonate (tosylate,mesylate and so on)",
            "ui_name": "Sulfonate #5",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 389,
            "name": "Pyridinyl triflate",
            "ui_name": "(Het)aryl triflate #8",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 390,
            "name": "Pyridinyl triflate (2-pos)",
            "ui_name": "(Het)aryl triflate #9",
            "smarts": "[c$(*1nacac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 391,
            "name": "Pyridinyl triflate (4-pos)",
            "ui_name": "(Het)aryl triflate #10",
            "smarts": "[c$(*1canac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 392,
            "name": "Pyrimidyl alkyl sulfide (2-pos) [n][c]([S])[n]",
            "ui_name": "Sulfide #3",
            "smarts": "[c$(*1nacan1)][SX2][CX4z1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 393,
            "name": "Pyrimidyl bromide (2-pos)",
            "ui_name": "(Het)aryl bromide #8",
            "smarts": "[c$(*1nacan1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 394,
            "name": "Pyrimidyl bromide (4-pos)",
            "ui_name": "(Het)aryl bromide #7",
            "smarts": "[c$(*1nanac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 395,
            "name": "Pyrimidyl chloride (2-pos)",
            "ui_name": "(Het)aryl chloride #9",
            "smarts": "[c$(*1nacan1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 396,
            "name": "Pyrimidyl chloride (4-pos)",
            "ui_name": "(Het)aryl chloride #10",
            "smarts": "[c$(*1nanac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 397,
            "name": "Pyrimidyl fluoride (2-pos)",
            "ui_name": "(Het)aryl fluoride #4",
            "smarts": "[c$(*1nacan1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 398,
            "name": "Pyrimidyl fluoride (4-pos)",
            "ui_name": "(Het)aryl fluoride #3",
            "smarts": "[c$(*1nanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 399,
            "name": "Pyrimidyl Iodide (2-pos)",
            "ui_name": "(Het)aryl iodide #9",
            "smarts": "[c$(*1nacan1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 400,
            "name": "Pyrimidyl Iodide (4-pos)",
            "ui_name": "(Het)aryl iodide #8",
            "smarts": "[c$(*1nanac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 401,
            "name": "Pyrimidyl sulfinate (tosylate,mesylate and so on) (2-pos)",
            "ui_name": "Sulfinate #3",
            "smarts": "[c;$(*1nacan1)][S](=[O])(=[O])[#6$([CX4z1,c])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 402,
            "name": "Pyrimidyl sulfonate (tosylate,mesylate and so on) (2-pos)",
            "ui_name": "Sulfonate #6",
            "smarts": "[c;$(*1nacan1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 403,
            "name": "Pyrimidyl sulfonate (tosylate,mesylate and so on) (4-pos)",
            "ui_name": "Sulfonate #7",
            "smarts": "[c;$(*1nanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 404,
            "name": "Pyrimidyl triflate (2-pos)",
            "ui_name": "(Het)aryl triflate #11",
            "smarts": "[c$(*1nacan1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 405,
            "name": "Pyrimidyl triflate (4-pos)",
            "ui_name": "(Het)aryl triflate #12",
            "smarts": "[c$(*1nanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 406,
            "name": "Pyrrole",
            "ui_name": "Hetarene #17",
            "smarts": "[n!R2]:1:[c!R2]:[c!R2]:[c!R2]:[c!R2]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 407,
            "name": "Pyrrole [ch] 2nd pos",
            "ui_name": "Hetarene #16",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 408,
            "name": "Pyrrole [ch] 3rd pos",
            "ui_name": "Hetarene #15",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 409,
            "name": "Pyrrole, Imidazole, Indole and other [Activated n-]",
            "ui_name": "Hetarene #13",
            "smarts": "[n;r5&!$(*[#6]=[O])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 410,
            "name": "Pyrrole, Imidazole, Indole and other [Activated n-Me bond]",
            "ui_name": "Hetarene #14",
            "smarts": "[nr5!$(*[#6]=[O])][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 411,
            "name": "Pyrrole, Imidazole, Indole and other [nh]",
            "ui_name": "Hetarene #12",
            "smarts": "[nr5h!$(*[#6]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 412,
            "name": "Rich electronic amine (primary) [!#6]-[NH2]",
            "ui_name": "Amine #19",
            "smarts": "[NX3,OX2][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 413,
            "name": "Rich electronic amine (secondary) [!#6]-[NH1]-[#6]",
            "ui_name": "Amine #18",
            "smarts": "[NX3,OX2][NX3;H1][#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 414,
            "name": "Rich electronic amine (tertiary) [!#6]-[NH0](-[#6])-[#6]",
            "ui_name": "Amine #17",
            "smarts": "[NX3,OX2][NX3;H0]([#6!$(*=[C,N,O,S])])[#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 415,
            "name": "S-Halogenanhydride [S](=[O])[Hal]",
            "ui_name": "S-Hal #1",
            "smarts": "[S!$(*(=[O])(=[O])[F])][F,Br,Cl,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 416,
            "name": "Selenols PhSeH",
            "ui_name": "(Het)aryl-SeH #1",
            "smarts": "[c][Sev2&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 417,
            "name": "Semi acetale and ketale O-[CX4R0]-O",
            "ui_name": "(Hemi)acetale and (hemi)ketale #1",
            "smarts": "[#6][O][CX4R0][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 418,
            "name": "Semi Carbamate [N][C](=[O])[O]",
            "ui_name": "Carboxyl(ate) #15",
            "smarts": "[#7][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 419,
            "name": "Semi Carbonate [O][C](=[O])[O]",
            "ui_name": "Carboxyl(ate) #16",
            "smarts": "[#8][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 420,
            "name": "Silane [C][SiH](C)[(C)",
            "ui_name": "Silyl #12",
            "smarts": "[#6][#14;X4h]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 421,
            "name": "Silyl chloride [#14][Cl]",
            "ui_name": "Silyl #10",
            "smarts": "[#14][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 422,
            "name": "Silyl derivatives (C)",
            "ui_name": "Silyl #9",
            "smarts": "[#6][#14&!$(*c1ccccc1)](C)(C)C",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 423,
            "name": "Silyl derivatives (heteroatom)",
            "ui_name": "Silyl #8",
            "smarts": "[O,#7][#14!$(*([CH3])([CH3])[C]([CH3])([CH3])[CH3])&!$(*(c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3])&!$(*([CH3])([CH3])[CH3])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 424,
            "name": "Small Cycle (3-memb)",
            "ui_name": "Carbocycle #1",
            "smarts": "A1AA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 425,
            "name": "Small Cycle (4-memb)",
            "ui_name": "Carbocycle #2",
            "smarts": "A1AAA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 426,
            "name": "Sulfamates [O][S](=O)(=O)[N]",
            "ui_name": "Sulfamate #2",
            "smarts": "[OH0][S](=[O])(=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 427,
            "name": "Sulfamates [O][S](=O)(=O)[Nh]",
            "ui_name": "Sulfamate #1",
            "smarts": "[OH0][S](=[O])(=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 428,
            "name": "Sulfate [#6][S](=[O])[O-]",
            "ui_name": "Sulfate #2",
            "smarts": "[#6,#7][S](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 429,
            "name": "Sulfate [#6][S](=[O])[O][Me]",
            "ui_name": "Sulfate #1",
            "smarts": "[#6,#7][S](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 430,
            "name": "Sulfides",
            "ui_name": "Sulfide #1",
            "smarts": "[#6;!$(*=[C,N,O,S])][Sv2][#6;!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 431,
            "name": "Sulfides [Ch]",
            "ui_name": "Sulfide #2",
            "smarts": "[Sv2][C;X4&h&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 432,
            "name": "sulfinate [#6][Sv4](=[O])[O]",
            "ui_name": "Sulfinate #2",
            "smarts": "[#6][Sv4](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 433,
            "name": "Sulfonamide (Activated [N-])",
            "ui_name": "Sulfonamide #4",
            "smarts": "[#6,#7][S](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 434,
            "name": "Sulfonamide (Activated N-Me bond)",
            "ui_name": "Sulfonamide #5",
            "smarts": "[#6,#7][S](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 435,
            "name": "Sulfonamide [Nh]",
            "ui_name": "Sulfonamide #2",
            "smarts": "[#6][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 436,
            "name": "Sulfonamide [Nh] type II",
            "ui_name": "Sulfonamide #1",
            "smarts": "[#7][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 437,
            "name": "Sulfonamide [Nh0]",
            "ui_name": "Sulfonamide #3",
            "smarts": "[#6,#7][S](=[O])[#7h0X3]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 438,
            "name": "Sulfone",
            "ui_name": "Sulfone #1",
            "smarts": "[#6][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 439,
            "name": "Sulfonic anhydride",
            "ui_name": "Sulfonic anhydride #1",
            "smarts": "[#6][S](=[O])(=[O])[O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 440,
            "name": "Sulfonyl fluoride [S](=[O])[F]",
            "ui_name": "Sulfonyl fluoride #1",
            "smarts": "[S](=[O])(=[O])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 441,
            "name": "Sulfoxide",
            "ui_name": "Sulfoxide #1",
            "smarts": "[#6][SX3](=[O])-[#6,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 442,
            "name": "Sulfuric acid [#6][S](=[O])[Oh]",
            "ui_name": "Sulfonic acid #1",
            "smarts": "[#6,#7][S](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 443,
            "name": "Sulfuric acid ester [#6][S](=[O])[O][#6]",
            "ui_name": "Sulfate #3",
            "smarts": "[#6,#7][S](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 444,
            "name": "tert-alcohol  HOC(C)(C)C",
            "ui_name": "tBu #7",
            "smarts": "[OH1][C]([#6])([#6])[CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 445,
            "name": "tert-alkoxy ester OC(C)(C)C",
            "ui_name": "tBu #6",
            "smarts": "[O][C]([#6z0])([#6z0])[#6z0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 446,
            "name": "tert-alkyl ester OC(C)(C)C",
            "ui_name": "tBu #5",
            "smarts": "[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 447,
            "name": "tert-alkyl heteroatom [A]C(C)(C)C",
            "ui_name": "tBu #3",
            "smarts": "[#7,S,Se,P,Si][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 448,
            "name": "tert-butyl amine, amide [N]tBu",
            "ui_name": "tBu #1",
            "smarts": "[#7][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 449,
            "name": "tert-alkyl halide",
            "ui_name": "tBu #4",
            "smarts": "[#6][C]([#6])([#6])[Cl,Br,I,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 450,
            "name": "tert-butoxy ester OtBu",
            "ui_name": "tBu #2",
            "smarts": "[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 451,
            "name": "tert-Butyldimethylsilyl OTBDMS",
            "ui_name": "Silyl #2",
            "smarts": "[O,#7,S][#14]([CH3])([CH3])[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 452,
            "name": "tert-Butyldiphenylsilyl OTBDPS",
            "ui_name": "Silyl #1",
            "smarts": "[O,#7,S][#14](c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 453,
            "name": "Thiazolium",
            "ui_name": "Hetarene #24",
            "smarts": "[n;$(*[#6])&+1]:1:[ch]:[s]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 454,
            "name": "Thio- and oxazole (1,2-)",
            "ui_name": "Hetarene #31",
            "smarts": "[o,s]:1:[n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 455,
            "name": "Thio- and oxazole [ch] (1,3-)",
            "ui_name": "Hetarene #30",
            "smarts": "[o,s]:1:[ch]:[nh0]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 456,
            "name": "Thioamide",
            "ui_name": "Thio-compound #20",
            "smarts": "[N][CX3z2]=[S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 457,
            "name": "Thioamide (Activated [N-])",
            "ui_name": "Thio-compound #18",
            "smarts": "[CX3z2](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 458,
            "name": "Thioamide (Activated N-Me bond)",
            "ui_name": "Thio-compound #19",
            "smarts": "[CX3z2](=[S])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 459,
            "name": "Thioamide [Nh]",
            "ui_name": "Thio-compound #17",
            "smarts": "[CX3z2](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 460,
            "name": "Thioarbamate [O][C](=[S])[Nh]",
            "ui_name": "Thio-compound #16",
            "smarts": "[OH0][C](=[S])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 461,
            "name": "Thioarbamate anion (Activated [N][Me])",
            "ui_name": "Thio-compound #24",
            "smarts": "[O][C](=[S])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 462,
            "name": "Thiocarbamate  [O][C](=[S])[Nh0]",
            "ui_name": "Thio-compound #15",
            "smarts": "[OH0][C](=[S])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 463,
            "name": "Thiocarbamate anion (Activated [N-])",
            "ui_name": "Thio-compound #14",
            "smarts": "[O!$(*C(C)(C)C)][C](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 464,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate [C](=[O,S,N])[Sh]",
            "ui_name": "Thio-compound #21",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 465,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate activated [C](=[O,S,N])[S-]",
            "ui_name": "Thio-compound #22",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 466,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate activated [C](=[O,S,N])[S][Me]",
            "ui_name": "Thio-compound #23",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 467,
            "name": "Thiocarboxylic acid (type I) [#6][C](=[S])[Oh]",
            "ui_name": "Thio-compound #13",
            "smarts": "[#6][C](=[S])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 468,
            "name": "Thiocarboxylic acid (type II) [#6][C](=[O,S])[Sh]",
            "ui_name": "Thio-compound #12",
            "smarts": "[#6][C](=[O,S])[Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 469,
            "name": "Thiocarboxylic anion [C](=[O,S])[S-]",
            "ui_name": "Thio-compound #11",
            "smarts": "[#6,#7,#8][C](=[O,S])[S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 470,
            "name": "Thiocarboxylic anion [C](=[O,S])[S][Me]",
            "ui_name": "Thio-compound #10",
            "smarts": "[#6,#7,#8][C](=[O,S])[SX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 471,
            "name": "Thiocarboxylic anion [C](=[S])[O-] type II",
            "ui_name": "Thio-compound #9",
            "smarts": "[#6,#7,#8][C](=[S])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 472,
            "name": "Thiocarboxylic anion [C](=[S])[O][Me] type II",
            "ui_name": "Thio-compound #8",
            "smarts": "[#6,#7,#8][C](=[S])[OX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 473,
            "name": "Thioester (type I)",
            "ui_name": "Thio-compound #7",
            "smarts": "[#6][C](=[S])[O][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 474,
            "name": "Thioester (type II)",
            "ui_name": "Thio-compound #6",
            "smarts": "[#6][C](=[O])[S][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 475,
            "name": "thiol (mercaptane) C-[Sh]",
            "ui_name": "Thiol #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 476,
            "name": "thiolate C-[S-]",
            "ui_name": "Thiolate #2",
            "smarts": "[C!$(*=[C,N,O,S])][SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 477,
            "name": "thiolate C-[S][Me]",
            "ui_name": "Thiolate #1",
            "smarts": "[C!$(*=[C,N,O,S])][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 478,
            "name": "Thionocarbonate",
            "ui_name": "Thio-compound #5",
            "smarts": "[#6]OC(=S)O[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 479,
            "name": "Thiophene",
            "ui_name": "Hetarene #9",
            "smarts": "s:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 480,
            "name": "Thiophene [ch] 2nd pos",
            "ui_name": "Hetarene #10",
            "smarts": "[ch]:1:[s]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 481,
            "name": "Thiophene [ch] 3rd pos",
            "ui_name": "Hetarene #11",
            "smarts": "[ch]:1:[a]:[s]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 482,
            "name": "thiophenol C-[Sh]",
            "ui_name": "Thiophenol #1",
            "smarts": "[c][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 483,
            "name": "thiophenolate C-[S-]",
            "ui_name": "Thiophenolate #2",
            "smarts": "[c][S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 484,
            "name": "thiophenolate C-[S][Me]",
            "ui_name": "Thiophenolate #1",
            "smarts": "[c][Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 485,
            "name": "Thiourea [N][C](=S)[Nh]",
            "ui_name": "Thio-compound #4",
            "smarts": "[#7][C](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 486,
            "name": "Thiourea [Nh0][C](=S)[Nh0]",
            "ui_name": "Thio-compound #3",
            "smarts": "[#7h0][C](=[S])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 487,
            "name": "Thiourea anion [N][C](=[O])[N-] (Activated [N-])",
            "ui_name": "Thio-compound #2",
            "smarts": "[#7][C](=[S])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 488,
            "name": "Thiourea anion [N][C](=[O])[N][Me] (Activated [N-])",
            "ui_name": "Thio-compound #1",
            "smarts": "[#7][C](=[S])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 489,
            "name": "Triethylsilyl OTES",
            "ui_name": "Silyl #7",
            "smarts": "[O][#14](CC)(CC)CC",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 490,
            "name": "Trimethylsilyl NTMS",
            "ui_name": "Silyl #6",
            "smarts": "[#7][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 491,
            "name": "Trimethylsilyl OTMS (aliphatic)",
            "ui_name": "Silyl #5",
            "smarts": "[C;X2,X3,X4H0][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 492,
            "name": "Trimethylsilyl OTMS (aromatic)",
            "ui_name": "Silyl #4",
            "smarts": "[c][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 493,
            "name": "Trimethylsilyl OTMS (sp3)",
            "ui_name": "Silyl #3",
            "smarts": "[CX4h][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 494,
            "name": "Trityl protection C(Ph)3",
            "ui_name": "Trityl-PG #1",
            "smarts": "[#7,O]C(c:1:c:c:c:c:c:1)(c:2:c:c:c:c:c:2)c:3:c:c:c:c:c:3",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 495,
            "name": "Urea [N][C](=[O])[Nh]",
            "ui_name": "Urea #1",
            "smarts": "[#7][#6](=[O])[#7h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 496,
            "name": "Urea [Nh0][C](=[O])[Nh0]",
            "ui_name": "Urea #2",
            "smarts": "[#7h0][#6](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 497,
            "name": "Urea anion [N][C](=[O])[N-] (Activated [N-])",
            "ui_name": "Urea #3",
            "smarts": "[#7][C](=[O])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 498,
            "name": "Urea anion [N][C](=[O])[N][Me] (Activated [N-])",
            "ui_name": "Urea #4",
            "smarts": "[#7][C](=[O])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 499,
            "name": "Vilsmeier ion",
            "ui_name": "Iminium #1",
            "smarts": "[C][N+]([C])=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 500,
            "name": "Vinyl ethers",
            "ui_name": "Ether #3",
            "smarts": "[CX3&!$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 501,
            "name": "Vinyl ethers (a-carbonyl)",
            "ui_name": "Ether #4",
            "smarts": "[CX3&$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 502,
            "name": "Weinreb amide",
            "ui_name": "Amide #6",
            "smarts": "[#6][C](=[O])[N]([CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 503,
            "name": "Ylide (N) [C-] (type I)",
            "ui_name": "N-ylide #4",
            "smarts": "[O]=[C,N,S][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 504,
            "name": "Ylide (N) [C-] (type II)",
            "ui_name": "N-ylide #3",
            "smarts": "[N]#[C][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 505,
            "name": "Ylide (N) [C][Me] (type I)",
            "ui_name": "N-ylide #2",
            "smarts": "[O]=[C,N,S][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 506,
            "name": "Ylide (N) [C][Me] (type II)",
            "ui_name": "N-ylide #1",
            "smarts": "[N]#[C][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 507,
            "name": "Ylide (P)",
            "ui_name": "P-ylide #5",
            "smarts": "[C]=[P]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 508,
            "name": "Ylide (P) [C-]",
            "ui_name": "P-ylide #4",
            "smarts": "[C-][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 509,
            "name": "Ylide (P) [C-] HWE",
            "ui_name": "P-ylide #3",
            "smarts": "[C-][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 510,
            "name": "Ylide (P) [C][Me]",
            "ui_name": "P-ylide #2",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 511,
            "name": "Ylide (P) [C][Me] HWE",
            "ui_name": "P-ylide #1",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 512,
            "name": "Ylide (S)",
            "ui_name": "S-ylide #3",
            "smarts": "[C]=[Sv4]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 513,
            "name": "Ylide (S) [C-]",
            "ui_name": "S-ylide #2",
            "smarts": "[C-][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 514,
            "name": "Ylide (S) [C][Me]",
            "ui_name": "S-ylide #1",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][CX4][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 515,
            "name": "Arenes [ch] (generic)",
            "ui_name": "Arene [ch] #0",
            "smarts": "[ch]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
)

FG_SIGNATURE_LENGTH: int = len(FUNCTIONAL_GROUPS)

FG_COLLECTION_GENERAL = FunctionalGroups.from_tuple(
    tuple(
        fg for fg in FUNCTIONAL_GROUPS if fg["fg_class"] == FunctionalGroupClass.GENERAL
    )
)
FG_COLLECTION_SEAR = FunctionalGroups.from_tuple(
    tuple(fg for fg in FUNCTIONAL_GROUPS if fg["fg_class"] == FunctionalGroupClass.SEAR)
)
