from frozendict import frozendict

from ..basic.functional_groups import FunctionalGroupClass
from ..basic.functional_groups import FunctionalGroups

FUNCTIONAL_GROUPS: tuple[frozendict[str, int | str | FunctionalGroupClass], ...] = (
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 0,
            "name": "Hetarene #25",
            "smarts": "[c]1[nH0][o][c](=[O])[nH1]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 1,
            "name": "Hetarene #26",
            "smarts": "[c]1[nH0][o][c](=[O])[nH0]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 2,
            "name": "(Het)aryl bromide #1",
            "smarts": "[c$(*1caa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 3,
            "name": "(Het)aryl bromide #2",
            "smarts": "[c$(*1naa[!c]1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 4,
            "name": "(Het)aryl chloride #1",
            "smarts": "[n][c]([n])[Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 5,
            "name": "(Het)aryl chloride #2",
            "smarts": "[c$(*1caa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 6,
            "name": "(Het)aryl chloride #3",
            "smarts": "[c$(*1naa[!c]1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 7,
            "name": "Aromatic (thio)amide #1",
            "smarts": "[c$(*n)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 8,
            "name": "(Het)aryl iodide #1",
            "smarts": "[c$(*1caa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 9,
            "name": "(Het)aryl iodide #2",
            "smarts": "[c$(*1naa[!c]1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 10,
            "name": "Nitro #1",
            "smarts": "[n][c]([n])[N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 11,
            "name": "(Het)aryl triflate #1",
            "smarts": "[c$(*1caa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 12,
            "name": "(Het)aryl triflate #2",
            "smarts": "[c$(*1naa[!c]1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 13,
            "name": "Aromatic (thio)amide #2",
            "smarts": "[O,S]=[c][n-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 14,
            "name": "Aromatic (thio)amide #4",
            "smarts": "[O,S]=[c][n][Li,K,Mg,Na,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 15,
            "name": "Aromatic (thio)amide #3",
            "smarts": "[O,S]=[c][nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 16,
            "name": "(Het)aryl bromide #3",
            "smarts": "[Br][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 17,
            "name": "(Het)aryl chloride #4",
            "smarts": "[Cl][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 18,
            "name": "(Het)aryl fluoride #1",
            "smarts": "[F][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 19,
            "name": "(Het)aryl iodide #3",
            "smarts": "[I][c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 20,
            "name": "Sulfonate #2",
            "smarts": "[O]([S](=[O])(=[O])[#6!$(*[F])])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 21,
            "name": "(Het)aryl triflate #3",
            "smarts": "[O]([S](=[O])(=[O])[#6]([F])([F])[F])[c]:1:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:[c$(*C#N),c$(*[C,S,P,N]=[O])]:a:a:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 22,
            "name": "(Het)aryl bromide #4",
            "smarts": "[c$(*1ca[!c]c1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 23,
            "name": "(Het)aryl chloride #5",
            "smarts": "[c$(*1ca[!c]c1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 24,
            "name": "(Het)aryl iodide #4",
            "smarts": "[c$(*1ca[!c]c1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 25,
            "name": "(Het)aryl triflate #4",
            "smarts": "[c$(*1ca[!c]c1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 26,
            "name": "(Het)aryl-(S,O)H #1",
            "smarts": "[c$(*:1:a:a:n:a:a:1)][Oh,Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 27,
            "name": "Hetarene #33",
            "smarts": "[c]1(=[O,S])aa[n-]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 28,
            "name": "Hetarene #34",
            "smarts": "[c]1(=[O,S])aa[n]([Li,K,Mg,Na,Zn])aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 29,
            "name": "Hetarene #35",
            "smarts": "[c]1(=[O,S])aa[nh]aa1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 30,
            "name": "Carbonyl #4",
            "smarts": "[Br][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 31,
            "name": "CH-anion #23",
            "smarts": "[C;X3&-1][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 32,
            "name": "CH-anion #12",
            "smarts": "[C;X3&-1][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 33,
            "name": "CH-anion #11",
            "smarts": "[C;X3&-1][C](=[O])[O;h,$(*[#6!$(*[C]=[O,S,N])])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 34,
            "name": "CH-anion #10",
            "smarts": "[C;X3&-1][C,S,N,P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 35,
            "name": "Dithiane #2",
            "smarts": "[S][C-;X3][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 36,
            "name": "CH-anion #9",
            "smarts": "[C;X3&-1][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 37,
            "name": "CH-anion #8",
            "smarts": "[C;X3&-1][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 38,
            "name": "Nitrile enolate #1",
            "smarts": "[C]=[C]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 39,
            "name": "CH-anion #7",
            "smarts": "[C;X3&-1][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 40,
            "name": "CH-anion #6",
            "smarts": "[C;X3&-1][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 41,
            "name": "CH-anion #5",
            "smarts": "[C;X3&-1][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 42,
            "name": "CH-anion #22",
            "smarts": "[C;X3&-1][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 43,
            "name": "CH-anion #21",
            "smarts": "[CX4$(*[C;X3&h]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 44,
            "name": "CH-anion #20",
            "smarts": "[CX4$(*[C](=[O])[#7])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 45,
            "name": "CH-anion #19",
            "smarts": "[CX4$(*[C](=[O])[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 46,
            "name": "CH-anion #18",
            "smarts": "[CX4$(*[C](=[O])[#6])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 47,
            "name": "CH-anion #17",
            "smarts": "[CX4$(*[C]#[N])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 48,
            "name": "CH-anion #16",
            "smarts": "[CX4$(*[N+](=[O])[O-])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 49,
            "name": "CH-anion #15",
            "smarts": "[CX4$(*[P]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 50,
            "name": "CH-anion #14",
            "smarts": "[CX4$(*[S]=[O])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 51,
            "name": "CH-anion #13",
            "smarts": "[CX4$(*[C](=[S])[#7,#8])][Li,Na,K,Mg,Cu,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 52,
            "name": "CH-acid #14",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C;X3&h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 53,
            "name": "CH-acid #13",
            "smarts": "[C]=[C][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 54,
            "name": "CH-acid #12",
            "smarts": "[C;X4&h][C](=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 55,
            "name": "CH-acid #11",
            "smarts": "[C;X4&h][#7;h0&+1&!$(*=O)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 56,
            "name": "CH-acid #10",
            "smarts": "[c][CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 57,
            "name": "CH-acid #9",
            "smarts": "[C;X4&h][C](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 58,
            "name": "CH-acid #8",
            "smarts": "[C;X4&h][C](=[O])[OH0][#6!$(*=[O,S,N,P])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 59,
            "name": "CH-acid #7",
            "smarts": "[C;X4&h][N]=[C;$(*[#6])&!$(*-[!#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 60,
            "name": "CH-acid #6",
            "smarts": "[CX4&h&!$(*[Na,K,Li,Mg,Zn])][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 61,
            "name": "CH-acid #5",
            "smarts": "[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 62,
            "name": "CH-acid #4",
            "smarts": "[C;X4&h][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 63,
            "name": "CH-acid #16",
            "smarts": "[C;X4&h][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 64,
            "name": "CH-acid #15",
            "smarts": "[C;X4&h][S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 65,
            "name": "CH-acid #3",
            "smarts": "[C;X4&h][C](=[S])[#7,#8]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 66,
            "name": "Carbonyl #2",
            "smarts": "[Cl][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 67,
            "name": "Carbonyl #5",
            "smarts": "[I][C;X4&h][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 68,
            "name": "Carbonyl #6",
            "smarts": "[N-1]=[N+1]=[CX3][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 69,
            "name": "Carboxyl(ate) #1",
            "smarts": "[C](#[N])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 70,
            "name": "Carboxyl(ate) #2",
            "smarts": "[C](=[O])[#6][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 71,
            "name": "Carbonyl #1",
            "smarts": "[C](=[O])[C;X4&h][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 72,
            "name": "Acetale and ketale #1",
            "smarts": "[#6][O]-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 73,
            "name": "Anhydride #1",
            "smarts": "[#6][C](=[O])[O][C](=[O])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 74,
            "name": "Alcohol #10",
            "smarts": "[C;X4&h][C;X4&!$(*[#7])&!$(*([O])[O])&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 75,
            "name": "Alcohol #9",
            "smarts": "[O]=[CX3][CX4h][CX4][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 76,
            "name": "Alcohol #1",
            "smarts": "[C;X4H2&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 77,
            "name": "Alcohol #3",
            "smarts": "[C;X4H1&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 78,
            "name": "Alcohol #6",
            "smarts": "[C;X4H0&!$(*=[C,N,O,S])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 79,
            "name": "Alcohol #4",
            "smarts": "[CX4][CX4H1]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 80,
            "name": "Alcohol #7",
            "smarts": "[CX4][CX4H0]([Oh])[c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 81,
            "name": "Alcohol #2",
            "smarts": "[CX4H2]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 82,
            "name": "Alcohol #5",
            "smarts": "[CX4H1]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 83,
            "name": "Alcohol #8",
            "smarts": "[CX4H0]([Oh])[CX4][c;r5,r6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 84,
            "name": "Alcoholate #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 85,
            "name": "Alcoholate #2",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 86,
            "name": "Geminal diol #1",
            "smarts": "[#6][CX4h][OH1][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 87,
            "name": "Carbonyl #3",
            "smarts": "[CX3z1h]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 88,
            "name": "Aldoxime #1",
            "smarts": "[#6][Ch](=[N][Oh])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 89,
            "name": "Aldoxime #2",
            "smarts": "[#6][Ch](=[N][Oh0])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 90,
            "name": "Aldoxime #3",
            "smarts": "[#6][Ch]=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 91,
            "name": "Aldoxime #4",
            "smarts": "[#6][Ch]=[N][O][Na,K,Li,Cu,Mg,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 92,
            "name": "Alkenyl bromide #1",
            "smarts": "[C]=[C][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 93,
            "name": "Alkenyl chloride #1",
            "smarts": "[C]=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 94,
            "name": "Alkenyl (pseudo)halide #1",
            "smarts": "[C]=[C][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 95,
            "name": "Alkenyl iodide #1",
            "smarts": "[C]=[C][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 96,
            "name": "Sulfonate #1",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 97,
            "name": "Alkenyl triflate #1",
            "smarts": "[C]=[C][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 98,
            "name": "Primary alkyl bromide #1",
            "smarts": "[CX4H2][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 99,
            "name": "Secondary alkyl bromide #1",
            "smarts": "[CX4H1][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 100,
            "name": "Tertiary alkyl bromide #1",
            "smarts": "[CX4H0][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 101,
            "name": "Primary alkyl chloride #1",
            "smarts": "[CX4H2][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 102,
            "name": "Secondary alkyl chloride #1",
            "smarts": "[CX4H1][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 103,
            "name": "Tertiary alkyl chloride #1",
            "smarts": "[CX4H0][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 104,
            "name": "Primary alkyl iodide #1",
            "smarts": "[CX4H2][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 105,
            "name": "Secondary alkyl iodide #1",
            "smarts": "[CX4H1][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 106,
            "name": "Tertiary alkyl iodide #1",
            "smarts": "[CX4H0][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 107,
            "name": "Sulfinate #1",
            "smarts": "[#6][Sv4](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 108,
            "name": "Sulfonate #4",
            "smarts": "[CX4H2][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 109,
            "name": "Sulfonate #8",
            "smarts": "[CX4H1][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 110,
            "name": "Sulfonate #9",
            "smarts": "[CX4H0][O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 111,
            "name": "Alkyne #1",
            "smarts": "[C]#[Ch]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 112,
            "name": "Alkyne #2",
            "smarts": "[C]#[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 113,
            "name": "Alkyne #6",
            "smarts": "[C;r3,r4,r5,r6]#[C;r3,r4,r5,r6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 114,
            "name": "Alkyne #3",
            "smarts": "[C]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 115,
            "name": "Alkyne #4",
            "smarts": "[C]#[C][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 116,
            "name": "Alkyne #5",
            "smarts": "[C]#[C][Cu,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 117,
            "name": "Amide #1",
            "smarts": "[CX3z2](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 118,
            "name": "Amide #2",
            "smarts": "[CX3z2](=[O])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 119,
            "name": "Amide #3",
            "smarts": "[CX3z2](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 120,
            "name": "Amide #4",
            "smarts": "[CX3z2](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 121,
            "name": "Amidine #1",
            "smarts": "[#6][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 122,
            "name": "Amidine #2",
            "smarts": "[#6][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 123,
            "name": "Amidine #3",
            "smarts": "[#6][C!R](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 124,
            "name": "Amidine #4",
            "smarts": "[#6][CR](=[N])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 125,
            "name": "(Hemi)aminal #1",
            "smarts": "[N&h&R0&$(*[CX4][#7])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 126,
            "name": "Primary amine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 127,
            "name": "Secondary amine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H1][C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 128,
            "name": "Tertiary alkylamine #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][NX3;H0]([C;X4&!$(*=[C,N,O,S])])[C;X4&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 129,
            "name": "Amine anion #1",
            "smarts": "[#6;!$(*=[O,S,N])][N;!$(*[!#6])&!$(*[C]=[O,S,N])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 130,
            "name": "Amine anion #2",
            "smarts": "[#6;!$(*=[O,S,N])][N;z1&!$(*[C]=[O,S,N])&+0][Li,Na,K,Cu,Mg,Zn,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 131,
            "name": "Amine #1",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 132,
            "name": "Amine #2",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 133,
            "name": "Amine #3",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 134,
            "name": "Amine #4",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 135,
            "name": "Amine #5",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 136,
            "name": "Amine #6",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 137,
            "name": "Amine #7",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])])[#6;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 138,
            "name": "Amine oxide #1",
            "smarts": "[NX4z+1][Oz-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 139,
            "name": "Amine #8",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 140,
            "name": "Amine #9",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 141,
            "name": "Amine #10",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 142,
            "name": "Amine #11",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][CX4]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 143,
            "name": "Amine #12",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 144,
            "name": "Amine #13",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O]),CX3$(*=[C]),CX2$(*#[N,C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 145,
            "name": "Amine #14",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H1][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 146,
            "name": "Amine #15",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)]=[NX2H0][c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 147,
            "name": "Amine #16",
            "smarts": "[c;$(*n),$(*1aanaa1),$(*c[C,N,S]=[O]),$(*1aaa([C,N,S]=[O])aa1)][NX3;H0]([#6!$(*=[O,S,N])])[#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 148,
            "name": "Aminoacetal and aminoketal #1",
            "smarts": "[#6][NH0]([#6])-[CX4](-[O][#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 149,
            "name": "Ammonium #1",
            "smarts": "[CX4][N+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 150,
            "name": "Ammonium #2",
            "smarts": "[#6!$(*=[O,S,N])][Nh+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 151,
            "name": "Anhydride #2",
            "smarts": "[#6][C](=[O])[O][S,N](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 152,
            "name": "Anhydride #3",
            "smarts": "[#6][C](=[O])[O][P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 153,
            "name": "Anhydride #4",
            "smarts": "[#6][C](=[O])[O][C!$(*[CH3])](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 154,
            "name": "Arene [ch] #1",
            "smarts": "[ch]:1:[c]:[c$(*[OH0,N!$(*=O),SX2])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 155,
            "name": "Arene [ch] #2",
            "smarts": "[ch]:1:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 156,
            "name": "Arene [ch] #3",
            "smarts": "[ch]:1:[c]:[c$(*[O;+0H1,-1H0])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 157,
            "name": "Arene [ch] #4",
            "smarts": "[ch]:1:[c]:[c$(*(a)(a)a)]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 158,
            "name": "Arene [ch] #5",
            "smarts": "[ch]:1:[c]:[c$(*[CX4])]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 159,
            "name": "Arene [ch] #6",
            "smarts": "[ch]:1:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 160,
            "name": "Arene [ch] #7",
            "smarts": "[cr6h]:[c$(*[OX2H0z0])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 161,
            "name": "Arene [ch] #8",
            "smarts": "[cr6h]:[c$(*[F,Cl,Br,I])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 162,
            "name": "Arene [ch] #9",
            "smarts": "[cr6h]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 163,
            "name": "Arene [ch] #10",
            "smarts": "[cr6h]:[c$(*(a)(a)a)]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 164,
            "name": "Arene [ch] #11",
            "smarts": "[cr6h]:[c;$(*[CX4z0]),$(*[CX4z1][O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 165,
            "name": "Arene [ch] #12",
            "smarts": "[cr6h]:[c$(*[NX3!$(*=O),SX2])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 166,
            "name": "Arene [ch] #13",
            "smarts": "[cr6h]:[c$(*[N$(*=O),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 167,
            "name": "Arene [ch] #14",
            "smarts": "[cr6h]:[c$(*[C]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 168,
            "name": "Arene [ch] #15",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[OX2H0z0,N!$(*=O),SX2])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 169,
            "name": "Arene [ch] #16",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[F,Cl,Br,I])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 170,
            "name": "Arene [ch] #17",
            "smarts": "[ch]:1:[c]:[c]:[c;$(*[O;+0H1,-1H0]),$(*[O][Na,K,Li,Mg,Cu,Zn])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 171,
            "name": "Arene [ch] #18",
            "smarts": "[ch]:1:[c]:[c]:[c$(*(a)(a)a)]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 172,
            "name": "Arene [ch] #19",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[CX4])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 173,
            "name": "Arene [ch] #20",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 174,
            "name": "Arene [ch] #21",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[a!$([nX2])]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 175,
            "name": "Hetarene #28",
            "smarts": "[ch]:1:[o,s,nX3]:[aR2]:[aR2]:[nX2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 176,
            "name": "Arene [c-] #1",
            "smarts": "[c-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 177,
            "name": "Arene [c-] #2",
            "smarts": "[c][Li,Mg,Na,K]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 178,
            "name": "Arene [c-] #3",
            "smarts": "[c][Sn,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 179,
            "name": "(Het)aryl bromide #5",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 180,
            "name": "(Het)aryl bromide #6",
            "smarts": "[cr6$(*1cncnc1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 181,
            "name": "Carboxyl(ate) #10",
            "smarts": "[c][C](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 182,
            "name": "(Het)aryl chloride #6",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 183,
            "name": "(Het)aryl fluoride #2",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 184,
            "name": "(Het)aryl (pseudo)halide #3",
            "smarts": "[c;!$(*n)&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I,Br,Cl,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 185,
            "name": "(Het)aryl iodide #5",
            "smarts": "[cr6;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 186,
            "name": "Sulfonate #3",
            "smarts": "[c;!$(*[n])&!$(*1aanaa1)&!$(*c[C,N,S]=[O])&!$(*1aac([C,N,S]=[O])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 187,
            "name": "(Het)aryl triflate #5",
            "smarts": "[cr6!$(*[n])&!$(*1aanaa1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 188,
            "name": "Azide #1",
            "smarts": "[#6][N]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 189,
            "name": "Hetarene #32",
            "smarts": "[n,s,o]:1:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 190,
            "name": "Hetarene #27",
            "smarts": "[ch]:1:[a]:[o]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 191,
            "name": "Hetarene #29",
            "smarts": "[ch]:1:[a]:[s]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 192,
            "name": "Bz-PG #1",
            "smarts": "[#6,#7,#8][O,#7][C](=[O])[c]:1:[cH1]:[cH1]:[cH1]:[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 193,
            "name": "Bn-PG #1",
            "smarts": "[#6,#7,#8][O,#7][CX4H2][c]:1:[c;H1,$(*OC)]:c:[c;H1,$(*OC),$(*[F,Cl,Br])]:c:[c;H1,$(*OC)]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 194,
            "name": "Boc-PG #2",
            "smarts": "[#7][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 195,
            "name": "Boc-PG #1",
            "smarts": "[Nh][C](=[O])[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 196,
            "name": "Boron #4",
            "smarts": "[#6][B]([Oh])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 197,
            "name": "Boron #3",
            "smarts": "[#6][BH0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 198,
            "name": "Boron #2",
            "smarts": "[#6][Bh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 199,
            "name": "Boron #1",
            "smarts": "[#6][B]1[O][C](C)(C)[C](C)(C)[O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 200,
            "name": "Enamine #9",
            "smarts": "[C]=[C;r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 201,
            "name": "Enamine #10",
            "smarts": "[C]=[C!r][N;X3&!$(*=[O,S,N])&!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 202,
            "name": "Acyl halide #1",
            "smarts": "[C](=[O])[Br,Cl,I,F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 203,
            "name": "Nitro #2",
            "smarts": "[C]=[N+]([O-])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 204,
            "name": "Oxonium #1",
            "smarts": "[CX4][O+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 205,
            "name": "Carbamate #1",
            "smarts": "[OH0][C](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 206,
            "name": "Carbamate #3",
            "smarts": "[OH0][C](=[O])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 207,
            "name": "Carbamate #4",
            "smarts": "[O!$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 208,
            "name": "Carbamate #5",
            "smarts": "[O][C](=[O])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 209,
            "name": "Carbamate #2",
            "smarts": "[O$(*C(C)(C)C)][C](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 210,
            "name": "Carbenium #1",
            "smarts": "[C;X3&+1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 211,
            "name": "Carbodiimide #1",
            "smarts": "[#6][N]=[C]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 212,
            "name": "Carboxyl(ate) #12",
            "smarts": "[#6][O][CX3](=[O])[O]c1ccc([N+1]([O-])=[O])cc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 213,
            "name": "Carboxyl(ate) #14",
            "smarts": "[#6][O][CX3](=[O])[O][CH1]=[CH2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 214,
            "name": "Carboxyl(ate) #13",
            "smarts": "[#8,#16][#6](=[O,S])[#8,#16]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 215,
            "name": "Carboxyl(ate) #3",
            "smarts": "[#6,#7][C](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 216,
            "name": "Carboxyl(ate) #4",
            "smarts": "[#6,#7][C](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 217,
            "name": "Carboxyl(ate) #5",
            "smarts": "[CX3z2](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 218,
            "name": "Carboxyl(ate) #6",
            "smarts": "[CX3z2](=[O])[O][CH2][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 219,
            "name": "Carboxyl(ate) #7",
            "smarts": "[CX3z2&$(*[#6&+0])&!$(*[CX3]=[CX3][O][Na,K,Li,Mg,Zn])&!$(*[CX3]=[CX3][O-1])](=[O])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 220,
            "name": "Carboxyl(ate) #8",
            "smarts": "[CX3z2](=[O])[O;!$(*[CH2][CH3])&!$(*[CH3])][#6;!$(*=[O,S,N])&!$(*([#6])([#6])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 221,
            "name": "Carboxyl(ate) #9",
            "smarts": "[CX3z2](=[O])[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 222,
            "name": "Dicarbonyl #1",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 223,
            "name": "Dicarbonyl #2",
            "smarts": "[C,S,N,P](=[O])[C;X3&-1][C,S,N,P](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 224,
            "name": "Dicarbonyl #3",
            "smarts": "[C,S,N,P](=[O])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 225,
            "name": "Dinitrile #1",
            "smarts": "[C](#[N])[C;X4&h][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 226,
            "name": "Diazirine #1",
            "smarts": "[CX4]1[N]=[N]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 227,
            "name": "Diazo #1",
            "smarts": "[C][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 228,
            "name": "Diazo #2",
            "smarts": "[c][N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 229,
            "name": "Diazo #3",
            "smarts": "[C]=[N+]=[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 230,
            "name": "Diazo #4",
            "smarts": "[#6][N]=[N][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 231,
            "name": "Diazo #5",
            "smarts": "[C-]-[N+]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 232,
            "name": "DMA-PG #1",
            "smarts": "[CX4z2]([O][CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 233,
            "name": "Dioxalane #1",
            "smarts": "[CX4]1[O][CH2][O][CX4]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 234,
            "name": "Disulfide #2",
            "smarts": "[Sv2][Sv2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 235,
            "name": "Disulfide #3",
            "smarts": "[Sv2][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 236,
            "name": "Disulfide #1",
            "smarts": "[Sv2][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 237,
            "name": "Dithiane #1",
            "smarts": "[S][C;X4&h][S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 238,
            "name": "Alkene #1",
            "smarts": "[CX3!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]=[CX3!$(*(=[CX3][a])[a])&!$(*[C,N,S]=[O,S,N])&!$(*[C]#[N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 239,
            "name": "Allene #1",
            "smarts": "[C]=[C]=[C]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 240,
            "name": "Alkene #2",
            "smarts": "[a][CX3]=[CX3][a]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 241,
            "name": "Enamine #5",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 242,
            "name": "Enamine #4",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3h!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 243,
            "name": "Enamine #3",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3h$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 244,
            "name": "Enamine #8",
            "smarts": "[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 245,
            "name": "Enamine #7",
            "smarts": "[CX3;$(*[C,S,N]=[O,S]),$(*[C]#[N])]=[CX3][NX3H0!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 246,
            "name": "Enamine #6",
            "smarts": "[CX3$(*[C,S,N]=[O,S])&!$(*[C]#[N])]=[CX3!$(*[C,S,N]=[O,S])&!$(*[C]#[N])][NX3H0$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 247,
            "name": "Enamine #2",
            "smarts": "[C]=[C][NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 248,
            "name": "Enamine #1",
            "smarts": "[C]=[C][NX3][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 249,
            "name": "Enol #2",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 250,
            "name": "Enol #1",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 251,
            "name": "Silyl #11",
            "smarts": "[CX3]=[CX3][O][#14]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 252,
            "name": "Enolate #4",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 253,
            "name": "Enolate #3",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 254,
            "name": "Enolate #2",
            "smarts": "[CX3!$(*[CX3]=[O,S])]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 255,
            "name": "Enolate #1",
            "smarts": "[O,S]=[CX3][CX3]=[CX3][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 256,
            "name": "Epoxide #1",
            "smarts": "[CX4]1[CX4][O]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 257,
            "name": "Ether #1",
            "smarts": "[C;X4&!$(*=[O,S,N])&!$(*([O])[O,S,N])][O][#6;!$(*=[O,S,N])&!$(*([O])[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 258,
            "name": "Ether #2",
            "smarts": "[c!$(*=[O,S,N])][O][c!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 259,
            "name": "(Het)aryl (pseudo)halide #2",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 260,
            "name": "(Het)aryl bromide #12",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 261,
            "name": "(Het)aryl chloride #11",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 262,
            "name": "(Het)aryl fluoride #7",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 263,
            "name": "(Het)aryl iodide #6",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 264,
            "name": "(Het)aryl triflate #6",
            "smarts": "[c$(*c[C,N,S]=[O]),c$(*c[C]#[N])][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 265,
            "name": "(Het)aryl (pseudo)halide #1",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 266,
            "name": "(Het)aryl bromide #11",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 267,
            "name": "(Het)aryl chloride #12",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 268,
            "name": "(Het)aryl fluoride #6",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 269,
            "name": "(Het)aryl iodide #7",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 270,
            "name": "(Het)aryl triflate #7",
            "smarts": "[c$(*1aac([C,N,S]=[O])aa1),c$(*1aac([C]#[N])aa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 271,
            "name": "Fluorene #1",
            "smarts": "[Ch]1[c][c][c][c]1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 272,
            "name": "Fmoc-PG #1",
            "smarts": "c:1:c:c:c2:c(:c:1)C(c:3:c2:c:c:c:c:3)COC(=O)[#7;X3&!$(*=[O])][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 273,
            "name": "Amide #5",
            "smarts": "[#7][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 274,
            "name": "Carboxyl(ate) #11",
            "smarts": "[O][Ch]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 275,
            "name": "Oxaphosphonium #1",
            "smarts": "[CX4][O+]=[P]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 276,
            "name": "Hetarene #1",
            "smarts": "o:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 277,
            "name": "Hetarene #2",
            "smarts": "[ch]:1:[o]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 278,
            "name": "Hetarene #3",
            "smarts": "[ch]:1:[a]:[o]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 279,
            "name": "Guanidine #6",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](-[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 280,
            "name": "Guanidine #5",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](-[NX3])=[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 281,
            "name": "Guanidine #4",
            "smarts": "[N][C](=[N])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 282,
            "name": "Guanidine #3",
            "smarts": "[N][C](=[N])[N][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 283,
            "name": "Guanidine #2",
            "smarts": "[NX3!$(*([C]=[N])[C,S,N]=[O,S,N])][C](=[N])[NX3h!$(*([C]=[N])[C,S,N]=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 284,
            "name": "Guanidine #1",
            "smarts": "[NX3$(*[C,S,N]=[O,S,N])][C](=[N])[NX3h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 285,
            "name": "(Hemi)aminal #2",
            "smarts": "[OH1][CX4][#7!$(*[C,S]=[O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 286,
            "name": "(Hemi)aminal #3",
            "smarts": "[N&h&R0&$(*[CX4][O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 287,
            "name": "N-N #9",
            "smarts": "[#6][Ch](=[N][Nh0$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 288,
            "name": "N-N #8",
            "smarts": "[#6][Ch](=[N][Nh$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 289,
            "name": "N-N #6",
            "smarts": "[#6][C](=[N][Nh$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 290,
            "name": "N-N #7",
            "smarts": "[#6][C](=[N][Nh0$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 291,
            "name": "N-N #5",
            "smarts": "[NX3!$(*=[O])][NX3h!$(*=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 292,
            "name": "N-N #4",
            "smarts": "[#6][Ch](=[N][Nh0!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 293,
            "name": "N-N #3",
            "smarts": "[#6][Ch](=[N][Nh!$(*[C,S]=[O,S])])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 294,
            "name": "N-N #1",
            "smarts": "[#6][C](=[N][Nh!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 295,
            "name": "N-N #2",
            "smarts": "[#6][C](=[N][Nh0!$(*[C,S]=[O,S])])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 296,
            "name": "N-O #7",
            "smarts": "[#6][C](=[O])[N][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 297,
            "name": "N-O #6",
            "smarts": "[#6][C](=[O])[Nh][O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 298,
            "name": "N-O #5",
            "smarts": "[#7;X3&!$(*[C]=[O])&!$(*=[O])][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 299,
            "name": "N-O #3",
            "smarts": "[#7h;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 300,
            "name": "N-O #4",
            "smarts": "[#7h0;X3&!$(*[C]=[O])&!$(*=[O])][Oh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 301,
            "name": "N-O #2",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 302,
            "name": "N-O #1",
            "smarts": "[#7&+0;X3&!$(*[C]=[O])&!$(*=[O])][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 303,
            "name": "Imidate #1",
            "smarts": "[#6][C](=[NH0][#6])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 304,
            "name": "Hetarene #5",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 305,
            "name": "Hetarene #4",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 306,
            "name": "Hetarene #6",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:c:n:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 307,
            "name": "Hetarene #36",
            "smarts": "[n;$(*-[#6])&+1]:1:[ch]:[n$(*[C])]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 308,
            "name": "Imide #1",
            "smarts": "[#6][C](=[O])[N-][C](=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 309,
            "name": "Imide #2",
            "smarts": "[C](=[O])[Nh][C](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 310,
            "name": "C=N #6",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 311,
            "name": "C=N #5",
            "smarts": "[#6][Ch](=[N][#6,S])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 312,
            "name": "C=N #3",
            "smarts": "[#6][C](=[N][#6,S])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 313,
            "name": "C=N #4",
            "smarts": "[#6][C](=[N+][#6,S,O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 314,
            "name": "C=N #1",
            "smarts": "[#6][Ch]=[N][#6,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 315,
            "name": "C=N #2",
            "smarts": "[#6][Ch]=[N+][#6,S,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 316,
            "name": "Hetarene #7",
            "smarts": "n:1:[cR2]:[cR2]:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 317,
            "name": "Hetarene #8",
            "smarts": "[ch]:1:[a]:[nX3]:[aR2]:[aR2]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 318,
            "name": "Iso(thio)cyanate #1",
            "smarts": "[N$(*([#6])=[C])]=[C]=[O,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 319,
            "name": "Isocyanide #1",
            "smarts": "[N+1&$(*([#6])#[C])]#[C-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 320,
            "name": "Ketene #1",
            "smarts": "[C]=[C]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 321,
            "name": "Carbonyl #7",
            "smarts": "[#6!$(*[Na,K,Li,Mg,Zn,Sn])][C!$([C;r5,r6](=[O])([c])[c])](=[O])[#6!$(*[Na,K,Li,Mg,Zn,Sn])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 322,
            "name": "Quinone #1",
            "smarts": "[c][C;r5,r6](=[O])[c]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 323,
            "name": "Geminal diol #2",
            "smarts": "[#6][CX4]([OH1])([OH1])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 324,
            "name": "C=N #9",
            "smarts": "[#6][C](=[N][Oh])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 325,
            "name": "C=N #10",
            "smarts": "[#6][C](=[N][Oh0])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 326,
            "name": "C=N #8",
            "smarts": "[#6][C]([#6])=[N][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 327,
            "name": "C=N #7",
            "smarts": "[#6][C]([#6])=[N][O][Na,K,Mg,Li,Cu,Sn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 328,
            "name": "Metal-organic compound #5",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][Na,K,Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 329,
            "name": "Metal-organic compound #4",
            "smarts": "[C;X4&!$(*[C,N,P,S]=[O,S,N])&!$(*[cr6]n)&!$(*c1aanaa1)][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 330,
            "name": "Metal-organic compound #3",
            "smarts": "[CX3]=[CX3][Li,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 331,
            "name": "Metal-organic compound #2",
            "smarts": "[CX3]=[CX3][#29,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 332,
            "name": "Metal-organic compound #1",
            "smarts": "[CX3,c][Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 333,
            "name": "Michael acceptor #10",
            "smarts": "[C,N,S](=[O])[C]#[C][C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 334,
            "name": "Michael acceptor #9",
            "smarts": "[C!$(*[O,N])]#[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 335,
            "name": "Michael acceptor #8",
            "smarts": "[C!$(*[O,N])]#[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 336,
            "name": "Michael acceptor #7",
            "smarts": "[C!$(*[O,N])]=[C]([C,N,S]=[O])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 337,
            "name": "Michael acceptor #6",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C,N,S]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 338,
            "name": "Michael acceptor #5",
            "smarts": "[C!$(*[O,N])]=[C]([C]#[N])[C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 339,
            "name": "Michael acceptor #4",
            "smarts": "[C!$(*[O,N])]=[C][C;X3&!$(*-[!#6])](=[O])",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 340,
            "name": "Michael acceptor #2",
            "smarts": "[C!$(*[O,N])]=[C][C](=[O,N,S])[O,N,S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 341,
            "name": "Michael acceptor #3",
            "smarts": "[C!$(*[O,N])]=[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 342,
            "name": "Michael acceptor #1",
            "smarts": "[C!$(*[O,N])]=[C][N,S,P]=[O,N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 343,
            "name": "MOM-PG #1",
            "smarts": "[#6!$(*=[O,S,N])][O][CH2][O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 344,
            "name": "Nitrile #2",
            "smarts": "[C][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 345,
            "name": "Nitrile #1",
            "smarts": "[c][C]#[N]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 346,
            "name": "N-oxide #1",
            "smarts": "[C]#[N+][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 347,
            "name": "Nitro #3",
            "smarts": "[#6][N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 348,
            "name": "Nitroso #1",
            "smarts": "[#6h0][NX2]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 349,
            "name": "CH-acid #1",
            "smarts": "[C;X4&h][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 350,
            "name": "CH-anion #3",
            "smarts": "[C;X3&-1][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 351,
            "name": "CH-anion #4",
            "smarts": "[Li,K,Na,Mg][C;X4][c]:1:[n]:[c,n]:[c,n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 352,
            "name": "THP-PG #1",
            "smarts": "[Ch2]1[O][Ch]([O,#7][#6])[Ch2][Ch2][Ch2]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 353,
            "name": "CH-acid #2",
            "smarts": "[C;X4&h][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 354,
            "name": "CH-anion #1",
            "smarts": "[C;X3&-1][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 355,
            "name": "CH-anion #2",
            "smarts": "[Li,K,Na,Mg][CX4][c]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 356,
            "name": "P-compound #8",
            "smarts": "[O]=[P][O][P]=[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 357,
            "name": "P-Hal #1",
            "smarts": "[P][Cl,Br,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 358,
            "name": "Peroxide #1",
            "smarts": "[O][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 359,
            "name": "Peroxide #2",
            "smarts": "[O][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 360,
            "name": "Peroxide #3",
            "smarts": "[O][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 361,
            "name": "Phenol #1",
            "smarts": "[c;!$(*n)&!$(*:1:a:a:n:a:a:1)][Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 362,
            "name": "Phenolate #2",
            "smarts": "[c][O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 363,
            "name": "Phenolate #1",
            "smarts": "[c][O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 364,
            "name": "Silyl #13",
            "smarts": "[#6][#14]([CH3])([CH3])c1ccccc1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 365,
            "name": "P-compound #7",
            "smarts": "[#6][P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 366,
            "name": "P-compound #6",
            "smarts": "[P;X3&!$(*[!#6])&!$(*[C]=[O,N,S])&h0][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 367,
            "name": "P-compound #5",
            "smarts": "[O][P;X3&!$(*([!#6,!O])[!#6,!O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 368,
            "name": "P-compound #4",
            "smarts": "[P](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 369,
            "name": "P-compound #3",
            "smarts": "[P](=[O])[OH0][Na,K,Cu,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 370,
            "name": "P-compound #2",
            "smarts": "[P+][C;X4&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 371,
            "name": "P-compound #1",
            "smarts": "[P](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 372,
            "name": "PMB-PG #2",
            "smarts": "[#6,#7,#8][O,#7][CH2][c]:1:[cH1]:[cH1]:[c]([O][CH3]):[cH1]:[cH1]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 373,
            "name": "PMB-PG #1",
            "smarts": "[#6,#7,#8][O,#7][C;R0&X4&h]c:1:c:c:[c]([O][C]):c:c:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 374,
            "name": "Hetarene #20",
            "smarts": "[O]=[c]1[c][c!$(*[O,N])][o][c!$(*[O,N])][c]1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 375,
            "name": "Hetarene #23",
            "smarts": "[ch]:1:[!n]:[nX3]:[nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 376,
            "name": "Hetarene #22",
            "smarts": "[ch]:1:[nX3]:[nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 377,
            "name": "Hetarene #21",
            "smarts": "[n;-1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 378,
            "name": "Hetarene #19",
            "smarts": "[n;H1&!$(*[#6]=[O])&$(*:1:n:c:c:c:1)]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 379,
            "name": "Hetarene #18",
            "smarts": "[c,n]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 380,
            "name": "N-oxide #2",
            "smarts": "[nr6&+1][O-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 381,
            "name": "(Het)aryl bromide #10",
            "smarts": "[c$(*1nacac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 382,
            "name": "(Het)aryl bromide #9",
            "smarts": "[c$(*1canac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 383,
            "name": "(Het)aryl chloride #7",
            "smarts": "[c$(*1nacac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 384,
            "name": "(Het)aryl chloride #8",
            "smarts": "[c$(*1canac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 385,
            "name": "(Het)aryl fluoride #5",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 386,
            "name": "(Het)aryl iodide #11",
            "smarts": "[c$(*1nacac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 387,
            "name": "(Het)aryl iodide #10",
            "smarts": "[c$(*1canac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 388,
            "name": "Sulfonate #5",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 389,
            "name": "(Het)aryl triflate #8",
            "smarts": "[c;$(*na[c!$(*C#N),c!$(*[C,S,P,N]=[O])]a[!n]),$(*1aanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 390,
            "name": "(Het)aryl triflate #9",
            "smarts": "[c$(*1nacac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 391,
            "name": "(Het)aryl triflate #10",
            "smarts": "[c$(*1canac1)][O][S](=[O])(=[O])[C]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 392,
            "name": "Sulfide #3",
            "smarts": "[c$(*1nacan1)][SX2][CX4z1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 393,
            "name": "(Het)aryl bromide #8",
            "smarts": "[c$(*1nacan1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 394,
            "name": "(Het)aryl bromide #7",
            "smarts": "[c$(*1nanac1)][Br]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 395,
            "name": "(Het)aryl chloride #9",
            "smarts": "[c$(*1nacan1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 396,
            "name": "(Het)aryl chloride #10",
            "smarts": "[c$(*1nanac1)][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 397,
            "name": "(Het)aryl fluoride #4",
            "smarts": "[c$(*1nacan1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 398,
            "name": "(Het)aryl fluoride #3",
            "smarts": "[c$(*1nanaa1)][F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 399,
            "name": "(Het)aryl iodide #9",
            "smarts": "[c$(*1nacan1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 400,
            "name": "(Het)aryl iodide #8",
            "smarts": "[c$(*1nanac1)][I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 401,
            "name": "Sulfinate #3",
            "smarts": "[c;$(*1nacan1)][S](=[O])(=[O])[#6$([CX4z1,c])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 402,
            "name": "Sulfonate #6",
            "smarts": "[c;$(*1nacan1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 403,
            "name": "Sulfonate #7",
            "smarts": "[c;$(*1nanaa1)][O][S](=[O])(=[O])[#6!$(*[F])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 404,
            "name": "(Het)aryl triflate #11",
            "smarts": "[c$(*1nacan1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 405,
            "name": "(Het)aryl triflate #12",
            "smarts": "[c$(*1nanaa1)][O][S](=[O])(=[O])[#6]([F])([F])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 406,
            "name": "Hetarene #17",
            "smarts": "[n!R2]:1:[c!R2]:[c!R2]:[c!R2]:[c!R2]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 407,
            "name": "Hetarene #16",
            "smarts": "[ch]:1:[nX3]:[!nR1]:[!nR1]:[!n]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 408,
            "name": "Hetarene #15",
            "smarts": "[ch]:1:[!n]:[nX3]:[!nR1]:[!nR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 409,
            "name": "Hetarene #13",
            "smarts": "[n;r5&!$(*[#6]=[O])&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 410,
            "name": "Hetarene #14",
            "smarts": "[nr5!$(*[#6]=[O])][Li,K,Mg,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 411,
            "name": "Hetarene #12",
            "smarts": "[nr5h!$(*[#6]=[O])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 412,
            "name": "Amine #19",
            "smarts": "[NX3,OX2][NX3;H2]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 413,
            "name": "Amine #18",
            "smarts": "[NX3,OX2][NX3;H1][#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 414,
            "name": "Amine #17",
            "smarts": "[NX3,OX2][NX3;H0]([#6!$(*=[C,N,O,S])])[#6!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 415,
            "name": "S-Hal #1",
            "smarts": "[S!$(*(=[O])(=[O])[F])][F,Br,Cl,I]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 416,
            "name": "(Het)aryl-SeH #1",
            "smarts": "[c][Sev2&h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 417,
            "name": "(Hemi)acetale and (hemi)ketale #1",
            "smarts": "[#6][O][CX4R0][OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 418,
            "name": "Carboxyl(ate) #15",
            "smarts": "[#7][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 419,
            "name": "Carboxyl(ate) #16",
            "smarts": "[#8][#6](=[O])[OH1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 420,
            "name": "Silyl #12",
            "smarts": "[#6][#14;X4h]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 421,
            "name": "Silyl #10",
            "smarts": "[#14][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 422,
            "name": "Silyl #9",
            "smarts": "[#6][#14&!$(*c1ccccc1)](C)(C)C",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 423,
            "name": "Silyl #8",
            "smarts": "[O,#7][#14!$(*([CH3])([CH3])[C]([CH3])([CH3])[CH3])&!$(*(c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3])&!$(*([CH3])([CH3])[CH3])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 424,
            "name": "Carbocycle #1",
            "smarts": "A1AA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 425,
            "name": "Carbocycle #2",
            "smarts": "A1AAA1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 426,
            "name": "Sulfamate #2",
            "smarts": "[OH0][S](=[O])(=[O])[#7]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 427,
            "name": "Sulfamate #1",
            "smarts": "[OH0][S](=[O])(=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 428,
            "name": "Sulfate #2",
            "smarts": "[#6,#7][S](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 429,
            "name": "Sulfate #1",
            "smarts": "[#6,#7][S](=[O])[O][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 430,
            "name": "Sulfide #1",
            "smarts": "[#6;!$(*=[C,N,O,S])][Sv2][#6;!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 431,
            "name": "Sulfide #2",
            "smarts": "[Sv2][C;X4&h&!$(*=[C,N,O,S])]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 432,
            "name": "Sulfinate #2",
            "smarts": "[#6][Sv4](=[O])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 433,
            "name": "Sulfonamide #4",
            "smarts": "[#6,#7][S](=[O])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 434,
            "name": "Sulfonamide #5",
            "smarts": "[#6,#7][S](=[O])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 435,
            "name": "Sulfonamide #2",
            "smarts": "[#6][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 436,
            "name": "Sulfonamide #1",
            "smarts": "[#7][S](=[O])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 437,
            "name": "Sulfonamide #3",
            "smarts": "[#6,#7][S](=[O])[#7h0X3]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 438,
            "name": "Sulfone #1",
            "smarts": "[#6][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 439,
            "name": "Sulfonic anhydride #1",
            "smarts": "[#6][S](=[O])(=[O])[O][S](=[O])(=[O])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 440,
            "name": "Sulfonyl fluoride #1",
            "smarts": "[S](=[O])(=[O])[F]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 441,
            "name": "Sulfoxide #1",
            "smarts": "[#6][SX3](=[O])-[#6,O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 442,
            "name": "Sulfonic acid #1",
            "smarts": "[#6,#7][S](=[O])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 443,
            "name": "Sulfate #3",
            "smarts": "[#6,#7][S](=[O])[O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 444,
            "name": "tBu #7",
            "smarts": "[OH1][C]([#6])([#6])[CX4h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 445,
            "name": "tBu #6",
            "smarts": "[O][C]([#6z0])([#6z0])[#6z0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 446,
            "name": "tBu #5",
            "smarts": "[O][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 447,
            "name": "tBu #3",
            "smarts": "[#7,S,Se,P,Si][C]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 448,
            "name": "tBu #1",
            "smarts": "[#7][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 449,
            "name": "tBu #4",
            "smarts": "[#6][C]([#6])([#6])[Cl,Br,I,O$(*[S](=[O])(=[O])[#6])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 450,
            "name": "tBu #2",
            "smarts": "[O][C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 451,
            "name": "Silyl #2",
            "smarts": "[O,#7,S][#14]([CH3])([CH3])[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 452,
            "name": "Silyl #1",
            "smarts": "[O,#7,S][#14](c1ccccc1)(c2ccccc2)[C]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 453,
            "name": "Hetarene #24",
            "smarts": "[n;$(*[#6])&+1]:1:[ch]:[s]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 454,
            "name": "Hetarene #31",
            "smarts": "[o,s]:1:[n]:[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 455,
            "name": "Hetarene #30",
            "smarts": "[o,s]:1:[ch]:[nh0]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 456,
            "name": "Thio-compound #20",
            "smarts": "[N][CX3z2]=[S]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 457,
            "name": "Thio-compound #18",
            "smarts": "[CX3z2](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 458,
            "name": "Thio-compound #19",
            "smarts": "[CX3z2](=[S])[N!$(*=[O])][Li,Mg,K,Na]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 459,
            "name": "Thio-compound #17",
            "smarts": "[CX3z2](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 460,
            "name": "Thio-compound #16",
            "smarts": "[OH0][C](=[S])[#7h&!$(*[C](=O)[O][C](C)(C)[C])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 461,
            "name": "Thio-compound #24",
            "smarts": "[O][C](=[S])[N][Na,Li,K,Mg,Sn,Zn]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 462,
            "name": "Thio-compound #15",
            "smarts": "[OH0][C](=[S])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 463,
            "name": "Thio-compound #14",
            "smarts": "[O!$(*C(C)(C)C)][C](=[S])[N-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 464,
            "name": "Thio-compound #21",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 465,
            "name": "Thio-compound #22",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 466,
            "name": "Thio-compound #23",
            "smarts": "[#6,#7,O,S][C](=[O,S,N])[Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 467,
            "name": "Thio-compound #13",
            "smarts": "[#6][C](=[S])[Oh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 468,
            "name": "Thio-compound #12",
            "smarts": "[#6][C](=[O,S])[Sh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 469,
            "name": "Thio-compound #11",
            "smarts": "[#6,#7,#8][C](=[O,S])[S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 470,
            "name": "Thio-compound #10",
            "smarts": "[#6,#7,#8][C](=[O,S])[SX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 471,
            "name": "Thio-compound #9",
            "smarts": "[#6,#7,#8][C](=[S])[O-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 472,
            "name": "Thio-compound #8",
            "smarts": "[#6,#7,#8][C](=[S])[OX2][Li,Mg,Na,K,Zn,Cu]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 473,
            "name": "Thio-compound #7",
            "smarts": "[#6][C](=[S])[O][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 474,
            "name": "Thio-compound #6",
            "smarts": "[#6][C](=[O])[S][#6!$(*=[O,S,N])]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 475,
            "name": "Thiol #1",
            "smarts": "[C;X4&!$(*=[C,N,O,S])][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 476,
            "name": "Thiolate #2",
            "smarts": "[C!$(*=[C,N,O,S])][SX1&-1]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 477,
            "name": "Thiolate #1",
            "smarts": "[C!$(*=[C,N,O,S])][Sv2h0][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 478,
            "name": "Thio-compound #5",
            "smarts": "[#6]OC(=S)O[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 479,
            "name": "Hetarene #9",
            "smarts": "s:1:c:c:c:c:1",
            "fg_class": FunctionalGroupClass.SKIP,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 480,
            "name": "Hetarene #10",
            "smarts": "[ch]:1:[s]:[aR1]:[aR1]:[a]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 481,
            "name": "Hetarene #11",
            "smarts": "[ch]:1:[a]:[s]:[aR1]:[aR1]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 482,
            "name": "Thiophenol #1",
            "smarts": "[c][Sv2h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 483,
            "name": "Thiophenolate #2",
            "smarts": "[c][S-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 484,
            "name": "Thiophenolate #1",
            "smarts": "[c][Sv2][Li,K,Na,Mg]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 485,
            "name": "Thio-compound #4",
            "smarts": "[#7][C](=[S])[Nh]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 486,
            "name": "Thio-compound #3",
            "smarts": "[#7h0][C](=[S])[Nh0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 487,
            "name": "Thio-compound #2",
            "smarts": "[#7][C](=[S])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 488,
            "name": "Thio-compound #1",
            "smarts": "[#7][C](=[S])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 489,
            "name": "Silyl #7",
            "smarts": "[O][#14](CC)(CC)CC",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 490,
            "name": "Silyl #6",
            "smarts": "[#7][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 491,
            "name": "Silyl #5",
            "smarts": "[C;X2,X3,X4H0][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 492,
            "name": "Silyl #4",
            "smarts": "[c][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 493,
            "name": "Silyl #3",
            "smarts": "[CX4h][O][#14]([CH3])([CH3])[CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 494,
            "name": "Trityl-PG #1",
            "smarts": "[#7,O]C(c:1:c:c:c:c:c:1)(c:2:c:c:c:c:c:2)c:3:c:c:c:c:c:3",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 495,
            "name": "Urea #1",
            "smarts": "[#7][#6](=[O])[#7h]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 496,
            "name": "Urea #2",
            "smarts": "[#7h0][#6](=[O])[#7h0]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 497,
            "name": "Urea #3",
            "smarts": "[#7][C](=[O])[NX2-]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 498,
            "name": "Urea #4",
            "smarts": "[#7][C](=[O])[NX3+0][Na,K,Mg,Li]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 499,
            "name": "Iminium #1",
            "smarts": "[C][N+]([C])=[C][Cl]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 500,
            "name": "Ether #3",
            "smarts": "[CX3&!$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 501,
            "name": "Ether #4",
            "smarts": "[CX3&$(*[CX3]=[O])]=[CX3][O][#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 502,
            "name": "Amide #6",
            "smarts": "[#6][C](=[O])[N]([CH3])[O][CH3]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 503,
            "name": "N-ylide #4",
            "smarts": "[O]=[C,N,S][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 504,
            "name": "N-ylide #3",
            "smarts": "[N]#[C][C-][n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 505,
            "name": "N-ylide #2",
            "smarts": "[O]=[C,N,S][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 506,
            "name": "N-ylide #1",
            "smarts": "[N]#[C][C]([Na,K,Li,Mg,Zn,Sn])[n+]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 507,
            "name": "P-ylide #5",
            "smarts": "[C]=[P]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 508,
            "name": "P-ylide #4",
            "smarts": "[C-][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 509,
            "name": "P-ylide #3",
            "smarts": "[C-][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 510,
            "name": "P-ylide #2",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P+]([#6])([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 511,
            "name": "P-ylide #1",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][C][P](=[O])([O])[O]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 512,
            "name": "S-ylide #3",
            "smarts": "[C]=[Sv4]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 513,
            "name": "S-ylide #2",
            "smarts": "[C-][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 514,
            "name": "S-ylide #1",
            "smarts": "[Na,K,Li,Mg,Zn,Sn][CX4][S;v4&+1]([#6])[#6]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 515,
            "name": "Arene [ch] #0",
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
