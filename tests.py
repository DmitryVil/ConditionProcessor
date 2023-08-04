from syntax_processor_parser import ProcessorLexer, ProcessorParser

# Test basic recognition of various tokens and literals


def test_simple():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('a = 3 + 4 * (5 + 6)'))
    assert result is None
    assert parser.names['a'] == 47

    result = parser.parse(lexer.tokenize('3 + 4 * (5 + 6)'))
    assert result == 47

    result = parser.parse(lexer.tokenize('-5 - 10'))
    assert result == -15

    result = parser.parse(lexer.tokenize('-5 - -10'))
    assert result == 5

    result = parser.parse(lexer.tokenize('-5 - (-10)'))
    assert result == 5


def test_ebnf():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('a()'))
    assert result == ('a', None)
    assert not parser.errors

    result = parser.parse(lexer.tokenize('a(2+3)'))
    assert result == ('a', [5])
    assert not parser.errors

    result = parser.parse(lexer.tokenize('a(2+3, 4+5)'))
    assert result == ('a', [5, 9])
    assert not parser.errors


def test_hex_and_binary_integers():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    number = 10
    result = parser.parse(lexer.tokenize(str(bin(number))))
    assert result == number
    assert not parser.errors

    number = 10
    result = parser.parse(lexer.tokenize(str(hex(number))))
    assert result == number
    assert not parser.errors


def test_parse_error():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('a 123 4 + 5'))
    assert result == 9
    assert len(parser.errors) == 1
    assert parser.errors[0].type == 'NUMBER'
    assert parser.errors[0].value == 123


