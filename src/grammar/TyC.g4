grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ============================================================================
// Parser Rules
// ============================================================================

// ----------------------------------------------------------------------------
// Program Structure
// ----------------------------------------------------------------------------

program
    : declaration* EOF
    ;

declaration
    : structDecl                                                    # StructDeclaration
    | funcDecl                                                      # FuncDeclaration
    ;

// ----------------------------------------------------------------------------
// Struct Declaration
// ----------------------------------------------------------------------------

structDecl
    : STRUCT ID LBRACE memberDecl* RBRACE SEMI
    ;

memberDecl
    : typ ID SEMI
    ;

// ----------------------------------------------------------------------------
// Function Declaration
// ----------------------------------------------------------------------------

funcDecl
    : typ ID LPAREN paramList? RPAREN blockStmt                     # TypedFuncDecl
    | VOID ID LPAREN paramList? RPAREN blockStmt                    # VoidFuncDecl
    | ID LPAREN paramList? RPAREN blockStmt                         # InferredFuncDecl
    ;

paramList
    : param (COMMA param)*
    ;

param
    : typ ID
    ;

// ----------------------------------------------------------------------------
// Types
// ----------------------------------------------------------------------------

typ
    : INT                                                           # IntType
    | FLOAT                                                         # FloatType
    | STRING                                                        # StringType
    | ID                                                            # StructType
    ;

// ----------------------------------------------------------------------------
// Statements
// ----------------------------------------------------------------------------

stmt
    : varDecl                                                       # VarDeclStmt
    | ifStmt                                                        # IfStatement
    | whileStmt                                                     # WhileStatement
    | forStmt                                                       # ForStatement
    | switchStmt                                                    # SwitchStatement
    | breakStmt                                                     # BreakStatement
    | continueStmt                                                  # ContinueStatement
    | returnStmt                                                    # ReturnStatement
    | blockStmt                                                     # BlockStatement
    | exprStmt                                                      # ExprStatement
    ;

// Variable Declaration
varDecl
    : typ ID (ASSIGN expr)? SEMI                                    # TypedVarDecl
    | AUTO ID (ASSIGN expr)? SEMI                                   # AutoVarDecl
    ;

// Block Statement
blockStmt
    : LBRACE stmt* RBRACE
    ;

// If Statement (dangling else handled by ANTLR's default: prefer shift)
ifStmt
    : IF LPAREN expr RPAREN stmt (ELSE stmt)?
    ;

// While Statement
whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;

// For Statement
forStmt
    : FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN stmt
    ;

forInit
    : typ ID (ASSIGN expr)?                                         # ForInitTypedVar
    | AUTO ID (ASSIGN expr)?                                        # ForInitAutoVar
    | expr                                                          # ForInitExpr
    ;

forUpdate
    : expr
    ;

// Switch Statement (C-style fall-through)
switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchBody RBRACE
    ;

switchBody
    : caseClause* defaultClause?
    ;

caseClause
    : CASE expr COLON stmt*
    ;

defaultClause
    : DEFAULT COLON stmt*
    ;

// Break Statement
breakStmt
    : BREAK SEMI
    ;

// Continue Statement
continueStmt
    : CONTINUE SEMI
    ;

// Return Statement
returnStmt
    : RETURN expr? SEMI
    ;

// Expression Statement
exprStmt
    : expr SEMI
    ;

// ----------------------------------------------------------------------------
// Expressions (Precedence from lowest to highest via rule nesting)
// ----------------------------------------------------------------------------

// Entry point for expressions
expr
    : assignExpr
    ;

// Assignment: right-associative (lowest precedence)
assignExpr
    : orExpr ASSIGN assignExpr                                      # Assignment
    | orExpr                                                        # AssignExprPassthrough
    ;

// Logical OR: left-associative
orExpr
    : orExpr OR andExpr                                             # LogicalOrExpr
    | andExpr                                                       # OrExprPassthrough
    ;

// Logical AND: left-associative
andExpr
    : andExpr AND equalityExpr                                      # LogicalAndExpr
    | equalityExpr                                                  # AndExprPassthrough
    ;

// Equality: left-associative
equalityExpr
    : equalityExpr op=(EQ | NEQ) relationalExpr                     # EqualityOp
    | relationalExpr                                                # EqualityExprPassthrough
    ;

// Relational: left-associative
relationalExpr
    : relationalExpr op=(LT | GT | LEQ | GEQ) additiveExpr          # RelationalOp
    | additiveExpr                                                  # RelationalExprPassthrough
    ;

// Additive: left-associative
additiveExpr
    : additiveExpr op=(PLUS | MINUS) multiplicativeExpr             # AdditiveOp
    | multiplicativeExpr                                            # AdditiveExprPassthrough
    ;

// Multiplicative: left-associative
multiplicativeExpr
    : multiplicativeExpr op=(MUL | DIV | MOD) unaryExpr             # MultiplicativeOp
    | unaryExpr                                                     # MultiplicativeExprPassthrough
    ;

// Unary/Prefix: right-associative
unaryExpr
    : op=(PLUS | MINUS | NOT) unaryExpr                             # UnaryOp
    | op=(INC | DEC) unaryExpr                                      # PrefixOp
    | postfixExpr                                                   # UnaryExprPassthrough
    ;

// Postfix: left-associative (++, --, member access, function call)
postfixExpr
    : postfixExpr op=(INC | DEC)                                    # PostfixIncDec
    | postfixExpr DOT ID                                            # MemberAccessExpr
    | postfixExpr LPAREN argList? RPAREN                            # FuncCallExpr
    | primaryExpr                                                   # PostfixExprPassthrough
    ;

