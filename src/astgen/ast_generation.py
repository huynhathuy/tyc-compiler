"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # ========================================================================
    # Program and Declarations
    # ========================================================================

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        """Visit program: declaration* EOF"""
        decls = [self.visit(decl) for decl in ctx.declaration()]
        return Program(decls)

    def visitStructDeclaration(self, ctx: TyCParser.StructDeclarationContext):
        """Passthrough for struct declaration label"""
        return self.visit(ctx.structDecl())

    def visitFuncDeclaration(self, ctx: TyCParser.FuncDeclarationContext):
        """Passthrough for function declaration label"""
        return self.visit(ctx.funcDecl())

    # ========================================================================
    # Struct Declaration
    # ========================================================================

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        """Visit struct: STRUCT ID LBRACE memberDecl* RBRACE SEMI"""
        name = ctx.ID().getText()
        members = [self.visit(m) for m in ctx.memberDecl()]
        return StructDecl(name, members)

    def visitMemberDecl(self, ctx: TyCParser.MemberDeclContext):
        """Visit member: typ ID SEMI"""
        member_type = self.visit(ctx.typ())
        name = ctx.ID().getText()
        return MemberDecl(member_type, name)

    # ========================================================================
    # Function Declaration
    # ========================================================================

    def visitTypedFuncDecl(self, ctx: TyCParser.TypedFuncDeclContext):
        """Visit function with explicit return type: typ ID ( params? ) block"""
        return_type = self.visit(ctx.typ())
        name = ctx.ID().getText()
        params = self._getParams(ctx.paramList())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitVoidFuncDecl(self, ctx: TyCParser.VoidFuncDeclContext):
        """Visit function with void return type: VOID ID ( params? ) block"""
        return_type = VoidType()
        name = ctx.ID().getText()
        params = self._getParams(ctx.paramList())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitInferredFuncDecl(self, ctx: TyCParser.InferredFuncDeclContext):
        """Visit function with inferred return type: ID ( params? ) block"""
        return_type = None  # Inferred type
        name = ctx.ID().getText()
        params = self._getParams(ctx.paramList())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def _getParams(self, paramListCtx):
        """Helper to extract parameter list"""
        if paramListCtx is None:
            return []
        return [self.visit(p) for p in paramListCtx.param()]

    def visitParam(self, ctx: TyCParser.ParamContext):
        """Visit parameter: typ ID"""
        param_type = self.visit(ctx.typ())
        name = ctx.ID().getText()
        return Param(param_type, name)

    # ========================================================================
    # Types
    # ========================================================================

    def visitIntType(self, ctx: TyCParser.IntTypeContext):
        """Visit INT type"""
        return IntType()

    def visitFloatType(self, ctx: TyCParser.FloatTypeContext):
        """Visit FLOAT type"""
        return FloatType()

    def visitStringType(self, ctx: TyCParser.StringTypeContext):
        """Visit STRING type"""
        return StringType()

    def visitStructType(self, ctx: TyCParser.StructTypeContext):
        """Visit struct type (ID)"""
        return StructType(ctx.ID().getText())

    # ========================================================================
    # Statements
    # ========================================================================

    def visitVarDeclStmt(self, ctx: TyCParser.VarDeclStmtContext):
        """Passthrough for variable declaration statement"""
        return self.visit(ctx.varDecl())

    def visitIfStatement(self, ctx: TyCParser.IfStatementContext):
        """Passthrough for if statement"""
        return self.visit(ctx.ifStmt())

    def visitWhileStatement(self, ctx: TyCParser.WhileStatementContext):
        """Passthrough for while statement"""
        return self.visit(ctx.whileStmt())

    def visitForStatement(self, ctx: TyCParser.ForStatementContext):
        """Passthrough for for statement"""
        return self.visit(ctx.forStmt())

    def visitSwitchStatement(self, ctx: TyCParser.SwitchStatementContext):
        """Passthrough for switch statement"""
        return self.visit(ctx.switchStmt())

    def visitBreakStatement(self, ctx: TyCParser.BreakStatementContext):
        """Passthrough for break statement"""
        return self.visit(ctx.breakStmt())

    def visitContinueStatement(self, ctx: TyCParser.ContinueStatementContext):
        """Passthrough for continue statement"""
        return self.visit(ctx.continueStmt())

    def visitReturnStatement(self, ctx: TyCParser.ReturnStatementContext):
        """Passthrough for return statement"""
        return self.visit(ctx.returnStmt())

    def visitBlockStatement(self, ctx: TyCParser.BlockStatementContext):
        """Passthrough for block statement"""
        return self.visit(ctx.blockStmt())

    def visitExprStatement(self, ctx: TyCParser.ExprStatementContext):
        """Passthrough for expression statement"""
        return self.visit(ctx.exprStmt())

    # ========================================================================
    # Variable Declaration
    # ========================================================================

    def visitTypedVarDecl(self, ctx: TyCParser.TypedVarDeclContext):
        """Visit typed variable declaration: typ ID (ASSIGN expr)? SEMI"""
        var_type = self.visit(ctx.typ())
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init_value)

    def visitAutoVarDecl(self, ctx: TyCParser.AutoVarDeclContext):
        """Visit auto variable declaration: AUTO ID (ASSIGN expr)? SEMI"""
        var_type = None  # auto means type inference
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init_value)

    # ========================================================================
    # Block Statement
    # ========================================================================

    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        """Visit block: LBRACE stmt* RBRACE"""
        statements = [self.visit(s) for s in ctx.stmt()]
        return BlockStmt(statements)

    # ========================================================================
    # Control Flow Statements
    # ========================================================================

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        """Visit if: IF ( expr ) stmt (ELSE stmt)?"""
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        """Visit while: WHILE ( expr ) stmt"""
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        """Visit for: FOR ( forInit? ; expr? ; forUpdate? ) stmt"""
        init = self.visit(ctx.forInit()) if ctx.forInit() else None
        condition = self.visit(ctx.expr()) if ctx.expr() else None
        update = self.visit(ctx.forUpdate()) if ctx.forUpdate() else None
        body = self.visit(ctx.stmt())
        return ForStmt(init, condition, update, body)

    def visitForInitTypedVar(self, ctx: TyCParser.ForInitTypedVarContext):
        """Visit for init with typed var: typ ID (ASSIGN expr)?"""
        var_type = self.visit(ctx.typ())
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init_value)

    def visitForInitAutoVar(self, ctx: TyCParser.ForInitAutoVarContext):
        """Visit for init with auto var: AUTO ID (ASSIGN expr)?"""
        var_type = None  # auto
        name = ctx.ID().getText()
        init_value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(var_type, name, init_value)

    def visitForInitExpr(self, ctx: TyCParser.ForInitExprContext):
        """Visit for init with expression"""
        return self.visit(ctx.expr())

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        """Visit for update: expr"""
        return self.visit(ctx.expr())

    # ========================================================================
    # Switch Statement
    # ========================================================================

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        """Visit switch: SWITCH ( expr ) { switchBody }"""
        expr = self.visit(ctx.expr())
        switch_body = ctx.switchBody()
        cases = [self.visit(c) for c in switch_body.caseClause()]
        default_case = self.visit(switch_body.defaultClause()) if switch_body.defaultClause() else None
        return SwitchStmt(expr, cases, default_case)

    def visitCaseClause(self, ctx: TyCParser.CaseClauseContext):
        """Visit case: CASE expr COLON stmt*"""
        expr = self.visit(ctx.expr())
        statements = [self.visit(s) for s in ctx.stmt()]
        return CaseStmt(expr, statements)

    def visitDefaultClause(self, ctx: TyCParser.DefaultClauseContext):
        """Visit default: DEFAULT COLON stmt*"""
        statements = [self.visit(s) for s in ctx.stmt()]
        return DefaultStmt(statements)

    # ========================================================================
    # Simple Statements
    # ========================================================================

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        """Visit break: BREAK SEMI"""
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        """Visit continue: CONTINUE SEMI"""
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        """Visit return: RETURN expr? SEMI"""
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(expr)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        """Visit expression statement: expr SEMI"""
        expr = self.visit(ctx.expr())
        return ExprStmt(expr)

    # ========================================================================
    # Expressions
    # ========================================================================

    def visitExpr(self, ctx: TyCParser.ExprContext):
        """Visit expr: assignExpr"""
        return self.visit(ctx.assignExpr())

    # Assignment
    def visitAssignment(self, ctx: TyCParser.AssignmentContext):
        """Visit assignment: orExpr ASSIGN assignExpr"""
        lhs = self.visit(ctx.orExpr())
        rhs = self.visit(ctx.assignExpr())
        return AssignExpr(lhs, rhs)

    def visitAssignExprPassthrough(self, ctx: TyCParser.AssignExprPassthroughContext):
        """Passthrough to orExpr"""
        return self.visit(ctx.orExpr())

    # Logical OR
    def visitLogicalOrExpr(self, ctx: TyCParser.LogicalOrExprContext):
        """Visit logical OR: orExpr OR andExpr"""
        left = self.visit(ctx.orExpr())
        right = self.visit(ctx.andExpr())
        return BinaryOp(left, "||", right)

    def visitOrExprPassthrough(self, ctx: TyCParser.OrExprPassthroughContext):
        """Passthrough to andExpr"""
        return self.visit(ctx.andExpr())

    # Logical AND
    def visitLogicalAndExpr(self, ctx: TyCParser.LogicalAndExprContext):
        """Visit logical AND: andExpr AND equalityExpr"""
        left = self.visit(ctx.andExpr())
        right = self.visit(ctx.equalityExpr())
        return BinaryOp(left, "&&", right)

    def visitAndExprPassthrough(self, ctx: TyCParser.AndExprPassthroughContext):
        """Passthrough to equalityExpr"""
        return self.visit(ctx.equalityExpr())

    # Equality
    def visitEqualityOp(self, ctx: TyCParser.EqualityOpContext):
        """Visit equality: equalityExpr op=(EQ|NEQ) relationalExpr"""
        left = self.visit(ctx.equalityExpr())
        op = ctx.op.text
        right = self.visit(ctx.relationalExpr())
        return BinaryOp(left, op, right)

    def visitEqualityExprPassthrough(self, ctx: TyCParser.EqualityExprPassthroughContext):
        """Passthrough to relationalExpr"""
        return self.visit(ctx.relationalExpr())

    # Relational
    def visitRelationalOp(self, ctx: TyCParser.RelationalOpContext):
        """Visit relational: relationalExpr op=(LT|GT|LEQ|GEQ) additiveExpr"""
        left = self.visit(ctx.relationalExpr())
        op = ctx.op.text
        right = self.visit(ctx.additiveExpr())
        return BinaryOp(left, op, right)

    def visitRelationalExprPassthrough(self, ctx: TyCParser.RelationalExprPassthroughContext):
        """Passthrough to additiveExpr"""
        return self.visit(ctx.additiveExpr())

    # Additive
    def visitAdditiveOp(self, ctx: TyCParser.AdditiveOpContext):
        """Visit additive: additiveExpr op=(PLUS|MINUS) multiplicativeExpr"""
        left = self.visit(ctx.additiveExpr())
        op = ctx.op.text
        right = self.visit(ctx.multiplicativeExpr())
        return BinaryOp(left, op, right)

    def visitAdditiveExprPassthrough(self, ctx: TyCParser.AdditiveExprPassthroughContext):
        """Passthrough to multiplicativeExpr"""
        return self.visit(ctx.multiplicativeExpr())

    # Multiplicative
    def visitMultiplicativeOp(self, ctx: TyCParser.MultiplicativeOpContext):
        """Visit multiplicative: multiplicativeExpr op=(MUL|DIV|MOD) unaryExpr"""
        left = self.visit(ctx.multiplicativeExpr())
        op = ctx.op.text
        right = self.visit(ctx.unaryExpr())
        return BinaryOp(left, op, right)

    def visitMultiplicativeExprPassthrough(self, ctx: TyCParser.MultiplicativeExprPassthroughContext):
        """Passthrough to unaryExpr"""
        return self.visit(ctx.unaryExpr())

    # Unary
    def visitUnaryOp(self, ctx: TyCParser.UnaryOpContext):
        """Visit unary: op=(PLUS|MINUS|NOT) unaryExpr"""
        op = ctx.op.text
        operand = self.visit(ctx.unaryExpr())
        return PrefixOp(op, operand)

    def visitPrefixOp(self, ctx: TyCParser.PrefixOpContext):
        """Visit prefix: op=(INC|DEC) unaryExpr"""
        op = ctx.op.text
        operand = self.visit(ctx.unaryExpr())
        return PrefixOp(op, operand)

    def visitUnaryExprPassthrough(self, ctx: TyCParser.UnaryExprPassthroughContext):
        """Passthrough to postfixExpr"""
        return self.visit(ctx.postfixExpr())

    # Postfix
    def visitPostfixIncDec(self, ctx: TyCParser.PostfixIncDecContext):
        """Visit postfix inc/dec: postfixExpr op=(INC|DEC)"""
        operand = self.visit(ctx.postfixExpr())
        op = ctx.op.text
        return PostfixOp(op, operand)

    def visitMemberAccessExpr(self, ctx: TyCParser.MemberAccessExprContext):
        """Visit member access: postfixExpr DOT ID"""
        obj = self.visit(ctx.postfixExpr())
        member = ctx.ID().getText()
        return MemberAccess(obj, member)

    def visitFuncCallExpr(self, ctx: TyCParser.FuncCallExprContext):
        """Visit function call: postfixExpr ( argList? )"""
        # The postfixExpr should be an Identifier for function name
        func_expr = self.visit(ctx.postfixExpr())
        
        # Get arguments
        args = []
        if ctx.argList():
            args = [self.visit(e) for e in ctx.argList().expr()]
        
        # Extract function name from the expression
        if isinstance(func_expr, Identifier):
            return FuncCall(func_expr.name, args)
        elif isinstance(func_expr, MemberAccess):
            # Method call on member: a.b.func() - this is still a FuncCall
            # but we need to handle it specially (the spec doesn't seem to support this)
            # For now, treat as member access followed by call
            # This shouldn't happen in TyC as per spec
            return FuncCall(func_expr.member, args)
        else:
            # Fallback: shouldn't reach here in valid TyC code
            return FuncCall(str(func_expr), args)

    def visitPostfixExprPassthrough(self, ctx: TyCParser.PostfixExprPassthroughContext):
        """Passthrough to primaryExpr"""
        return self.visit(ctx.primaryExpr())

    # ========================================================================
    # Primary Expressions
    # ========================================================================

    def visitParenExpr(self, ctx: TyCParser.ParenExprContext):
        """Visit parenthesized expression: ( expr )"""
        return self.visit(ctx.expr())

    def visitIntLitExpr(self, ctx: TyCParser.IntLitExprContext):
        """Visit integer literal"""
        value = int(ctx.INTLIT().getText())
        return IntLiteral(value)

    def visitFloatLitExpr(self, ctx: TyCParser.FloatLitExprContext):
        """Visit float literal"""
        value = float(ctx.FLOATLIT().getText())
        return FloatLiteral(value)

    def visitStringLitExpr(self, ctx: TyCParser.StringLitExprContext):
        """Visit string literal - quotes already stripped by lexer"""
        # The lexer already strips the surrounding quotes
        value = ctx.STRINGLIT().getText()
        return StringLiteral(value)

    def visitStructLitExpr(self, ctx: TyCParser.StructLitExprContext):
        """Visit struct literal: { exprList? }"""
        values = []
        if ctx.exprList():
            values = [self.visit(e) for e in ctx.exprList().expr()]
        return StructLiteral(values)

    def visitIdExpr(self, ctx: TyCParser.IdExprContext):
        """Visit identifier expression"""
        name = ctx.ID().getText()
        return Identifier(name)
