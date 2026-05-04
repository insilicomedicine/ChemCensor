from frozendict import frozendict

from ..basic.functional_groups import FunctionalGroupClass
from ..basic.functional_groups import FunctionalGroups

FUNCTIONAL_GROUPS: tuple[frozendict[str, int | str | FunctionalGroupClass], ...] = (
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 0,
            "name": "1,2,4-oxadiazol-5(4H)-one [nH]",
            "smarts": "[c]1[nH0][o][c](=[O])[nH1]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 1,
            "name": "1,2,4-oxadiazol-5(4H)-one [nH0]",
            "smarts": "[c]1[nH0][o][c](=[O])[nH0]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 2,
            "name": "2-bromo-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1caa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 3,
            "name": "2-bromo-azole",
            "smarts": "[c$(*1naa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 4,
            "name": "2-chloro- pyrimidine and 2-chloro-imidazole",
            "smarts": "[n][c]([n])[Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 5,
            "name": "2-chloro-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1caa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 6,
            "name": "2-chloro-azole",
            "smarts": "[c$(*1naa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 7,
            "name": "2-Hydroxypyridine nc[O,S]H",
            "smarts": "[c$(*n)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 8,
            "name": "2-iodo-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1caa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 9,
            "name": "2-iodo-azole",
            "smarts": "[c$(*1naa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 10,
            "name": "2-nitro- pyrimidine and 2-nitro-imidazole",
            "smarts": "[n][c]([n])[N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 11,
            "name": "2-OTf-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1caa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 12,
            "name": "2-OTf-azole",
            "smarts": "[c$(*1naa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 13,
            "name": "2-Pyridone [O,S]=[#6][n-] activated",
            "smarts": "[O,S]=[c][n-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 14,
            "name": "2-Pyridone [O,S]=[#6][n][Me] activated",
            "smarts": "[O,S]=[c][n][Li,K,Mg,Na,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 15,
            "name": "2-Pyridone [O,S]=[#6][nh]",
            "smarts": "[O,S]=[c][nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 16,
            "name": "2,4-EWG Aryl bromide",
            "smarts": "[Br][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 17,
            "name": "2,4-EWG Aryl chloride",
            "smarts": "[Cl][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 18,
            "name": "2,4-EWG Aryl fluoride",
            "smarts": "[F][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 19,
            "name": "2,4-EWG Aryl iodide",
            "smarts": "[I][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 20,
            "name": "2,4-EWG Aryl sulfonate",
            "smarts": "[O]([S](=[O])(=[O])[#6!$(*[F])])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 21,
            "name": "2,4-EWG Aryl triflate",
            "smarts": "[O]([S](=[O])(=[O])[#6]([F])([F])[F])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 22,
            "name": "3-bromo-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1ca[!c]c1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 23,
            "name": "3-chloro-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1ca[!c]c1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 24,
            "name": "3-iodo-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1ca[!c]c1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 25,
            "name": "3-OTf-(pyrrole, thiophene, furan)",
            "smarts": "[c$(*1ca[!c]c1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 26,
            "name": "4-Hydroxypyridine",
            "smarts": "[c$(*:1:a:a:n:a:a:1)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 27,
            "name": "4-Pyridone [O,S]=[#6]aa[n-] activated",
            "smarts": "[c]1(=[O,S])aa[n-]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 28,
            "name": "4-Pyridone [O,S]=[#6]aa[n][Me] activated",
            "smarts": "[c]1(=[O,S])aa[n]([Li,K,Mg,Na,Zn])aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 29,
            "name": "4-Pyridone [O,S]=[#6]aa[nh]",
            "smarts": "[c]1(=[O,S])aa[nh]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 30,
            "name": "a-[Br] bromo-carbonyle",
            "smarts": "[Br][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 31,
            "name": "a-[C-] aldehyde anion (type I)",
            "smarts": "[C;X3&-1][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 32,
            "name": "a-[C-] amide anion",
            "smarts": "[C;X3&-1][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 33,
            "name": "a-[C-] carboxylic ester and acid anion",
            "smarts": "[C;X3&-1][C](=[O])[O;h,$(*[#6!$(*[C]=[O,S,N])])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 34,
            "name": "a-[C-] Common template anion",
            "smarts": "[C;X3&-1][C,S,N,P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 35,
            "name": "a-[C-] dithiane anion",
            "smarts": "[S][C-;X3][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 36,
            "name": "a-[C-] ketone anion",
            "smarts": "[C;X3&-1][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 37,
            "name": "a-[C-] nitrile derivatives anion (form I)",
            "smarts": "[C;X3&-1][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 38,
            "name": "a-[C-] nitrile enolate derivatives (form II)",
            "smarts": "[C]=[C]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 39,
            "name": "a-[C-] nitro derivatives anion",
            "smarts": "[C;X3&-1][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 40,
            "name": "a-[C-] phosphonate and phosphine oxide anion",
            "smarts": "[C;X3&-1][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 41,
            "name": "a-[C-] sulfo derivatives anion",
            "smarts": "[C;X3&-1][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 42,
            "name": "a-[C-] thioamide, thioester anion",
            "smarts": "[C;X3&-1][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 43,
            "name": "a-[C-][Me] aldehyde anion (type I)",
            "smarts": "[CX4$(*[C;X3&h]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 44,
            "name": "a-[C-][Me] amide anion",
            "smarts": "[CX4$(*[C](=[O])[#7])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 45,
            "name": "a-[C-][Me] carboxylic ester and acid anion",
            "smarts": "[CX4$(*[C](=[O])[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 46,
            "name": "a-[C-][Me] ketone anion",
            "smarts": "[CX4$(*[C](=[O])[#6])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 47,
            "name": "a-[C-][Me] nitrile derivatives anion (form I)",
            "smarts": "[CX4$(*[C]#[N])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 48,
            "name": "a-[C-][Me] nitro derivatives anion",
            "smarts": "[CX4$(*[N+](=[O])[O-])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 49,
            "name": "a-[C-][Me] phosphonate and phosphine oxide anion",
            "smarts": "[CX4$(*[P]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 50,
            "name": "a-[C-][Me] sulfo derivatives anion",
            "smarts": "[CX4$(*[S]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 51,
            "name": "a-[C-][Me] thioamide, thioester anion",
            "smarts": "[CX4$(*[C](=[S])[#7,#8])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 52,
            "name": "a-[Ch] aldehyde",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 53,
            "name": "a-[Ch] allyl derivatives",
            "smarts": "[C]=[C][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 54,
            "name": "a-[Ch] amide",
            "smarts": "[C;X4&h][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 55,
            "name": "a-[Ch] ammoium salt",
            "smarts": "[C;X4&h][#7;h0&+1&!$(*=O)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 56,
            "name": "a-[Ch] arenes",
            "smarts": "[c][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 57,
            "name": "a-[Ch] carboxylic acid",
            "smarts": "[C;X4&h][C](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 58,
            "name": "a-[Ch] carboxylic ester",
            "smarts": "[C;X4&h][C](=[O])[OH0][#6!$(*=[O,S,N,P])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 59,
            "name": "a-[Ch] Imine =N[Ch]",
            "smarts": "[C;X4&h][N]=[C;$(*[#6])&!$(*-[!#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 60,
            "name": "a-[Ch] ketone",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 61,
            "name": "a-[Ch] nitrile",
            "smarts": "[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 62,
            "name": "a-[Ch] nitro derivatives",
            "smarts": "[C;X4&h][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 63,
            "name": "a-[Ch] phosponate and phosphine oxide",
            "smarts": "[C;X4&h][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 64,
            "name": "a-[Ch] sulfo derivatives",
            "smarts": "[C;X4&h][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 65,
            "name": "a-[Ch] thioamide, thioester",
            "smarts": "[C;X4&h][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 66,
            "name": "a-[Cl] chloro-carbonyle",
            "smarts": "[Cl][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 67,
            "name": "a-[I] Iodo-carbonyle",
            "smarts": "[I][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 68,
            "name": "a-[N2] diazo-carbonyle",
            "smarts": "[N-1]=[N+1]=[CX3][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 69,
            "name": "a-Carboxylic group C(#[N])[C]COOH (type II)",
            "smarts": "[C](#[N])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 70,
            "name": "a-Carboxylic group C(=O)[C]COOH (type I)",
            "smarts": "[C](=[O])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 71,
            "name": "a-sulfonate-carbonyle",
            "smarts": "[C](=[O])[C;X4&h][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 72,
            "name": "Acetale and Ketale O-[CX4]-O",
            "smarts": "[#6][O]-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 73,
            "name": "Acetic anhydride (mixed) C(=O)OC(=O)",
            "smarts": "[#6][C](=[O])[O][C](=[O])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 74,
            "name": "Alcohol [Ch][C][Oh] (type III)",
            "smarts": "[C;X4&h][C;X4&!$(*[#7])&!$(*([O])[O])&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 75,
            "name": "Alcohol [C](=[O])[Ch][C][Oh]",
            "smarts": "[O]=[CX3][CX4h][CX4][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 76,
            "name": "Alcohol C-[Oh] (primary)",
            "smarts": "[C;X4H2&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 77,
            "name": "Alcohol C-[Oh] (secondary)",
            "smarts": "[C;X4H1&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 78,
            "name": "Alcohol C-[Oh] (tertiary)",
            "smarts": "[C;X4H0&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 79,
            "name": "Alcohol OH (OBn) ( benzyl type I) secondary",
            "smarts": "[CX4][CX4H1]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 80,
            "name": "Alcohol OH (OBn) ( benzyl type I) tertiary",
            "smarts": "[CX4][CX4H0]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 81,
            "name": "Alcohol OH (OBn) ( benzyl type II) primary",
            "smarts": "[CX4H2]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 82,
            "name": "Alcohol OH (OBn) ( benzyl type II) secondary",
            "smarts": "[CX4H1]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 83,
            "name": "Alcohol OH (OBn) ( benzyl type II) tertiary",
            "smarts": "[CX4H0]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 84,
            "name": "Alcoholate C-[O-]",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 85,
            "name": "Alcoholate C-[O][Me]",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 86,
            "name": "Aldehyde [Ch][OH1][OH1] and H2O",
            "smarts": "[#6][CX4h][OH1][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 87,
            "name": "Aldehyde [Ch]=[O]",
            "smarts": "[CX3z1h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 88,
            "name": "Aldoxime  [#6][Ch](=[N][Oh]) (type I)",
            "smarts": "[#6][Ch](=[N][Oh])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 89,
            "name": "Aldoxime  [#6][Ch](=[N][Oh0]) (type II)",
            "smarts": "[#6][Ch](=[N][Oh0])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 90,
            "name": "Aldoxime anions [N][O-]",
            "smarts": "[#6][Ch]=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 91,
            "name": "Aldoxime anions [N][O][Me]",
            "smarts": "[#6][Ch]=[N][O][Na,K,Li,Cu,Mg,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 92,
            "name": "Alkenyl bromide",
            "smarts": "[C]=[C][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 93,
            "name": "Alkenyl chloride",
            "smarts": "[C]=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 94,
            "name": "Alkenyl halide, mesylate, tosylate",
            "smarts": "[C]=[C][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 95,
            "name": "Alkenyl iodide",
            "smarts": "[C]=[C][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 96,
            "name": "Alkenyl sulfonate",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 97,
            "name": "Alkenyl triflate",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 98,
            "name": "Alkyl bromide (primary)",
            "smarts": "[CX4H2][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 99,
            "name": "Alkyl bromide (secondary)",
            "smarts": "[CX4H1][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 100,
            "name": "Alkyl bromide (tertiary)",
            "smarts": "[CX4H0][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 101,
            "name": "Alkyl chloride (primary)",
            "smarts": "[CX4H2][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 102,
            "name": "Alkyl chloride (secondary)",
            "smarts": "[CX4H1][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 103,
            "name": "Alkyl chloride (tertiary)",
            "smarts": "[CX4H0][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 104,
            "name": "Alkyl iodide (primary)",
            "smarts": "[CX4H2][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 105,
            "name": "Alkyl iodide (secondary)",
            "smarts": "[CX4H1][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 106,
            "name": "Alkyl iodide (tertiary)",
            "smarts": "[CX4H0][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 107,
            "name": "alkyl sulfinate [#6][Sv4](=[O])[O]",
            "smarts": "[#6][Sv4](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 108,
            "name": "Alkyl sulfonate (primary)",
            "smarts": "[CX4H2][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 109,
            "name": "Alkyl sulfonate (secondary)",
            "smarts": "[CX4H1][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 110,
            "name": "Alkyl sulfonate (tertiary)",
            "smarts": "[CX4H0][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 111,
            "name": "Alkyne (terminal [C]#[Ch])",
            "smarts": "[C]#[Ch]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 112,
            "name": "Alkyne (triple bond C#C)",
            "smarts": "[C]#[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 113,
            "name": "Alkyne (triple bond C#C) small cycles",
            "smarts": "[C;r3,r4,r5,r6]#[C;r3,r4,r5,r6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 114,
            "name": "Alkyne activated",
            "smarts": "[C]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 115,
            "name": "Alkyne Metallorganic C#C[Me] (type I)",
            "smarts": "[C]#[C][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 116,
            "name": "Alkyne Metallorganic C#C[Me] (type II)",
            "smarts": "[C]#[C][Cu,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 117,
            "name": "Amide [Nh]",
            "smarts": "[CX3z2](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 118,
            "name": "Amide [Nh0]",
            "smarts": "[CX3z2](=[O])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 119,
            "name": "Amide anion (Activated [N-])",
            "smarts": "[CX3z2](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 120,
            "name": "Amide anion (Activated N-Me bond)",
            "smarts": "[CX3z2](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 121,
            "name": "Amidine [#6]C(=N)[N-] (activated)",
            "smarts": "[#6][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 122,
            "name": "Amidine [#6]C(=N)[N][Me] (activated)",
            "smarts": "[#6][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 123,
            "name": "Amidine [#6]C(=N)[Nh]",
            "smarts": "[#6][C!R](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 124,
            "name": "Amidine [#6]C(=N)[Nh] cyclic",
            "smarts": "[#6][CR](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 125,
            "name": "Aminal non-cyclic [Nh][CX4][Nh]",
            "smarts": "[N&h&R0&$(*[CX4][#7])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 126,
            "name": "Amine aliphatic (primary) C-NH2",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 127,
            "name": "Amine aliphatic (secondary) C-NH-C",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H1][C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 128,
            "name": "Amine aliphatic (tertiary) C-N(-C)-C",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H0]([C;X4&!$(*=[C,N,O,S])])[C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 129,
            "name": "Amine anion [#6][N-]",
            "smarts": "[#6;!$(*=[O,S,N])][N;!$(*[!#6])&!$(*[C]=[O,S,N])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 130,
            "name": "Amine anion [#6][N-][Me]",
            "smarts": "[#6;!$(*=[O,S,N])][N;z1&!$(*[C]=[O,S,N])&+0][Li,Na,K,Cu,Mg,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 131,
            "name": "Amine aromatic (primary) c-NH2",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 132,
            "name": "Amine aromatic (primary) c-NH2 (tautomeric form)",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 133,
            "name": "Amine aromatic (secondary, aliphatic) c-NH-[C]",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 134,
            "name": "Amine aromatic (secondary, aliphatic) c-NH-[C] (tautomeric form)",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 135,
            "name": "Amine aromatic (secondary, aromatic) c-NH-c",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 136,
            "name": "Amine aromatic (secondary, aromatic) c-NH-c (tautomeric form)",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 137,
            "name": "Amine aromatic (tertiary) c-N(-[#6])-[#6]",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])])[#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 138,
            "name": "Amine oxide",
            "smarts": "[NX4z+1][Oz-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 139,
            "name": "Amine poor electronic (primary) c-NH2",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 140,
            "name": "Amine poor electronic (primary) c-NH2 (tautomeric form)",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 141,
            "name": "Amine poor electronic (secondary, aliphatic) c-NH-[C]",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 142,
            "name": "Amine poor electronic (secondary, aliphatic) c-NH-[C] (tautomeric form)",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 143,
            "name": "Amine poor electronic (secondary, aromatic) c-NH-[c,CX3]",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 144,
            "name": "Amine poor electronic (secondary, aromatic) c-NH-[c,CX3] (tautomeric form)",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 145,
            "name": "Amine poor electronic (secondary, poor) c-NH-c",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 146,
            "name": "Amine poor electronic (secondary, poor) c-NH-c (tautomeric form)",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 147,
            "name": "Amine poor electronic (tertinary) c-N(-[#6])-[#6]",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6!$(*=[O,S,N])])[#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 148,
            "name": "Aminoacetal and aminoketal N-[CX4]-O",
            "smarts": "[#6][NH0]([#6])-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 149,
            "name": "Ammonium Salts [N+] (alkyl)",
            "smarts": "[CX4][N+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 150,
            "name": "Ammonium Salts [Nh+]",
            "smarts": "[#6!$(*=[O,S,N])][Nh+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 151,
            "name": "Anhydride (mixed) C(=O)O[N,S](=O) type I",
            "smarts": "[#6][C](=[O])[O][S,N](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 152,
            "name": "Anhydride (mixed) C(=O)O[P](=O) type II",
            "smarts": "[#6][C](=[O])[O][P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 153,
            "name": "Anhydride C(=O)OC(=O)",
            "smarts": "[#6][C](=[O])[O][C!$(*[CH3])](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 154,
            "name": "Arenes [ch] (meta-EDG) Type I",
            "smarts": "[ch]:1:[c]:[c$(*[OH0,N!$(*=O),SX2])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 155,
            "name": "Arenes [ch] (meta-EDG) Type II",
            "smarts": "[ch]:1:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 156,
            "name": "Arenes [ch] (meta-EDG) Type III",
            "smarts": "[ch]:1:[c]:[c$(*[O;+0H1,-1H0])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 157,
            "name": "Arenes [ch] (meta-EDG) Type IV",
            "smarts": "[ch]:1:[c]:[c$(*(a)(a)a)]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 158,
            "name": "Arenes [ch] (meta-EDG) Type V",
            "smarts": "[ch]:1:[c]:[c$(*[CX4])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 159,
            "name": "Arenes [ch] (meta-EWG)",
            "smarts": "[ch]:1:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 160,
            "name": "Arenes [ch] (ortho-EDG) Type I",
            "smarts": "[cr6h]:[c$(*[OX2H0z0])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 161,
            "name": "Arenes [ch] (ortho-EDG) Type II",
            "smarts": "[cr6h]:[c$(*[F,Cl,Br,I])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 162,
            "name": "Arenes [ch] (ortho-EDG) Type III",
            "smarts": "[cr6h]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 163,
            "name": "Arenes [ch] (ortho-EDG) Type IV",
            "smarts": "[cr6h]:[c$(*(a)(a)a)]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 164,
            "name": "Arenes [ch] (ortho-EDG) Type V",
            "smarts": "[cr6h]:[c;$(*[CX4z0]),$(*[CX4z1][O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 165,
            "name": "Arenes [ch] (ortho-EDG) Type VI",
            "smarts": "[cr6h]:[c$(*[NX3!$(*=O),SX2])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 166,
            "name": "Arenes [ch] (ortho-EWG)",
            "smarts": "[cr6h]:[c$(*[N$(*=O),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 167,
            "name": "Arenes [ch] (ortho-EWG) Type II",
            "smarts": "[cr6h]:[c$(*[C]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 168,
            "name": "Arenes [ch] (para-EDG) Type I",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[OX2H0z0,N!$(*=O),SX2])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 169,
            "name": "Arenes [ch] (para-EDG) Type II",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 170,
            "name": "Arenes [ch] (para-EDG) Type III",
            "smarts": "[ch]:1:[c]:[c]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 171,
            "name": "Arenes [ch] (para-EDG) Type IV",
            "smarts": "[ch]:1:[c]:[c]:[c$(*(a)(a)a)]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 172,
            "name": "Arenes [ch] (para-EDG) Type V",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[CX4])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 173,
            "name": "Arenes [ch] (para-EWG)",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 174,
            "name": "Arenes [ch] 5-memb 2nd pos 2 rings",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[a!$([nX2])]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 175,
            "name": "Benzoimidazole [ch] 5-memb",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[nX2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 176,
            "name": "Arenes activated [c-]",
            "smarts": "[c-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 177,
            "name": "Arenes activated metallorganic [c][Me] (type I)",
            "smarts": "[c][Li,Mg,Na,K]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 178,
            "name": "Arenes activated metallorganic [c][Me] (type II)",
            "smarts": "[c][Sn,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 179,
            "name": "Aryl bromide",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 180,
            "name": "5-bromo pyrimidine",
            "smarts": "[cr6$(*1cncnc1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 181,
            "name": "Aryl carboxylic group [c]COOH",
            "smarts": "[c][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 182,
            "name": "Aryl chloride",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 183,
            "name": "Aryl fluoride",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 184,
            "name": "Aryl halide and sulfanate",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 185,
            "name": "Aryl iodide",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 186,
            "name": "Aryl sulfonate",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 187,
            "name": "Aryl triflate",
            "smarts": "[cr6!$(*[n])&!$(*1aanaa1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 188,
            "name": "Azide [C,c][N3]",
            "smarts": "[#6][N]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 189,
            "name": "Azole (thiazole, oxazole, imidazole and other) [n:]",
            "smarts": "[n,s,o]:1:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 190,
            "name": "Benzofuran [ch] 3rd pos",
            "smarts": "[ch]:1:[a]:[o]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 191,
            "name": "Benzothiophene [ch] 3rd pos",
            "smarts": "[ch]:1:[a]:[s]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 192,
            "name": "Benzoyl O,N ([O,N]Bz)",
            "smarts": "[#6,#7,#8][O,#7][C](=[O])[c]:1:[cH1]:[cH1]:[cH1]:[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 193,
            "name": "Benzyl O,N ([O,N]Bn)",
            "smarts": "[#6,#7,#8][O,#7][CX4H2][c]:1:[c;H1,$(*OC)]:c:[c;H1,$(*OC),$(*[F,Cl,Br])]:c:[c;H1,$(*OC)]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 194,
            "name": "Boc-protection",
            "smarts": "[#7][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 195,
            "name": "Boc-protection [Nh]",
            "smarts": "[Nh][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 196,
            "name": "Boron acid",
            "smarts": "[#6][B]([Oh])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 197,
            "name": "Boron derivates",
            "smarts": "[#6][BH0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 198,
            "name": "Boron derivates [Bh]",
            "smarts": "[#6][Bh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 199,
            "name": "Boron pinocolate",
            "smarts": "[#6][B]1[O][C](C)(C)[C](C)(C)[O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 200,
            "name": "C-enamine C=C[N] cyclic",
            "smarts": "[C]=[C;r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 201,
            "name": "C-enamine C=C[N] non-cyclic",
            "smarts": "[C]=[C!r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 202,
            "name": "C-Halogenanhydride [C](=[O])[Hal]",
            "smarts": "[C](=[O])[Br,Cl,I,F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 203,
            "name": "C-nitro derivatives",
            "smarts": "[C]=[N+]([O-])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 204,
            "name": "C-O activated",
            "smarts": "[CX4][O+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 205,
            "name": "Carbamate  [O][C](=[O])[Nh0]",
            "smarts": "[OH0][C](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 206,
            "name": "Carbamate [O][C](=[O])[Nh]",
            "smarts": "[OH0][C](=[O])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 207,
            "name": "Carbamate anion (Activated [N-])",
            "smarts": "[O!$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 208,
            "name": "Carbamate anion (Activated [N][Me])",
            "smarts": "[O][C](=[O])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 209,
            "name": "Carbamate Boc anion (Activated [N-])",
            "smarts": "[O$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 210,
            "name": "Carbocation [C+]",
            "smarts": "[C;X3&+1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 211,
            "name": "Carbodiimide",
            "smarts": "[#6][N]=[C]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 212,
            "name": "Carbonate (4-nitrophenyl) [O][C](=[O])O[C6H4][NO2]",
            "smarts": "[#6][O][CX3](=[O])[O]c1ccc([N+1]([O-])=[O])cc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 213,
            "name": "Carbonate (vinyl) [O][C](=[O])O[CH1]=[CH2]",
            "smarts": "[#6][O][CX3](=[O])[O][CH1]=[CH2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 214,
            "name": "Carbonate and thiocarbonate [O,S][C](=[O,S])[O,S]",
            "smarts": "[#8,#16][#6](=[O,S])[#8,#16]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 215,
            "name": "Carboxylate [C][C](=[O])[O-]",
            "smarts": "[#6,#7][C](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 216,
            "name": "Carboxylate [C][C](=[O])[O][Me]",
            "smarts": "[#6,#7][C](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 217,
            "name": "Carboxylic acid [C](=[O])[Oh]",
            "smarts": "[CX3z2](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 218,
            "name": "Carboxylic ester (ethyl) COOEt",
            "smarts": "[CX3z2](=[O])[O][CH2][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 219,
            "name": "Carboxylic ester (methyl) COOCH3",
            "smarts": "[CX3z2&$(*[#6&+0])&!$(*[CX3]=[CX3][O][Na,K,Li,Mg,Zn])&!$(*[CX3]=[CX3][O-1])](=[O])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 220,
            "name": "Carboxylic ester COOR (ordinary)",
            "smarts": "[CX3z2](=[O])[O;!$(*[CH2][CH3])&!$(*[CH3])][#6;!$(*=[O,S,N])&!$(*([#6])([#6])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 221,
            "name": "Carboxylic ester COOR (tert-butyl)",
            "smarts": "[CX3z2](=[O])[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 222,
            "name": "Di-carbonyl derivatives (type I) Malonic derivatives",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 223,
            "name": "Di-carbonyl derivatives (type I) Malonic derivatives (activated)",
            "smarts": "[C,S,N,P](=[O])[C;X3&-1][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 224,
            "name": "Di-carbonyl derivatives (type II) Malonic derivatives",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 225,
            "name": "Di-nitrile derivatives (Malonic derivatives)",
            "smarts": "[C](#[N])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 226,
            "name": "Diazirine",
            "smarts": "[CX4]1[N]=[N]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 227,
            "name": "Diazo compound (type I, aliphatic)",
            "smarts": "[C][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 228,
            "name": "Diazo compound (type I, aromatic)",
            "smarts": "[c][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 229,
            "name": "Diazo compounds",
            "smarts": "[C]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 230,
            "name": "Diazo compounds (type II) (diazene or diimide or diimine)",
            "smarts": "[#6][N]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 231,
            "name": "Diazo compounds anion (type III)",
            "smarts": "[C-]-[N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 232,
            "name": "Dimethylacetale protecting group",
            "smarts": "[CX4z2]([O][CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 233,
            "name": "Dioxalane",
            "smarts": "[CX4]1[O][CH2][O][CX4]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 234,
            "name": "Disulfide activated S-[S-]",
            "smarts": "[Sv2][Sv2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 235,
            "name": "Disulfide activated S-[S][Me]",
            "smarts": "[Sv2][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 236,
            "name": "Disulfide S-[Sh]",
            "smarts": "[Sv2][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 237,
            "name": "Dithiane S-[Ch]-S",
            "smarts": "[S][C;X4&h][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 238,
            "name": "Double bond",
            "smarts": "[CX3!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]=[CX3!$(*(=[CX3][a])[a])&!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 239,
            "name": "Double bond (allen)",
            "smarts": "[C]=[C]=[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 240,
            "name": "Double bond (isolated)",
            "smarts": "[a][CX3]=[CX3][a]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 241,
            "name": "Enamine C=C-[Nh]",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 242,
            "name": "Enamine C=C-[Nh] (conjugated)",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 243,
            "name": "Enamine C=C-[Nh] Acylated",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3h$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 244,
            "name": "Enamine C=C-[NH0]",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 245,
            "name": "Enamine C=C-[NH0] (conjugated)",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 246,
            "name": "Enamine C=C-[NH0] Acylated",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3H0$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 247,
            "name": "Enamine C=C[N-]",
            "smarts": "[C]=[C][NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 248,
            "name": "Enamine C=C[N][Me]",
            "smarts": "[C]=[C][NX3][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 249,
            "name": "Enol C=C-[Oh] (conjugated)",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 250,
            "name": "Enol C=C-[Oh] (non-conjugated)",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 251,
            "name": "Enol silyl ether C=C[O][Si]",
            "smarts": "[CX3]=[CX3][O][#14]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 252,
            "name": "Enolate C=C[O-]",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 253,
            "name": "Enolate C=C[O-] (conjugated)",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 254,
            "name": "Enolate C=C[O][Me]",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 255,
            "name": "Enolate C=C[O][Me] (conjugated)",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 256,
            "name": "Epoxide",
            "smarts": "[CX4]1[CX4][O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 257,
            "name": "Ether",
            "smarts": "[C;X4&!$(*=[O,S,N])&!$(*([O])[O,S,N])][O][#6;!$(*=[O,S,N])&!$(*([O])[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 258,
            "name": "Ether (di-phenyl)",
            "smarts": "[c!$(*=[O,S,N])][O][c!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 259,
            "name": "EWG aryl ortho- (tosylate,mesylate and so on)",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 260,
            "name": "EWG aryl ortho- bromide",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 261,
            "name": "EWG aryl ortho- chloride",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 262,
            "name": "EWG aryl ortho- fluoride",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 263,
            "name": "EWG aryl ortho- iodide",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 264,
            "name": "EWG aryl ortho- triflate",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 265,
            "name": "EWG aryl para-  (tosylate,mesylate and so on)",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 266,
            "name": "EWG aryl para- bromide",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 267,
            "name": "EWG aryl para- chloride",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 268,
            "name": "EWG aryl para- fluoride",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 269,
            "name": "EWG aryl para- iodide",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 270,
            "name": "EWG aryl para- triflate",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 271,
            "name": "Fluorene [Ch]",
            "smarts": "[Ch]1[c][c][c][c]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 272,
            "name": "Fmoc group",
            "smarts": "c:1:c:c:c2:c(:c:1)C(c:3:c2:c:c:c:c:3)COC(=O)[#7;X3&!$(*=[O])][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 273,
            "name": "Formic acid amide [Ch]=[O]",
            "smarts": "[#7][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 274,
            "name": "Formic acid ester [Ch]=O",
            "smarts": "[O][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 275,
            "name": "Fukuyama-Mitsunobu intermediate",
            "smarts": "[CX4][O+]=[P]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 276,
            "name": "Furan",
            "smarts": "o:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 277,
            "name": "Furan [ch]  2nd pos",
            "smarts": "[ch]:1:[o]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 278,
            "name": "Furan [ch]  3rd pos",
            "smarts": "[ch]:1:[a]:[o]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 279,
            "name": "Guanidine (=Nh)",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](-[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 280,
            "name": "Guanidine (=Nh) deactivated",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](-[NX3])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 281,
            "name": "Guanidine NC(=N)[N-] activated",
            "smarts": "[N][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 282,
            "name": "Guanidine NC(=N)[N][Me] activated",
            "smarts": "[N][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 283,
            "name": "Guanidine NC(=N)[Nh]",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](=[N])[NX3h!$(*([C]=[N])[C,S,N]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 284,
            "name": "Guanidine NC(=N)[Nh] deactivated",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](=[N])[NX3h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 285,
            "name": "Hemiaminal non-cyclic [N][CX4][Oh]",
            "smarts": "[OH1][CX4][#7!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 286,
            "name": "Hemiaminal non-cyclic [Nh][CX4][O]",
            "smarts": "[N&h&R0&$(*[CX4][O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 287,
            "name": "Hydrazide from aldehyde  [C][C](=[N][Nh0])[C] (type II)",
            "smarts": "[#6][Ch](=[N][Nh0$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 288,
            "name": "Hydrazide from aldehyde  [C][Ch](=[N][Nh]) (type I)",
            "smarts": "[#6][Ch](=[N][Nh$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 289,
            "name": "Hydrazide from ketone  [C][C](=[N][Nh])[C] (type I)",
            "smarts": "[#6][C](=[N][Nh$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 290,
            "name": "Hydrazide from ketone  [C][C](=[N][Nh0])[C] (type II)",
            "smarts": "[#6][C](=[N][Nh0$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 291,
            "name": "Hydrazine, hydrazide and hydrazone [N][Nh]",
            "smarts": "[NX3!$(*=[O])][NX3h!$(*=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 292,
            "name": "Hydrazone from aldehyde  [C][C](=[N][Nh0]) (type II)",
            "smarts": "[#6][Ch](=[N][Nh0!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 293,
            "name": "Hydrazone from aldehyde  [C][Ch](=[N][Nh]) (type I)",
            "smarts": "[#6][Ch](=[N][Nh!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 294,
            "name": "Hydrazone from ketone  [C][C](=[N][Nh])[C] (type I)",
            "smarts": "[#6][C](=[N][Nh!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 295,
            "name": "Hydrazone from ketone  [C][C](=[N][Nh0])[C] (type II)",
            "smarts": "[#6][C](=[N][Nh0!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 296,
            "name": "Hydroxamic acid C(=O)[N][Oh]",
            "smarts": "[#6][C](=[O])[N][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 297,
            "name": "Hydroxamic acid C(=O)[Nh][O]",
            "smarts": "[#6][C](=[O])[Nh][O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 298,
            "name": "Hydroxylamine [N][Oh]",
            "smarts": "[#7;X3&!$(*[C]=[O])&!$(*=[O])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 299,
            "name": "Hydroxylamine [Nh][O]",
            "smarts": "[#7h;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 300,
            "name": "Hydroxylamine [Nh0][Oh0]",
            "smarts": "[#7h0;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 301,
            "name": "Hydroxylamine anions [N][O-]",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 302,
            "name": "Hydroxylamine anions [N][O][Me]",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 303,
            "name": "Imidate [#6][C](=[N][C])[O][C]",
            "smarts": "[#6][C](=[NH0][#6])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 304,
            "name": "Imidazole [ch] 4th pos",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 305,
            "name": "Imidazole [ch] 5th pos",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 306,
            "name": "Imidazole [nh]",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:c:n:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 307,
            "name": "Imidazolium",
            "smarts": "[n;$(*-[#6])&+1]:1:[ch]:[n$(*[C])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 308,
            "name": "Imide anion (Activated [N-])",
            "smarts": "[#6][C](=[O])[N-][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 309,
            "name": "Imide C(=O)[Nh]C(=O)",
            "smarts": "[C](=[O])[Nh][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 310,
            "name": "Imine [#6][C](=[N][#6])[#6] (ketone)",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 311,
            "name": "Imine [#6][Ch](=[N][#6]) (aldehyde)",
            "smarts": "[#6][Ch](=[N][#6,S])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 312,
            "name": "Imine, oxyme [#6][C](=[N])[#6] (ketone)",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 313,
            "name": "Imine, oxyme [#6][C](=[N+])[#6] activated (ketone)",
            "smarts": "[#6][C](=[N+][#6,S,O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 314,
            "name": "Imine, oxyme [#6][C]=[N] (aldehyde)",
            "smarts": "[#6][Ch]=[N][#6,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 315,
            "name": "Imine, oxyme [#6][C]=[N+] activated (aldehyde)",
            "smarts": "[#6][Ch]=[N+][#6,S,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 316,
            "name": "Indole",
            "smarts": "n:1:[cR2]:[cR2]:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 317,
            "name": "Indole [ch] 3rd pos",
            "smarts": "[ch]:1:[a]:[nX3]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 318,
            "name": "Isocyanate and Isothiocyanate R-N=C=O,S",
            "smarts": "[N$(*([#6])=[C])]=[C]=[O,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 319,
            "name": "Isocyanide (Isonitrile) R-[N+]#[C-]",
            "smarts": "[N+1&$(*([#6])#[C])]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 320,
            "name": "Ketene [C]=[C]=[O]",
            "smarts": "[C]=[C]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 321,
            "name": "Ketone [C]=[O]",
            "smarts": "[#6!$(*[Na,K,Li,Mg,Zn,Sn])][C!$([C;r5,r6](=[O])([c])[c])](=[O])[#6!$(*[Na,K,Li,Mg,Zn,Sn])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 322,
            "name": "Anthraquinone [C]=[O]",
            "smarts": "[c][C;r5,r6](=[O])[c]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 323,
            "name": "Ketone [C]=[O] and H2O",
            "smarts": "[#6][CX4]([OH1])([OH1])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 324,
            "name": "Ketoxime  [#6][C](=[N][Oh])[#6] (type I)",
            "smarts": "[#6][C](=[N][Oh])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 325,
            "name": "Ketoxime  [#6][C](=[N][Oh0])[#6] (type II)",
            "smarts": "[#6][C](=[N][Oh0])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 326,
            "name": "Ketoxime anions [N][O-]",
            "smarts": "[#6][C]([#6])=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 327,
            "name": "Ketoxime anions [N][O][Me]",
            "smarts": "[#6][C]([#6])=[N][O][Na,K,Mg,Li,Cu,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 328,
            "name": "Metallorganic aliphatic (type I)",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 329,
            "name": "Metallorganic aliphatic (type II)",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 330,
            "name": "Metallorganic alkene (type I)",
            "smarts": "[CX3]=[CX3][Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 331,
            "name": "Metallorganic alkene (type II)",
            "smarts": "[CX3]=[CX3][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 332,
            "name": "Metallorganic sp2 (lithium and magnesium)",
            "smarts": "[CX3,c][Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 333,
            "name": "Michael acceptor [C,N,S](=[O])[C]#[C][C,N,S]=[O] (type VIII)",
            "smarts": "[C,N,S](=[O])[C]#[C][C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 334,
            "name": "Michael acceptor [C]#[C][C;X3&!$(*[!#6])](=[O]) (type X)",
            "smarts": "[C!$(*[O,N])]#[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 335,
            "name": "Michael acceptor [C]#[C][C](=[O,N,S])[O,N,S] (type IX) ",
            "smarts": "[C!$(*[O,N])]#[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 336,
            "name": "Michael acceptor [C]=[C]([C,N,S]=[O])[C,N,S]=[O] (type VI)",
            "smarts": "[C!$(*[O,N])]=[C]([C,N,S]=[O])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 337,
            "name": "Michael acceptor [C]=[C]([C]#[N])[C,N,S]=[O] (type VII)",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 338,
            "name": "Michael acceptor [C]=[C]([C]#[N])[C]#[N] (type III)",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 339,
            "name": "Michael acceptor [C]=[C][C;X3&!$(*[!#6])](=[O]) (type II)",
            "smarts": "[C!$(*[O,N])]=[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 340,
            "name": "Michael acceptor [C]=[C][C](=[O,N,S])[O,N,S] (type I) ",
            "smarts": "[C!$(*[O,N])]=[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 341,
            "name": "Michael acceptor [C]=[C][C]#[N] (type IV)",
            "smarts": "[C!$(*[O,N])]=[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 342,
            "name": "Michael acceptor [C]=[C][N,S,P]=[O,N] (type V)",
            "smarts": "[C!$(*[O,N])]=[C][N,S,P]=[O,N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 343,
            "name": "MOM protecting group",
            "smarts": "[#6!$(*=[O,S,N])][O][CH2][O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 344,
            "name": "Nitrile C#N (aliphatic)",
            "smarts": "[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 345,
            "name": "Nitrile C#N (aromatic)",
            "smarts": "[c][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 346,
            "name": "Nitrile oxide",
            "smarts": "[C]#[N+][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 347,
            "name": "Nitro compounds",
            "smarts": "[#6][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 348,
            "name": "Nitroso derivatives",
            "smarts": "[#6h0][NX2]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 349,
            "name": "o-Alkyl pyridine (PyCH)",
            "smarts": "[C;X4&h][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 350,
            "name": "o-Alkyl pyridine anione Py[C-]",
            "smarts": "[C;X3&-1][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 351,
            "name": "o-Alkyl pyridine anione Py[C][Me]",
            "smarts": "[Li,K,Na,Mg][C;X4][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 352,
            "name": "O-Tetrahydropyrane protection (OTHP)",
            "smarts": "[Ch2]1[O][Ch]([O,#7][#6])[Ch2][Ch2][Ch2]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 353,
            "name": "p-Alkyl pyridine (PyCH)",
            "smarts": "[C;X4&h][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 354,
            "name": "p-Alkyl pyridine anione Py[C-]",
            "smarts": "[C;X3&-1][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 355,
            "name": "p-Alkyl pyridine anione Py[C][Me]",
            "smarts": "[Li,K,Na,Mg][CX4][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 356,
            "name": "P-anhydride [O]=[P][O][P]=[O]",
            "smarts": "[O]=[P][O][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 357,
            "name": "P-Halogenanhydride [P][Hal]",
            "smarts": "[P][Cl,Br,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 358,
            "name": "Peroxide [O][Oh]",
            "smarts": "[O][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 359,
            "name": "Peroxy anions [N,O][O][Me]",
            "smarts": "[O][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 360,
            "name": "Peroxy anions [O][O-]",
            "smarts": "[O][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 361,
            "name": "phenol c-[Oh]",
            "smarts": "[c;!$(*n)&!$(*:1:a:a:n:a:a:1)][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 362,
            "name": "phenolate c-[O-]",
            "smarts": "[c][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 363,
            "name": "phenolate c-[O][Me]",
            "smarts": "[c][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 364,
            "name": "Phenyldimethylsilane group (C)",
            "smarts": "[#6][#14]([CH3])([CH3])c1ccccc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 365,
            "name": "Phosphine and phosphane [#6]-P",
            "smarts": "[#6][P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 366,
            "name": "Phosphine and phosphane [Ch]",
            "smarts": "[P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 367,
            "name": "Phosphite, Phosphinite,Phosphonite [O]-P",
            "smarts": "[O][P;X3&!$(*([!#6,!O])[!#6,!O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 368,
            "name": "Phosphonate anion",
            "smarts": "[P](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 369,
            "name": "Phosphonate anion [Me]",
            "smarts": "[P](=[O])[OH0][Na,K,Cu,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 370,
            "name": "Phosphonium salts [P+][C;X4&h] Wittig",
            "smarts": "[P+][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 371,
            "name": "Phosphoric acid",
            "smarts": "[P](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 372,
            "name": "PMB protecting group",
            "smarts": "[#6,#7,#8][O,#7][CH2][c]:1:[cH1]:[cH1]:[c]([O][CH3]):[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 373,
            "name": "PMB protecting group (common)",
            "smarts": "[#6,#7,#8][O,#7][C;R0&X4&h]c:1:c:c:[c]([O][C]):c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 374,
            "name": "Pyranone group",
            "smarts": "[O]=[c]1[c][c!$(*[O,N])][o][c!$(*[O,N])][c]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 375,
            "name": "Pyrazole [ch] 4th pos",
            "smarts": "[ch]:1:[!n]:[nX3]:[nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 376,
            "name": "Pyrazole [ch] 5th pos",
            "smarts": "[ch]:1:[nX3]:[nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 377,
            "name": "Pyrazole [n-] activated",
            "smarts": "[n;-1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 378,
            "name": "Pyrazole [nh]",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 379,
            "name": "Pyridine",
            "smarts": "[c,n]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 380,
            "name": "Pyridine oxide [n+1][O-]",
            "smarts": "[nr6&+1][O-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 381,
            "name": "Pyridinyl bromide (2-pos)",
            "smarts": "[c$(*1nacac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 382,
            "name": "Pyridinyl bromide (4-pos)",
            "smarts": "[c$(*1canac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 383,
            "name": "Pyridinyl chloride (2-pos)",
            "smarts": "[c$(*1nacac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 384,
            "name": "Pyridinyl chloride (4-pos)",
            "smarts": "[c$(*1canac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 385,
            "name": "Pyridinyl fluoride",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 386,
            "name": "Pyridinyl iodide (2-pos)",
            "smarts": "[c$(*1nacac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 387,
            "name": "Pyridinyl iodide (4-pos)",
            "smarts": "[c$(*1canac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 388,
            "name": "Pyridinyl sulfonate (tosylate,mesylate and so on)",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 389,
            "name": "Pyridinyl triflate",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 390,
            "name": "Pyridinyl triflate (2-pos)",
            "smarts": "[c$(*1nacac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 391,
            "name": "Pyridinyl triflate (4-pos)",
            "smarts": "[c$(*1canac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 392,
            "name": "Pyrimidyl alkyl sulfide (2-pos) [n][c]([S])[n]",
            "smarts": "[c$(*1nacan1)][SX2][CX4z1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 393,
            "name": "Pyrimidyl bromide (2-pos)",
            "smarts": "[c$(*1nacan1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 394,
            "name": "Pyrimidyl bromide (4-pos)",
            "smarts": "[c$(*1nanac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 395,
            "name": "Pyrimidyl chloride (2-pos)",
            "smarts": "[c$(*1nacan1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 396,
            "name": "Pyrimidyl chloride (4-pos)",
            "smarts": "[c$(*1nanac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 397,
            "name": "Pyrimidyl fluoride (2-pos)",
            "smarts": "[c$(*1nacan1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 398,
            "name": "Pyrimidyl fluoride (4-pos)",
            "smarts": "[c$(*1nanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 399,
            "name": "Pyrimidyl Iodide (2-pos)",
            "smarts": "[c$(*1nacan1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 400,
            "name": "Pyrimidyl Iodide (4-pos)",
            "smarts": "[c$(*1nanac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 401,
            "name": "Pyrimidyl sulfinate (tosylate,mesylate and so on) (2-pos)",
            "smarts": "[c;$(*1nacan1)][S](=[O])(=[O])[#6$([CX4z1,c])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 402,
            "name": "Pyrimidyl sulfonate (tosylate,mesylate and so on) (2-pos)",
            "smarts": "[c;$(*1nacan1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 403,
            "name": "Pyrimidyl sulfonate (tosylate,mesylate and so on) (4-pos)",
            "smarts": "[c;$(*1nanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 404,
            "name": "Pyrimidyl triflate (2-pos)",
            "smarts": "[c$(*1nacan1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 405,
            "name": "Pyrimidyl triflate (4-pos)",
            "smarts": "[c$(*1nanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 406,
            "name": "Pyrrole",
            "smarts": "[n!R2]:1:[c!R2]:[c!R2]:[c!R2]:[c!R2]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 407,
            "name": "Pyrrole [ch] 2nd pos",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 408,
            "name": "Pyrrole [ch] 3rd pos",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 409,
            "name": "Pyrrole, Imidazole, Indole and other [Activated n-]",
            "smarts": "[n;r5&!$(*[#6]=[O])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 410,
            "name": "Pyrrole, Imidazole, Indole and other [Activated n-Me bond]",
            "smarts": "[nr5!$(*[#6]=[O])][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 411,
            "name": "Pyrrole, Imidazole, Indole and other [nh]",
            "smarts": "[nr5h!$(*[#6]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 412,
            "name": "Rich electronic amine (primary) [!#6]-[NH2]",
            "smarts": "[NX3,OX2][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 413,
            "name": "Rich electronic amine (secondary) [!#6]-[NH1]-[#6]",
            "smarts": "[NX3,OX2][NX3;H1][#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 414,
            "name": "Rich electronic amine (tertiary) [!#6]-[NH0](-[#6])-[#6]",
            "smarts": "[NX3,OX2][NX3;H0]([#6!$(*=[C,N,O,S])])[#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 415,
            "name": "S-Halogenanhydride [S](=[O])[Hal]",
            "smarts": "[S!$(*(=[O])(=[O])[F])][F,Br,Cl,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 416,
            "name": "Selenols PhSeH",
            "smarts": "[c][Sev2&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 417,
            "name": "Semi acetale and ketale O-[CX4R0]-O",
            "smarts": "[#6][O][CX4R0][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 418,
            "name": "Semi Carbamate [N][C](=[O])[O]",
            "smarts": "[#7][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 419,
            "name": "Semi Carbonate [O][C](=[O])[O]",
            "smarts": "[#8][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 420,
            "name": "Silane [C][SiH](C)[(C)",
            "smarts": "[#6][#14;X4h]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 421,
            "name": "Silyl chloride [#14][Cl]",
            "smarts": "[#14][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 422,
            "name": "Silyl derivatives (C)",
            "smarts": "[#6][#14&!$(*c1ccccc1)](C)(C)C",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 423,
            "name": "Silyl derivatives (heteroatom)",
            "smarts": "[O,#7][#14!$(*([CH3])([CH3])[C]([CH3])([CH3])[CH3])&!$(*(c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3])&!$(*([CH3])([CH3])[CH3])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 424,
            "name": "Small Cycle (3-memb)",
            "smarts": "A1AA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 425,
            "name": "Small Cycle (4-memb)",
            "smarts": "A1AAA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 426,
            "name": "Sulfamates [O][S](=O)(=O)[N]",
            "smarts": "[OH0][S](=[O])(=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 427,
            "name": "Sulfamates [O][S](=O)(=O)[Nh]",
            "smarts": "[OH0][S](=[O])(=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 428,
            "name": "Sulfate [#6][S](=[O])[O-]",
            "smarts": "[#6,#7][S](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 429,
            "name": "Sulfate [#6][S](=[O])[O][Me]",
            "smarts": "[#6,#7][S](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 430,
            "name": "Sulfides",
            "smarts": "[#6;!$(*=[C,N,O,S])][Sv2][#6;!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 431,
            "name": "Sulfides [Ch]",
            "smarts": "[Sv2][C;X4&h&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 432,
            "name": "sulfinate [#6][Sv4](=[O])[O]",
            "smarts": "[#6][Sv4](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 433,
            "name": "Sulfonamide (Activated [N-])",
            "smarts": "[#6,#7][S](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 434,
            "name": "Sulfonamide (Activated N-Me bond)",
            "smarts": "[#6,#7][S](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 435,
            "name": "Sulfonamide [Nh]",
            "smarts": "[#6][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 436,
            "name": "Sulfonamide [Nh] type II",
            "smarts": "[#7][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 437,
            "name": "Sulfonamide [Nh0]",
            "smarts": "[#6,#7][S](=[O])[#7h0X3]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 438,
            "name": "Sulfone",
            "smarts": "[#6][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 439,
            "name": "Sulfonic anhydride",
            "smarts": "[#6][S](=[O])(=[O])[O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 440,
            "name": "Sulfonyl fluoride [S](=[O])[F]",
            "smarts": "[S](=[O])(=[O])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 441,
            "name": "Sulfoxide",
            "smarts": "[#6][SX3](=[O])-[#6,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 442,
            "name": "Sulfuric acid [#6][S](=[O])[Oh]",
            "smarts": "[#6,#7][S](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 443,
            "name": "Sulfuric acid ester [#6][S](=[O])[O][#6]",
            "smarts": "[#6,#7][S](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 444,
            "name": "tert-alcohol  HOC(C)(C)C",
            "smarts": "[OH1][C]([#6])([#6])[CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 445,
            "name": "tert-alkoxy ester OC(C)(C)C",
            "smarts": "[O][C]([#6z0])([#6z0])[#6z0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 446,
            "name": "tert-alkyl ester OC(C)(C)C",
            "smarts": "[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 447,
            "name": "tert-alkyl heteroatom [A]C(C)(C)C",
            "smarts": "[#7,S,Se,P,Si][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 448,
            "name": "tert-butyl amine, amide [N]tBu",
            "smarts": "[#7][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 449,
            "name": "tert-alkyl halide",
            "smarts": "[#6][C]([#6])([#6])[Cl,Br,I,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 450,
            "name": "tert-butoxy ester OtBu",
            "smarts": "[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 451,
            "name": "tert-Butyldimethylsilyl OTBDMS",
            "smarts": "[O,#7,S][#14]([CH3])([CH3])[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 452,
            "name": "tert-Butyldiphenylsilyl OTBDPS",
            "smarts": "[O,#7,S][#14](c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 453,
            "name": "Thiazolium",
            "smarts": "[n;$(*[#6])&+1]:1:[ch]:[s]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 454,
            "name": "Thio- and oxazole (1,2-)",
            "smarts": "[o,s]:1:[n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 455,
            "name": "Thio- and oxazole [ch] (1,3-)",
            "smarts": "[o,s]:1:[ch]:[nh0]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 456,
            "name": "Thioamide",
            "smarts": "[N][CX3z2]=[S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 457,
            "name": "Thioamide (Activated [N-])",
            "smarts": "[CX3z2](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 458,
            "name": "Thioamide (Activated N-Me bond)",
            "smarts": "[CX3z2](=[S])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 459,
            "name": "Thioamide [Nh]",
            "smarts": "[CX3z2](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 460,
            "name": "Thioarbamate [O][C](=[S])[Nh]",
            "smarts": "[OH0][C](=[S])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 461,
            "name": "Thioarbamate anion (Activated [N][Me])",
            "smarts": "[O][C](=[S])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 462,
            "name": "Thiocarbamate  [O][C](=[S])[Nh0]",
            "smarts": "[OH0][C](=[S])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 463,
            "name": "Thiocarbamate anion (Activated [N-])",
            "smarts": "[O!$(*C(C)(C)C)][C](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 464,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate [C](=[O,S,N])[Sh]",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 465,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate activated [C](=[O,S,N])[S-]",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 466,
            "name": "thiocarbamate, thiocarbonate, thiocarboxylate activated [C](=[O,S,N])[S][Me]",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 467,
            "name": "Thiocarboxylic acid (type I) [#6][C](=[S])[Oh]",
            "smarts": "[#6][C](=[S])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 468,
            "name": "Thiocarboxylic acid (type II) [#6][C](=[O,S])[Sh]",
            "smarts": "[#6][C](=[O,S])[Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 469,
            "name": "Thiocarboxylic anion [C](=[O,S])[S-]",
            "smarts": "[#6,#7,#8][C](=[O,S])[S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 470,
            "name": "Thiocarboxylic anion [C](=[O,S])[S][Me]",
            "smarts": "[#6,#7,#8][C](=[O,S])[SX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 471,
            "name": "Thiocarboxylic anion [C](=[S])[O-] type II",
            "smarts": "[#6,#7,#8][C](=[S])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 472,
            "name": "Thiocarboxylic anion [C](=[S])[O][Me] type II",
            "smarts": "[#6,#7,#8][C](=[S])[OX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 473,
            "name": "Thioester (type I)",
            "smarts": "[#6][C](=[S])[O][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 474,
            "name": "Thioester (type II)",
            "smarts": "[#6][C](=[O])[S][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 475,
            "name": "thiol (mercaptane) C-[Sh]",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 476,
            "name": "thiolate C-[S-]",
            "smarts": "[C!$(*=[C,N,O,S])][SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 477,
            "name": "thiolate C-[S][Me]",
            "smarts": "[C!$(*=[C,N,O,S])][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 478,
            "name": "Thionocarbonate",
            "smarts": "[#6]OC(=S)O[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 479,
            "name": "Thiophene",
            "smarts": "s:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 480,
            "name": "Thiophene [ch] 2nd pos",
            "smarts": "[ch]:1:[s]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 481,
            "name": "Thiophene [ch] 3rd pos",
            "smarts": "[ch]:1:[a]:[s]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 482,
            "name": "thiophenol C-[Sh]",
            "smarts": "[c][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 483,
            "name": "thiophenolate C-[S-]",
            "smarts": "[c][S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 484,
            "name": "thiophenolate C-[S][Me]",
            "smarts": "[c][Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 485,
            "name": "Thiourea [N][C](=S)[Nh]",
            "smarts": "[#7][C](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 486,
            "name": "Thiourea [Nh0][C](=S)[Nh0]",
            "smarts": "[#7h0][C](=[S])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 487,
            "name": "Thiourea anion [N][C](=[O])[N-] (Activated [N-])",
            "smarts": "[#7][C](=[S])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 488,
            "name": "Thiourea anion [N][C](=[O])[N][Me] (Activated [N-])",
            "smarts": "[#7][C](=[S])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 489,
            "name": "Triethylsilyl OTES",
            "smarts": "[O][#14](CC)(CC)CC",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 490,
            "name": "Trimethylsilyl NTMS",
            "smarts": "[#7][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 491,
            "name": "Trimethylsilyl OTMS (aliphatic)",
            "smarts": "[C;X2,X3,X4H0][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 492,
            "name": "Trimethylsilyl OTMS (aromatic)",
            "smarts": "[c][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 493,
            "name": "Trimethylsilyl OTMS (sp3)",
            "smarts": "[CX4h][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 494,
            "name": "Trityl protection C(Ph)3",
            "smarts": "[#7,O]C(c:1:c:c:c:c:c:1)(c:2:c:c:c:c:c:2)c:3:c:c:c:c:c:3",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 495,
            "name": "Urea [N][C](=[O])[Nh]",
            "smarts": "[#7][#6](=[O])[#7h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 496,
            "name": "Urea [Nh0][C](=[O])[Nh0]",
            "smarts": "[#7h0][#6](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 497,
            "name": "Urea anion [N][C](=[O])[N-] (Activated [N-])",
            "smarts": "[#7][C](=[O])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 498,
            "name": "Urea anion [N][C](=[O])[N][Me] (Activated [N-])",
            "smarts": "[#7][C](=[O])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 499,
            "name": "Vilsmeier ion",
            "smarts": "[C][N+]([C])=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 500,
            "name": "Vinyl ethers",
            "smarts": "[CX3&!$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 501,
            "name": "Vinyl ethers (a-carbonyl)",
            "smarts": "[CX3&$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 502,
            "name": "Weinreb amide",
            "smarts": "[#6][C](=[O])[N]([CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 503,
            "name": "Ylide (N) [C-] (type I)",
            "smarts": "[O]=[C,N,S][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 504,
            "name": "Ylide (N) [C-] (type II)",
            "smarts": "[N]#[C][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 505,
            "name": "Ylide (N) [C][Me] (type I)",
            "smarts": "[O]=[C,N,S][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 506,
            "name": "Ylide (N) [C][Me] (type II)",
            "smarts": "[N]#[C][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 507,
            "name": "Ylide (P)",
            "smarts": "[C]=[P]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 508,
            "name": "Ylide (P) [C-]",
            "smarts": "[C-][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 509,
            "name": "Ylide (P) [C-] HWE",
            "smarts": "[C-][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 510,
            "name": "Ylide (P) [C][Me]",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 511,
            "name": "Ylide (P) [C][Me] HWE",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 512,
            "name": "Ylide (S)",
            "smarts": "[C]=[Sv4]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 513,
            "name": "Ylide (S) [C-]",
            "smarts": "[C-][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 514,
            "name": "Ylide (S) [C][Me]",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][CX4][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 515,
            "name": "Arenes [ch] (generic)",
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
