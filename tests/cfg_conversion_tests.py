from automata.cfg import CFG

def test1():
    rules = {'S': ['AC','B'], 'A': ['a'], 'C': ['c', 'BC'], 'E': ['aA', 'e']}
    c = CFG(rules)
    c.start = 'S'
    c.reduce()
    c.print_cfg()

    """
    Correct Output:

    S* --> AC
    A --> a
    C --> c
    """
#test1()

def test2():
    rules = {'T': ['aaB','abA', 'aaT'], 'A': ['aA'], 'B': ['ab', 'b'], 'C': ['ad']}
    c = CFG(rules)
    c.start = 'T'
    c.reduce()
    c.print_cfg()

    """
    Correct Output:

    T* --> aaB | aaT
    B --> ab | b
    """
#test2()

def test3():
    rules = {'S': ['Aa','B', 'c'], 'B': ['A', 'bb', 'aD'], 'A': ['a', 'bc', 'B'], 'D': ['d']}
    c = CFG(rules)
    c.start = 'S'
    c.elim_unit()
    c.print_cfg()

    """
    Correct Output:

    S* --> Aa | c | bb | aD | a | bc
    A --> a | bc | bb | aD
    D --> d
    """
#test3()

def test4():
    rules = {'S': ['XY'], 'X': ['a'], 'Y': ['Z', 'b'], 'Z': ['M'], 'M': ['N'], 'N': ['a']}
    c = CFG(rules)
    c.start = 'S'
    c.elim_unit()
    c.print_cfg()

    """
    Correct Output:

    S* --> XY
    X --> a
    Y --> b | a
    """
#test4()

def test5():
    rules = {'S': ['AB', 'aS'], 'A': ['aAA', 'ε'], 'B': ['bBB', 'ε']}
    c = CFG(rules)
    c.start = 'S'
    c.elim_null()
    c.print_cfg()

    """
    Correct Output:

    S* --> AB | A | B | ε | aS | a
    A --> aAA | aA | a
    B --> bBB | bB | b
    """
#test5()

def test6():
    rules = {'S': ['ABCd'], 'A': ['BC'], 'B': ['bB', 'ε'], 'C': ['cC', 'ε']}
    c = CFG(rules)
    c.start = 'S'
    c.elim_null()
    c.print_cfg()

    """
    Correct Output:

    S* --> ABCd | BCd | ABd | Bd | ACd | Cd | Ad | d
    A --> BC | B | C
    B --> bB | b
    C --> cC | c
    """
#test6()

def test7():
    rules = {'S': ['aXbX'], 'X': ['aY', 'bY', 'ε'], 'Y': ['X', 'c']}
    c = CFG(rules)
    c.start = 'S'
    c.convert_to_cnf()
    c.print_cfg()

    """
    Correct Output:

    0* --> AE | AF | AD | AB
    A --> a
    B --> b
    F --> XB
    E --> XD
    D --> BX
    X --> AY | a | BY | b
    Y --> c | AY | a | BY | b
    """
#test7()

def test8():
    rules = {'S': ['aB', 'a'], 'B': ['Ba', 'b']}
    c = CFG(rules)
    c.start = 'S'
    c.convert_to_cnf()
    c.print_cfg()

    """
    Correct Output:

    0* --> CB | a
    B --> BC | b
    C --> a
    """
#test8()

def test9():
    rules = {'S': ['CA', 'BB'], 'B': ['b', 'SB'], 'C': ['b'], 'A': ['a']}
    c = CFG(rules)
    c.start = 'S'
    c.convert_to_gnf()
    c.print_cfg()

    """
    Correct Output:

    0* --> bA | bB | bABB | bBBB | bADBB | bBDBB
    B --> b | bAB | bBB | bADB | bBDB
    D --> bBD | bABBD | bBBBD | bADBBD | bBDBBD | bB | bABB | bBBB | bADBB | bBDBB
    A --> a
    """
#test9()
