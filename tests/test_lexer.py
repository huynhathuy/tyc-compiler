"""
Lexer test cases for TyC compiler
100 test cases covering all lexical elements of TyC language
"""

import pytest
from tests.utils import Tokenizer


# ============================================================================
# KEYWORDS (Tests 1-16)
# ============================================================================

def test_keyword_auto():
    """1. Keyword: auto"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_keyword_break():
    """2. Keyword: break"""
    tokenizer = Tokenizer("break")
    assert tokenizer.get_tokens_as_string() == "break,<EOF>"


def test_keyword_case():
    """3. Keyword: case"""
    tokenizer = Tokenizer("case")
    assert tokenizer.get_tokens_as_string() == "case,<EOF>"


def test_keyword_continue():
    """4. Keyword: continue"""
    tokenizer = Tokenizer("continue")
    assert tokenizer.get_tokens_as_string() == "continue,<EOF>"


def test_keyword_default():
    """5. Keyword: default"""
    tokenizer = Tokenizer("default")
    assert tokenizer.get_tokens_as_string() == "default,<EOF>"


def test_keyword_else():
    """6. Keyword: else"""
    tokenizer = Tokenizer("else")
    assert tokenizer.get_tokens_as_string() == "else,<EOF>"


def test_keyword_float():
    """7. Keyword: float"""
    tokenizer = Tokenizer("float")
    assert tokenizer.get_tokens_as_string() == "float,<EOF>"


def test_keyword_for():
    """8. Keyword: for"""
    tokenizer = Tokenizer("for")
    assert tokenizer.get_tokens_as_string() == "for,<EOF>"


def test_keyword_if():
    """9. Keyword: if"""
    tokenizer = Tokenizer("if")
    assert tokenizer.get_tokens_as_string() == "if,<EOF>"


def test_keyword_int():
    """10. Keyword: int"""
    tokenizer = Tokenizer("int")
    assert tokenizer.get_tokens_as_string() == "int,<EOF>"


def test_keyword_return():
    """11. Keyword: return"""
    tokenizer = Tokenizer("return")
    assert tokenizer.get_tokens_as_string() == "return,<EOF>"


def test_keyword_string():
    """12. Keyword: string"""
    tokenizer = Tokenizer("string")
    assert tokenizer.get_tokens_as_string() == "string,<EOF>"


def test_keyword_struct():
    """13. Keyword: struct"""
    tokenizer = Tokenizer("struct")
    assert tokenizer.get_tokens_as_string() == "struct,<EOF>"


def test_keyword_switch():
    """14. Keyword: switch"""
    tokenizer = Tokenizer("switch")
    assert tokenizer.get_tokens_as_string() == "switch,<EOF>"


def test_keyword_void():
    """15. Keyword: void"""
    tokenizer = Tokenizer("void")
    assert tokenizer.get_tokens_as_string() == "void,<EOF>"


def test_keyword_while():
    """16. Keyword: while"""
    tokenizer = Tokenizer("while")
    assert tokenizer.get_tokens_as_string() == "while,<EOF>"


# ============================================================================
# OPERATORS (Tests 17-37)
# ============================================================================

def test_operator_plus():
    """17. Operator: +"""
    tokenizer = Tokenizer("+")
    assert tokenizer.get_tokens_as_string() == "+,<EOF>"


def test_operator_minus():
    """18. Operator: -"""
    tokenizer = Tokenizer("-")
    assert tokenizer.get_tokens_as_string() == "-,<EOF>"


def test_operator_mul():
    """19. Operator: *"""
    tokenizer = Tokenizer("*")
    assert tokenizer.get_tokens_as_string() == "*,<EOF>"


def test_operator_div():
    """20. Operator: /"""
    tokenizer = Tokenizer("/")
    assert tokenizer.get_tokens_as_string() == "/,<EOF>"


def test_operator_mod():
    """21. Operator: %"""
    tokenizer = Tokenizer("%")
    assert tokenizer.get_tokens_as_string() == "%,<EOF>"


def test_operator_eq():
    """22. Operator: =="""
    tokenizer = Tokenizer("==")
    assert tokenizer.get_tokens_as_string() == "==,<EOF>"


def test_operator_neq():
    """23. Operator: !="""
    tokenizer = Tokenizer("!=")
    assert tokenizer.get_tokens_as_string() == "!=,<EOF>"


def test_operator_lt():
    """24. Operator: <"""
    tokenizer = Tokenizer("<")
    assert tokenizer.get_tokens_as_string() == "<,<EOF>"


def test_operator_gt():
    """25. Operator: >"""
    tokenizer = Tokenizer(">")
    assert tokenizer.get_tokens_as_string() == ">,<EOF>"


def test_operator_leq():
    """26. Operator: <="""
    tokenizer = Tokenizer("<=")
    assert tokenizer.get_tokens_as_string() == "<=,<EOF>"


def test_operator_geq():
    """27. Operator: >="""
    tokenizer = Tokenizer(">=")
    assert tokenizer.get_tokens_as_string() == ">=,<EOF>"


def test_operator_and():
    """28. Operator: &&"""
    tokenizer = Tokenizer("&&")
    assert tokenizer.get_tokens_as_string() == "&&,<EOF>"


def test_operator_or():
    """29. Operator: ||"""
    tokenizer = Tokenizer("||")
    assert tokenizer.get_tokens_as_string() == "||,<EOF>"


def test_operator_not():
    """30. Operator: !"""
    tokenizer = Tokenizer("!")
    assert tokenizer.get_tokens_as_string() == "!,<EOF>"


def test_operator_inc():
    """31. Operator: ++"""
    tokenizer = Tokenizer("++")
    assert tokenizer.get_tokens_as_string() == "++,<EOF>"


def test_operator_dec():
    """32. Operator: --"""
    tokenizer = Tokenizer("--")
    assert tokenizer.get_tokens_as_string() == "--,<EOF>"


def test_operator_assign():
    """33. Operator: ="""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_operator_dot():
    """34. Operator: ."""
    tokenizer = Tokenizer(".")
    assert tokenizer.get_tokens_as_string() == ".,<EOF>"


def test_operators_combined():
    """35. Multiple operators together"""
    tokenizer = Tokenizer("+ - * /")
    assert tokenizer.get_tokens_as_string() == "+,-,*,/,<EOF>"


def test_operators_no_space():
    """36. Operators without spaces"""
    tokenizer = Tokenizer("a+b*c")
    assert tokenizer.get_tokens_as_string() == "a,+,b,*,c,<EOF>"


def test_comparison_chain():
    """37. Comparison operators"""
    tokenizer = Tokenizer("< <= > >= == !=")
    assert tokenizer.get_tokens_as_string() == "<,<=,>,>=,==,!=,<EOF>"


# ============================================================================
# SEPARATORS (Tests 38-44)
# ============================================================================

def test_separator_lbrace():
    """38. Separator: {"""
    tokenizer = Tokenizer("{")
    assert tokenizer.get_tokens_as_string() == "{,<EOF>"


def test_separator_rbrace():
    """39. Separator: }"""
    tokenizer = Tokenizer("}")
    assert tokenizer.get_tokens_as_string() == "},<EOF>"


def test_separator_lparen():
    """40. Separator: ("""
    tokenizer = Tokenizer("(")
    assert tokenizer.get_tokens_as_string() == "(,<EOF>"


def test_separator_rparen():
    """41. Separator: )"""
    tokenizer = Tokenizer(")")
    assert tokenizer.get_tokens_as_string() == "),<EOF>"


def test_separator_semi():
    """42. Separator: ;"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_separator_comma():
    """43. Separator: ,"""
    tokenizer = Tokenizer(",")
    assert tokenizer.get_tokens_as_string() == ",,<EOF>"


