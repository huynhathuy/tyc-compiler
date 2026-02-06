"""
Parser test cases for TyC compiler
100 test cases covering all parser rules of TyC language
"""

import pytest
from tests.utils import Parser


# ============================================================================
# PROGRAM STRUCTURE (Tests 1-5)
# ============================================================================

def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_single_function():
    """2. Program with single function"""
    assert Parser("void main() {}").parse() == "success"


def test_program_multiple_functions():
    """3. Program with multiple functions"""
    source = """
    int add(int a, int b) { return a + b; }
    void main() { add(1, 2); }
    """
    assert Parser(source).parse() == "success"


def test_program_struct_and_function():
    """4. Program with struct and function"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


def test_program_multiple_structs():
    """5. Program with multiple structs"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void main() {}
    """
    assert Parser(source).parse() == "success"


# ============================================================================
# STRUCT DECLARATIONS (Tests 6-12)
# ============================================================================

def test_struct_empty():
    """6. Empty struct"""
    assert Parser("struct Empty {};").parse() == "success"


def test_struct_single_member():
    """7. Struct with single member"""
    assert Parser("struct Single { int x; };").parse() == "success"


def test_struct_multiple_members():
    """8. Struct with multiple members"""
    source = "struct Point { int x; int y; int z; };"
    assert Parser(source).parse() == "success"


def test_struct_mixed_types():
    """9. Struct with mixed types"""
    source = "struct Person { string name; int age; float height; };"
    assert Parser(source).parse() == "success"


def test_struct_nested_type():
    """10. Struct with nested struct type"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    """
    assert Parser(source).parse() == "success"


def test_struct_with_struct_member():
    """11. Struct with another struct as member"""
    source = """
    struct Inner { int val; };
    struct Outer { Inner inner; int count; };
    """
    assert Parser(source).parse() == "success"


def test_struct_all_primitive_types():
    """12. Struct with all primitive types"""
    source = "struct AllTypes { int i; float f; string s; };"
    assert Parser(source).parse() == "success"


# ============================================================================
# FUNCTION DECLARATIONS (Tests 13-22)
# ============================================================================

def test_func_void_no_params():
    """13. Void function with no parameters"""
    assert Parser("void greet() {}").parse() == "success"


def test_func_void_with_params():
    """14. Void function with parameters"""
    source = "void printSum(int a, int b) { printInt(a + b); }"
    assert Parser(source).parse() == "success"


def test_func_int_return():
    """15. Function with int return type"""
    source = "int add(int a, int b) { return a + b; }"
    assert Parser(source).parse() == "success"


def test_func_float_return():
    """16. Function with float return type"""
    source = "float multiply(float a, float b) { return a * b; }"
    assert Parser(source).parse() == "success"


def test_func_string_return():
    """17. Function with string return type"""
    source = 'string getName() { return "John"; }'
    assert Parser(source).parse() == "success"


def test_func_struct_return():
    """18. Function with struct return type"""
    source = """
    struct Point { int x; int y; };
    Point createPoint(int x, int y) { return {x, y}; }
    """
    assert Parser(source).parse() == "success"


def test_func_inferred_return():
    """19. Function with inferred return type"""
    source = "add(int a, int b) { return a + b; }"
    assert Parser(source).parse() == "success"


def test_func_multiple_params():
    """20. Function with multiple parameters"""
    source = "int sum(int a, int b, int c, int d) { return a + b + c + d; }"
    assert Parser(source).parse() == "success"


def test_func_struct_param():
    """21. Function with struct parameter"""
    source = """
    struct Point { int x; int y; };
    int getX(Point p) { return p.x; }
    """
    assert Parser(source).parse() == "success"


def test_func_mixed_params():
    """22. Function with mixed parameter types"""
    source = "void display(int num, float val, string msg) {}"
    assert Parser(source).parse() == "success"


# ============================================================================
# VARIABLE DECLARATIONS (Tests 23-32)
# ============================================================================