// Argument list for function calls
argList
    : expr (COMMA expr)*
    ;

// Primary expressions (highest precedence)
primaryExpr
    : LPAREN expr RPAREN                                            # ParenExpr
    | INTLIT                                                        # IntLitExpr
    | FLOATLIT                                                      # FloatLitExpr
    | STRINGLIT                                                     # StringLitExpr
    | LBRACE exprList? RBRACE                                       # StructLitExpr
    | ID                                                            # IdExpr
    ;

// Expression list for struct literals
exprList
    : expr (COMMA expr)*
    ;

// ============================================================================
// Lexer Rules
// ============================================================================

// ----------------------------------------------------------------------------
// Keywords (must come before ID to take precedence)
// ----------------------------------------------------------------------------
AUTO:       'auto';
BREAK:      'break';
CASE:       'case';
CONTINUE:   'continue';
DEFAULT:    'default';
ELSE:       'else';
FLOAT:      'float';
FOR:        'for';
IF:         'if';
INT:        'int';
RETURN:     'return';
STRING:     'string';
STRUCT:     'struct';
SWITCH:     'switch';
VOID:       'void';
WHILE:      'while';

// ----------------------------------------------------------------------------
// Operators (multi-character operators first)
// ----------------------------------------------------------------------------
// Increment/Decrement
INC:        '++';
DEC:        '--';

// Comparison operators (multi-char)
LEQ:        '<=';
GEQ:        '>=';
EQ:         '==';
NEQ:        '!=';

// Logical operators (multi-char)
AND:        '&&';
OR:         '||';

// Single-character operators
PLUS:       '+';
MINUS:      '-';
MUL:        '*';
DIV:        '/';
MOD:        '%';
LT:         '<';
GT:         '>';
NOT:        '!';
ASSIGN:     '=';
DOT:        '.';

// ----------------------------------------------------------------------------
// Separators
// ----------------------------------------------------------------------------
LBRACE:     '{';
RBRACE:     '}';
LPAREN:     '(';
RPAREN:     ')';
SEMI:       ';';
COMMA:      ',';
COLON:      ':';

// ----------------------------------------------------------------------------
// Literals
// ----------------------------------------------------------------------------

// FLOATLIT must come before INTLIT (maximal munch + rule order)
// Float patterns: 1.0, 1., .5, 1e5, 1.5e-3, etc.
FLOATLIT
    : DIGIT+ '.' DIGIT* EXPONENT?   // 1.  1.0  1.5e10
    | DIGIT* '.' DIGIT+ EXPONENT?   // .5  .5e10  0.5
    | DIGIT+ EXPONENT               // 1e5  2E-3
    ;

// Integer literal: one or more digits
INTLIT
    : DIGIT+
    ;

// ----------------------------------------------------------------------------
// String Literals with Error Handling
// ----------------------------------------------------------------------------
// Order is CRITICAL: ILLEGAL_ESCAPE > UNCLOSE_STRING > STRINGLIT
// ANTLR uses rule order for same-length matches, but longer matches win first.
// We structure rules so errors are detected correctly.

// ILLEGAL_ESCAPE: String with an invalid escape sequence
// Matches: opening quote, valid content, then backslash followed by invalid char
// The invalid char is NOT: b, f, r, n, t, ", \, and NOT newline/CR (those cause UNCLOSE)
ILLEGAL_ESCAPE
    : '"' STR_CHAR* '\\' ~[bfnrt"\\\r\n]
    {
        # Remove the opening quote, keep content up to and including illegal escape
        self.text = self.text[1:]
    }
    ;

// UNCLOSE_STRING: String not closed before newline, CR, or EOF
// Matches: opening quote, valid content (may include valid escapes), then newline/CR/EOF
UNCLOSE_STRING
    : '"' STR_CHAR* ('\r' | '\n' | EOF)
    {
        # Remove the opening quote; if ended with newline/CR, remove it too
        text = self.text[1:]
        if len(text) > 0 and text[-1] in '\r\n':
            text = text[:-1]
        self.text = text
    }
    ;

// STRINGLIT: Valid string literal with proper escapes
STRINGLIT
    : '"' STR_CHAR* '"'
    {
        # Strip the enclosing double quotes
        self.text = self.text[1:-1]
    }
    ;

// ----------------------------------------------------------------------------
// Identifier (after keywords)
// ----------------------------------------------------------------------------
ID
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

// ----------------------------------------------------------------------------
// Whitespace and Comments (skip)
// ----------------------------------------------------------------------------
WS
    : [ \t\f\r\n]+ -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

// ----------------------------------------------------------------------------
// Error Token (catch-all for unrecognized characters - MUST BE LAST)
// ----------------------------------------------------------------------------
ERROR_CHAR
    : .
    ;

// ============================================================================
// Fragment Rules (not tokens, just reusable patterns)
// ============================================================================

fragment DIGIT
    : [0-9]
    ;

fragment EXPONENT
    : [eE] [+-]? DIGIT+
    ;

// Valid escape sequences: \b \f \r \n \t \" \\
fragment ESC_SEQ
    : '\\' [bfnrt"\\]
    ;

// Characters allowed inside a string (excluding the quote, backslash, CR, LF)
// Either an escape sequence OR any char except ", \, \r, \n
fragment STR_CHAR
    : ESC_SEQ
    | ~["\\\r\n]
    ;
