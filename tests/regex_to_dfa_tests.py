from automata.regex import Regex

def test1():
    ex = Regex('(000* + 111*)*')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output

    States:  [11, '∅', 10, 9, 12, 8]
    Start State:  12
    Accept States:  [8, 9, 12]
    Outpaths:
    State: 11 , Outpaths:  [('0', 8), ('1', '∅')]
    State: ∅ , Outpaths:  [('0', '∅'), ('1', '∅')]
    State: 10 , Outpaths:  [('0', '∅'), ('1', 9)]
    State: 9 , Outpaths:  [('0', 11), ('1', 9)]
    State: 12 , Outpaths:  [('0', 11), ('1', 10)]
    State: 8 , Outpaths:  [('0', 8), ('1', 10)]
    """
#test1()

def test2():
    ex = Regex('(01 + 10)(01 + 10)(01 + 10)')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output

    States:  [22, 14, 23, 15, 16, 17, 18, '∅', 19, 20, 21]
    Start State:  20
    Accept States:  [16]
    Outpaths:
    State: 22 , Outpaths:  [('1', '∅'), ('0', 16)]
    State: 14 , Outpaths:  [('1', 21), ('0', 18)]
    State: 23 , Outpaths:  [('1', 14), ('0', '∅')]
    State: 15 , Outpaths:  [('1', 22), ('0', 19)]
    State: 16 , Outpaths:  [('1', '∅'), ('0', '∅')]
    State: 17 , Outpaths:  [('1', '∅'), ('0', 14)]
    State: 18 , Outpaths:  [('1', 15), ('0', '∅')]
    State: ∅ , Outpaths:  [('1', '∅'), ('0', '∅')]
    State: 19 , Outpaths:  [('1', 16), ('0', '∅')]
    State: 20 , Outpaths:  [('1', 17), ('0', 23)]
    State: 21 , Outpaths:  [('1', '∅'), ('0', 15)]
    """

#test2()

def test3():
    ex = Regex('(0 +  1(01*0)*1)*')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output

    States:  [7, 6, 8]
    Start State:  6
    Accept States:  [6]
    Outpaths:
    State: 7 , Outpaths:  [('0', 8), ('1', 6)]
    State: 6 , Outpaths:  [('0', 6), ('1', 7)]
    State: 8 , Outpaths:  [('0', 7), ('1', 8)]
    """
#test3()
