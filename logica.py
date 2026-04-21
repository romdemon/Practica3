import os
from collections import defaultdict, deque

class Automata:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def lambda_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.transitions and 'λ' in self.transitions[state]:
                for next_state in self.transitions[state]['λ']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def simulate_step(self, current_states, symbol):
        next_states = set()
        for state in current_states:
            if state in self.transitions and symbol in self.transitions[state]:
                next_states.update(self.transitions[state][symbol])
        return self.lambda_closure(next_states)

    def simulate_word(self, word):
        current_states = self.lambda_closure({self.start_state})
        history = [current_states.copy()]
        for symbol in word:
            current_states = self.simulate_step(current_states, symbol)
            history.append(current_states.copy())
        is_accepted = any(state in self.accept_states for state in current_states)
        return is_accepted, history

def nfa_to_dfa(nfa: Automata):
    dfa_states = []
    dfa_transitions = defaultdict(dict)
    dfa_accept = set()
    
    start_closure = frozenset(nfa.lambda_closure({nfa.start_state}))
    dfa_states.append(start_closure)
    unprocessed = [start_closure]
    
    while unprocessed:
        current = unprocessed.pop(0)
        if any(s in nfa.accept_states for s in current):
            dfa_accept.add(current)
            
        for symbol in nfa.alphabet:
            if symbol == 'λ': continue
            next_state_set = frozenset(nfa.simulate_step(current, symbol))
            if not next_state_set: continue
            
            dfa_transitions[current][symbol] = {next_state_set}
            if next_state_set not in dfa_states:
                dfa_states.append(next_state_set)
                unprocessed.append(next_state_set)
                
    name_map = {state: f"S{i}" for i, state in enumerate(dfa_states)}
    new_trans = {}
    for state, paths in dfa_transitions.items():
        new_trans[name_map[state]] = {sym: {name_map[next_s.copy().pop()]} for sym, next_s in paths.items()}
        
    return Automata(
        states=set(name_map.values()),
        alphabet=nfa.alphabet - {'λ'},
        transitions=new_trans,
        start_state=name_map[start_closure],
        accept_states={name_map[s] for s in dfa_accept}
    )

def minimize_dfa(dfa: Automata):
    # 1. Eliminar estados inaccesibles
    reachable = set()
    queue = deque([dfa.start_state])
    while queue:
        state = queue.popleft()
        if state not in reachable:
            reachable.add(state)
            if state in dfa.transitions:
                for symbol, next_states in dfa.transitions[state].items():
                    for ns in next_states: queue.append(ns)
                    
    # 2. Algoritmo de Hopcroft
    accept = reachable & dfa.accept_states
    non_accept = reachable - dfa.accept_states
    P = [accept, non_accept] if non_accept else [accept]
    W = [accept, non_accept] if non_accept else [accept]

    reverse_trans = defaultdict(lambda: defaultdict(set))
    for state in reachable:
        if state in dfa.transitions:
            for sym, targets in dfa.transitions[state].items():
                for t in targets: reverse_trans[t][sym].add(state)

    while W:
        A = W.pop(0)
        if not A: continue
        for c in dfa.alphabet:
            X = set()
            for state in A: X.update(reverse_trans[state][c])
            if not X: continue
            
            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    new_P.append(inter)
                    new_P.append(diff)
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        W.append(inter if len(inter) <= len(diff) else diff)
                else:
                    new_P.append(Y)
            P = new_P

    # 3. Construcción del nuevo AFD
    P = [group for group in P if group]
    state_map = {list(group)[0]: f"Q{i}" for i, group in enumerate(P)}
    group_map = {s: state_map[list(group)[0]] for group in P for s in group}
    
    new_states = set(state_map.values())
    new_start = group_map.get(dfa.start_state, "")
    new_accept = {group_map[s] for s in dfa.accept_states if s in group_map}
    
    new_trans = defaultdict(dict)
    for group in P:
        rep = list(group)[0]
        if rep in dfa.transitions:
            for sym, targets in dfa.transitions[rep].items():
                target = list(targets)[0]
                if target in group_map:
                    new_trans[group_map[rep]][sym] = {group_map[target]}

    str_partitions = [list(g) for g in P]
    return Automata(new_states, dfa.alphabet, dict(new_trans), new_start, new_accept), str_partitions

def get_substrings(s: str) -> list[str]:
    seen = set()
    result = []
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            sub = s[i:j]
            if sub not in seen:
                seen.add(sub)
                result.append(sub)
    return sorted(result, key=lambda x: (len(x), x))

def get_prefixes(s: str) -> list[str]: return [s[: i + 1] for i in range(len(s))]
def get_suffixes(s: str) -> list[str]: return [s[i:] for i in range(len(s))]

def kleene_star(alphabet: list[str], max_len: int) -> list[str]:
    result = ["ε"]
    queue = [""]
    while queue:
        curr = queue.pop(0)
        for c in alphabet:
            nxt = curr + c
            if len(nxt) <= max_len:
                result.append(nxt)
                queue.append(nxt)
    return result

def kleene_plus(alphabet: list[str], max_len: int) -> list[str]:
    return [s for s in kleene_star(alphabet, max_len) if s != "ε"]

def export_to_file(path: str, content: str):
    if not os.path.isabs(path):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        path = os.path.join(desktop, path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(path)