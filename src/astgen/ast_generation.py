"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):
    """AST Generation visitor that converts parse tree to AST nodes."""

    # ============================================================================
    # Program and Top-level
    # ============================================================================
    
    def visitProgram(self, ctx: OPLangParser.ProgramContext):
        """Visit program: class_decl_list EOF"""
        class_decls = self.visit(ctx.class_decl_list())
        return Program(class_decls)

    def visitClass_decl_list(self, ctx: OPLangParser.Class_decl_listContext):
        """Visit class_decl_list: class_decl class_decl_list | class_decl"""
        class_decls = []
        # Handle both cases: single class_decl or class_decl followed by class_decl_list
        class_decls.append(self.visit(ctx.class_decl()))
        if ctx.class_decl_list():
            class_decls.extend(self.visit(ctx.class_decl_list()))
        return class_decls

    def visitClass_decl(self, ctx: OPLangParser.Class_declContext):
        """Visit class declaration with optional extends"""
        # Lấy tên class từ ID đầu tiên
        class_name = ctx.ID(0).getText()
        superclass = None
        
        # Check if class extends another class (has EXTEND keyword)
        if ctx.EXTEND():
            # Lấy tên superclass từ ID thứ hai
            superclass = ctx.ID(1).getText()
            
        members = self.visit(ctx.class_member()) if ctx.class_member() else []
        return ClassDecl(class_name, superclass, members)

    def visitClass_member(self, ctx: OPLangParser.Class_memberContext):
        """Visit class_member: decl"""
        return self.visit(ctx.decl()) if ctx.decl() else []

    def visitDecl(self, ctx: OPLangParser.DeclContext):
        """Visit decl: (attr_decl|func_decl) decl | empty"""
        current_decl = []
        
        if ctx.attr_decl():
            current_decl = [self.visit(ctx.attr_decl())]
        elif ctx.func_decl():
            current_decl = [self.visit(ctx.func_decl())]
        
        # Get remaining declarations recursively
        remaining_decls = self.visit(ctx.decl()) if ctx.decl() else []
        
        return current_decl + remaining_decls

    # ============================================================================
    # Variable/Attribute Declarations
    # ============================================================================

    def visitVar_decl_stm(self, ctx: OPLangParser.Var_decl_stmContext):
        """Visit var_decl_stm: var_decl_no_stafin var_decl_stm | empty"""
        var_decls = []
        if ctx.var_decl_no_stafin():
            var_decls.append(self.visit(ctx.var_decl_no_stafin()))
        if ctx.var_decl_stm():
            var_decls.extend(self.visit(ctx.var_decl_stm()))
        return var_decls

    def visitStafin(self, ctx: OPLangParser.StafinContext):
        """Visit stafin: STA FIN | FIN STA | STA | FIN | empty"""
        modifiers = []
        if ctx.STA():
            modifiers.append('static')
        if ctx.FIN():
            modifiers.append('final')
        return modifiers

    # Dùng cho AttributeDecl (thuộc tính trong class)
    def _visit_var_decl_list_as_attributes(self, ctx: OPLangParser.Var_decl_listContext):
        attributes = []
        var_name = ctx.var_name().getText()
        init_value = self.visit(ctx.vardecl_assign()) if ctx.vardecl_assign() else None
        attributes.append(Attribute(var_name, init_value))
        if ctx.var_decl_list():
            attributes.extend(self._visit_var_decl_list_as_attributes(ctx.var_decl_list()))
        return attributes

    def _visit_var_decl_list_ref_as_attributes(self, ctx: OPLangParser.Var_decl_list_refContext):
        attributes = []
        var_name = ctx.var_name().getText()
        init_value = self.visit(ctx.vardecl_assign())
        attributes.append(Attribute(var_name, init_value))
        if ctx.var_decl_list_ref():
            attributes.extend(self._visit_var_decl_list_ref_as_attributes(ctx.var_decl_list_ref()))
        return attributes

    # Dùng cho VariableDecl (biến cục bộ)
    def visitVar_decl_list(self, ctx: OPLangParser.Var_decl_listContext):
        variables = []
        var_name = ctx.var_name().getText()
        init_value = self.visit(ctx.vardecl_assign()) if ctx.vardecl_assign() else None
        variables.append(Variable(var_name, init_value))
        if ctx.var_decl_list():
            variables.extend(self.visit(ctx.var_decl_list()))
        return variables

    def visitVar_decl_list_ref(self, ctx: OPLangParser.Var_decl_list_refContext):
        variables = []
        var_name = ctx.var_name().getText()
        init_value = self.visit(ctx.vardecl_assign())
        variables.append(Variable(var_name, init_value))
        if ctx.var_decl_list_ref():
            variables.extend(self.visit(ctx.var_decl_list_ref()))
        return variables

    # Trong visitVar_decl, gọi helper tạo Attribute
    def visitAttr_decl(self, ctx: OPLangParser.Attr_declContext):
        """Visit attr_decl: stafin type attr_decl_list SEMI | stafin referencetype attr_decl_list_ref SEMI"""
        stafin = self.visit(ctx.stafin())
        is_static = 'static' in stafin
        is_final = 'final' in stafin

        if ctx.type_():
            attr_type = self.visit(ctx.type_())
            attributes = self._visit_attr_decl_list_as_attributes(ctx.attr_decl_list())
        else:
            attr_type = self.visit(ctx.referencetype())
            attributes = self._visit_attr_decl_list_ref_as_attributes(ctx.attr_decl_list_ref())

        return AttributeDecl(is_static, is_final, attr_type, attributes)

    def _visit_attr_decl_list_as_attributes(self, ctx: OPLangParser.Attr_decl_listContext):
        """Helper to visit attr_decl_list and create Attribute objects"""
        attributes = []
        attr_name = ctx.attr_name().getText()
        init_value = self.visit(ctx.vardecl_assign()) if ctx.vardecl_assign() else None
        attributes.append(Attribute(attr_name, init_value))
        if ctx.attr_decl_list():
            attributes.extend(self._visit_attr_decl_list_as_attributes(ctx.attr_decl_list()))
        return attributes

    def _visit_attr_decl_list_ref_as_attributes(self, ctx: OPLangParser.Attr_decl_list_refContext):
        """Helper to visit attr_decl_list_ref and create Attribute objects"""
        attributes = []
        attr_name = ctx.attr_name().getText()
        init_value = self.visit(ctx.vardecl_assign())
        attributes.append(Attribute(attr_name, init_value))
        if ctx.attr_decl_list_ref():
            attributes.extend(self._visit_attr_decl_list_ref_as_attributes(ctx.attr_decl_list_ref()))
        return attributes

    # Trong visitVar_decl_no_stafin, gọi helper tạo Variable
    def visitVar_decl_no_stafin(self, ctx: OPLangParser.Var_decl_no_stafinContext):
    # Kiểm tra có FIN hay không
        is_final = ctx.FIN() is not None
        
        if ctx.type_():
            var_type = self.visit(ctx.type_())
            variables = self.visit(ctx.var_decl_list())
        else:
            var_type = self.visit(ctx.referencetype())
            variables = self.visit(ctx.var_decl_list_ref())
            
        return VariableDecl(is_final, var_type, variables)

    def visitVardecl_assign(self, ctx: OPLangParser.Vardecl_assignContext):
        """Visit vardecl_assign: ASSIGN expr"""
        return self.visit(ctx.expr())

    # ============================================================================
    # Function/Method Declarations
    # ============================================================================

    def visitFunc_decl(self, ctx: OPLangParser.Func_declContext):
        """Visit func_decl: normal_func | constructor | destructor"""
        if ctx.normal_func():
            return self.visit(ctx.normal_func())
        elif ctx.constructor():
            return self.visit(ctx.constructor())
        else:  # destructor
            return self.visit(ctx.destructor())

    def visitNormal_func(self, ctx: OPLangParser.Normal_funcContext):
        """Visit normal function declaration"""
        is_static = ctx.STA() is not None
        
        # Check if it's main function
        if ctx.main_func():
            return_type = PrimitiveType("void")
            name = "main"
            params = []
        else:
            # Get return type
            if ctx.func_type():
                return_type = self.visit(ctx.func_type())
            else:  # referencetype
                return_type = self.visit(ctx.referencetype())
                
            name = ctx.ID().getText()
            params = self.visit(ctx.func_param_list()) if ctx.func_param_list() else []
            
        body = self.visit(ctx.blockstm())
        return MethodDecl(is_static, return_type, name, params, body)

    def visitConstructor(self, ctx: OPLangParser.ConstructorContext):
        """Visit constructor: default_constructor | copy_constructor | user_constructor"""
        if ctx.default_constructor():
            return self.visit(ctx.default_constructor())
        elif ctx.copy_constructor():
            return self.visit(ctx.copy_constructor())
        else:  # user_constructor
            return self.visit(ctx.user_constructor())

    def visitDefault_constructor(self, ctx: OPLangParser.Default_constructorContext):
        """Visit default_constructor: ID LRB RRB blockstm"""
        name = ctx.ID().getText()
        body = self.visit(ctx.blockstm())
        return ConstructorDecl(name, [], body)

    def visitCopy_constructor(self, ctx: OPLangParser.Copy_constructorContext):
        """Visit copy_constructor: ID LRB ID ID RRB blockstm"""
        name = ctx.ID(0).getText()
        param_type = ClassType(ctx.ID(1).getText())
        param_name = ctx.ID(2).getText()
        params = [Parameter(param_type, param_name)]
        body = self.visit(ctx.blockstm())
        return ConstructorDecl(name, params, body)

    def visitUser_constructor(self, ctx: OPLangParser.User_constructorContext):
        """Visit user_constructor: ID LRB func_param_list RRB blockstm"""
        name = ctx.ID().getText()
        params = self.visit(ctx.func_param_list()) if ctx.func_param_list() else []
        body = self.visit(ctx.blockstm())
        return ConstructorDecl(name, params, body)

    def visitDestructor(self, ctx: OPLangParser.DestructorContext):
        """Visit destructor: '~' ID LRB RRB blockstm"""
        name = ctx.ID().getText()
        body = self.visit(ctx.blockstm())
        return DestructorDecl(name, body)

    def visitFunc_param_list(self, ctx: OPLangParser.Func_param_listContext):
        """Visit func_param_list"""
        if ctx.func_param_prime():
            return self.visit(ctx.func_param_prime())
        return []

    def visitFunc_param_prime(self, ctx: OPLangParser.Func_param_primeContext):
        """Visit func_param_prime"""
        params = []
        
        # Get parameter type
        if ctx.type_():
            param_type = self.visit(ctx.type_())
        else:  # referencetype
            param_type = self.visit(ctx.referencetype())
            
        # Get parameter names from func_param
        param_names = self.visit(ctx.func_param())
        for name in param_names:
            params.append(Parameter(param_type, name))
            
        # Process remaining parameters if any
        if ctx.func_param_prime():
            params.extend(self.visit(ctx.func_param_prime()))
            
        return params

    def visitFunc_param(self, ctx: OPLangParser.Func_paramContext):
        """Visit func_param: var_name COMMA func_param | var_name"""
        param_names = [ctx.var_name().getText()]
        
        if ctx.func_param():
            param_names.extend(self.visit(ctx.func_param()))
            
        return param_names

    # ============================================================================
    # Type System
    # ============================================================================

    def visitFunc_type(self, ctx: OPLangParser.Func_typeContext):
        """Visit func_type: type | VOID"""
        if ctx.VOID():
            return PrimitiveType("void")
        return self.visit(ctx.type_())

    def visitType(self, ctx: OPLangParser.TypeContext):
        """Visit type: primitivetype | arraytype | classtype"""
        if ctx.primitivetype():
            return self.visit(ctx.primitivetype())
        elif ctx.arraytype():
            return self.visit(ctx.arraytype())
        else:  # classtype
            return self.visit(ctx.classtype())

    def visitPrimitivetype(self, ctx: OPLangParser.PrimitivetypeContext):
        """Visit primitivetype: INT | FLOAT | STRING | BOOL"""
        if ctx.INT():
            return PrimitiveType("int")
        elif ctx.FLOAT():
            return PrimitiveType("float")
        elif ctx.STRING():
            return PrimitiveType("string")
        else:  # BOOL
            return PrimitiveType("boolean")

    def visitArraytype(self, ctx: OPLangParser.ArraytypeContext):
        """Visit arraytype"""
        if ctx.arraytype_primitive():
            return self.visit(ctx.arraytype_primitive())
        else:  # arraytype_non_primitive
            return self.visit(ctx.arraytype_non_primitive())

    def visitArraytype_primitive(self, ctx: OPLangParser.Arraytype_primitiveContext):
        """Visit arraytype_primitive: primitivetype LSB INTLIT RSB"""
        element_type = self.visit(ctx.primitivetype())
        size = int(ctx.INTLIT().getText())
        return ArrayType(element_type, size)

    def visitArraytype_non_primitive(self, ctx: OPLangParser.Arraytype_non_primitiveContext):
        """Visit arraytype_non_primitive: ID LSB INTLIT RSB"""
        element_type = ClassType(ctx.ID().getText())
        size = int(ctx.INTLIT().getText())
        return ArrayType(element_type, size)

    def visitReferencetype(self, ctx: OPLangParser.ReferencetypeContext):
        """Visit referencetype: (primitivetype | classtype | arraytype) REF"""
        if ctx.primitivetype():
            referenced_type = self.visit(ctx.primitivetype())
        elif ctx.classtype():
            referenced_type = self.visit(ctx.classtype())
        else:  # arraytype
            referenced_type = self.visit(ctx.arraytype())
        return ReferenceType(referenced_type)

    def visitClasstype(self, ctx: OPLangParser.ClasstypeContext):
        """Visit classtype: ID"""
        return ClassType(ctx.ID().getText())

    # ============================================================================
    # Statements
    # ============================================================================

    def visitBlockstm(self, ctx: OPLangParser.BlockstmContext):
        """Visit blockstm: LB var_decl_stm stmlist RB"""
        var_decls = self.visit(ctx.var_decl_stm()) if ctx.var_decl_stm() else []
        statements = self.visit(ctx.stmlist()) if ctx.stmlist() else []
        return BlockStatement(var_decls, statements)

    def visitStmlist(self, ctx: OPLangParser.StmlistContext):
        """Visit stmlist: stm stmlist | empty"""
        statements = []
        if ctx.stm():
            statements.append(self.visit(ctx.stm()))
        if ctx.stmlist():
            statements.extend(self.visit(ctx.stmlist()))
        return statements

    def visitStm(self, ctx: OPLangParser.StmContext):
        """Visit stm: various statement types"""
        if ctx.assingstm():
            return self.visit(ctx.assingstm())
        elif ctx.ifstm():
            return self.visit(ctx.ifstm())
        elif ctx.forstm():
            return self.visit(ctx.forstm())
        elif ctx.breakstm():
            return self.visit(ctx.breakstm())
        elif ctx.continuestm():
            return self.visit(ctx.continuestm())
        elif ctx.returnstm():
            return self.visit(ctx.returnstm())
        elif ctx.blockstm():
            return self.visit(ctx.blockstm())
        else:  # invocationstm
            return self.visit(ctx.invocationstm())

    def visitAssingstm(self, ctx: OPLangParser.AssingstmContext):
        """Visit assignment statement"""
        # Determine LHS type based on what's present
        if ctx.invocationstm_frame():
            # Method/member access on LHS (like obj.field or obj.method())
            postfix_expr = self.visit(ctx.invocationstm_frame())
            lhs = PostfixLHS(postfix_expr)
        elif ctx.ID() and ctx.LSB():  
            # Array access (ID[expr])
            name = ctx.ID().getText()  # Không dùng index
            index = self.visit(ctx.expr())
            array_access = PostfixExpression(Identifier(name), [ArrayAccess(index)])
            lhs = PostfixLHS(array_access)
        elif ctx.ID():  
            # Simple ID
            lhs = IdLHS(ctx.ID().getText())  # Không dùng index
        else:
            # Should not reach here if grammar is correct
            raise Exception("Invalid assignment statement")
            
        rhs = self.visit(ctx.vardecl_assign())
        return AssignmentStatement(lhs, rhs)

    def visitIfstm(self, ctx: OPLangParser.IfstmContext):
        """Visit if statement"""
        # Get condition expression
        condition = self.visit(ctx.expr())
        
        # Get then statement/block
        # Kiểm tra xem phần THEN là blockstm hay stm
        if ctx.blockstm():
            then_stmt = self.visit(ctx.blockstm())  # Không dùng index
        else:
            then_stmt = self.visit(ctx.stm())  # Không dùng index
            
        # Get else statement/block from elsestm if exists
        else_stmt = None
        if ctx.elsestm():
            else_stmt = self.visit(ctx.elsestm())
                    
        return IfStatement(condition, then_stmt, else_stmt)
    
    def visitElsestm(self, ctx: OPLangParser.ElsestmContext):
        """Visit elsestm: ELSE (stm | blockstm) | empty"""
        if ctx.ELSE():
            # There is an else clause
            if ctx.blockstm():
                return self.visit(ctx.blockstm())
            else:
                return self.visit(ctx.stm())
        return None  # No else clause

    def visitForstm(self, ctx: OPLangParser.ForstmContext):
        """Visit for statement"""
        variable = ctx.ID().getText()
        start_expr = self.visit(ctx.expr(0))
        direction = "to" if ctx.TO() else "downto"
        end_expr = self.visit(ctx.expr(1))
        
        if ctx.blockstm():
            body = self.visit(ctx.blockstm())
        else:
            body = self.visit(ctx.stm())
            
        return ForStatement(variable, start_expr, direction, end_expr, body)

    def visitBreakstm(self, ctx: OPLangParser.BreakstmContext):
        """Visit break statement"""
        return BreakStatement()

    def visitContinuestm(self, ctx: OPLangParser.ContinuestmContext):
        """Visit continue statement"""
        return ContinueStatement()

    def visitReturnstm(self, ctx: OPLangParser.ReturnstmContext):
        """Visit return statement: RETURN expr SEMI"""
        # Bắt buộc có expr theo grammar mới
        value = self.visit(ctx.expr())
        return ReturnStatement(value)

    def visitInvocationstm(self, ctx: OPLangParser.InvocationstmContext):
        """Visit invocation statement"""
        method_call = self.visit(ctx.invocationstm_frame())
        return MethodInvocationStatement(method_call)

    def visitInvocationstm_frame(self, ctx: OPLangParser.Invocationstm_frameContext):
        """Visit invocationstm_frame: expr dotting"""
        left_expr = self.visit(ctx.expr())
        postfix_ops = self.visit(ctx.dotting())
        return PostfixExpression(left_expr, postfix_ops)

    # ============================================================================
    # Expressions
    # ============================================================================

    def visitExpr(self, ctx: OPLangParser.ExprContext):
        """Visit expr: comparison operators"""
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expr1(0))
            right = self.visit(ctx.expr1(1))
            if ctx.LESST():
                op = "<"
            elif ctx.LESSEQ():
                op = "<="
            elif ctx.MORET():
                op = ">"
            else:  # MOREEQ
                op = ">="
            return BinaryOp(left, op, right)
        return self.visit(ctx.expr1(0))

    def visitExpr1(self, ctx: OPLangParser.Expr1Context):
        """Visit expr1: equality operators"""
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expr2(0))
            right = self.visit(ctx.expr2(1))
            op = "==" if ctx.EQ() else "!="
            return BinaryOp(left, op, right)
        return self.visit(ctx.expr2(0))

    def visitExpr2(self, ctx: OPLangParser.Expr2Context):
        """Visit expr2: logical operators"""
        if ctx.getChildCount() > 1:
            left = self.visit(ctx.expr2())
            right = self.visit(ctx.expr3())
            op = "&&" if ctx.AND() else "||"
            return BinaryOp(left, op, right)
        return self.visit(ctx.expr3())

    def visitExpr3(self, ctx: OPLangParser.Expr3Context):
        """Visit expr3: addition/subtraction"""
        if ctx.getChildCount() > 1:
            left = self.visit(ctx.expr3())
            right = self.visit(ctx.expr4())
            op = "+" if ctx.ADD() else "-"
            return BinaryOp(left, op, right)
        return self.visit(ctx.expr4())

    def visitExpr4(self, ctx: OPLangParser.Expr4Context):
        """Visit expr4: multiplication/division/modulo"""
        if ctx.getChildCount() > 1:
            left = self.visit(ctx.expr4())
            right = self.visit(ctx.expr5())
            if ctx.MUL():
                op = "*"
            elif ctx.INTDIV():
                op = "\\"
            elif ctx.FLOATDIV():
                op = "/"
            else:  # MOD
                op = "%"
            return BinaryOp(left, op, right)
        return self.visit(ctx.expr5())

    def visitExpr5(self, ctx: OPLangParser.Expr5Context):
        """Visit expr5: string concatenation"""
        if ctx.getChildCount() > 1:
            left = self.visit(ctx.expr5())
            right = self.visit(ctx.expr6())
            return BinaryOp(left, "^", right)
        return self.visit(ctx.expr6())

    def visitExpr6(self, ctx: OPLangParser.Expr6Context):
        """Visit expr6: logical NOT"""
        if ctx.NOT():
            operand = self.visit(ctx.expr6())
            return UnaryOp("!", operand)
        return self.visit(ctx.expr7())

    def visitExpr7(self, ctx: OPLangParser.Expr7Context):
        """Visit expr7: unary plus/minus"""
        if ctx.ADD() or ctx.SUB():
            op = "+" if ctx.ADD() else "-"
            operand = self.visit(ctx.expr7())
            return UnaryOp(op, operand)
        return self.visit(ctx.expr8())

    def visitExpr8(self, ctx: OPLangParser.Expr8Context):
        """Visit expr8: expr8 LSB expr RSB | expr9"""
        if ctx.LSB():  # Has array access
            base = self.visit(ctx.expr8())
            index = self.visit(ctx.expr())
            # Mỗi array access tạo PostfixExpression mới
            return PostfixExpression(base, [ArrayAccess(index)])
        return self.visit(ctx.expr9())

    def visitExpr9(self, ctx: OPLangParser.Expr9Context):
        """Visit expr9: expr9 dotting | expr10"""
        if ctx.dotting():  # Has dotting
            base = self.visit(ctx.expr9())
            ops = self.visit(ctx.dotting())
            
            # Tạo PostfixExpression lồng nhau
            result = base
            for op in ops:
                result = PostfixExpression(result, [op])
            return result
        return self.visit(ctx.expr10())

    def visitDotting(self, ctx: OPLangParser.DottingContext):
        """Visit dotting - trả về list các operations"""
        ops = []
        
        if ctx.callfuncstm():
            ops.append(self.visit(ctx.callfuncstm()))
        elif ctx.ID():
            ops.append(MemberAccess(ctx.ID().getText()))
        
        # Xử lý đệ quy
        if ctx.dotting():
            ops.extend(self.visit(ctx.dotting()))
        
        return ops

    def visitExpr10(self, ctx: OPLangParser.Expr10Context):
        """Visit expr10: object creation"""
        if ctx.NEW():
            expr = self.visit(ctx.expr10())
            # Extract class name and arguments from the expression
            if isinstance(expr, PostfixExpression) and expr.postfix_ops:
                if isinstance(expr.postfix_ops[0], MethodCall):
                    class_name = expr.primary.name if isinstance(expr.primary, Identifier) else ""
                    args = expr.postfix_ops[0].args
                    return ObjectCreation(class_name, args)
            elif isinstance(expr, Identifier):
                return ObjectCreation(expr.name, [])
        return self.visit(ctx.expr11())

    def visitExpr11(self, ctx: OPLangParser.Expr11Context):
        """Visit expr11: primary expressions"""
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        elif ctx.BOOLLIT():
            return BoolLiteral(ctx.BOOLLIT().getText() == 'true')
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.callfuncstm():
            # Method call without receiver
            call = self.visit(ctx.callfuncstm())
            return PostfixExpression(Identifier(call.method_name), [call])
        elif ctx.array():
            return self.visit(ctx.array())
        elif ctx.THIS():
            return ThisExpression()
        elif ctx.NIL():
            return NilLiteral()
        else:  # Parenthesized expression
            expr = self.visit(ctx.expr())
            return ParenthesizedExpression(expr)

    def visitCallfuncstm(self, ctx: OPLangParser.CallfuncstmContext):
        """Visit callfuncstm: ID LRB input_func_param_list RRB"""
        method_name = ctx.ID().getText()
        args = self.visit(ctx.input_func_param_list()) if ctx.input_func_param_list() else []
        return MethodCall(method_name, args)

    def visitInput_func_param_list(self, ctx: OPLangParser.Input_func_param_listContext):
        """Visit input_func_param_list"""
        if ctx.input_func_param_prime():
            return self.visit(ctx.input_func_param_prime())
        return []

    def visitInput_func_param_prime(self, ctx: OPLangParser.Input_func_param_primeContext):
        """Visit input_func_param_prime"""
        params = [self.visit(ctx.input_func_param())]
        if ctx.input_func_param_prime():
            params.extend(self.visit(ctx.input_func_param_prime()))
        return params

    def visitInput_func_param(self, ctx: OPLangParser.Input_func_paramContext):
        """Visit input_func_param"""
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        else:  # expr
            return self.visit(ctx.expr())

    # ============================================================================
    # Array Literals
    # ============================================================================

       # ============================================================================
    # Array Literals – HỖ TRỢ TẤT CẢ CÁC KIỂU (MIXED TYPES) ← QUAN TRỌNG NHẤT
    # ============================================================================

    def visitArray(self, ctx: OPLangParser.ArrayContext):
        """array: LCB array_element_list? RCB"""
        if ctx.array_element_list():
            elements = self.visit(ctx.array_element_list())
        else:
            elements = []                       # mảng rỗng {}
        return ArrayLiteral(elements)

    def visitArray_element_list(self, ctx: OPLangParser.Array_element_listContext):
        """array_element_list: expr (COMMA expr)*"""
        # ctx.expr() trả về danh sách tất cả các expr trong { ... }
        return [self.visit(e) for e in ctx.expr()]