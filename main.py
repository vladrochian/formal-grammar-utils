import sys
from typing import List, Tuple, Dict


class Grammar:
    def __init__(self, start: str, non_terminals: str, terminals: str, transitions: List[Tuple[str, str]]):
        self.start = start
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.transitions = transitions


def get_transitions(line: str) -> Tuple[str, List[str]]:
    [first, second] = line.split('=')
    return first, second.split('|')


def read_grammar(path: str) -> Grammar:
    with open(path, 'r') as f:
        start = f.readline().rstrip()
        non_terminals = f.readline().rstrip()
        terminals = f.readline().rstrip()
        lines = [line.rstrip() for line in f.readlines()]
        transitions: List[Tuple[str, str]] = []
        for line in lines:
            from_str, to_strs = get_transitions(line)
            transitions.extend([(from_str, s) for s in to_strs])
        return Grammar(start, non_terminals, terminals, transitions)


def get_word_transitions_from_rule(w: str, from_str: str, to_str: str) -> List[str]:
    pos = w.find(from_str)
    ans: List[str] = []
    while pos != -1:
        new_w = w[:pos] + to_str + w[pos + len(from_str):]
        ans.append(new_w)
        pos = w.find(from_str, pos + 1)
    return ans


def get_word_transitions(g: Grammar, w: str) -> List[str]:
    transitions = list(filter(lambda t: w.find(t[0]) != -1, g.transitions))
    ans: List[str] = []
    for from_str, to_str in transitions:
        ans.extend(get_word_transitions_from_rule(w, from_str, to_str))
    return ans


def is_final(g: Grammar, w: str) -> bool:
    for letter in w:
        if letter not in g.terminals:
            return False
    return True


def generate_words(g: Grammar, depth: int, debug=False):
    q = [g.start]
    q_index = 0
    word_details: Dict[str, Tuple[int, str]] = {g.start: (0, '')}
    final_words: List[str] = []
    while q_index < len(q):
        word = q[q_index]
        q_index += 1
        w_depth, w_parent = word_details[word]
        if w_depth < depth:
            new_words = list(set(get_word_transitions(g, word)))
            for new_word in new_words:
                if new_word not in word_details:
                    if debug:
                        print(f'{word} -> {new_word}')
                    word_details[new_word] = w_depth + 1, word
                    if is_final(g, new_word):
                        final_words.append(new_word)
                    else:
                        q.append(new_word)
        else:
            break
    return final_words


if __name__ == '__main__':
    grammar = read_grammar(sys.argv[1])
    words = generate_words(grammar, 20, True)
    print(words)