def test_separator_colon():
    """44. Separator: :"""
    tokenizer = Tokenizer(":")
    assert tokenizer.get_tokens_as_string() == ":,<EOF>"


# ============================================================================
# INTEGER LITERALS (Tests 45-52)
# ============================================================================

def test_integer_zero():
    """45. Integer: zero"""
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"


def test_integer_single_digit():
    """46. Integer: single digit"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_integer_multiple_digits():
    """47. Integer: multiple digits"""
    tokenizer = Tokenizer("12345")
    assert tokenizer.get_tokens_as_string() == "12345,<EOF>"


def test_integer_large_number():
    """48. Integer: large number"""
    tokenizer = Tokenizer("999999999")
    assert tokenizer.get_tokens_as_string() == "999999999,<EOF>"


def test_integer_leading_zeros():
    """49. Integer: leading zeros (treated as single number)"""
    tokenizer = Tokenizer("007")
    assert tokenizer.get_tokens_as_string() == "007,<EOF>"


def test_integer_sequence():
    """50. Integer: sequence of integers"""
    tokenizer = Tokenizer("1 2 3")
    assert tokenizer.get_tokens_as_string() == "1,2,3,<EOF>"


def test_integer_in_expression():
    """51. Integer: in arithmetic expression"""
    tokenizer = Tokenizer("10+20")
    assert tokenizer.get_tokens_as_string() == "10,+,20,<EOF>"


def test_integer_with_parentheses():
    """52. Integer: with parentheses"""
    tokenizer = Tokenizer("(42)")
    assert tokenizer.get_tokens_as_string() == "(,42,),<EOF>"


# ============================================================================
# FLOAT LITERALS (Tests 53-64)
# ============================================================================

def test_float_simple():
    """53. Float: simple decimal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_float_zero():
    """54. Float: zero point zero"""
    tokenizer = Tokenizer("0.0")
    assert tokenizer.get_tokens_as_string() == "0.0,<EOF>"


