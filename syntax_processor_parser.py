# Source: https://github.com/dabeaz/sly/blob/master/tests/test_parser.py

from sly import Parser
from syntax_processor_lexer import ProcessorLexer


class ProcessorParser(Parser):
    """
        It is class that describes at a syntax parser
    """
    tokens = ProcessorLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('right', NOT),
        ('left', IN, LT, LE, GT, GE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS))

    def __init__(self):
        self.names = {}
        self.errors = []

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('ID "(" [ arglist ] ")"')
    def statement(self, p):
        return (p.ID, p.arglist)

    @_(' arglist ')
    def statement(self, p):
        return p.arglist

    @_('expr IN arglist ')
    def expr(self, p):
        return p.expr in p.arglist

    @_('"(" [ arglist ] ")"')       # works also as "def expr (self, p):"
    def arglist(self, p):
        return p.arglist

    @_('expr { COMMA expr }')
    def arglist(self, p):
        return [p.expr0, *p.expr1]

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr LT expr')
    def expr(self, p):
        return p.expr0 < p.expr1

    @_('expr EQ expr')
    def expr(self, p):
        return p.expr0 == p.expr1

    @_('expr NE expr')
    def expr(self, p):
        return p.expr0 != p.expr1

    @_('expr GE expr')
    def expr(self, p):
        return p.expr0 >= p.expr1

    @_('expr LE expr')
    def expr(self, p):
        return p.expr0 <= p.expr1

    @_('expr AND expr')
    def expr(self, p):
        return bool(p.expr0) and bool(p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return bool(p.expr0) or bool(p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return not bool(p.expr)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            self.errors.append(('undefined', p.ID))
            return 0

    def error(self, tok):
        self.errors.append(tok)









