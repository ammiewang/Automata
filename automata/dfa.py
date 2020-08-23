import random
from display.dfa_regex_window import ToRegExWindow, AnsWindow
from automata.state import state, path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class DFA():
    def __init__(self, states):
        self.start_state = None
        self.accept_states = []
        self.states = states
        self.alphabet = []

    def possible_paths(self, left_out, origin, dest, final=False):
        if not final:
            for state in self.states:
                state.parent = (None, None)
                state.children = []
            t = path(origin)

        start_pts = [(None, origin)]
        paths = []
        loops = set()

        while len(start_pts) > 0:
            new_starts = []
            for char1, pt in start_pts:
                for char2, pt2 in pt.outpaths.items():
                    curr = pt
                    visited = False
                    ancestors = {pt}

                    while curr is not None:
                        if pt2.id == curr.id:
                            visited = True
                            break
                        ancestors.add(curr)
                        curr = curr.parent[1]

                    if not visited and pt2 not in left_out and pt2.id != dest.id:
                        pt.children.append((char2,pt2),)
                        pt2.parent = (char1, pt)
                        new_starts.append((char2, pt2),)

                    elif pt2.id == dest.id and not final:
                        if pt.id == t.root.id and pt2.id == pt.id and pt not in left_out:
                            paths.append([(char2, pt2)])
                            loops.add((pt, pt2),)
                        else:
                            real_path = [(char2, pt2)]
                            curr_state = pt
                            curr_char = char1
                            while curr_char is not None or curr_state is not None:
                                real_path = [(curr_char, curr_state)] + real_path
                                curr_char = curr_state.parent[0]
                                curr_state = curr_state.parent[1]
                            #print([(char, p.id) for char, p in real_path])
                            paths.append(real_path)

                    elif pt2.id == dest.id and final:
                        loops.add((dest, pt))
                        if pt.id != dest.id:
                            real_path = [(char2, pt2)]
                            curr_state = pt
                            curr_char = char1
                            while curr_char is not None and curr_state is not None:
                                real_path = [(curr_char, curr_state)] + real_path
                                curr_char = curr_state.parent[0]
                                curr_state = curr_state.parent[1]
                        else:
                            real_path = []
                        paths.append(real_path)

                    elif visited and pt not in left_out and curr not in left_out \
                    and (curr,pt) not in loops:
                        loops.add((curr, pt),)

            start_pts = new_starts
        return paths, loops

    def make_regex_parts(self, paths, loops):
        regexes = []
        for st in self.states:
            st.reverse_outpaths()

        for path in paths:
            regex = ''
            for i in range(len(path)):
                possible_endpts = []
                for s, f in loops:
                    if path[i][1].id == s.id:
                        if len(s.rev_op[s]) == 1:
                            regex += s.rev_op[s][0] + '*'
                        else:
                            regex += '('
                            count = 0
                            for char in s.rev_op[s]:
                                if count != len(s.rev_op[s]) - 1:
                                    regex += char + ' + '
                                else:
                                    regex += char + ')*'
                                count += 1

                if i != len(path)-1:
                    regex += path[i+1][0]

            regexes.append(regex)
        return ' + '.join(regexes)

    def make_paths(self, left_out, s1, s2, randomized_left_out=True, window=False):
        #print([l.id for l in left_out], s1.id, s2.id)
        no_nonself_loops = True
        paths, loops = self.possible_paths(left_out, s1, s2)
        #print('paths: ', [[(c,p.id) for c,p in path] for path in paths])
        #print('loops: ', [(s.id, f.id) for s, f in loops])
        if s2 not in left_out:
            final_pths, final_loops = self.possible_paths(left_out + [s2], s2, s2, True)
            #print('paths f: ', [[(c,p.id) for c,p in path] for path in final_pths])
            #print('loops f: ', [(s.id, f.id) for s, f in final_loops])
            new_paths = []
            if len(final_pths) > 0:
                for pth in paths:
                    for pth2 in final_pths:
                        new_paths.append(pth + pth2)
            else:
                new_paths = paths
            loops = loops.union(final_loops)

        else:
            new_paths = paths
        #print('paths: ', [[(c,p.id) for c,p in path] for path in new_paths])
        #print('loops: ', [(s.id, f.id) for s, f in loops])
        for s,f in loops:
            if s.id != f.id:
                no_nonself_loops = False
                break
        if no_nonself_loops:
            if len(paths) != 0:
                return self.make_regex_parts(new_paths, loops)
            else:
                if s1.id == s2.id: #and s1 in left_out:
                    return 'ε'
                else:
                    return ''
        else:
            if randomized_left_out:
                choices = self.states[:]
                for s in left_out:
                    choices.remove(s)
                choice = random.choice(choices)
            else:
                if not window:
                    print('Start state: ', s1.id, ', End state: ', s2.id)
                    print('States currently left out: ', [state.id for state in left_out])
                    choice_id = int(input('Choose a state not listed above to leave out: '))
                    print('\n')
                    for s in self.states:
                        if s.id == choice_id:
                            choice = s
                            break
                else:
                    win = ToRegExWindow(self, s1, s2, left_out)
                    win.connect("destroy", Gtk.main_quit)
                    win.show_all()
                    Gtk.main()
                    choice = self.choice

            new_left_out = left_out[:] + [choice]
            #print(s1.id, s2.id, choice.id)
            if s1.id == s2.id and s1 == choice: #and s1 in self.accept_states and s1 == self.start_state :
                empty_path = 'ε + '
            else:
                empty_path = ''

            if s1.id == choice.id and choice.id == s2.id:
                uv = self.make_paths(new_left_out, s1, s2, randomized_left_out, window)
                qv = uv[:]
                uq = uv[:]
                qq = uv[:]
            elif s1.id == choice.id:
                uv = self.make_paths(new_left_out, s1, s2, randomized_left_out, window)
                qv = uv[:]
                uq = self.make_paths(new_left_out, s1, choice, randomized_left_out, window)
                qq = uq[:]
            elif s2.id == choice.id:
                uv = self.make_paths(new_left_out, s1, s2, randomized_left_out, window)
                uq = uv[:]
                qq = self.make_paths(new_left_out, choice, choice, randomized_left_out, window)
                qv = qq[:]
            else:
                uv = self.make_paths(new_left_out, s1, s2, randomized_left_out, window)
                uq = self.make_paths(new_left_out, s1, choice, randomized_left_out, window)
                qq = self.make_paths(new_left_out, choice, choice, randomized_left_out, window)
                qv = self.make_paths(new_left_out, choice, s2, randomized_left_out, window)
            if len(uv) > 0 and len(uq) * len(qq) * len(qv) > 0:
                uv = uv + ' + '
            if len(uq) > 0:
                uq = '(' + uq + ')'
            else:
                return empty_path + uv
            if len(qq) > 0:
                qq = '(' + qq + ')*'
            else:
                return empty_path + uv
            if len(qv) > 0:
                qv = '(' + qv + ')'
            else:
                return empty_path + uv
            return empty_path + uv + uq + qq + qv

    def all_regex(self,randomized_left_out=True, window=False):
        exps = []
        for acc in self.accept_states:
            exp = self.make_paths([], self.start_state, acc, randomized_left_out, window)
            exps.append(exp)
        self.regex = ' + '.join(exps)
        return self.regex

    def remove_unreachable(self):
        reachable = set([self.start_state])
        state_set = set([self.start_state])
        while len(state_set) > 0:
            new_state_set = set()
            for s in state_set:
                for s2 in s.outpaths.values():
                    if s2 not in reachable:
                        reachable.add(s2)
                        new_state_set.add(s2)
            state_set = new_state_set
        self.states = list(reachable)
        self.accept_states = [a for a in self.accept_states if a in self.states]

    def minimize(self):
        i = 0
        for st in self.states:
            st.index = i
            i += 1

        num_states = len(self.states)
        self.matrix = [[None for _ in range(num_states)] for _ in range(num_states)]

        for i in range(num_states):
            is_acc = True if self.states[i] in self.accept_states else False
            for j in range(i+1, num_states):
                if self.states[j] in self.accept_states:
                    if not is_acc:
                        self.matrix[i][j] = 0
                else:
                    if is_acc:
                        self.matrix[i][j] = 0

        round_num = 1
        cont = True
        while cont:
            cont = False
            for i in range(num_states):
                for j in range(i+1, num_states):
                    if self.matrix[i][j] is None:
                        for sym in self.alphabet:
                            s1 = self.states[i].outpaths[sym] if sym in self.states[i].outpaths else None
                            s2 = self.states[j].outpaths[sym] if sym in self.states[j].outpaths else None
                            if s1 is not None and s2 is not None:
                                maxid1 = max(s1.index, self.states[i].index)
                                maxid2 = max(s2.index, self.states[j].index)
                                minid1 = min(s1.index, self.states[i].index)
                                minid2 = min(s2.index, self.states[j].index)
                                x1 = self.matrix[minid1][maxid1]
                                x2 = self.matrix[minid2][maxid2]
                                if x1 is None or x1 == round_num:
                                    if x2 is not None and x2 < round_num:
                                        self.matrix[i][j] = round_num
                                        cont = True
                                        break
                                elif x2 is None or x2 == round_num:
                                    if x1 is not None and x1 < round_num:
                                        self.matrix[i][j] = round_num
                                        cont = True
                                        break
                            elif (s1 is None and s2 is not None) or (s1 is not None and s2 is None):
                                self.matrix[i][j] = round_num
                                cont = True
                                break
            round_num += 1

        unique = 0
        count = 0
        for i in range(num_states):
            for j in range(i+1, num_states):
                if self.matrix[i][j] is not None:
                    unique += 1
                count += 1

        if unique == count:
            print('Your DFA is already minimized.')
            return

        self.new_states = {}
        count = num_states
        for i in range(num_states):
            for j in range(i+1, num_states):
                if self.matrix[i][j] is None:
                    found = False
                    for key, val in self.new_states.items():
                        if self.states[i] in val and self.states[j] not in val:
                            self.new_states[key].add(self.states[j])
                            found = True
                            break
                        elif self.states[j] in val and self.states[i] not in val:
                            self.new_states[key].add(self.states[j])
                            found = True
                            break
                        elif self.states[j] in val and self.states[i] in val:
                            found = True
                            break
                    if not found:
                        self.new_states[state(count)] = {self.states[i], self.states[j]}
                        count += 1

        existing_states = set()
        for key, val in self.new_states.items():
            existing_states = existing_states.union(val)
        missing_states = set(self.states).difference(existing_states)

        for st in missing_states:
            self.new_states[st] = {st}

        self.new_start_state = None
        self.new_acc_states = []
        for new,old in self.new_states.items():
            for s in old:
                if s.id == self.start_state.id:
                    self.new_start_state = new
                if s in self.accept_states and new not in self.new_acc_states:
                    self.new_acc_states.append(new)
            for key, val in s.outpaths.items():
                for new2,old2 in self.new_states.items():
                    if val in old2:
                        new.outpaths[key] = new2

        self.states = [key for key in self.new_states]
        self.start_state = self.new_start_state
        self.accept_states = self.new_acc_states
        self.remove_unreachable()
