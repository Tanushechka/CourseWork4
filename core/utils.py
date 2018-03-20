import itertools
import re


class Operator(object):

    @staticmethod
    def and_(a, b):
        for p, q in zip(a, b):
            yield p and q

    @staticmethod
    def or_(a, b):
        for p, q in zip(a, b):
            yield p or q

    @staticmethod
    def not_(a):
        for p in a:
            yield not p

    @staticmethod
    def eq_(a, b):
        for p, q in zip(a, b):
            yield p is q

    @staticmethod
    def imp_(a, b):
        for p, q in zip(a, b):
            yield (not p) or q

    @staticmethod
    def ar_p_(a, b):
        for p, q in zip(a, b):
            yield not any((q, p))

    @staticmethod
    def shf_(a, b):
        for p, q in zip(a, b):
            yield not all((q, p))

    @staticmethod
    def xor_(a, b):
        for p, q in zip(a, b):
            yield q ^ p


class Utils(object):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    OP_OR = '∨'
    OP_AND = '∧'
    OP_XOR = '⊕'
    OP_NOT = '!'
    OP_AR_P = "↓"
    OP_SHEFF = '|'
    OP_IMPL = "→"
    OP_EQ = "↔"
    OP_ATTRIBUTES = {
        OP_NOT: {'prcd': 2, 'fn': Operator.not_},
        OP_OR: {'prcd': 1, 'fn': Operator.or_},
        OP_AND: {'prcd': 1, 'fn': Operator.and_},
        OP_XOR: {'prcd': 1, 'fn': Operator.xor_},
        OP_AR_P: {'prcd': 1, 'fn': Operator.ar_p_},
        OP_SHEFF: {'prcd': 1, 'fn': Operator.shf_},
        OP_IMPL: {'prcd': 1, 'fn': Operator.imp_},
        OP_EQ: {'prcd': 1, 'fn': Operator.eq_},
    }

    SEP_RE = re.compile(r'\s*(%s)\s*' % re.escape('|'.join(map(
        re.escape, list(OP_ATTRIBUTES.keys()) + [LEFT_PAREN, RIGHT_PAREN]))))
    SEP_RE = re.compile()

    @classmethod
    def get_truth_table(cls, n):
        return list(itertools.product((0, 1), repeat=n))
    
    @staticmethod
    def unpack(data):
        return [[elem[i] for elem in lst] for i, lst in enumerate(itertools.tee(data, len(data[0])))]

    @staticmethod
    def is_balanced_brackets(expression):
        opening = tuple('({[')
        closing = tuple(')}]')
        mapping = dict(zip(opening, closing))
        queue = []

        for letter in expression:
            if letter in opening:
                queue.append(mapping[letter])
            elif letter in closing:
                if not queue or letter != queue.pop():
                    return False
        return not queue

    @classmethod
    def tokenize(cls, expr):
        return [t.strip() for t in cls.SEP_RE.split(expr.strip()) if t]

    @classmethod
    def infix2postfix(cls, expression):
        tokens = cls.tokenize(expression)
        op_stack = []
        postfix = []
        for t in tokens:
            if t in cls.OP_ATTRIBUTES:
                while len(op_stack) > 0 and op_stack[-1] in cls.OP_ATTRIBUTES \
                        and cls.OP_ATTRIBUTES[t]['prcd'] <= cls.OP_ATTRIBUTES[op_stack[-1]]['prcd']:
                    postfix.append(op_stack.pop())
                op_stack.append(t)
            elif t == cls.LEFT_PAREN:
                op_stack.append(t)
            elif t == cls.RIGHT_PAREN:
                while op_stack[-1] != cls.LEFT_PAREN:
                    postfix.append(op_stack.pop())
                op_stack.pop()
            else:
                postfix.append(t)
        postfix.extend(reversed(op_stack))
        return postfix
