# Source: https://github.com/dabeaz/sly/blob/master/tests/test_parser.py

from sly import Lexer


class ProcessorLexer(Lexer):
    """
        It is class that describes syntax at lexer
    """
    # Set of token names.   This is always required
    tokens = {ID, NUMBER, PLUS, MINUS, TIMES, DIVIDE,
              ASSIGN, COMMA, GT, LT, EQ, NE, GE, LE,
              AND, OR, NOT, IN}

    literals = {'(', ')'}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    AND     = r'and'
    NOT     = r'not'
    OR      = r'or'
    IN      = r'in'
    ID      = r'[a-zA-Z_][a-zA-Z0-9_@]*'
    EQ      = r'=='
    NE      = r'!='
    GE      = r'>='
    LE      = r'<='
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    COMMA   = r','
    GT      = r'>'
    LT      = r'<'

    @_(r'0x[0-9a-fA-F]+',
       r'0b[01]+',
       r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        elif t.value.startswith('0b'):
            t.value = int(t.value[2:], 2)
        else:
            t.value = int(t.value)
        return t

    # Ignored text
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.errors.append(t.value[0])
        self.index += 1

    def __init__(self):
        self.errors = []