def test_float_trailing_dot():
    """55. Float: trailing dot (1.)"""
    tokenizer = Tokenizer("1.")
    assert tokenizer.get_tokens_as_string() == "1.,<EOF>"


def test_float_leading_dot():
    """56. Float: leading dot (.5)"""
    tokenizer = Tokenizer(".5")
    assert tokenizer.get_tokens_as_string() == ".5,<EOF>"


def test_float_exponent_lowercase():
    """57. Float: with lowercase exponent"""
    tokenizer = Tokenizer("1e5")
    assert tokenizer.get_tokens_as_string() == "1e5,<EOF>"


def test_float_exponent_uppercase():
    """58. Float: with uppercase exponent"""
    tokenizer = Tokenizer("2E3")
    assert tokenizer.get_tokens_as_string() == "2E3,<EOF>"


def test_float_exponent_positive():
    """59. Float: exponent with positive sign"""
    tokenizer = Tokenizer("1.5e+10")
    assert tokenizer.get_tokens_as_string() == "1.5e+10,<EOF>"


def test_float_exponent_negative():
    """60. Float: exponent with negative sign"""
    tokenizer = Tokenizer("5.67E-2")
    assert tokenizer.get_tokens_as_string() == "5.67E-2,<EOF>"


def test_float_leading_dot_with_exponent():
    """61. Float: leading dot with exponent"""
    tokenizer = Tokenizer(".5e10")
    assert tokenizer.get_tokens_as_string() == ".5e10,<EOF>"


def test_float_trailing_dot_with_exponent():
    """62. Float: trailing dot with exponent"""
    tokenizer = Tokenizer("1.e5")
    assert tokenizer.get_tokens_as_string() == "1.e5,<EOF>"


def test_float_only_exponent():
    """63. Float: integer with exponent only"""
    tokenizer = Tokenizer("2E-3")
    assert tokenizer.get_tokens_as_string() == "2E-3,<EOF>"


def test_float_sequence():
    """64. Float: multiple floats"""
    tokenizer = Tokenizer("1.0 2.5 3.14")
    assert tokenizer.get_tokens_as_string() == "1.0,2.5,3.14,<EOF>"


# ============================================================================
# STRING LITERALS (Tests 65-74)
# ============================================================================

def test_string_simple():
    """65. String: simple string"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_string_empty():
    """66. String: empty string"""
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == ",<EOF>"


def test_string_with_spaces():
    """67. String: with spaces"""
    tokenizer = Tokenizer('"hello world"')
    assert tokenizer.get_tokens_as_string() == "hello world,<EOF>"


def test_string_escape_newline():
    """68. String: escape newline \\n"""
    tokenizer = Tokenizer('"line1\\nline2"')
    assert tokenizer.get_tokens_as_string() == "line1\\nline2,<EOF>"


def test_string_escape_tab():
    """69. String: escape tab \\t"""
    tokenizer = Tokenizer('"tab\\there"')
    assert tokenizer.get_tokens_as_string() == "tab\\there,<EOF>"


def test_string_escape_backslash():
    """70. String: escape backslash \\\\"""
    tokenizer = Tokenizer('"path\\\\file"')
    assert tokenizer.get_tokens_as_string() == "path\\\\file,<EOF>"


def test_string_escape_quote():
    """71. String: escape quote"""
    tokenizer = Tokenizer('"He said \\"Hi\\""')
    assert tokenizer.get_tokens_as_string() == 'He said \\"Hi\\",<EOF>'


def test_string_escape_carriage_return():
    """72. String: escape carriage return \\r"""
    tokenizer = Tokenizer('"test\\rvalue"')
    assert tokenizer.get_tokens_as_string() == "test\\rvalue,<EOF>"


def test_string_escape_backspace():
    """73. String: escape backspace \\b"""
    tokenizer = Tokenizer('"back\\bspace"')
    assert tokenizer.get_tokens_as_string() == "back\\bspace,<EOF>"


def test_string_escape_formfeed():
    """74. String: escape formfeed \\f"""
    tokenizer = Tokenizer('"form\\ffeed"')
    assert tokenizer.get_tokens_as_string() == "form\\ffeed,<EOF>"


# ============================================================================
# IDENTIFIERS (Tests 75-82)
# ============================================================================

def test_identifier_single_letter():
    """75. Identifier: single letter"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_identifier_uppercase():
    """76. Identifier: uppercase"""
    tokenizer = Tokenizer("MyVar")
    assert tokenizer.get_tokens_as_string() == "MyVar,<EOF>"


def test_identifier_with_digits():
    """77. Identifier: with digits"""
    tokenizer = Tokenizer("var123")
    assert tokenizer.get_tokens_as_string() == "var123,<EOF>"


