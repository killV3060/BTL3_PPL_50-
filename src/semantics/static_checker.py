"""
Static Semantic Checker for OPLang Programming Language
"""

from typing import Dict, List, Optional, Any
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ClassDecl, AttributeDecl, Attribute, MethodDecl,
    ConstructorDecl, DestructorDecl, Parameter, VariableDecl, Variable,
    AssignmentStatement, IfStatement, ForStatement, BreakStatement,
    ContinueStatement, ReturnStatement, MethodInvocationStatement,
    BlockStatement, PrimitiveType, ArrayType, ClassType, ReferenceType,
    IdLHS, PostfixLHS, BinaryOp, UnaryOp, PostfixExpression, PostfixOp,
    MethodCall, MemberAccess, ArrayAccess, ObjectCreation, Identifier,
    ThisExpression, ParenthesizedExpression, IntLiteral, FloatLiteral,
    BoolLiteral, StringLiteral, ArrayLiteral, NilLiteral
)
from .static_error import (
    StaticError, Redeclared, UndeclaredIdentifier, UndeclaredClass,
    UndeclaredAttribute, UndeclaredMethod, CannotAssignToConstant,
    TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
    MustInLoop, IllegalConstantExpression, IllegalArrayLiteral,
    IllegalMemberAccess, NoEntryPoint
)


class ErrorType:
    def __repr__(self):
        return "<ErrorType>"

ERROR = ErrorType()