def test_var_int_no_init():
    """23. Int variable without initialization"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_var_int_with_init():
    """24. Int variable with initialization"""
    source = "void main() { int x = 10; }"
    assert Parser(source).parse() == "success"


def test_var_float_no_init():
    """25. Float variable without initialization"""
    source = "void main() { float f; }"
    assert Parser(source).parse() == "success"


def test_var_float_with_init():
    """26. Float variable with initialization"""
    source = "void main() { float f = 3.14; }"
    assert Parser(source).parse() == "success"


def test_var_string_no_init():
    """27. String variable without initialization"""
    source = "void main() { string s; }"
    assert Parser(source).parse() == "success"


def test_var_string_with_init():
    """28. String variable with initialization"""
    source = 'void main() { string s = "hello"; }'
    assert Parser(source).parse() == "success"


def test_var_auto_with_init():
    """29. Auto variable with initialization"""
    source = "void main() { auto x = 42; }"
    assert Parser(source).parse() == "success"


def test_var_auto_no_init():
    """30. Auto variable without initialization"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"


def test_var_struct_no_init():
    """31. Struct variable without initialization"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(source).parse() == "success"


def test_var_struct_with_init():
    """32. Struct variable with initialization"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {10, 20}; }
    """
    assert Parser(source).parse() == "success"


# ============================================================================
# IF STATEMENTS (Tests 33-38)
# ============================================================================

def test_if_simple():
    """33. Simple if statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_if_with_block():
    """34. If statement with block"""
    source = "void main() { if (x > 0) { printInt(x); } }"
    assert Parser(source).parse() == "success"


def test_if_else():
    """35. If-else statement"""
    source = "void main() { if (x) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


def test_if_else_blocks():
    """36. If-else with blocks"""
    source = "void main() { if (x > 0) { printInt(1); } else { printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_if_nested():
    """37. Nested if statements"""
    source = "void main() { if (a) if (b) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


def test_if_complex_condition():
    """38. If with complex condition"""
    source = "void main() { if (x > 0 && y < 10 || z == 5) printInt(1); }"
    assert Parser(source).parse() == "success"


# ============================================================================
# WHILE STATEMENTS (Tests 39-42)
# ============================================================================

