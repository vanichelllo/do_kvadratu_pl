"""Порівняння алгебраїчних виразів для завдань «Вираз»: «2(a+b)», «2a+2b» і «2*a + b*2» — однакові.

Вираз учня ніколи не виконується як код: власний розбір підтримує лише числа, змінні із завдання,
+ − · : / ^, дужки, неявне множення («2a», «3(x+1)») і sqrt(…). Вирази порівнюємо, підставляючи
кілька випадкових значень змінних.
"""
import math
import random
import re

MAX_LENGTH = 100
TOKEN = re.compile(r'\s*(?:(\d+(?:[.,]\d+)?)|(sqrt|√)|([a-zA-Z])|(.))')
REPLACEMENTS = {'−': '-', '–': '-', '·': '*', '×': '*', '∙': '*', ':': '/', '²': '^2', '³': '^3', '÷': '/'}


class ExprError(ValueError):
    pass


def tokenize(text):
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    tokens = []
    for number, func, name, other in TOKEN.findall(text):
        if number:
            tokens.append(('num', float(number.replace(',', '.'))))
        elif func:
            tokens.append(('func', 'sqrt'))
        elif name:
            tokens.append(('var', name))
        elif other.strip():
            if other not in '+-*/^()':
                raise ExprError(f'недозволений символ «{other}»')
            tokens.append(('op', other))
    return tokens


class Parser:
    """Рекурсивний спуск: expr = term (± term)*; term = unary ((*|/|неявне) unary)*; unary = ±unary | power;
    power = atom (^ unary)?; atom = число | змінна | sqrt(expr) | (expr)."""

    def __init__(self, tokens, variables):
        self.tokens, self.pos, self.variables = tokens, 0, variables

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def take(self):
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, op):
        if self.take() != ('op', op):
            raise ExprError(f'очікувалось «{op}»')

    def parse(self):
        node = self.expr()
        if self.pos != len(self.tokens):
            raise ExprError('зайві символи')
        return node

    def expr(self):
        node = self.term()
        while self.peek() in (('op', '+'), ('op', '-')):
            op = self.take()[1]
            node = (op, node, self.term())
        return node

    def term(self):
        node = self.unary()
        while True:
            kind, value = self.peek()
            if (kind, value) in (('op', '*'), ('op', '/')):
                self.take()
                node = (value, node, self.unary())
            elif kind in ('num', 'var', 'func') or (kind, value) == ('op', '('):
                node = ('*', node, self.power())  # неявне множення: 2a, 3(x+1), a b
            else:
                return node

    def unary(self):
        if self.peek() == ('op', '-'):
            self.take()
            return ('neg', self.unary())
        if self.peek() == ('op', '+'):
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        node = self.atom()
        if self.peek() == ('op', '^'):
            self.take()
            node = ('^', node, self.unary())
        return node

    def atom(self):
        kind, value = self.take()
        if kind == 'num':
            return ('num', value)
        if kind == 'var':
            if value not in self.variables:
                raise ExprError(f'невідома змінна «{value}»')
            return ('var', value)
        if kind == 'func':
            if self.peek() == ('op', '('):
                self.take()
                inner = self.expr()
                self.expect(')')
            else:
                inner = self.atom()
            return ('sqrt', inner)
        if (kind, value) == ('op', '('):
            inner = self.expr()
            self.expect(')')
            return inner
        raise ExprError('вираз обірвано')


def evaluate(node, values):
    kind = node[0]
    if kind == 'num':
        return node[1]
    if kind == 'var':
        return values[node[1]]
    if kind == 'neg':
        return -evaluate(node[1], values)
    if kind == 'sqrt':
        inner = evaluate(node[1], values)
        if inner < 0:
            raise ArithmeticError
        return math.sqrt(inner)
    left, right = evaluate(node[1], values), evaluate(node[2], values)
    if kind == '+':
        return left + right
    if kind == '-':
        return left - right
    if kind == '*':
        return left * right
    if kind == '/':
        return left / right
    if abs(right) > 12 or (left < 0 and right != int(right)):
        raise ArithmeticError
    return left ** right


def parse(text, variables):
    text = str(text or '').strip()
    if not text or len(text) > MAX_LENGTH:
        raise ExprError('порожній або задовгий вираз')
    return Parser(tokenize(text), set(variables)).parse()


def expressions_equal(answer, correct, variables, samples=6):
    """Чи дорівнює вираз учня правильному при кількох випадкових значеннях змінних."""
    try:
        student = parse(answer, variables)
    except (ExprError, RecursionError):
        return False
    reference = parse(correct, variables)
    rng = random.Random(f'{correct}|{answer}')
    checked = 0
    for _ in range(samples * 4):
        values = {v: rng.uniform(0.3, 4.7) * rng.choice((1, -1)) for v in variables}
        try:
            expected = evaluate(reference, values)
        except (ArithmeticError, OverflowError):
            continue
        try:
            got = evaluate(student, values)
        except (ArithmeticError, OverflowError):
            return False
        if not math.isclose(got, expected, rel_tol=1e-7, abs_tol=1e-9):
            return False
        checked += 1
        if checked >= samples:
            break
    return checked > 0
