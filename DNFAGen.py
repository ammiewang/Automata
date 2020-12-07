from browser import document
from browser import window

import urllib.request

state_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/state.py")
exec(state_link.read())

dfa_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/dfa.py")
exec(dfa_link.read())

nfa_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/nfa.py")
exec(nfa_link.read())

re_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/regex.py")
exec(re_link.read())

def make_dfa_wrapper():
  sts = []
  rows = len(document["rows"].children)
  cols = len(document["rows"].children[1].children)
  alph = document["alphabet"].value.split()
  id_to_st = {}

  for i in range(rows):
    st_name = document["original_table"].children[1].children[i].children[0].children[0].value
    s = state(st_name)
    sts.append(s)
    id_to_st[st_name] = s

  for i in range(rows):
    s = sts[i]
    s.outpaths = {}
    for j in range(1, cols):
      st2 = document["original_table"].children[1].children[i].children[j].children[0].value
      if st2 != "":
        s.outpaths[alph[j-1]] = id_to_st[st2]

  d = DFA(sts)
  d.start_state = id_to_st[document["ss"].value]
  d.alphabet = alph
  acc_list = document["accs"].value.split()
  d.accept_states = [id_to_st[i] for i in acc_list]
  return d

def make_nfa_wrapper():
  sts = []
  rows = len(document["rows"].children)
  cols = len(document["rows"].children[1].children)
  alph = document["alphabet"].value.split()
  id_to_st= {}

  for i in range(rows):
    st_name = document["original_table"].children[1].children[i].children[0].children[0].value
    s = state(st_name)
    sts.append(s)
    id_to_st[st_name] = s

  for i in range(rows):
    s = sts[i]
    s.outpaths = {}
    for j in range(1, cols):
      s.outpaths[alph[j-1]] = []
      lst = document["original_table"].children[1].children[i].children[j].children[0].value.split(" ")
      for st2 in lst:
        if st2 != "":
          s.outpaths[alph[j-1]].append(id_to_st[st2])

  n = NFA(sts)
  ss_list = document["ss"].value.split()
  n.start_states = [id_to_st[i] for i in ss_list]
  n.alphabet = alph
  acc_list = document["accs"].value.split()
  n.accept_states = [id_to_st[i] for i in acc_list]
  return n

def render_dfa(d, tab_name):
  tab = document[tab_name]
  thead = document.createElement('thead')
  headRow = document.createElement('tr')

  th = document.createElement('th')
  th.appendChild(document.createTextNode(''))
  headRow.appendChild(th)

  for char in d.alphabet:
    th = document.createElement('th')
    th.appendChild(document.createTextNode(char))
    headRow.appendChild(th)

  thead.appendChild(headRow)

  tbody = document.createElement('tbody')
  tbody.setAttribute("id", "new_rows")

  for st in d.states:
    tr = document.createElement('tr')
    lab = document.createElement('label')
    lab.innerHTML = st.id
    tr.appendChild(lab);
    if (st in d.accept_states):
      if (st.id == d.start_state.id):
        lab.innerHTML = "→ " + str(d.start_state.id) + " F"
      else:
        lab.innerHTML = str(st.id) + " F"
    else:
      if (st.id == d.start_state.id):
        lab.innerHTML = "→ " + str(d.start_state.id)
      else:
        lab.innerHTML = str(st.id)

    for letter in d.alphabet:
      td = document.createElement('td')
      td.classList.add("input")
      input = document.createElement('input')
      input.type = "text"
      if letter in st.outpaths:
        input.value = st.outpaths[letter].id
      td.appendChild(input);
      tr.appendChild(td);


    tbody.appendChild(tr);

  tab.appendChild(thead);
  tab.appendChild(tbody);

  width = 238*(len(alphabet)) + 100;
  document["minDFAbox"].style.width = width


def dfa2regex():
  document["dfa2reg_ans_pg"].style.display = "block"
  d = make_dfa_wrapper()
  d.all_regex()
  r = d.regex
  document["reg_ans"].value = r

def mindfa():
  document["min_dfa"].style.display = "block"
  d = make_dfa_wrapper()
  d.minimize()
  render_dfa(d, "min_table")

def nfa2dfa():
  document["nfa_dfa_ans"].style.display = "block"
  n = make_nfa_wrapper()
  n.nfa_to_dfa()
  render_dfa(n.my_dfa, "nfa2dfa_table")

def dnfa_ops(event):
  f = document["dnfa_gen"].getAttribute("from")
  if f == "dfa2re":
    dfa2regex()
  elif f == "mindfa":
    mindfa()
  elif f == "nfa2dfa":
    nfa2dfa()

def re2dfa():
  document["re_dfa_ans"].style.display = "block"
  exp = document["re_txt"].value
  r = Regex(exp)
  r.dfa_maker()
  render_dfa(r.my_dfa, "re2dfa_table")

def recomp():
  document["re_comp_ans"].style.display = "block"
  exp = document["re_txt"].value
  r = Regex(exp)
  r.complement_maker()
  document["re_ans"].value = r.complement

def re_ops(event):
  f = document["re_inp"].getAttribute("from")
  document["re_inp"].style.display = "none"
  if f == "re2dfa":
    re2dfa()
  elif f == "recomp":
    recomp()

document["enter_dnfa_inp"].bind("click", dnfa_ops)
document["enter_re"].bind("click", re_ops)