def test_while_simple():
    """39. Simple while statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_with_block():
    """40. While with block"""
    source = "void main() { while (i < 10) { printInt(i); i = i + 1; } }"
    assert Parser(source).parse() == "success"


def test_while_complex_condition():
    """41. While with complex condition"""
    source = "void main() { while (x > 0 && x < 100) x = x - 1; }"
    assert Parser(source).parse() == "success"


def test_while_nested():
    """42. Nested while loops"""
    source = "void main() { while (i < 10) { while (j < 10) j = j + 1; i = i + 1; } }"
    assert Parser(source).parse() == "success"


# ============================================================================
# FOR STATEMENTS (Tests 43-50)
# ============================================================================

def test_for_simple():
    """43. Simple for statement"""
    source = "void main() { for (auto i = 0; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_with_block():
    """44. For with block"""
    source = "void main() { for (int i = 0; i < 10; ++i) { printInt(i); } }"
    assert Parser(source).parse() == "success"


def test_for_no_init():
    """45. For without init"""
    source = "void main() { for (; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_no_condition():
    """46. For without condition (infinite loop)"""
    source = "void main() { for (int i = 0; ; i++) { if (i > 10) break; } }"
    assert Parser(source).parse() == "success"


def test_for_no_update():
    """47. For without update"""
    source = "void main() { for (int i = 0; i < 10;) { i = i + 1; } }"
    assert Parser(source).parse() == "success"


def test_for_empty():
    """48. For with all parts empty"""
    source = "void main() { for (;;) break; }"
    assert Parser(source).parse() == "success"


def test_for_expr_init():
    """49. For with expression as init"""
    source = "void main() { int i; for (i = 0; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_for_nested():
    """50. Nested for loops"""
    source = "void main() { for (int i = 0; i < 10; i++) for (int j = 0; j < 10; j++) printInt(i+j); }"
    assert Parser(source).parse() == "success"


# ============================================================================
# SWITCH STATEMENTS (Tests 51-58)
# ============================================================================

def test_switch_simple():
    """51. Simple switch statement"""
    source = "void main() { switch (x) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases():
    """52. Switch with multiple cases"""
    source = "void main() { switch (x) { case 1: printInt(1); break; case 2: printInt(2); break; } }"
    assert Parser(source).parse() == "success"


def test_switch_with_default():
    """53. Switch with default"""
    source = "void main() { switch (x) { case 1: printInt(1); break; default: printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_switch_fallthrough():
    """54. Switch with fall-through"""
    source = "void main() { switch (x) { case 1: case 2: printInt(12); break; } }"
    assert Parser(source).parse() == "success"


def test_switch_empty():
    """55. Empty switch body"""
    source = "void main() { switch (x) { } }"
    assert Parser(source).parse() == "success"


def test_switch_only_default():
    """56. Switch with only default"""
    source = "void main() { switch (x) { default: printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_switch_complex_case():
    """57. Switch with expression in case"""
    source = "void main() { switch (x) { case 1+2: printInt(3); break; } }"
    assert Parser(source).parse() == "success"


def test_switch_nested():
    """58. Nested switch statements"""
    source = "void main() { switch (x) { case 1: switch (y) { case 2: break; } break; } }"
    assert Parser(source).parse() == "success"


# ============================================================================
# CONTROL FLOW STATEMENTS (Tests 59-62)
# ============================================================================

def test_break_in_loop():
    """59. Break in while loop"""
    source = "void main() { while (1) { break; } }"
    assert Parser(source).parse() == "success"


def test_continue_in_loop():
    """60. Continue in while loop"""
    source = "void main() { while (1) { continue; } }"
    assert Parser(source).parse() == "success"


def test_return_void():
    """61. Return without value"""
    source = "void main() { return; }"
    assert Parser(source).parse() == "success"


def test_return_value():
    """62. Return with value"""
    source = "int getValue() { return 42; }"
    assert Parser(source).parse() == "success"


# ============================================================================
# EXPRESSIONS - ARITHMETIC (Tests 63-70)
# ============================================================================

def test_expr_addition():
    """63. Addition expression"""
    source = "void main() { auto x = 1 + 2; }"
    assert Parser(source).parse() == "success"


def test_expr_subtraction():
    """64. Subtraction expression"""
    source = "void main() { auto x = 5 - 3; }"
    assert Parser(source).parse() == "success"


def test_expr_multiplication():
    """65. Multiplication expression"""
    source = "void main() { auto x = 4 * 5; }"
    assert Parser(source).parse() == "success"


def test_expr_division():
    """66. Division expression"""
    source = "void main() { auto x = 10 / 2; }"
    assert Parser(source).parse() == "success"


def test_expr_modulo():
    """67. Modulo expression"""
    source = "void main() { auto x = 10 % 3; }"
    assert Parser(source).parse() == "success"


def test_expr_unary_minus():
    """68. Unary minus expression"""
    source = "void main() { auto x = -5; }"
    assert Parser(source).parse() == "success"


def test_expr_unary_plus():
    """69. Unary plus expression"""
    source = "void main() { auto x = +5; }"
    assert Parser(source).parse() == "success"


def test_expr_complex_arithmetic():
    """70. Complex arithmetic expression"""
    source = "void main() { auto x = (1 + 2) * 3 - 4 / 2; }"
    assert Parser(source).parse() == "success"


# ============================================================================
# EXPRESSIONS - COMPARISON & LOGICAL (Tests 71-78)
# ============================================================================

def test_expr_equal():
    """71. Equality expression"""
    source = "void main() { auto x = a == b; }"
    assert Parser(source).parse() == "success"


def test_expr_not_equal():
    """72. Not equal expression"""
    source = "void main() { auto x = a != b; }"
    assert Parser(source).parse() == "success"


def test_expr_less_than():
    """73. Less than expression"""
    source = "void main() { auto x = a < b; }"
    assert Parser(source).parse() == "success"


def test_expr_greater_than():
    """74. Greater than expression"""
    source = "void main() { auto x = a > b; }"
    assert Parser(source).parse() == "success"


def test_expr_less_equal():
    """75. Less than or equal expression"""
    source = "void main() { auto x = a <= b; }"
    assert Parser(source).parse() == "success"


def test_expr_greater_equal():
    """76. Greater than or equal expression"""
    source = "void main() { auto x = a >= b; }"
    assert Parser(source).parse() == "success"


def test_expr_logical_and():
    """77. Logical AND expression"""
    source = "void main() { auto x = a && b; }"
    assert Parser(source).parse() == "success"


def test_expr_logical_or():
    """78. Logical OR expression"""
    source = "void main() { auto x = a || b; }"
    assert Parser(source).parse() == "success"


# ============================================================================
# EXPRESSIONS - INCREMENT/DECREMENT & OTHERS (Tests 79-86)
# ============================================================================

def test_expr_logical_not():
    """79. Logical NOT expression"""
    source = "void main() { auto x = !a; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_increment():
    """80. Prefix increment"""
    source = "void main() { ++x; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_decrement():
    """81. Prefix decrement"""
    source = "void main() { --x; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_increment():
    """82. Postfix increment"""
    source = "void main() { x++; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_decrement():
    """83. Postfix decrement"""
    source = "void main() { x--; }"
    assert Parser(source).parse() == "success"


def test_expr_member_access():
    """84. Member access expression"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p; auto x = p.x; }
    """
    assert Parser(source).parse() == "success"


def test_expr_function_call():
    """85. Function call expression"""
    source = "void main() { printInt(42); }"
    assert Parser(source).parse() == "success"


def test_expr_function_call_multiple_args():
    """86. Function call with multiple arguments"""
    source = "int add(int a, int b) { return a + b; } void main() { add(1, 2); }"
    assert Parser(source).parse() == "success"


# ============================================================================
# EXPRESSIONS - ASSIGNMENT & LITERALS (Tests 87-94)
# ============================================================================

def test_expr_assignment():
    """87. Assignment expression"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"