def test_parse_logical_operations():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('5 > 3'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('3 > 5'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('3 < 5'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('3 < 2'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('2 == 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('3 == 2'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('3 != 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('2 != 2'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('3 >= 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('2 >= 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('1 >= 2'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('1 <= 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('2 <= 2'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('3 <= 2'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('1 <= 2 < 3'))
    assert result is True
    assert not parser.errors
    result = parser.parse(lexer.tokenize('1 <= 2 > 3'))
    assert result is False
    assert not parser.errors


def test_parse_logical_operator_and():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('(5 > 3) and (8 > 4 + 2)'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(5 > 3) and (5 < 4)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(5 < 3) and (5 > 4)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(5 < 3) and (5 < 4)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('((((((5 != 3) and ((5 < 3) and (5 < 4)))) '
                                         'and ((5 < 3) and (5 < 4)))) and ((5 != 3) '
                                         'and ((5 < 3) and (5 < 4)))) and (5 < 4)'))
    assert result is False
    assert not parser.errors


def test_parse_logical_operator_or():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('(5 == 5) or (5 == 5)'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(5 == 5) or (5 == 4)'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(5 == 4) or (5 == 5)'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(50 < 30) or (50 < 40)'))
    assert result is False
    assert not parser.errors


def test_parse_logical_operator_not():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('not (5 < 4)'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('not (5 == 5)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('not (5 == 5) and not (5 == 5)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('not (5 == 5) or not (5 == 5)'))
    assert result is False
    assert not parser.errors

    result = parser.parse(lexer.tokenize('not (not (5 == 5) or not (5 == 5)) or (5 == 4)'))
    assert result is True
    assert not parser.errors


def test_parse_operation_in_the_list():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('[8, 9]'))
    assert result == [8, 9]
    assert not parser.errors

    result = parser.parse(lexer.tokenize('[8, 9]'))
    assert result != [9, 9]
    assert not parser.errors

    result = parser.parse(lexer.tokenize('[8, 9, 10]'))
    assert result == [8, 9, 10]
    assert not parser.errors

    result = parser.parse(lexer.tokenize('[8, 9, 10, 11]'))
    assert result == [8, 9, 10, 11]
    assert not parser.errors


def test_parse_operation_in_the_list_with_error():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('a(2, 9)'))
    assert result == ('a', [2, 9])
    assert not parser.errors

    result = parser.parse(lexer.tokenize('[8, 9, 10,, b, 11]'))
    assert result != [8, 9, 10, 11]
    assert parser.errors


def test_parse_operation_IN_with_the_list():
    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('2 in [2, 3]'))
    assert result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('2 in [2, 3,4,    5,6]'))
    assert result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('3 in [2, 3]'))
    assert result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('4 in [2, 3]'))
    assert not result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    assert not result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('a in [2, 3]'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('a in [4, 3]'))
    assert result is False
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(a in [2, 3])'))
    assert result is True
    assert not parser.errors
    assert not hasattr(parser, 'errorok')

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('(2 in [2, 3])'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('(((2 in [2, 3])))'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('AAA_Bbb_@ = 2'))
    result = parser.parse(lexer.tokenize('(AAA_Bbb_@ in [2, 3])'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('AAA_Bbb_@ = 4'))
    result = parser.parse(lexer.tokenize('(AAA_Bbb_@ in [2, 3])'))
    assert result is False
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('((a in [2, 3]))'))
    assert result is True
    assert not parser.errors
    assert not hasattr(parser, 'errorok')

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(((a in [2, 3])))'))
    assert result is True
    assert not parser.errors
    assert not hasattr(parser, 'errorok')

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('a in [2, 3] and (a < 3 or 1 > a)'))
    assert result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('a in [2, 3] == (a in [2, 3] and 1 == 1)'))
    assert result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('b = (a in [2, 3])'))
    result = parser.parse(lexer.tokenize('c = (a < 4) or (1 > a)'))
    result = parser.parse(lexer.tokenize('c and b'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('((a < 4) or (1 > a)) and (a in [2, 3])'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(a in [2, 3] and 1 < 2) and ((a < 3) or (1 > a))'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(a < 3) or (1 > a)'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(a < 3) or (1 > a)'))
    assert result is True
    assert not parser.errors


    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('2 in [3, 3]'))
    assert not result
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('2 in [a, 3]'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('1 in [a/2, 3]'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('4 in [(a/2)*4, 3]'))
    assert result is True
    assert not parser.errors

    #####################################################################################
    ##################  It shows solved problem with precedence  ######################
    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(0 < 3 or 1 > a)'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(2 < 3 or 1 > a)'))
    assert result is True
    assert not parser.errors
    #####################################################################################


def test_parse_operation_unknown_variables():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('b in [2, 3] and (c < 3)'))
    assert not result
    assert parser.errors


def test_parse_operation_with_parentheses():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('2 + (3)'))
    assert result == 5
    assert not parser.errors

    result = parser.parse(lexer.tokenize('2 + ((3))'))
    assert result == 5
    assert not parser.errors

    result = parser.parse(lexer.tokenize('((((3))))'))
    assert result == 3
    assert not parser.errors


def test_parse_operation_list_in_nested_parentheses():
    lexer = ProcessorLexer()
    parser = ProcessorParser()

    result = parser.parse(lexer.tokenize('([2, 3])'))
    assert result == [2, 3]
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(([2, 3]))'))
    assert result == [2, 3]
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(((((((([2, 3]))))))))'))
    assert result == [2, 3]
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 1'))
    result = parser.parse(lexer.tokenize('a == (a) == ((a))'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('2 + 2 == (2 + 2)'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('(2 + 2 == (((2 + 2))))'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('(2 + 2) == ((2 + 2))'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('((2 + 2) == ((2 + 2)))'))
    assert result is True
    assert not parser.errors

    result = parser.parse(lexer.tokenize('(((((((([2, 3])))))))'))
    assert result is None
    assert parser.errors

def test_parse_operations_with_precedence():
    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('3 + 4 * 5'))
    assert result == 23
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('(1 + 4) > (4 + 0)'))
    assert result is True
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('-5 + 10'))
    assert result == 5
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('-5 - 10'))
    assert result == -15
    assert not parser.errors

    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('4 + 1 > 4 + 0'))
    assert result is True
    assert not parser.errors




    lexer = ProcessorLexer()
    parser = ProcessorParser()
    result = parser.parse(lexer.tokenize('a = 2'))
    result = parser.parse(lexer.tokenize('(2 < 3 or 1 > a)'))
    assert result is True
    assert not parser.errors