def test_identifier_underscore_start():
    """78. Identifier: starting with underscore"""
    tokenizer = Tokenizer("_private")
    assert tokenizer.get_tokens_as_string() == "_private,<EOF>"


def test_identifier_underscore_only():
    """79. Identifier: underscore only"""
    tokenizer = Tokenizer("_")
    assert tokenizer.get_tokens_as_string() == "_,<EOF>"


def test_identifier_mixed_case():
    """80. Identifier: mixed case"""
    tokenizer = Tokenizer("camelCase")
    assert tokenizer.get_tokens_as_string() == "camelCase,<EOF>"


def test_identifier_all_uppercase():
    """81. Identifier: all uppercase"""
    tokenizer = Tokenizer("CONSTANT")
    assert tokenizer.get_tokens_as_string() == "CONSTANT,<EOF>"


def test_identifier_with_multiple_underscores():
    """82. Identifier: multiple underscores"""
    tokenizer = Tokenizer("my_var_name")
    assert tokenizer.get_tokens_as_string() == "my_var_name,<EOF>"


# ============================================================================
# COMMENTS (Tests 83-88)
# ============================================================================

def test_comment_line_simple():
    """83. Line comment: simple"""
    tokenizer = Tokenizer("// comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_line_before_code():
    """84. Line comment: before code"""
    tokenizer = Tokenizer("x // comment\ny")
    assert tokenizer.get_tokens_as_string() == "x,y,<EOF>"


def test_comment_block_simple():
    """85. Block comment: simple"""
    tokenizer = Tokenizer("/* comment */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_block_multiline():
    """86. Block comment: multiline"""
    tokenizer = Tokenizer("/* line1\nline2 */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_block_inline():
    """87. Block comment: inline"""
    tokenizer = Tokenizer("x /* comment */ y")
    assert tokenizer.get_tokens_as_string() == "x,y,<EOF>"


def test_comment_line_with_block_marker():
    """88. Line comment containing block comment marker"""
    tokenizer = Tokenizer("// /* not a block */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


# ============================================================================
# ERROR CASES (Tests 89-96)
# ============================================================================

def test_error_unrecognized_char():
    """89. Error: unrecognized character"""
    tokenizer = Tokenizer("@")
    assert "Error Token @" in tokenizer.get_tokens_as_string()


def test_error_unrecognized_hash():
    """90. Error: hash symbol"""
    tokenizer = Tokenizer("#")
    assert "Error Token #" in tokenizer.get_tokens_as_string()


def test_error_unclosed_string_newline():
    """91. Error: unclosed string (newline)"""
    tokenizer = Tokenizer('"hello\n')
    assert "Unclosed String: hello" in tokenizer.get_tokens_as_string()


def test_error_unclosed_string_eof():
    """92. Error: unclosed string (EOF)"""
    tokenizer = Tokenizer('"hello')
    assert "Unclosed String: hello" in tokenizer.get_tokens_as_string()


def test_error_illegal_escape_a():
    """93. Error: illegal escape \\a"""
    tokenizer = Tokenizer('"test\\a"')
    assert "Illegal Escape In String: test\\a" in tokenizer.get_tokens_as_string()


def test_error_illegal_escape_x():
    """94. Error: illegal escape \\x"""
    tokenizer = Tokenizer('"path\\x"')
    assert "Illegal Escape In String: path\\x" in tokenizer.get_tokens_as_string()


def test_error_illegal_escape_digit():
    """95. Error: illegal escape with digit"""
    tokenizer = Tokenizer('"test\\1abc"')
    assert "Illegal Escape In String: test\\1" in tokenizer.get_tokens_as_string()


def test_error_illegal_escape_space():
    """96. Error: illegal escape with space"""
    tokenizer = Tokenizer('"test\\ abc"')
    assert "Illegal Escape In String: test\\ " in tokenizer.get_tokens_as_string()


# ============================================================================
# COMPLEX/COMBINED CASES (Tests 97-100)
# ============================================================================

def test_complex_variable_declaration():
    """97. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"


def test_complex_function_signature():
    """98. Complex: function signature"""
    tokenizer = Tokenizer("int add(int a, int b)")
    assert tokenizer.get_tokens_as_string() == "int,add,(,int,a,,,int,b,),<EOF>"


def test_complex_for_loop():
    """99. Complex: for loop"""
    tokenizer = Tokenizer("for(int i=0; i<10; i++)")
    assert tokenizer.get_tokens_as_string() == "for,(,int,i,=,0,;,i,<,10,;,i,++,),<EOF>"


def test_complex_struct_access():
    """100. Complex: struct member access"""
    tokenizer = Tokenizer("point.x = point.y + 1;")
    assert tokenizer.get_tokens_as_string() == "point,.,x,=,point,.,y,+,1,;,<EOF>"