def test_expr_chained_assignment():
    """88. Chained assignment"""
    source = "void main() { int x; int y; int z; x = y = z = 10; }"
    assert Parser(source).parse() == "success"


def test_expr_int_literal():
    """89. Integer literal"""
    source = "void main() { auto x = 12345; }"
    assert Parser(source).parse() == "success"


def test_expr_float_literal():
    """90. Float literal"""
    source = "void main() { auto x = 3.14159; }"
    assert Parser(source).parse() == "success"


def test_expr_float_exponent():
    """91. Float literal with exponent"""
    source = "void main() { auto x = 1.5e-10; }"
    assert Parser(source).parse() == "success"


def test_expr_string_literal():
    """92. String literal"""
    source = 'void main() { auto s = "Hello, World!"; }'
    assert Parser(source).parse() == "success"


def test_expr_struct_literal():
    """93. Struct literal"""
    source = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    assert Parser(source).parse() == "success"


def test_expr_parenthesized():
    """94. Parenthesized expression"""
    source = "void main() { auto x = (1 + 2) * (3 + 4); }"
    assert Parser(source).parse() == "success"


# ============================================================================
# COMPLEX/COMBINED CASES (Tests 95-100)
# ============================================================================

def test_complex_fibonacci():
    """95. Fibonacci function"""
    source = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    void main() { printInt(fib(10)); }
    """
    assert Parser(source).parse() == "success"


def test_complex_nested_loops():
    """96. Nested loops with all control flow"""
    source = """
    void main() {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                if (i == j) continue;
                if (i + j > 15) break;
                printInt(i * j);
            }
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_struct_operations():
    """97. Complex struct operations"""
    source = """
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    int getLength(Line l) {
        auto dx = l.end.x - l.start.x;
        auto dy = l.end.y - l.start.y;
        return dx * dx + dy * dy;
    }
    void main() {
        Line l = {{0, 0}, {3, 4}};
        printInt(getLength(l));
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_expression_precedence():
    """98. Expression with all precedence levels"""
    source = """
    void main() {
        auto result = a = b || c && d == e < f + g * -h++;
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_all_statements():
    """99. Program using all statement types"""
    source = """
    void main() {
        int x = 10;
        auto y = 20;
        if (x < y) {
            while (x < y) {
                x++;
            }
        } else {
            for (int i = 0; i < 5; i++) {
                printInt(i);
            }
        }
        switch (x) {
            case 10: printInt(10); break;
            case 20: printInt(20); break;
            default: printInt(0);
        }
        return;
    }
    """
    assert Parser(source).parse() == "success"


def test_complex_full_program():
    """100. Full program with all features"""
    source = """
    struct Point { int x; int y; };
    
    Point createPoint(int x, int y) {
        return {x, y};
    }
    
    int distance(Point p1, Point p2) {
        auto dx = p2.x - p1.x;
        auto dy = p2.y - p1.y;
        return dx * dx + dy * dy;
    }
    
    void main() {
        Point p1 = createPoint(0, 0);
        Point p2 = {3, 4};
        auto dist = distance(p1, p2);
        
        if (dist > 0) {
            printInt(dist);
        }
        
        for (int i = 0; i < 10; i++) {
            if (i % 2 == 0) continue;
            printInt(i);
        }
    }
    """
    assert Parser(source).parse() == "success"