class StaticChecker(ASTVisitor):
    
    def __init__(self):
        self.class_table: Dict[str, Dict[str, Any]] = {}
        self.scopes: List[Dict[str, Any]] = []
        self.current_class: Optional[str] = None
        self.current_method: Optional[str] = None
        self.current_method_return_type: Optional[Any] = None
        self.current_method_is_static: bool = False
        self.loop_depth: int = 0
        self.has_main: bool = False
        self.in_constructor: bool = False

    def check_program(self, ast: Program, require_main: bool = False):
        self._build_class_table(ast)
        self._add_io_class()
        self.visitProgram(ast)
        if require_main and not self.has_main:
            raise NoEntryPoint()

    def _add_io_class(self):
        if "IO" not in self.class_table:
            self.class_table["IO"] = {
                "parent": None,
                "attributes": {},
                "methods": {
                    "writeInt": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("int"), "x")], "isStatic": True},
                    "writeFloat": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("float"), "x")], "isStatic": True},
                    "writeString": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("string"), "x")], "isStatic": True},
                    "writeBool": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("boolean"), "x")], "isStatic": True},
                    "writeIntLn": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("int"), "x")], "isStatic": True},
                    "writeFloatLn": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("float"), "x")], "isStatic": True},
                    "writeStringLn": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("string"), "x")], "isStatic": True},
                    "writeBoolLn": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("boolean"), "x")], "isStatic": True},
                    "writeStrLn": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("string"), "x")], "isStatic": True},
                    "readInt": {"returnType": PrimitiveType("int"), "params": [], "isStatic": True},
                    "readFloat": {"returnType": PrimitiveType("float"), "params": [], "isStatic": True},
                    "readString": {"returnType": PrimitiveType("void"), "params": [], "isStatic": True},
                    "readBool": {"returnType": PrimitiveType("boolean"), "params": [], "isStatic": True},
                },
                "constructors": {},
                "destructor": None
            }

    def _get_constructor_signature(self, params):
        return tuple(self._get_type_signature(p.param_type) for p in (params or []))
    
    def _get_type_signature(self, t):
        if isinstance(t, PrimitiveType):
            return t.type_name
        if isinstance(t, ClassType):
            return t.class_name
        if isinstance(t, ArrayType):
            return f"{self._get_type_signature(t.element_type)}[{t.size}]"
        if isinstance(t, ReferenceType):
            return f"{self._get_type_signature(t.referenced_type)}&"
        return str(t)

    def _build_class_table(self, ast: Program):
        self.class_table = {}
        self.has_main = False
        class_list = ast.class_decls or []
        
        for c in class_list:
            if not isinstance(c, ClassDecl):
                continue
            name = c.name
            if name in self.class_table:
                raise Redeclared("Class", name)
            parent = c.superclass
            self.class_table[name] = {
                "parent": parent, 
                "attributes": {}, 
                "methods": {},
                "constructors": {},
                "destructor": None
            }

        for name, info in self.class_table.items():
            parent = info["parent"]
            if parent and parent not in self.class_table:
                raise UndeclaredClass(parent)

        for c in class_list:
            if not isinstance(c, ClassDecl):
                continue
            cname = c.name
            info = self.class_table[cname]
            
            declared_names = set()
            
            for m in c.members or []:
                if isinstance(m, AttributeDecl):
                    for a in m.attributes or []:
                        aname = a.name
                        if aname in declared_names:
                            if m.is_final:
                                raise Redeclared("Constant", aname)
                            else:
                                raise Redeclared("Attribute", aname)
                        declared_names.add(aname)
                        info["attributes"][aname] = {
                            "type": m.attr_type,
                            "isFinal": m.is_final,
                            "isStatic": m.is_static,
                            "init": a.init_value,
                        }
                elif isinstance(m, MethodDecl):
                    mname = m.name
                    if mname in declared_names:
                        raise Redeclared("Method", mname)
                    declared_names.add(mname)
                    info["methods"][mname] = {
                        "returnType": m.return_type,
                        "params": m.params or [],
                        "isStatic": m.is_static,
                    }
                    if (mname == "main" and m.is_static and 
                        isinstance(m.return_type, PrimitiveType) and
                        m.return_type.type_name == "void" and 
                        len(m.params or []) == 0):
                        self.has_main = True
                elif isinstance(m, ConstructorDecl):
                    cons_name = m.name
                    if cons_name in declared_names:
                        raise Redeclared("Constructor", cons_name)
                    
                    sig = self._get_constructor_signature(m.params)
                    if sig in info["constructors"]:
                        raise Redeclared("Constructor", cname)
                    
                    if not info["constructors"]:
                        declared_names.add(cons_name)
                    
                    info["constructors"][sig] = {
                        "returnType": ClassType(cname),
                        "params": m.params or [],
                        "isStatic": False
                    }
                elif isinstance(m, DestructorDecl):
                    dname = m.name
                    if dname in declared_names:
                        raise Redeclared("Destructor", dname)
                    
                    if info["destructor"] is not None:
                        raise Redeclared("Destructor", cname)
                    
                    declared_names.add(dname)
                    info["destructor"] = {
                        "returnType": None,
                        "params": [],
                        "isStatic": False
                    }

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if self.scopes:
            self.scopes.pop()

    def declare_local(self, name: str, typeNode: Any, isFinal: bool, initialized: bool = False):
        if not self.scopes:
            self.enter_scope()
        cur = self.scopes[-1]
        if name in cur:
            if isFinal:
                raise Redeclared("Constant", name)
            else:
                raise Redeclared("Variable", name)
        cur[name] = {"type": typeNode, "isFinal": isFinal, "initialized": initialized}

    def declare_param(self, name: str, typeNode: Any):
        if not self.scopes:
            self.enter_scope()
        if name in self.scopes[-1]:
            raise Redeclared("Parameter", name)
        self.scopes[-1][name] = {"type": typeNode, "isFinal": False, "initialized": True}

    def lookup(self, name: str):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def lookup_in_class_attrs(self, class_name: str, attr: str):
        cur = class_name
        visited = set()
        while cur and cur not in visited:
            visited.add(cur)
            clsinfo = self.class_table.get(cur)
            if clsinfo and attr in clsinfo["attributes"]:
                return clsinfo["attributes"][attr]
            cur = clsinfo["parent"] if clsinfo else None
        return None

    def lookup_method(self, class_name: str, method_name: str):
        cur = class_name
        visited = set()
        while cur and cur not in visited:
            visited.add(cur)
            clsinfo = self.class_table.get(cur)
            if clsinfo and method_name in clsinfo["methods"]:
                return clsinfo["methods"][method_name]
            cur = clsinfo["parent"] if clsinfo else None
        return None
    
    def lookup_constructor(self, class_name: str, arg_types: List):
        clsinfo = self.class_table.get(class_name)
        if not clsinfo:
            return None
        sig = tuple(self._get_type_signature(t) for t in arg_types)
        return clsinfo["constructors"].get(sig)

    def type_name(self, t: Any) -> str:
        if t is None:
            return "void"
        if isinstance(t, ErrorType):
            return "<error>"
        if isinstance(t, PrimitiveType):
            return t.type_name
        if isinstance(t, ClassType):
            return t.class_name
        if isinstance(t, ArrayType):
            return f"{self.type_name(t.element_type)}[{t.size}]"
        return str(t)

    def is_int_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and t.type_name.lower() == "int"

    def is_float_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and t.type_name.lower() == "float"

    def is_bool_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and t.type_name.lower() in ("boolean", "bool")

    def is_string_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and t.type_name.lower() == "string"

    def is_array_type(self, t: Any) -> bool:
        return isinstance(t, ArrayType)

    def is_class_type(self, t: Any) -> bool:
        return isinstance(t, ClassType)

    def _require_class_defined(self, type_node):
        if isinstance(type_node, ClassType):
            if type_node.class_name != "nil" and type_node.class_name not in self.class_table:
                raise UndeclaredClass(type_node.class_name)
        elif isinstance(type_node, ArrayType):
            self._require_class_defined(type_node.element_type)
        elif isinstance(type_node, ReferenceType):
            self._require_class_defined(type_node.referenced_type)

    def same_type(self, a: Any, b: Any) -> bool:
        if a is ERROR or b is ERROR:
            return False
        if a is None and b is None:
            return True
        if type(a) != type(b):
            return False
        if isinstance(a, PrimitiveType):
            return a.type_name.lower() == b.type_name.lower()
        if isinstance(a, ClassType):
            return a.class_name == b.class_name
        if isinstance(a, ArrayType):
            return self.same_type(a.element_type, b.element_type) and a.size == b.size
        return str(a) == str(b)

    def is_subtype(self, sub: Any, sup: Any) -> bool:
        if isinstance(sub, ClassType) and isinstance(sup, ClassType):
            sub_name = sub.class_name
            sup_name = sup.class_name
            cur = sub_name
            visited = set()
            while cur and cur not in visited:
                if cur == sup_name:
                    return True
                visited.add(cur)
                clsinfo = self.class_table.get(cur)
                cur = clsinfo["parent"] if clsinfo else None
            return False
        return False

    def compatible(self, expected: Any, actual: Any) -> bool:
        if expected is ERROR or actual is ERROR:
            return True
        if expected is None:
            return actual is None
        if self.same_type(expected, actual):
            return True
        if self.is_float_type(expected) and self.is_int_type(actual):
            return True
        if self.is_class_type(actual) and self.is_class_type(expected):
            return self.is_subtype(actual, expected)
        if self.is_array_type(expected) and self.is_array_type(actual):
            return (self.compatible(expected.element_type, actual.element_type) and 
                    expected.size == actual.size)
        return False

    def _is_constant_expr(self, expr) -> bool:
        if expr is None:
            return False
        if isinstance(expr, (IntLiteral, FloatLiteral, BoolLiteral, StringLiteral)):
            return True
        if isinstance(expr, NilLiteral):
            return False
        if isinstance(expr, ArrayLiteral):
            return all(self._is_constant_expr(e) for e in (expr.value or []))
        if isinstance(expr, BinaryOp):
            return self._is_constant_expr(expr.left) and self._is_constant_expr(expr.right)
        if isinstance(expr, UnaryOp):
            return self._is_constant_expr(expr.operand)
        if isinstance(expr, ParenthesizedExpression):
            return self._is_constant_expr(expr.expr)
        if isinstance(expr, Identifier):
            info = self.lookup(expr.name)
            if info and info.get("isFinal"):
                return True
            if self.current_class:
                attr = self.lookup_in_class_attrs(self.current_class, expr.name)
                if attr and attr.get("isFinal"):
                    return True
            return False
        return False

    def _is_constant_expr_for_attr(self, expr, expected_type) -> bool:
        if expr is None:
            return False
        if isinstance(expr, (IntLiteral, FloatLiteral, BoolLiteral, StringLiteral)):
            return True
        if isinstance(expr, NilLiteral):
            return False
        if isinstance(expr, ObjectCreation):
            return True
        if isinstance(expr, ArrayLiteral):
            return all(self._is_constant_expr_for_attr(e, None) for e in (expr.value or []))
        if isinstance(expr, BinaryOp):
            return self._is_constant_expr_for_attr(expr.left, None) and self._is_constant_expr_for_attr(expr.right, None)
        if isinstance(expr, UnaryOp):
            return self._is_constant_expr_for_attr(expr.operand, None)
        if isinstance(expr, ParenthesizedExpression):
            return self._is_constant_expr_for_attr(expr.expr, expected_type)
        if isinstance(expr, Identifier):
            info = self.lookup(expr.name)
            if info and info.get("isFinal"):
                return True
            if self.current_class:
                attr = self.lookup_in_class_attrs(self.current_class, expr.name)
                if attr and attr.get("isFinal"):
                    return True
            return False
        return False

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit{node.__class__.__name__}'
        visitor = getattr(self, method_name, None)
        if visitor:
            return visitor(node)
        return None

    def visitProgram(self, ast: Program):
        self.enter_scope()
        self.scopes[-1]["io"] = {"type": ClassType("IO"), "isFinal": True, "initialized": True}
        for cls in ast.class_decls or []:
            if cls:
                self.visitClassDecl(cls)
        self.exit_scope()

    def visitClassDecl(self, ast: ClassDecl):
        self.current_class = ast.name
        self.enter_scope()
        self.scopes[-1]["this"] = {"type": ClassType(ast.name), "isFinal": True}
        for mem in ast.members or []:
            if mem:
                self.visit(mem)
        self.exit_scope()
        self.current_class = None

    def visitAttributeDecl(self, ast: AttributeDecl):
        for attr in ast.attributes or []:
            if ast.is_final:
                if attr.init_value is None:
                    pass
                elif isinstance(attr.init_value, NilLiteral):
                    if self.is_class_type(ast.attr_type) or self.is_array_type(ast.attr_type):
                        raise IllegalConstantExpression(attr.init_value)
                    else:
                        raise TypeMismatchInConstant(ast)
                elif not self._is_constant_expr_for_attr(attr.init_value, ast.attr_type):
                    raise IllegalConstantExpression(ast)
                elif attr.init_value:
                    try:
                        init_type = self.visit(attr.init_value)
                    except TypeMismatchInExpression:
                        raise TypeMismatchInConstant(ast)
                    if init_type is not ERROR and not self.compatible(ast.attr_type, init_type):
                        raise TypeMismatchInConstant(ast)
            elif attr.init_value:
                init_type = self.visit(attr.init_value)
                if init_type is not ERROR and not self.compatible(ast.attr_type, init_type):
                    raise TypeMismatchInStatement(ast)

    def visitMethodDecl(self, ast: MethodDecl):
        self.current_method = ast.name
        self.current_method_return_type = ast.return_type
        self.current_method_is_static = ast.is_static
        self.enter_scope()
        
        for param in ast.params or []:
            self._require_class_defined(param.param_type)
            self.declare_param(param.name, param.param_type)
        
        if ast.body:
            self.visitBlockStatement(ast.body)
        
        self.exit_scope()
        self.current_method = None
        self.current_method_return_type = None
        self.current_method_is_static = False

    def visitConstructorDecl(self, ast: ConstructorDecl):
        if ast.name != self.current_class:
            raise TypeMismatchInStatement(ast)
        
        self.current_method = ast.name
        self.current_method_return_type = ClassType(self.current_class) if self.current_class else None
        self.in_constructor = True
        self.enter_scope()
        
        for param in ast.params or []:
            self._require_class_defined(param.param_type)
            self.declare_param(param.name, param.param_type)
        
        if ast.body:
            self.visitBlockStatement(ast.body)
        
        self.exit_scope()
        self.current_method = None
        self.current_method_return_type = None
        self.in_constructor = False

    def visitDestructorDecl(self, ast: DestructorDecl):
        if ast.name != self.current_class:
            raise TypeMismatchInStatement(ast)
        
        self.current_method = "~" + ast.name
        self.current_method_return_type = None
        self.enter_scope()
        if ast.body:
            self.visitBlockStatement(ast.body)
        self.exit_scope()
        self.current_method = None

    def visitBlockStatement(self, ast: BlockStatement):
        self.enter_scope()
        for vdecl in ast.var_decls or []:
            if vdecl:
                self.visitVariableDecl(vdecl)
        for stmt in ast.statements or []:
            if stmt:
                self.visit(stmt)
        self.exit_scope()

    def visitVariableDecl(self, ast: VariableDecl):
        self._require_class_defined(ast.var_type)
        for var in ast.variables or []:
            if var.init_value:
                if ast.is_final:
                    if not self._is_constant_expr(var.init_value):
                        raise IllegalConstantExpression(var.init_value)
                    init_type = self.visit(var.init_value)
                    if init_type is not ERROR and not self.compatible(ast.var_type, init_type):
                        raise TypeMismatchInConstant(ast)
                else:
                    init_node = var.init_value
                    init_type = self.visit(init_node)
                    if init_type is not ERROR and not self.compatible(ast.var_type, init_type):
                        if isinstance(init_node, (UnaryOp, BinaryOp, PostfixExpression, MethodCall,
                                                ParenthesizedExpression, ArrayAccess, Identifier)):
                            raise TypeMismatchInExpression(init_node)
                        raise TypeMismatchInStatement(ast)


            self.declare_local(var.name, ast.var_type, ast.is_final, var.init_value is not None)

    def visitAssignmentStatement(self, ast: AssignmentStatement):
        if isinstance(ast.lhs, IdLHS):
            name = ast.lhs.name
            info = self.lookup(name)
            if info is None:
                if self.current_class:
                    attr = self.lookup_in_class_attrs(self.current_class, name)
                    if attr:
                        if attr.get("isFinal") and not self.in_constructor:
                            raise CannotAssignToConstant(ast)
                        lhs_type = attr["type"]
                    else:
                        raise UndeclaredIdentifier(name)
                else:
                    raise UndeclaredIdentifier(name)
            else:
                if info.get("isFinal"):
                    raise CannotAssignToConstant(ast)
                lhs_type = info["type"]
        elif isinstance(ast.lhs, PostfixLHS):
            lhs_type = self._visit_postfix_lhs(ast.lhs, ast)
            if lhs_type is ERROR:
                return
        else:
            lhs_type = ERROR

        rhs_type = self.visit(ast.rhs)
        if rhs_type is ERROR or lhs_type is ERROR:
            return
        
        if isinstance(ast.rhs, NilLiteral):
            if not (self.is_class_type(lhs_type) or self.is_array_type(lhs_type)):
                raise TypeMismatchInStatement(ast)
            return
        
        if not self.compatible(lhs_type, rhs_type):
            rhs_node = ast.rhs
            if isinstance(rhs_node, PostfixExpression) and any(isinstance(op, MethodCall) for op in (rhs_node.postfix_ops or [])):
                raise TypeMismatchInExpression(rhs_node)
            if isinstance(rhs_node, (PostfixExpression, BinaryOp, UnaryOp, ParenthesizedExpression, MethodCall)):
                raise TypeMismatchInExpression(rhs_node)
            raise TypeMismatchInStatement(ast)


    def _visit_postfix_lhs(self, lhs: PostfixLHS, stmt):
        pexpr = lhs.postfix_expr
        current_type = self.visit(pexpr.primary)
        if current_type is ERROR:
            return ERROR
        
        is_class_name_access = False
        if isinstance(pexpr.primary, Identifier):
            name = pexpr.primary.name
            if name in self.class_table:
                is_class_name_access = True
        
        for i, op in enumerate(pexpr.postfix_ops):
            is_last = (i == len(pexpr.postfix_ops) - 1)
            
            if isinstance(op, MemberAccess):
                if is_class_name_access:
                    cls_name = pexpr.primary.name
                    attr_info = self.lookup_in_class_attrs(cls_name, op.member_name)
                    if attr_info is None:
                        raise UndeclaredAttribute(op.member_name)
                    if not attr_info.get("isStatic", False):
                        raise IllegalMemberAccess(pexpr)
                    if is_last and attr_info.get("isFinal") and not self.in_constructor:
                        raise CannotAssignToConstant(stmt)
                    current_type = attr_info["type"]
                    is_class_name_access = False
                else:
                    if not isinstance(current_type, ClassType):
                        raise TypeMismatchInExpression(pexpr)
                    cls_name = current_type.class_name
                    attr_info = self.lookup_in_class_attrs(cls_name, op.member_name)
                    if attr_info is None:
                        raise UndeclaredAttribute(op.member_name)
                    if attr_info.get("isStatic", False):
                        raise IllegalMemberAccess(pexpr)
                    if is_last and attr_info.get("isFinal") and not self.in_constructor:
                        raise CannotAssignToConstant(stmt)
                    current_type = attr_info["type"]
            elif isinstance(op, ArrayAccess):
                idx_type = self.visit(op.index)
                if not self.is_array_type(current_type):
                    raise TypeMismatchInExpression(pexpr)
                if not self.is_int_type(idx_type):
                    raise TypeMismatchInExpression(pexpr)
                current_type = current_type.element_type
            elif isinstance(op, MethodCall):
                raise TypeMismatchInExpression(pexpr)

        
        return current_type

    def visitIfStatement(self, ast: IfStatement):
        cond_type = self.visit(ast.condition)
        if cond_type is not ERROR and not self.is_bool_type(cond_type):
            raise TypeMismatchInStatement(ast)
        
        if ast.then_stmt:
            self.visit(ast.then_stmt)
        if ast.else_stmt:
            self.visit(ast.else_stmt)

    def visitForStatement(self, ast: ForStatement):
        var_name = ast.variable
        info = self.lookup(var_name)
        if info is None:
            if self.current_class:
                attr = self.lookup_in_class_attrs(self.current_class, var_name)
                if attr:
                    if attr.get("isFinal"):
                        raise CannotAssignToConstant(ast)
                    if not self.is_int_type(attr["type"]):
                        raise TypeMismatchInStatement(ast)
                else:
                    raise UndeclaredIdentifier(var_name)
            else:
                raise UndeclaredIdentifier(var_name)
        else:
            if info.get("isFinal"):
                raise CannotAssignToConstant(ast)
            if not self.is_int_type(info["type"]):
                raise TypeMismatchInStatement(ast)
        
        start_type = self.visit(ast.start_expr)
        end_type = self.visit(ast.end_expr)
        
        if start_type is not ERROR and not self.is_int_type(start_type):
            raise TypeMismatchInStatement(ast)
        if end_type is not ERROR and not self.is_int_type(end_type):
            raise TypeMismatchInStatement(ast)
        
        self.loop_depth += 1
        if ast.body:
            self.visit(ast.body)
        self.loop_depth -= 1

    def visitBreakStatement(self, ast: BreakStatement):
        if self.loop_depth == 0:
            raise MustInLoop(ast)

    def visitContinueStatement(self, ast: ContinueStatement):
        if self.loop_depth == 0:
            raise MustInLoop(ast)

    def visitReturnStatement(self, ast: ReturnStatement):
        if ast.value is None:
            ret_t = None
        else:
            ret_t = self.visit(ast.value)

        expected = self.current_method_return_type
        if expected is None:
            if ret_t is not None and ret_t is not ERROR:
                raise TypeMismatchInStatement(ast)
            return

        if ret_t is ERROR:
            return

        if isinstance(ast.value, NilLiteral):
            if not (self.is_class_type(expected) or self.is_array_type(expected)):
                raise TypeMismatchInStatement(ast)
            return

        if not self.compatible(expected, ret_t):
            raise TypeMismatchInStatement(ast)

    def visitMethodInvocationStatement(self, ast: MethodInvocationStatement):
        try:
            call_t = self.visit(ast.method_call)
        except TypeMismatchInExpression:
            raise TypeMismatchInStatement(ast)
        if call_t is not ERROR and call_t is not None and self.type_name(call_t) != "void":
            raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast: BinaryOp):
        left_t = self.visit(ast.left)
        right_t = self.visit(ast.right)
        op = ast.operator
        if left_t is ERROR or right_t is ERROR:
            return ERROR
        
        if op in ['+', '-', '*', '/', '\\', '%']:
            if self.is_int_type(left_t) and self.is_int_type(right_t):
                return PrimitiveType("int")
            if ((self.is_int_type(left_t) or self.is_float_type(left_t)) and
                (self.is_int_type(right_t) or self.is_float_type(right_t))):
                return PrimitiveType("float")
            raise TypeMismatchInExpression(ast)
        
        if op in ['<', '>', '<=', '>=']:
            if ((self.is_int_type(left_t) or self.is_float_type(left_t)) and
                (self.is_int_type(right_t) or self.is_float_type(right_t))):
                return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        
        if op in ['==', '!=']:
            if self.same_type(left_t, right_t):
                return PrimitiveType("boolean")
            if (self.is_int_type(left_t) and self.is_float_type(right_t)) or \
               (self.is_float_type(left_t) and self.is_int_type(right_t)):
                return PrimitiveType("boolean")
            if isinstance(ast.left, NilLiteral) or isinstance(ast.right, NilLiteral):
                if (self.is_class_type(left_t) or self.is_array_type(left_t) or 
                    self.is_class_type(right_t) or self.is_array_type(right_t)):
                    return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        
        if op in ['&&', '||']:
            if self.is_bool_type(left_t) and self.is_bool_type(right_t):
                return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        
        if op == '^':
            if self.is_string_type(left_t) and self.is_string_type(right_t):
                return PrimitiveType("string")
            raise TypeMismatchInExpression(ast)
        
        raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self, ast: UnaryOp):
        op = ast.operator
        operand_t = self.visit(ast.operand)
        if operand_t is ERROR:
            return ERROR
        if op in ['+', '-']:
            if self.is_int_type(operand_t) or self.is_float_type(operand_t):
                return operand_t
            raise TypeMismatchInExpression(ast)
        if op == '!':
            if self.is_bool_type(operand_t):
                return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        raise TypeMismatchInExpression(ast)

    def visitPostfixExpression(self, ast: PostfixExpression):
        current_type = self.visit(ast.primary)
        if current_type is ERROR:
            return ERROR

        is_class_name_access = False
        is_io_access = False
        is_this_access = False
        accessed_class_name = None
        if isinstance(ast.primary, Identifier):
            name = ast.primary.name
            if name in self.class_table:
                is_class_name_access = True
                accessed_class_name = name
            elif name == "io":
                is_io_access = True
                accessed_class_name = "IO"
        elif isinstance(ast.primary, ThisExpression):
            is_this_access = True

        for op in ast.postfix_ops:
            if isinstance(op, MemberAccess):
                member_name = op.member_name
                if is_class_name_access or is_io_access:
                    attr_info = self.lookup_in_class_attrs(accessed_class_name, member_name)
                    if attr_info is None:
                        raise UndeclaredAttribute(member_name)
                    if not is_io_access and not attr_info.get("isStatic", False):
                        raise IllegalMemberAccess(ast)
                    current_type = attr_info["type"]
                    is_class_name_access = False
                    is_io_access = False
                else:
                    if not isinstance(current_type, ClassType):
                        raise TypeMismatchInExpression(ast)
                    cls_name = current_type.class_name
                    attr_info = self.lookup_in_class_attrs(cls_name, member_name)
                    if attr_info is None:
                        raise UndeclaredAttribute(member_name)
                    if attr_info.get("isStatic", False) and not is_this_access:
                        raise IllegalMemberAccess(ast)
                    current_type = attr_info["type"]
                    is_this_access = False
            elif isinstance(op, ArrayAccess):
                idx_type = self.visit(op.index)
                if not self.is_array_type(current_type):
                    raise TypeMismatchInExpression(ast)
                if idx_type is not ERROR and not self.is_int_type(idx_type):
                    raise TypeMismatchInExpression(ast)
                current_type = current_type.element_type
            elif isinstance(op, MethodCall):
                method_name = op.method_name
                arg_types = [self.visit(arg) for arg in (op.args or [])]
                
                if is_class_name_access or is_io_access:
                    method_info = self.lookup_method(accessed_class_name, method_name)
                    if method_info is None:
                        raise UndeclaredMethod(method_name)
                    if not is_io_access and not method_info.get("isStatic", False):
                        raise IllegalMemberAccess(ast)
                    params = method_info.get("params", [])
                    if len(params) != len(arg_types):
                        raise TypeMismatchInExpression(ast)
                    for p, a in zip(params, arg_types):
                        if a is not ERROR and not self.compatible(p.param_type, a):
                            raise TypeMismatchInExpression(ast)
                    current_type = method_info["returnType"]
                    is_class_name_access = False
                    is_io_access = False
                else:
                    if not isinstance(current_type, ClassType):
                        raise TypeMismatchInExpression(ast)
                    cls_name = current_type.class_name
                    method_info = self.lookup_method(cls_name, method_name)
                    if method_info is None:
                        raise UndeclaredMethod(method_name)
                    if method_info.get("isStatic", False) and not is_this_access:
                        raise IllegalMemberAccess(ast)
                    params = method_info.get("params", [])
                    if len(params) != len(arg_types):
                        raise TypeMismatchInExpression(ast)
                    for p, a in zip(params, arg_types):
                        if a is not ERROR and not self.compatible(p.param_type, a):
                            raise TypeMismatchInExpression(ast)
                    current_type = method_info["returnType"]
                    is_this_access = False

        return current_type

    def visitIdentifier(self, ast: Identifier):
        name = ast.name
        if name in self.class_table:
            return ClassType(name)
        info = self.lookup(name)
        if info:
            return info["type"]
        if self.current_class:
            attr = self.lookup_in_class_attrs(self.current_class, name)
            if attr:
                if attr.get("isStatic") and not self.current_method_is_static:
                    pass
                return attr["type"]
        raise UndeclaredIdentifier(name)

    def visitThisExpression(self, ast: ThisExpression):
        if self.current_class:
            return ClassType(self.current_class)
        return ERROR

    def visitObjectCreation(self, ast: ObjectCreation):
        class_name = ast.class_name
        if class_name not in self.class_table:
            raise UndeclaredClass(class_name)
        arg_types = [self.visit(arg) for arg in (ast.args or [])]
        clsinfo = self.class_table.get(class_name)
        constructors = clsinfo.get("constructors", {})
        
        if len(arg_types) == 0:
            pass
        elif constructors:
            sig = tuple(self._get_type_signature(t) for t in arg_types if t is not ERROR)
            if sig not in constructors:
                found = False
                for cons_sig, cons_info in constructors.items():
                    params = cons_info.get("params", [])
                    if len(params) == len(arg_types):
                        match = True
                        for p, a in zip(params, arg_types):
                            if a is not ERROR and not self.compatible(p.param_type, a):
                                match = False
                                break
                        if match:
                            found = True
                            break
                if not found and constructors:
                    raise TypeMismatchInExpression(ast)
        return ClassType(class_name)

    def visitParenthesizedExpression(self, ast: ParenthesizedExpression):
        return self.visit(ast.expr)

    def visitIntLiteral(self, ast: IntLiteral):
        return PrimitiveType("int")

    def visitFloatLiteral(self, ast: FloatLiteral):
        return PrimitiveType("float")

    def visitBoolLiteral(self, ast: BoolLiteral):
        return PrimitiveType("boolean")

    def visitStringLiteral(self, ast: StringLiteral):
        return PrimitiveType("string")

    def visitNilLiteral(self, ast: NilLiteral):
        return ClassType("nil")

    def visitArrayLiteral(self, ast: ArrayLiteral):
        elements = ast.value or []
        if not elements:
            return ArrayType(PrimitiveType("void"), 0)
        
        first_type = self.visit(elements[0])
        if first_type is ERROR:
            return ERROR
        
        for elem in elements[1:]:
            elem_type = self.visit(elem)
            if elem_type is ERROR:
                continue
            if not self.same_type(first_type, elem_type):
                raise IllegalArrayLiteral(ast)
        
        return ArrayType(first_type, len(elements))

    def visitMemberAccess(self, ast: MemberAccess):
        return None

    def visitMethodCall(self, ast: MethodCall):
        return None

    def visitArrayAccess(self, ast: ArrayAccess):
        return None

    def visit_array_access(self, ast): return self.visitArrayAccess(ast)
    def visit_array_literal(self, ast): return self.visitArrayLiteral(ast)
    def visit_array_type(self, ast): return None
    def visit_assignment_statement(self, ast): return self.visitAssignmentStatement(ast)
    def visit_attribute(self, ast): return None
    def visit_attribute_decl(self, ast): return self.visitAttributeDecl(ast)
    def visit_binary_op(self, ast): return self.visitBinaryOp(ast)
    def visit_block_statement(self, ast): return self.visitBlockStatement(ast)
    def visit_bool_literal(self, ast): return self.visitBoolLiteral(ast)
    def visit_break_statement(self, ast): return self.visitBreakStatement(ast)
    def visit_class_decl(self, ast): return self.visitClassDecl(ast)
    def visit_class_type(self, ast): return None
    def visit_constructor_decl(self, ast): return self.visitConstructorDecl(ast)
    def visit_continue_statement(self, ast): return self.visitContinueStatement(ast)
    def visit_destructor_decl(self, ast): return self.visitDestructorDecl(ast)
    def visit_float_literal(self, ast): return self.visitFloatLiteral(ast)
    def visit_for_statement(self, ast): return self.visitForStatement(ast)
    def visit_id_lhs(self, ast): return None
    def visit_identifier(self, ast): return self.visitIdentifier(ast)
    def visit_if_statement(self, ast): return self.visitIfStatement(ast)
    def visit_int_literal(self, ast): return self.visitIntLiteral(ast)
    def visit_member_access(self, ast): return self.visitMemberAccess(ast)
    def visit_method_call(self, ast): return self.visitMethodCall(ast)
    def visit_method_decl(self, ast): return self.visitMethodDecl(ast)
    def visit_method_invocation(self, ast): return self.visitMethodCall(ast)
    def visit_method_invocation_statement(self, ast): return self.visitMethodInvocationStatement(ast)
    def visit_nil_literal(self, ast): return self.visitNilLiteral(ast)
    def visit_object_creation(self, ast): return self.visitObjectCreation(ast)
    def visit_parameter(self, ast): return None
    def visit_parenthesized_expression(self, ast): return self.visitParenthesizedExpression(ast)
    def visit_postfix_expression(self, ast): return self.visitPostfixExpression(ast)
    def visit_postfix_lhs(self, ast): return None
    def visit_primitive_type(self, ast): return None
    def visit_program(self, ast): return self.visitProgram(ast)
    def visit_reference_type(self, ast): return None
    def visit_return_statement(self, ast): return self.visitReturnStatement(ast)
    def visit_static_member_access(self, ast): return self.visitMemberAccess(ast)
    def visit_static_method_invocation(self, ast): return self.visitMethodCall(ast)
    def visit_string_literal(self, ast): return self.visitStringLiteral(ast)
    def visit_this_expression(self, ast): return self.visitThisExpression(ast)
    def visit_unary_op(self, ast): return self.visitUnaryOp(ast)
    def visit_variable(self, ast): return None
    def visit_variable_decl(self, ast): return self.visitVariableDecl(ast)
