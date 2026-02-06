"""
AST Generation test cases for TyC compiler.
100 test cases covering all AST node types and language constructs.
"""

import pytest
from tests.utils import ASTGenerator


# ============================================================================
# PROGRAM STRUCTURE (Tests 1-5)
# ============================================================================

def test_empty_program():
    """1. Empty program generates Program with empty decls list"""
    source = ""
    ast = ASTGenerator(source).generate()
    assert str(ast) == "Program([])"


def test_program_single_void_function():
    """2. Program with single void function"""
    source = "void main() {}"
    ast = ASTGenerator(source).generate()
    assert str(ast) == "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"


def test_program_multiple_functions():
    """3. Program with multiple functions"""
    source = """
    void foo() {}
    void main() {}
    """
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(VoidType(), foo" in str(ast)
    assert "FuncDecl(VoidType(), main" in str(ast)


def test_program_struct_and_function():
    """4. Program with struct and function"""
    source = """
    struct Point { int x; };
    void main() {}
    """
    ast = ASTGenerator(source).generate()
    assert "StructDecl(Point" in str(ast)
    assert "FuncDecl(VoidType(), main" in str(ast)


def test_program_order_preserved():
    """5. Program preserves declaration order"""
    source = """
    struct A {};
    void first() {}
    struct B {};
    void second() {}
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    assert ast_str.index("StructDecl(A") < ast_str.index("first")
    assert ast_str.index("first") < ast_str.index("StructDecl(B")


# ============================================================================
# STRUCT DECLARATIONS (Tests 6-12)
# ============================================================================

def test_struct_empty():
    """6. Empty struct declaration"""
    source = "struct Empty {};"
    ast = ASTGenerator(source).generate()
    assert str(ast) == "Program([StructDecl(Empty, [])])"


def test_struct_single_int_member():
    """7. Struct with single int member"""
    source = "struct Point { int x; };"
    ast = ASTGenerator(source).generate()
    assert "StructDecl(Point, [MemberDecl(IntType(), x)])" in str(ast)


def test_struct_multiple_members():
    """8. Struct with multiple members"""
    source = "struct Point { int x; int y; };"
    ast = ASTGenerator(source).generate()
    assert "MemberDecl(IntType(), x)" in str(ast)
    assert "MemberDecl(IntType(), y)" in str(ast)


def test_struct_float_member():
    """9. Struct with float member"""
    source = "struct Data { float value; };"
    ast = ASTGenerator(source).generate()
    assert "MemberDecl(FloatType(), value)" in str(ast)


def test_struct_string_member():
    """10. Struct with string member"""
    source = "struct Person { string name; };"
    ast = ASTGenerator(source).generate()
    assert "MemberDecl(StringType(), name)" in str(ast)


def test_struct_mixed_types():
    """11. Struct with mixed member types"""
    source = "struct Person { string name; int age; float height; };"
    ast = ASTGenerator(source).generate()
    assert "MemberDecl(StringType(), name)" in str(ast)
    assert "MemberDecl(IntType(), age)" in str(ast)
    assert "MemberDecl(FloatType(), height)" in str(ast)


def test_struct_nested_type():
    """12. Struct with nested struct type member"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    """
    ast = ASTGenerator(source).generate()
    assert "MemberDecl(StructType(Point), start)" in str(ast)
    assert "MemberDecl(StructType(Point), end)" in str(ast)


# ============================================================================
# FUNCTION DECLARATIONS (Tests 13-22)
# ============================================================================

def test_func_void_no_params():
    """13. Void function with no parameters"""
    source = "void main() {}"
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(VoidType(), main, []" in str(ast)


def test_func_int_return():
    """14. Function with int return type"""
    source = "int getValue() { return 42; }"
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(IntType(), getValue" in str(ast)


def test_func_float_return():
    """15. Function with float return type"""
    source = "float getPi() { return 3.14; }"
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(FloatType(), getPi" in str(ast)


def test_func_string_return():
    """16. Function with string return type"""
    source = 'string getName() { return "John"; }'
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(StringType(), getName" in str(ast)


def test_func_struct_return():
    """17. Function with struct return type"""
    source = """
    struct Point { int x; };
    Point createPoint() { return {0}; }
    """
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(StructType(Point), createPoint" in str(ast)


def test_func_inferred_return():
    """18. Function with inferred return type (no type specified)"""
    source = "add(int a, int b) { return a + b; }"
    ast = ASTGenerator(source).generate()
    assert "FuncDecl(auto, add" in str(ast)


def test_func_single_param():
    """19. Function with single parameter"""
    source = "void print(int x) {}"
    ast = ASTGenerator(source).generate()
    assert "Param(IntType(), x)" in str(ast)


def test_func_multiple_params():
    """20. Function with multiple parameters"""
    source = "int add(int a, int b) { return a + b; }"
    ast = ASTGenerator(source).generate()
    assert "Param(IntType(), a)" in str(ast)
    assert "Param(IntType(), b)" in str(ast)


def test_func_mixed_param_types():
    """21. Function with mixed parameter types"""
    source = "void display(int num, float val, string msg) {}"
    ast = ASTGenerator(source).generate()
    assert "Param(IntType(), num)" in str(ast)
    assert "Param(FloatType(), val)" in str(ast)
    assert "Param(StringType(), msg)" in str(ast)


def test_func_struct_param():
    """22. Function with struct parameter"""
    source = """
    struct Point { int x; };
    int getX(Point p) { return p.x; }
    """
    ast = ASTGenerator(source).generate()
    assert "Param(StructType(Point), p)" in str(ast)


# ============================================================================
# VARIABLE DECLARATIONS (Tests 23-30)
# ============================================================================

def test_var_int_no_init():
    """23. Int variable without initialization"""
    source = "void main() { int x; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(IntType(), x)" in str(ast)


def test_var_int_with_init():
    """24. Int variable with initialization"""
    source = "void main() { int x = 10; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(IntType(), x = IntLiteral(10))" in str(ast)


def test_var_float_with_init():
    """25. Float variable with initialization"""
    source = "void main() { float f = 3.14; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(FloatType(), f = FloatLiteral(3.14))" in str(ast)


def test_var_string_with_init():
    """26. String variable with initialization"""
    source = 'void main() { string s = "hello"; }'
    ast = ASTGenerator(source).generate()
    assert "VarDecl(StringType(), s = StringLiteral(" in str(ast)


def test_var_auto_no_init():
    """27. Auto variable without initialization"""
    source = "void main() { auto x; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(auto, x)" in str(ast)


def test_var_auto_with_int_init():
    """28. Auto variable with int initialization"""
    source = "void main() { auto x = 42; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(auto, x = IntLiteral(42))" in str(ast)


def test_var_auto_with_expr_init():
    """29. Auto variable with expression initialization"""
    source = "void main() { auto x = 1 + 2; }"
    ast = ASTGenerator(source).generate()
    assert "VarDecl(auto, x = BinaryOp" in str(ast)


def test_var_struct_with_init():
    """30. Struct variable with struct literal initialization"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    ast = ASTGenerator(source).generate()
    assert "VarDecl(StructType(Point), p = StructLiteral" in str(ast)


# ============================================================================
# IF STATEMENTS (Tests 31-36)
# ============================================================================

def test_if_simple():
    """31. Simple if statement"""
    source = "void main() { if (1) x = 1; }"
    ast = ASTGenerator(source).generate()
    assert "IfStmt(if IntLiteral(1)" in str(ast)


def test_if_with_block():
    """32. If statement with block"""
    source = "void main() { if (x) { y = 1; } }"
    ast = ASTGenerator(source).generate()
    assert "IfStmt(if Identifier(x) then BlockStmt" in str(ast)


def test_if_else():
    """33. If-else statement"""
    source = "void main() { if (x) y = 1; else y = 0; }"
    ast = ASTGenerator(source).generate()
    assert "IfStmt(if Identifier(x)" in str(ast)
    assert "else ExprStmt" in str(ast)


def test_if_condition_comparison():
    """34. If with comparison condition"""
    source = "void main() { if (x > 0) y = 1; }"
    ast = ASTGenerator(source).generate()
    assert "IfStmt(if BinaryOp(Identifier(x), >, IntLiteral(0))" in str(ast)


def test_if_condition_logical():
    """35. If with logical condition"""
    source = "void main() { if (x && y) z = 1; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(x), &&, Identifier(y))" in str(ast)


def test_if_nested():
    """36. Nested if statements"""
    source = "void main() { if (a) if (b) c = 1; }"
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    # Should have two IfStmt nodes
    assert ast_str.count("IfStmt") == 2


# ============================================================================
# WHILE STATEMENTS (Tests 37-40)
# ============================================================================

def test_while_simple():
    """37. Simple while statement"""
    source = "void main() { while (1) x = 1; }"
    ast = ASTGenerator(source).generate()
    assert "WhileStmt(while IntLiteral(1)" in str(ast)


def test_while_with_block():
    """38. While with block body"""
    source = "void main() { while (x) { y = 1; } }"
    ast = ASTGenerator(source).generate()
    assert "WhileStmt(while Identifier(x) do BlockStmt" in str(ast)


def test_while_condition():
    """39. While with comparison condition"""
    source = "void main() { while (i < 10) i = i + 1; }"
    ast = ASTGenerator(source).generate()
    assert "WhileStmt(while BinaryOp(Identifier(i), <, IntLiteral(10))" in str(ast)


def test_while_nested():
    """40. Nested while loops"""
    source = "void main() { while (a) while (b) c = 1; }"
    ast = ASTGenerator(source).generate()
    assert str(ast).count("WhileStmt") == 2


# ============================================================================
# FOR STATEMENTS (Tests 41-48)
# ============================================================================

def test_for_complete():
    """41. Complete for statement"""
    source = "void main() { for (int i = 0; i < 10; i++) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "ForStmt(for VarDecl(IntType(), i = IntLiteral(0))" in str(ast)


def test_for_auto_init():
    """42. For with auto init"""
    source = "void main() { for (auto i = 0; i < 10; i++) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "ForStmt(for VarDecl(auto, i = IntLiteral(0))" in str(ast)


def test_for_no_init():
    """43. For without init"""
    source = "void main() { for (; i < 10; i++) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "ForStmt(for None;" in str(ast)


def test_for_no_condition():
    """44. For without condition"""
    source = "void main() { for (int i = 0; ; i++) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "; None;" in str(ast)


def test_for_no_update():
    """45. For without update"""
    source = "void main() { for (int i = 0; i < 10;) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "; None do" in str(ast)


def test_for_empty():
    """46. For with all parts empty"""
    source = "void main() { for (;;) break; }"
    ast = ASTGenerator(source).generate()
    assert "ForStmt(for None; None; None" in str(ast)


def test_for_expr_init():
    """47. For with expression init"""
    source = "void main() { int i; for (i = 0; i < 10; i++) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "ForStmt(for AssignExpr" in str(ast)


def test_for_prefix_update():
    """48. For with prefix increment update"""
    source = "void main() { for (int i = 0; i < 10; ++i) x = i; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(++Identifier(i))" in str(ast)


# ============================================================================
# SWITCH STATEMENTS (Tests 49-54)
# ============================================================================

def test_switch_single_case():
    """49. Switch with single case"""
    source = "void main() { switch (x) { case 1: y = 1; break; } }"
    ast = ASTGenerator(source).generate()
    assert "SwitchStmt(switch Identifier(x)" in str(ast)
    assert "CaseStmt(case IntLiteral(1)" in str(ast)


def test_switch_multiple_cases():
    """50. Switch with multiple cases"""
    source = "void main() { switch (x) { case 1: break; case 2: break; } }"
    ast = ASTGenerator(source).generate()
    assert str(ast).count("CaseStmt") == 2


def test_switch_with_default():
    """51. Switch with default"""
    source = "void main() { switch (x) { case 1: break; default: y = 0; } }"
    ast = ASTGenerator(source).generate()
    assert "default DefaultStmt" in str(ast)


def test_switch_empty():
    """52. Empty switch body"""
    source = "void main() { switch (x) { } }"
    ast = ASTGenerator(source).generate()
    assert "SwitchStmt(switch Identifier(x) cases [])" in str(ast)


def test_switch_only_default():
    """53. Switch with only default"""
    source = "void main() { switch (x) { default: y = 0; } }"
    ast = ASTGenerator(source).generate()
    assert "cases [], default DefaultStmt" in str(ast)


def test_switch_case_multiple_stmts():
    """54. Case with multiple statements"""
    source = "void main() { switch (x) { case 1: a = 1; b = 2; break; } }"
    ast = ASTGenerator(source).generate()
    # Check that case has multiple statements
    ast_str = str(ast)
    assert "CaseStmt" in ast_str


# ============================================================================
# CONTROL FLOW STATEMENTS (Tests 55-58)
# ============================================================================

def test_break_stmt():
    """55. Break statement"""
    source = "void main() { while (1) { break; } }"
    ast = ASTGenerator(source).generate()
    assert "BreakStmt()" in str(ast)


def test_continue_stmt():
    """56. Continue statement"""
    source = "void main() { while (1) { continue; } }"
    ast = ASTGenerator(source).generate()
    assert "ContinueStmt()" in str(ast)


def test_return_void():
    """57. Return without value"""
    source = "void main() { return; }"
    ast = ASTGenerator(source).generate()
    assert "ReturnStmt(return)" in str(ast)


def test_return_value():
    """58. Return with value"""
    source = "int getValue() { return 42; }"
    ast = ASTGenerator(source).generate()
    assert "ReturnStmt(return IntLiteral(42))" in str(ast)


# ============================================================================
# ARITHMETIC EXPRESSIONS (Tests 59-66)
# ============================================================================

def test_expr_addition():
    """59. Addition expression"""
    source = "void main() { auto x = 1 + 2; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(IntLiteral(1), +, IntLiteral(2))" in str(ast)


def test_expr_subtraction():
    """60. Subtraction expression"""
    source = "void main() { auto x = 5 - 3; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(IntLiteral(5), -, IntLiteral(3))" in str(ast)


def test_expr_multiplication():
    """61. Multiplication expression"""
    source = "void main() { auto x = 2 * 3; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(IntLiteral(2), *, IntLiteral(3))" in str(ast)


def test_expr_division():
    """62. Division expression"""
    source = "void main() { auto x = 10 / 2; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(IntLiteral(10), /, IntLiteral(2))" in str(ast)


def test_expr_modulo():
    """63. Modulo expression"""
    source = "void main() { auto x = 10 % 3; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(IntLiteral(10), %, IntLiteral(3))" in str(ast)


def test_expr_unary_minus():
    """64. Unary minus expression"""
    source = "void main() { auto x = -5; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(-IntLiteral(5))" in str(ast)


def test_expr_unary_plus():
    """65. Unary plus expression"""
    source = "void main() { auto x = +5; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(+IntLiteral(5))" in str(ast)


def test_expr_precedence():
    """66. Expression with precedence (1 + 2 * 3 = 1 + (2 * 3))"""
    source = "void main() { auto x = 1 + 2 * 3; }"
    ast = ASTGenerator(source).generate()
    # Multiplication should be inside, addition outside
    assert "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))" in str(ast)


# ============================================================================
# COMPARISON & LOGICAL EXPRESSIONS (Tests 67-74)
# ============================================================================

def test_expr_equal():
    """67. Equality expression"""
    source = "void main() { auto x = a == b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), ==, Identifier(b))" in str(ast)


def test_expr_not_equal():
    """68. Not equal expression"""
    source = "void main() { auto x = a != b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), !=, Identifier(b))" in str(ast)


def test_expr_less_than():
    """69. Less than expression"""
    source = "void main() { auto x = a < b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), <, Identifier(b))" in str(ast)


def test_expr_greater_than():
    """70. Greater than expression"""
    source = "void main() { auto x = a > b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), >, Identifier(b))" in str(ast)


def test_expr_less_equal():
    """71. Less than or equal expression"""
    source = "void main() { auto x = a <= b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), <=, Identifier(b))" in str(ast)


def test_expr_greater_equal():
    """72. Greater than or equal expression"""
    source = "void main() { auto x = a >= b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), >=, Identifier(b))" in str(ast)


def test_expr_logical_and():
    """73. Logical AND expression"""
    source = "void main() { auto x = a && b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), &&, Identifier(b))" in str(ast)


def test_expr_logical_or():
    """74. Logical OR expression"""
    source = "void main() { auto x = a || b; }"
    ast = ASTGenerator(source).generate()
    assert "BinaryOp(Identifier(a), ||, Identifier(b))" in str(ast)


# ============================================================================
# INCREMENT/DECREMENT & OTHER EXPRESSIONS (Tests 75-84)
# ============================================================================

def test_expr_logical_not():
    """75. Logical NOT expression"""
    source = "void main() { auto x = !a; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(!Identifier(a))" in str(ast)


def test_expr_prefix_increment():
    """76. Prefix increment"""
    source = "void main() { ++x; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(++Identifier(x))" in str(ast)


def test_expr_prefix_decrement():
    """77. Prefix decrement"""
    source = "void main() { --x; }"
    ast = ASTGenerator(source).generate()
    assert "PrefixOp(--Identifier(x))" in str(ast)


def test_expr_postfix_increment():
    """78. Postfix increment"""
    source = "void main() { x++; }"
    ast = ASTGenerator(source).generate()
    assert "PostfixOp(Identifier(x)++)" in str(ast)


def test_expr_postfix_decrement():
    """79. Postfix decrement"""
    source = "void main() { x--; }"
    ast = ASTGenerator(source).generate()
    assert "PostfixOp(Identifier(x)--)" in str(ast)


def test_expr_member_access():
    """80. Member access expression"""
    source = """
    struct Point { int x; };
    void main() { Point p; auto val = p.x; }
    """
    ast = ASTGenerator(source).generate()
    assert "MemberAccess(Identifier(p).x)" in str(ast)


def test_expr_nested_member_access():
    """81. Nested member access"""
    source = """
    struct Point { int x; };
    struct Line { Point start; };
    void main() { Line l; auto val = l.start.x; }
    """
    ast = ASTGenerator(source).generate()
    assert "MemberAccess(MemberAccess(Identifier(l).start).x)" in str(ast)


def test_expr_function_call_no_args():
    """82. Function call with no arguments"""
    source = "void main() { foo(); }"
    ast = ASTGenerator(source).generate()
    assert "FuncCall(foo, [])" in str(ast)


def test_expr_function_call_one_arg():
    """83. Function call with one argument"""
    source = "void main() { printInt(42); }"
    ast = ASTGenerator(source).generate()
    assert "FuncCall(printInt, [IntLiteral(42)])" in str(ast)


def test_expr_function_call_multiple_args():
    """84. Function call with multiple arguments"""
    source = "void main() { add(1, 2, 3); }"
    ast = ASTGenerator(source).generate()
    assert "FuncCall(add, [IntLiteral(1), IntLiteral(2), IntLiteral(3)])" in str(ast)


# ============================================================================
# ASSIGNMENT & LITERALS (Tests 85-92)
# ============================================================================

def test_expr_assignment():
    """85. Assignment expression"""
    source = "void main() { int x; x = 5; }"
    ast = ASTGenerator(source).generate()
    assert "AssignExpr(Identifier(x) = IntLiteral(5))" in str(ast)


def test_expr_chained_assignment():
    """86. Chained assignment (right-associative)"""
    source = "void main() { int x; int y; x = y = 10; }"
    ast = ASTGenerator(source).generate()
    # Should be x = (y = 10)
    assert "AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(10)))" in str(ast)


def test_expr_member_assignment():
    """87. Member access assignment"""
    source = """
    struct Point { int x; };
    void main() { Point p; p.x = 10; }
    """
    ast = ASTGenerator(source).generate()
    assert "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(10))" in str(ast)


def test_literal_int():
    """88. Integer literal"""
    source = "void main() { auto x = 12345; }"
    ast = ASTGenerator(source).generate()
    assert "IntLiteral(12345)" in str(ast)


def test_literal_float():
    """89. Float literal"""
    source = "void main() { auto x = 3.14; }"
    ast = ASTGenerator(source).generate()
    assert "FloatLiteral(3.14)" in str(ast)


def test_literal_float_exponent():
    """90. Float literal with exponent"""
    source = "void main() { auto x = 1.5e10; }"
    ast = ASTGenerator(source).generate()
    assert "FloatLiteral(15000000000.0)" in str(ast)


def test_literal_string():
    """91. String literal"""
    source = 'void main() { auto s = "hello"; }'
    ast = ASTGenerator(source).generate()
    assert "StringLiteral(" in str(ast)


def test_literal_struct():
    """92. Struct literal"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    ast = ASTGenerator(source).generate()
    assert "StructLiteral({IntLiteral(1), IntLiteral(2)})" in str(ast)


# ============================================================================
# COMPLEX/COMBINED CASES (Tests 93-100)
# ============================================================================

def test_complex_expression_parentheses():
    """93. Parenthesized expression changes precedence"""
    source = "void main() { auto x = (1 + 2) * 3; }"
    ast = ASTGenerator(source).generate()
    # (1 + 2) * 3: addition should be inside multiplication
    assert "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3))" in str(ast)


def test_complex_nested_function_calls():
    """94. Nested function calls"""
    source = "void main() { foo(bar(1), 2); }"
    ast = ASTGenerator(source).generate()
    assert "FuncCall(foo, [FuncCall(bar, [IntLiteral(1)]), IntLiteral(2)])" in str(ast)


def test_complex_expression_all_operators():
    """95. Expression with multiple operator types"""
    source = "void main() { auto x = a + b * c - d / e; }"
    ast = ASTGenerator(source).generate()
    # Check that operators are present
    ast_str = str(ast)
    assert "+" in ast_str
    assert "*" in ast_str
    assert "-" in ast_str
    assert "/" in ast_str


def test_complex_struct_literal_nested():
    """96. Nested struct literal"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void main() { Line l = {{0, 0}, {1, 1}}; }
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    # Should have nested StructLiteral
    assert ast_str.count("StructLiteral") == 3  # outer + 2 inner


def test_complex_for_with_complex_body():
    """97. For loop with complex body"""
    source = """
    void main() {
        for (int i = 0; i < 10; i++) {
            if (i % 2 == 0) continue;
            printInt(i);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    assert "ForStmt" in ast_str
    assert "IfStmt" in ast_str
    assert "ContinueStmt" in ast_str
    assert "FuncCall(printInt" in ast_str


def test_complex_switch_with_fallthrough():
    """98. Switch with fallthrough cases"""
    source = """
    void main() {
        switch (x) {
            case 1:
            case 2:
                y = 12;
                break;
            default:
                y = 0;
        }
    }
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    assert "CaseStmt(case IntLiteral(1): [])" in ast_str  # Empty case 1
    assert "CaseStmt(case IntLiteral(2)" in ast_str


def test_complex_fibonacci():
    """99. Recursive function (Fibonacci)"""
    source = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    assert "FuncDecl(IntType(), fib" in ast_str
    assert "IfStmt" in ast_str
    assert "ReturnStmt" in ast_str
    assert "FuncCall(fib" in ast_str


def test_complex_full_program():
    """100. Full program with all features"""
    source = """
    struct Point { int x; int y; };
    
    Point createPoint(int x, int y) {
        return {x, y};
    }
    
    void main() {
        Point p = createPoint(0, 0);
        auto sum = p.x + p.y;
        
        if (sum == 0) {
            printInt(0);
        } else {
            for (int i = 0; i < sum; i++) {
                printInt(i);
            }
        }
    }
    """
    ast = ASTGenerator(source).generate()
    ast_str = str(ast)
    # Check all major components are present
    assert "StructDecl(Point" in ast_str
    assert "FuncDecl(StructType(Point), createPoint" in ast_str
    assert "FuncDecl(VoidType(), main" in ast_str
    assert "MemberAccess" in ast_str
    assert "IfStmt" in ast_str
    assert "ForStmt" in ast_str
    assert "FuncCall" in ast_str
