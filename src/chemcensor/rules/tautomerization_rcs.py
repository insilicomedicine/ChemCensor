TAUTOMERIZATION_RCS: tuple[str, ...] = (
    "c=O.c[nH]c>>cO.cnc",  # piridone to parahydroxypiridine
    "cO.cnc>>c=O.c[nH]c",  # parahydroxypiridine to piridone
    "c[nH]c=O>>cncO",  # pyridone to hydroxypyridine
    "cncO>>c[nH]c=O",  # hydroxypyridine to pyridone
    "c[nH]cnc=O>>cnc[nH]c=O",  # pyrimidinone tautomerization 1
    "cnc[nH]c=O>>c[nH]cnc=O",  # pyrimidinone tautomerization 2
    "cn[nH]c>>cn[nH]c",  # pyrazole tautomerization
    "cnc[nH]c>>cnc[nH]c",  # imidazole tautomerization
    "cn[nH]n>>c[nH]nn",  # triazole tautomerization 1
    "c[nH]nn>>cn[nH]n",  # triazole tautomerization 2
    "c[nH]cnn>>cnc[nH]n",  # triazole tautomerization 3
    "c1nnc[nH]1>>c1nc[nH]n1",  # triazole tautomerization 4
)
