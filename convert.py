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

pda_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/pda.py")
exec(pda_link.read())

cfg_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/cfg.py")
exec(cfg_link.read())

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

  width = 238*(len(d.alphabet)) + 100;
  document["minDFAbox"].style.width = str(width) + 'px'


def dfa2regex():
  document["reg_ans_pg"].style.display = "block"
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
  document["reg_ans_pg"].style.display = "block"
  exp = document["re_txt"].value
  r = Regex(exp)
  r.complement_maker()
  document["reg_ans"].value = r.complement

def re_ops(event):
  f = document["re_inp"].getAttribute("from")
  document["re_inp"].style.display = "none"
  if f == "re2dfa":
    re2dfa()
  elif f == "recomp":
    recomp()

def make_pda():
  sts = set()
  num_transitions = len(document["pda_tab_body"].children)
  inp_alph = document["pda_inp_alphabet"].value.split()
  stack_alph = document["pda_stack_alphabet"].value.split()
  id_to_st = {}

  for i in range(num_transitions):
    st1 = document["pda_tab_body"].children[i].children[0].children[1].value
    inp1 = document["pda_tab_body"].children[i].children[0].children[3].value
    stack1 = document["pda_tab_body"].children[i].children[0].children[5].value
    st2 = document["pda_tab_body"].children[i].children[0].children[7].value
    stack2 = document["pda_tab_body"].children[i].children[0].children[9].value
    if st1 not in id_to_st:
      s = state(st1)
      sts.add(s)
      id_to_st[st1] = s
    if st2 not in id_to_st:
      s = state(st2)
      sts.add(s)
      id_to_st[st2] = s
    st = id_to_st[st1]
    if (inp1, stack1) not in st.outpaths:
      st.outpaths[(inp1, stack1)] = {(id_to_st[st2], stack2)}
    else:
      st.outpaths[(inp1, stack1)].add((id_to_st[st2], stack2))

  p = PDA(sts, document["pda_init_stack_sym"].value)
  p.start_state = id_to_st[document["pda_ss"].value]
  p.input_alphabet = set(inp_alph)
  p.stack_symbols = set(stack_alph)
  #p.stack_symbols.add(p.init_stack_symbol)
  acc_list = document["pda_accs"].value.split()
  p.accept_states = {id_to_st[i] for i in acc_list}
  return p

def render_cfg(c):
  tab = document["cfg_ans_table"]
  tbody = document.createElement("tbody")
  for nt, prods in c.rules.items():
    tr = document.createElement('tr')
    td = document.createElement('td')
    lab = document.createElement("label")
    if nt != c.start:
      lab.innerHTML = nt + " → "
    else:
      lab.innerHTML = nt + "* → "
    s = ''
    for str in prods:
        s2 = ' '.join(str)
        s += s2 + '  |  '
    s = s[:-5]
    inp = document.createElement('input')
    inp.type = 'text'
    inp.value = s
    td.append(lab)
    td.append(inp)
    tr.append(td)
    tbody.append(tr)
  tab.append(tbody)

def pda2cfg():
  p = make_pda()
  p.to_cfg()
  document["pda_transitions"].style.display = "none"
  document["cfg_ans"].style.display = "block"
  render_cfg(p.my_cfg)

def pda_ops(event):
  f = document["pda_gen"].getAttribute("from")
  document["pda_gen"].style.display = "none"
  if f == "pda2cfg":
    pda2cfg()

document["enter_dnfa_inp"].bind("click", dnfa_ops)
document["enter_re"].bind("click", re_ops)
document["pda_enter"].bind("click", pda_ops)
