"""
Static Semantic Checker for OPLang Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the OPLang object-oriented programming language. It performs type checking,
scope management, inheritance validation, and detects all semantic errors as 
specified in the OPLang language specification.
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
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




# class StaticChecker(ASTVisitor):
#     """
#     Stateless static semantic checker for OPLang using visitor pattern.
    
#     Checks for all 10 error types specified in OPLang semantic constraints:
#     1. Redeclared - Variables, constants, attributes, classes, methods, parameters
#     2. Undeclared - Identifiers, classes, attributes, methods  
#     3. CannotAssignToConstant - Assignment to final variables/attributes
#     4. TypeMismatchInStatement - Type incompatibilities in statements
#     5. TypeMismatchInExpression - Type incompatibilities in expressions
#     6. TypeMismatchInConstant - Type incompatibilities in constant declarations
#     7. MustInLoop - Break/continue outside loop contexts
#     8. IllegalConstantExpression - Invalid expressions in constant initialization
#     9. IllegalArrayLiteral - Inconsistent types in array literals
#     10. IllegalMemberAccess - Improper access to static/instance members

#     Also checks for valid entry point: static void main() with no parameters.
#     """
#     pass
class ErrorType:
    """Internal sentinel type to prevent cascading errors."""
    def __repr__(self):
        return "<ErrorType>"

ERROR = ErrorType()

class StaticChecker(ASTVisitor):
    
    def check(self, ast: Program):
        """Main entry point - thêm method này"""
        if ast is None:
            self.emit(NoEntryPoint())
            return self.errors
            
        self._build_class_table(ast)
        self.visitProgram(ast)
        
        if not self.has_main:
            self.emit(NoEntryPoint())
        
        return self.errors

    def __init__(self):
        # ----- Class Table -----
        # class_name -> { attributes: {name: {"type": typeNode, "isFinal": bool, "isStatic": bool}},
        #                 methods: {name: {"returnType": typeNode, "params": [Parameter], "isStatic": bool}},
        #                 parent: Optional[str] }
        self.class_table: Dict[str, Dict[str, Any]] = {}

        # ----- Scopes -----
        # stack of dict: var_name -> SymbolInfo {"type": typeNode, "isFinal": bool, "initialized": bool, "isStatic": bool}
        self.scopes: List[Dict[str, Any]] = []

        # ----- Current Context -----
        self.current_class: Optional[str] = None
        self.current_method: Optional[str] = None
        self.loop_depth: int = 0
        self.current_method_return_type: Optional[Any] = None

        # ----- Error Storage -----
        self.errors: List[StaticError] = []

        # ----- Constant Checking Flag -----
        self.is_checking_constant: bool = False

    # ====================================================================
    #                       SUPPORT / HELPER FUNCTIONS
    # ====================================================================

    def _contains_non_constant_expr(self, expr):
        """Return True if expr uses identifiers, method calls, object creation, member access, array access, nil etc."""
        if expr is None:
            return False
        # literals are OK
        if isinstance(expr, (IntLiteral, FloatLiteral, BoolLiteral, StringLiteral)):
            return False
        if isinstance(expr, NilLiteral):
            return True
        if isinstance(expr, ArrayLiteral):
            # elements stored in .value (see nodes.py)
            return any(self._contains_non_constant_expr(e) for e in expr.value)
        if isinstance(expr, BinaryOp):
            return self._contains_non_constant_expr(expr.left) or self._contains_non_constant_expr(expr.right)
        if isinstance(expr, UnaryOp):
            return self._contains_non_constant_expr(expr.operand)
        # anything else (Identifier, MethodCall, PostfixExpression, ObjectCreation, ArrayAccess, MemberAccess) => non-constant
        return True
    
    def emit(self, err: StaticError):
        """Add error to list"""
        self.errors.append(err)
        print(f"[ERROR EMITTED] {err}")  # Debug

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if self.scopes:
            self.scopes.pop()

    def declare_local(self, name: str, typeNode: Any, isFinal: bool, node: ASTNode, initialized: bool = False):
        # ensure a scope exists
        if not self.scopes:
            self.enter_scope()
        cur = self.scopes[-1]
        if name in cur:
            # raise ngay để test harness bắt và trả về "Redeclared(Variable, x)"
            raise Redeclared("Variable", name)
        cur[name] = {"type": typeNode, "isFinal": isFinal, "initialized": initialized}

    def declare_param(self, name: str, typeNode: Any, node: ASTNode):
        if not self.scopes:
            self.enter_scope()
        if name in self.scopes[-1]:
            self.emit(Redeclared("Parameter", name, node))
            return
        # parameters considered initialized/final (cannot reassign param name in same method)
        self.scopes[-1][name] = {"type": typeNode, "isFinal": True, "initialized": True}

    def lookup(self, name: str):
        # lookup local scopes first
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def lookup_in_class_attrs(self, class_name: str, attr: str):
        c = self.class_table.get(class_name, None)
        if c is None:
            return None
        # search in inheritance chain
        cur = class_name
        while cur:
            clsinfo = self.class_table.get(cur)
            if clsinfo and attr in clsinfo["attributes"]:
                return clsinfo["attributes"][attr]
            cur = clsinfo["parent"] if clsinfo else None
        return None

    def lookup_method(self, class_name: str, method_name: str):
        """Tìm method trong class và các lớp cha (inheritance chain)"""
        cur = class_name
        visited = set()  # chống vòng lặp kế thừa (nếu có)
        while cur and cur not in visited:
            visited.add(cur)
            clsinfo = self.class_table.get(cur)
            if clsinfo and method_name in clsinfo["methods"]:
                return clsinfo["methods"][method_name]
            cur = clsinfo["parent"] if clsinfo else None
        return None  # Không tìm thấy
    # ---------- type helpers ----------
    def type_name(self, t: Any) -> str:
        """Return type name as string"""
        if t is None:
            return "void"
        if isinstance(t, ErrorType):
            return "<error>"
        
        if isinstance(t, PrimitiveType):
            # SỬA: Kiểm tra nodes.py xem PrimitiveType lưu tên như thế nào
            # Nếu là self.type_name:
            return t.type_name if hasattr(t, 'type_name') else str(t)
        
        if isinstance(t, ClassType):
            # SỬA: Kiểm tra nodes.py xem ClassType lưu tên như thế nào
            # Nếu là self.class_name:
            return t.class_name if hasattr(t, 'class_name') else str(t)
        
        if isinstance(t, ArrayType):
            # SỬA: Kiểm tra nodes.py xem ArrayType lưu như thế nào
            # Thường là: self.element_type và self.size
            elem = t.element_type if hasattr(t, 'element_type') else None
            size = t.size if hasattr(t, 'size') else None
            if elem:
                return f"{self.type_name(elem)}[{size}]"
            return "unknown[]"
        
        if isinstance(t, ReferenceType):
            ref = t.referenced_type if hasattr(t, 'referenced_type') else None
            if ref:
                return self.type_name(ref) + "&"
            return "unknown&"
        
        return str(t)

    def is_int_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and self.type_name(t).lower() == "int"

    def is_float_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and self.type_name(t).lower() == "float"

    def is_bool_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and self.type_name(t).lower() == "boolean" or self.type_name(t).lower() == "bool"

    def is_string_type(self, t: Any) -> bool:
        return isinstance(t, PrimitiveType) and self.type_name(t).lower() == "string"

    def is_array_type(self, t: Any) -> bool:
        return isinstance(t, ArrayType)

    def is_class_type(self, t: Any) -> bool:
        return isinstance(t, ClassType)

    def same_type(self, a: Any, b: Any) -> bool:
        # consider ErrorType
        if a is ERROR or b is ERROR:
            return False
        if a is None and b is None:
            return True
        if type(a) != type(b):
            return False
        if isinstance(a, PrimitiveType):
            return self.type_name(a).lower() == self.type_name(b).lower()
        if isinstance(a, ClassType):
            return self.type_name(a) == self.type_name(b)
        if isinstance(a, ArrayType):
            # compare element type and size (size must match)
            a_ele = getattr(a, "eleType", getattr(a, "elementType", None))
            b_ele = getattr(b, "eleType", getattr(b, "elementType", None))
            a_size = getattr(a, "size", getattr(a, "length", None))
            b_size = getattr(b, "size", getattr(b, "length", None))
            return self.same_type(a_ele, b_ele) and (a_size == b_size)
        # fallback to string compare
        return self.type_name(a) == self.type_name(b)

    def is_subtype(self, sub: Any, sup: Any) -> bool:
        # only class inheritance allowed as subtype -> supertype
        if isinstance(sub, ClassType) and isinstance(sup, ClassType):
            sub_name = self.type_name(sub)
            sup_name = self.type_name(sup)
            cur = sub_name
            while cur:
                if cur == sup_name:
                    return True
                clsinfo = self.class_table.get(cur, None)
                cur = clsinfo["parent"] if clsinfo else None
            return False
        return False

    def compatible(self, expected: Any, actual: Any) -> bool:
        # returns True if actual can be assigned to expected
        if expected is ERROR or actual is ERROR:
            return True  # avoid cascades; already emitted earlier
        if expected is None:  # expected void?
            return actual is None
        if self.same_type(expected, actual):
            return True
        # int -> float coercion
        if self.is_float_type(expected) and self.is_int_type(actual):
            return True
        # subtype -> supertype
        if self.is_class_type(actual) and self.is_class_type(expected):
            return self.is_subtype(actual, expected)
        return False

    # ====================================================================
    #                          PUBLIC API
    # ====================================================================

    def check_program(self, ast: Program):
        """
        Thực hiện kiểm tra ngữ nghĩa tĩnh trên toàn bộ chương trình.
        Đây là phương thức chính cần được gọi từ bên ngoài.
        """
        # 1. Xây dựng bảng class trước (Pass 1)
        self._build_class_table(ast)

        # 2. Duyệt cây AST để kiểm tra (Pass 2)
        self.visit(ast)

        # 3. Kiểm tra điểm vào của chương trình
        self._check_entry_point()
        
        return self.errors
    
    # ====================================================================
    #                          DECLARATION VISITORS
    # ====================================================================

    def _populate_class_members(self, class_decl):
        """Populate class members in class_table"""
        # SỬA: Truy cập trực tiếp class_decl.name
        name = class_decl.name
        if name not in self.class_table:
            return
            
        attrs = self.class_table[name]["attributes"]
        methods = self.class_table[name]["methods"]
        
        # SỬA: Truy cập trực tiếp class_decl.members
        members = class_decl.members if class_decl.members else []
        
        for member in members:
            if member is None:
                continue
                
            if isinstance(member, AttributeDecl):
                # AttributeDecl có: is_static, is_final, attr_type, attributes (list)
                # Mỗi Attribute có: attr_name, init_value
                for attr in member.attributes:
                    attr_name = attr.attr_name  # SỬA: Truy cập trực tiếp
                    if attr_name in attrs:
                        self.emit(Redeclared("Attribute", attr_name, member))
                        continue
                        
                    attrs[attr_name] = {
                        "type": member.attr_type,
                        "isFinal": member.is_final,
                        "isStatic": member.is_static,
                        "init_value": attr.init_value
                    }
                    
            elif isinstance(member, MethodDecl):
                # MethodDecl có: is_static, return_type, name, params, body
                meth_name = member.name  # SỬA: Truy cập trực tiếp
                if meth_name in methods:
                    self.emit(Redeclared("Method", meth_name, member))
                    continue
                    
                methods[meth_name] = {
                    "returnType": member.return_type,
                    "params": member.params,
                    "isStatic": member.is_static
                }
                
                # Check main
                if meth_name == "main" and member.is_static:
                    if isinstance(member.return_type, PrimitiveType):
                        # Cần kiểm tra thuộc tính của PrimitiveType
                        # Theo ast_generation line 263: PrimitiveType("void")
                        # Cần xem PrimitiveType trong nodes.py lưu như thế nào
                        if self.type_name(member.return_type) == "void" and len(member.params) == 0:
                            self.has_main = True
                            
            elif isinstance(member, ConstructorDecl):
                # ConstructorDecl có: name, params, body
                # Constructor có tên trùng với class
                if name in methods:
                    self.emit(Redeclared("Method", name, member))
                # Lưu constructor info nếu cần
                
            elif isinstance(member, DestructorDecl):
                # DestructorDecl có: name, body
                dest_name = f"~{member.name}"
                if dest_name in methods:
                    self.emit(Redeclared("Method", dest_name, member))
                
    def _build_class_table(self, ast: Program):
        # reset
        self.class_table = {}
        self.has_main = False

        class_list = getattr(ast, "class_decls", []) or []
        # collect class names
        for c in class_list:
            if not isinstance(c, ClassDecl):
                continue
            name = c.name
            if name in self.class_table:
                raise Redeclared("Class", name)
            parent = c.superclass
            self.class_table[name] = {"parent": parent, "attributes": {}, "methods": {}, "node": c}

        # check parents exist
        for name, info in self.class_table.items():
            parent = info["parent"]
            if parent and parent not in self.class_table:
                raise UndeclaredClass(parent)

        # collect members
        for c in class_list:
            if not isinstance(c, ClassDecl):
                continue
            cname = c.name
            info = self.class_table[cname]
            for m in c.members or []:
                if isinstance(m, AttributeDecl):
                    for a in m.attributes or []:
                        aname = a.name
                        if aname in info["attributes"]:
                            raise Redeclared("Attribute", aname)
                        info["attributes"][aname] = {
                            "type": m.attr_type,
                            "isFinal": m.is_final,
                            "isStatic": m.is_static,
                            "init": a.init_value,
                        }
                elif isinstance(m, MethodDecl):
                    mname = m.name
                    if mname in info["methods"]:
                        raise Redeclared("Method", mname)
                    info["methods"][mname] = {
                        "returnType": m.return_type,
                        "params": m.params,
                        "isStatic": m.is_static,
                        "node": m,
                    }
                    # check main
                    if (mname == "main" and m.is_static and isinstance(m.return_type, PrimitiveType)
                            and m.return_type.type_name == "void" and len(m.params) == 0):
                        self.has_main = True
                elif isinstance(m, ConstructorDecl):
                    cname_m = m.name
                    if cname_m in info["methods"]:
                        raise Redeclared("Method", cname_m)
                    info["methods"][cname_m] = {"returnType": ClassType(cname), "params": m.params, "isStatic": False}
                elif isinstance(m, DestructorDecl):
                    # optional: treat as method named ~classname
                    dname = "~" + cname
                    if dname in info["methods"]:
                        raise Redeclared("Method", dname)
                    info["methods"][dname] = {"returnType": None, "params": [], "isStatic": False}
                
    def _check_entry_point(self):
        # (Giữ nguyên logic)
        found = False
        for cls_name, info in self.class_table.items():
            methods = info["methods"]
            if "main" in methods:
                m = methods["main"]
                if m["isStatic"] and self.type_name(m["returnType"]) == "void" and len(m["params"]) == 0:
                    found = True
                    break
        if not found:
            self.emit(NoEntryPoint())
            
    def visit(self, node):
        """Override visit to handle None nodes"""
        if node is None:
            return None
            
        # Gọi visitor method tương ứng
        method_name = f'visit{node.__class__.__name__}'
        visitor = getattr(self, method_name, None)
        
        if visitor:
            return visitor(node)
        
        # Try snake_case 
        method_name_snake = f'visit_{node.__class__.__name__.lower()}'
        visitor = getattr(self, method_name_snake, None)
        if visitor:
            return visitor(node)
            
        # Default: return None
        return None

    def visitProgram(self, ast: Program, o=None):
        if not self.class_table:  # chỉ chạy lần đầu
            self._build_class_table(ast)

            # Thêm class IO và biến io global
            if "IO" not in self.class_table:
                self.class_table["IO"] = {
                    "parent": None,
                    "attributes": {},
                    "methods": {
                        "writeInt": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("int"), "x")], "isStatic": True},
                        "writeFloat": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("float"), "x")], "isStatic": True},
                        "writeString": {"returnType": PrimitiveType("void"), "params": [Parameter(PrimitiveType("string"), "x")], "isStatic": True},
                        "readInt": {"returnType": PrimitiveType("int"), "params": [], "isStatic": True},
                        "readFloat": {"returnType": PrimitiveType("float"), "params": [], "isStatic": True},
                        "readString": {"returnType": PrimitiveType("string"), "params": [], "isStatic": True},
                    }
                }

        self.enter_scope()  # global scope
        self.scopes[-1]["io"] = {"type": ClassType("IO"), "isFinal": True, "initialized": True}

        for cls in ast.class_decls or []:
            if cls is not None:
                self.visitClassDecl(cls)

        self.exit_scope()

    def visitClassDecl(self, ast: ClassDecl, o=None):
        if ast is None:
            return
        self.current_class = ast.name
        self.enter_scope()
        # put 'this' in current scope
        self.scopes[-1]["this"] = {"type": ClassType(ast.name), "isFinal": True}
        for mem in ast.members or []:
            if mem is not None:
                # call existing visitor dispatch (use safe mapping present in your file)
                self.safe_visit(mem) if hasattr(self, "safe_visit") else self.visit(mem)
        self.exit_scope()
        self.current_class = None

    def visitAttributeDecl(self, ast: AttributeDecl):
        """Visit AttributeDecl node"""
        if ast is None:
            return
        
        for attr in ast.attributes:
            if attr.init_value:
                if ast.is_final:
                    self.in_constant_init = True
                    init_type = self.visit(attr.init_value)
                    self.in_constant_init = False
                    
                    # Check IllegalConstantExpression
                    if self._contains_non_constant_expr(attr.init_value):
                        self.emit(IllegalConstantExpression(attr.init_value))
                        
                    if init_type is not ERROR and not self.compatible(ast.attr_type, init_type):
                        self.emit(TypeMismatchInConstant(ast))
                else:
                    init_type = self.visit(attr.init_value)
                    if init_type is not ERROR and not self.compatible(ast.attr_type, init_type):
                        self.emit(TypeMismatchInStatement(ast))

    def visitMethodDecl(self, ast: MethodDecl, o=None):
        self.current_method = ast.name
        self.current_method_return_type = ast.return_type
        self.enter_scope()
        
        # Khai báo tham số
        for p in ast.params or []:
            pname = getattr(p, "name", getattr(p, "param_name", None))
            ptype = getattr(p, "param_type", getattr(p, "var_type", None))
            self.declare_param(pname, ptype, p)
        if ast.body:                   
            self.visit(ast.body)     

        self.exit_scope()
        self.current_method = None
        self.current_method_return_type = None

    def visitConstructorDecl(self, ast: ConstructorDecl):
        self.current_method = ast.name
        self.current_method_return_type = ClassType(self.current_class)
        self.enter_scope()
        
        # SỬA DÒNG NÀY:
        # for param in ast.parameters:          # ← cũ, sai
        for param in ast.params:                 # ← đúng (hoặc getattr(ast, "params", []))
            self.visit(param)                     # hoặc self.declare_param(...) nếu cần
        
        if ast.body:
            self.visit(ast.body)
        
        self.exit_scope()
        self.current_method = None
        self.current_method_return_type = None

    def visitDestructorDecl(self, ast: DestructorDecl):
        self.current_method = ast.name
        self.current_method_return_type = None  # void
        self.enter_scope()
        self.visit(ast.body)
        self.exit_scope()
        self.current_method = None
        self.current_method_return_type = None

    def visitParameter(self, ast: Parameter):
        if ast is None:
            return
            
        param_name = ast.name
        param_type = ast.param_type

        if param_name in self.scopes[-1]:
            self.emit(Redeclared("Parameter", param_name))
            return

        self.scopes[-1][param_name] = {
            "type": param_type,
            "isFinal": True  # Parameters are final
        }

    def visitVariableDecl(self, ast: VariableDecl, o=None):
        print(f"[DEBUG] Visiting VariableDecl: {ast.variables[0].name}, is_final = {ast.is_final}")
        # ast.variables is list of Variable nodes
        for var in ast.variables or []:
            vname = getattr(var, "name", None)
            if vname is None:
                continue
            # declare in current scope (declare_local will raise Redeclared if exists)
            self.declare_local(vname, ast.var_type, ast.is_final, ast, initialized=(getattr(var, "init_value", None) is not None))
            # check initializer
            if getattr(var, "init_value", None) is not None:
                init_t = self.visit(var.init_value)
                if ast.is_final:
                    # if initializer contains non-constant construct -> IllegalConstantExpression
                    if self._contains_non_constant_expr(var.init_value):
                        raise IllegalConstantExpression(var.init_value)
                    if not self.compatible(ast.var_type, init_t):
                        raise TypeMismatchInConstant(ast)
                else:
                    if not self.compatible(ast.var_type, init_t):
                        raise TypeMismatchInStatement(ast)

    # ====================================================================
    #                        EXPRESSIONS & STATEMENTS
    # ====================================================================

    # --- Primary / identifiers ---
    def visitIdentifier(self, ast: Identifier, o=None):
        # check local scopes
        for s in reversed(self.scopes):
            if ast.name in s:
                return s[ast.name]["type"]
        # check class attributes
        if self.current_class:
            clsinfo = self.class_table.get(self.current_class)
            if clsinfo and ast.name in clsinfo["attributes"]:
                return clsinfo["attributes"][ast.name]["type"]
        # check if it's a class name (type)
        if ast.name in self.class_table:
            return ClassType(ast.name)
        raise UndeclaredIdentifier(ast.name)

    def visitThisExpression(self, ast: ThisExpression):
        # 'this' refers to current class type
        if not self.current_class:
            # out of class context? treat as error
            self.emit(UndeclaredIdentifier("this", ast))
            return ERROR
        return ClassType(self.current_class) if "ClassType" in globals() else ClassType(ast)  # best-effort

    def visitIntLiteral(self, ast: IntLiteral):
        return PrimitiveType("int") if "PrimitiveType" in globals() else ast

    def visitFloatLiteral(self, ast: FloatLiteral):
        return PrimitiveType("float") if "PrimitiveType" in globals() else ast

    def visitBoolLiteral(self, ast: BoolLiteral):
        return PrimitiveType("boolean") if "PrimitiveType" in globals() else ast

    def visitStringLiteral(self, ast: StringLiteral):
        return PrimitiveType("string") if "PrimitiveType" in globals() else ast

    def visitNilLiteral(self, ast: NilLiteral):
        # nil can be compatible with any class or array type in many languages; treat as special
        return ast  # caller will handle nil semantics (we return node itself)

    # --- Array literal ---
    def visitArrayLiteral(self, ast: ArrayLiteral):
        if not ast.value:  # mảng rỗng
            return ast  # để context quyết định kiểu

        elem_types = [self.visit(e) for e in ast.value]  # ← đúng là .value
        if any(t is ERROR for t in elem_types):
            return ERROR

        base_type = elem_types[0]
        for t in elem_types[1:]:
            if not self.same_type(base_type, t):
                # nil được phép nếu base là class/array
                if isinstance(t, NilLiteral) and (self.is_class_type(base_type) or self.is_array_type(base_type)):
                    continue
                if isinstance(base_type, NilLiteral) and (self.is_class_type(t) or self.is_array_type(t)):
                    base_type = t
                    continue
                self.emit(IllegalArrayLiteral(ast))
                return ERROR

        size = len(ast.value)
        return ArrayType(base_type, size)

    # --- Array access ---
    def visitArrayAccess(self, ast: ArrayAccess):
        arr_t = self.visit(ast.array)
        idx_t = self.visit(ast.index)
        # E1 must be array type
        if isinstance(arr_t, ErrorType) or arr_t is ERROR:
            return ERROR
        if not self.is_array_type(arr_t):
            self.emit(TypeMismatchInExpression(ast))
            return ERROR
        # index must be integer
        if not self.is_int_type(idx_t):
            self.emit(TypeMismatchInExpression(ast))
            return ERROR
        # return element type
        ele = getattr(arr_t, "eleType", getattr(arr_t, "elementType", None))
        return ele if ele is not None else ERROR

    # --- Member access (obj.member or ClassName.member) ---
    def visitMemberAccess(self, ast: MemberAccess):
        # ast.obj could be Identifier (class name or object), ThisExpression, MethodCall, MemberAccess (chained)
        # ast.member is Identifier with .name
        # Evaluate obj type
        obj = ast.obj
        # if obj is Identifier with class name (static access)
        if isinstance(obj, Identifier):
            # could be class name or variable
            # If class name exists in class_table -> static access
            if obj.name in self.class_table:
                # static access on class
                clsinfo = self.class_table[obj.name]
                # member could be attribute or method
                attr = clsinfo["attributes"].get(ast.member.name, None)
                m = clsinfo["methods"].get(ast.member.name, None)
                if attr:
                    # static vs instance check: attribute must be static to access via ClassName
                    if not getattr(attr, "get", lambda k, d: attr.get(k, d)) and not attr.get("isStatic", False):
                        # attribute exists but not static -> IllegalMemberAccess
                        self.emit(IllegalMemberAccess(ast))
                        return ERROR
                    return attr["type"]
                if m:
                    if not m.get("isStatic", False):
                        self.emit(IllegalMemberAccess(ast))
                        return ERROR
                    return m["returnType"]
                # not found
                self.emit(UndeclaredAttribute(ast.member.name))
                return ERROR
            else:
                # identifier is variable/object: evaluate its type
                obj_t = self.visit(obj)
                if obj_t is ERROR:
                    return ERROR
                # must be class type
                if not isinstance(obj_t, ClassType):
                    self.emit(TypeMismatchInExpression(ast))  # accessing member on non-object
                    return ERROR
                clsname = self.type_name(obj_t)
                attr = self.lookup_in_class_attrs(clsname, ast.member.name)
                if attr is None:
                    self.emit(UndeclaredAttribute(ast.member.name))
                    return ERROR
                # if attribute is static and accessed via instance -> IllegalMemberAccess
                if attr.get("isStatic", False):
                    self.emit(IllegalMemberAccess(ast))
                    return ERROR
                return attr["type"]
        else:
            # obj is expression -> evaluate expression type
            obj_t = self.visit(obj)
            if obj_t is ERROR:
                return ERROR
            if isinstance(obj_t, ClassType):
                clsname = self.type_name(obj_t)
                attr = self.lookup_in_class_attrs(clsname, ast.member.name)
                if attr is None:
                    self.emit(UndeclaredAttribute(ast.member.name))
                    return ERROR
                # if attribute is static but accessed through instance -> IllegalMemberAccess
                if attr.get("isStatic", False):
                    self.emit(IllegalMemberAccess(ast))
                    return ERROR
                return attr["type"]
            else:
                self.emit(TypeMismatchInExpression(ast))
                return ERROR

    # --- Object creation ---
    def visitObjectCreation(self, ast: ObjectCreation):
        # SỬA: Trong nodes.py, ast.class_name là kiểu str, lấy trực tiếp
        class_name = ast.class_name
        
        if class_name not in self.class_table:
            self.emit(UndeclaredClass(class_name, ast))
            return ERROR

        # Tìm constructor (method có tên trùng với class)
        cons = self.lookup_method(class_name, class_name)
        
        # Kiểm tra tham số
        if cons:
            params = cons.get("params", [])
            if len(params) != len(ast.args):
                self.emit(TypeMismatchInExpression(ast))
                return ERROR
            for arg_expr, param in zip(ast.args, params):
                arg_t = self.visit(arg_expr)
                # Trong nodes.py, Parameter có thuộc tính param_type
                p_t = param.param_type
                if not self.compatible(p_t, arg_t):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
        else:
            # Nếu không có constructor tường minh, chỉ cho phép tạo nếu không có đối số
            if len(ast.args) > 0:
                self.emit(TypeMismatchInExpression(ast))
                return ERROR

        # Trả về ClassType tương ứng
        return ClassType(class_name)

    # --- Method call / invocation expression ---
    def visitMethodCall(self, ast: MethodCall):
        # ast.obj could be Identifier (class name or object) or expression; ast.method is Identifier; ast.args list
        # Evaluate target
        obj = ast.obj
        # static call: ClassName.method(...)
        if isinstance(obj, Identifier) and obj.name in self.class_table:
            clsname = obj.name
            m = self.lookup_method(clsname, ast.method.name)
            if m is None:
                self.emit(UndeclaredMethod(ast.method.name))
                return ERROR
            # method must be static to call via class name
            if not m.get("isStatic", False):
                self.emit(IllegalMemberAccess(ast))
                return ERROR
            # check params
            params = m.get("params", [])
            if len(params) != len(ast.args):
                self.emit(TypeMismatchInExpression(ast))
                return ERROR
            for arg_expr, param in zip(ast.args, params):
                arg_t = self.visit(arg_expr)
                p_t = getattr(param, "paramType", getattr(param, "varType", None))
                if not self.compatible(p_t, arg_t):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
            return m.get("returnType", None)
        else:
            # instance call
            obj_t = self.visit(obj)
            if obj_t is ERROR:
                return ERROR
            if isinstance(obj_t, NilLiteral):
                self.emit(TypeMismatchInExpression(ast))
                return ERROR
            if not isinstance(obj_t, ClassType):
                self.emit(TypeMismatchInExpression(ast))
                return ERROR
            clsname = self.type_name(obj_t)
            m = self.lookup_method(clsname, ast.method.name)
            if m is None:
                self.emit(UndeclaredMethod(ast.method.name))
                return ERROR
            if m.get("isStatic", False):
                # calling static via instance -> IllegalMemberAccess
                self.emit(IllegalMemberAccess(ast))
                return ERROR
            # check params
            params = m.get("params", [])
            if len(params) != len(ast.args):
                self.emit(TypeMismatchInExpression(ast))
                return ERROR
            for arg_expr, param in zip(ast.args, params):
                arg_t = self.visit(arg_expr)
                p_t = getattr(param, "paramType", getattr(param, "varType", None))
                if not self.compatible(p_t, arg_t):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
            return m.get("returnType", None)

    # --- Assignment Statement ---
    def visitAssignmentStatement(self, ast: AssignmentStatement):
        rhs_t = self.visit(ast.rhs)

        lhs = ast.lhs

        # === Trường hợp 1: LHS là Identifier (x := 10) ===
        if isinstance(lhs, IdLHS):
            var_name = lhs.name

            # Tìm trong local scopes
            sym = self.lookup(var_name)

            # Nếu không tìm thấy trong local → tìm trong instance attributes (this.field)
            if sym is None and self.current_class:
                attr_info = self.lookup_in_class_attrs(self.current_class, var_name)
                if attr_info is not None:
                    # Là attribute → cho phép gán (sẽ kiểm tra final ở dưới)
                    lhs_t = attr_info["type"]
                    is_final = attr_info.get("isFinal", False)
                    # Gán cho attribute trong constructor → được phép dù final
                    if is_final and not (self.current_method == self.current_class):  # không phải constructor
                        self.emit(CannotAssignToConstant(ast))
                else:
                    # ← Không tìm thấy ở bất kỳ đâu → UndeclaredIdentifier
                    self.emit(UndeclaredIdentifier(var_name))
                    return
            elif sym is None:
                # ← Không tìm thấy ở local và không có trong class → UndeclaredIdentifier
                self.emit(UndeclaredIdentifier(var_name))
                return
            else: 
                # Tìm thấy trong local scope
                lhs_t = sym["type"]
                if sym.get("isFinal", False):
                    self.emit(CannotAssignToConstant(ast))

        # === Trường hợp 2: LHS là PostfixLHS (obj.x := ..., arr[i] := ...) ===
        elif isinstance(lhs, PostfixLHS):
            # Đã xử lý ở visitPostfixExpression → chỉ cần visit để kiểm tra lỗi
            lhs_t = self.visit(lhs.postfix_expr)
            if lhs_t is ERROR:
                return

        # Kiểm tra kiểu (nếu cả hai bên đều không error)
        if lhs_t is not ERROR and rhs_t is not ERROR:
            if not self.compatible(lhs_t, rhs_t):
                self.emit(TypeMismatchInStatement(ast))

    # --- If Statement ---
    def visitIfStatement(self, ast: IfStatement):
        cond_t = self.visit(ast.condition)
        if cond_t is ERROR:
            return
        if not self.is_bool_type(cond_t):
            self.emit(TypeMismatchInStatement(ast))
            return
        # then
        self.enter_scope()
        self.visit(ast.then_tmt)
        self.exit_scope()
        # else
        if ast.else_stmt:
            self.enter_scope()
            self.visit(ast.else_stmt)
            self.exit_scope()

    # --- For Statement ---
    def visitForStatement(self, ast: ForStatement):
        self.loop_depth += 1
        self.enter_scope()  # tạo scope mới cho thân for → int i := 5; mới bị Redeclared

        # Biến lặp là một string (không phải VariableDecl hay IdLHS)
        var_name = ast.variable  # ← đây là str, ví dụ: "i"

        # Kiểm tra biến có tồn tại không (nếu dùng biến ngoài thì phải đã khai báo)
        sym = self.lookup(var_name)
        if sym is None:
            # Nếu chưa tồn tại → coi như khai báo ngầm kiểu int (theo spec OPLang)
            # → khai báo vào scope hiện tại (scope của for)
            self.declare_local(var_name, PrimitiveType("int"), isFinal=False, node=ast, initialized=True)
        else:
            # Nếu đã tồn tại → phải là int
            if not self.is_int_type(sym["type"]):
                self.emit(TypeMismatchInStatement(ast))

        # Kiểm tra start_expr và end_expr phải là int
        start_t = self.visit(ast.start_expr)
        end_t = self.visit(ast.end_expr)

        if not self.is_int_type(start_t) or not self.is_int_type(end_t):
            self.emit(TypeMismatchInStatement(ast))

        # Thân vòng lặp
        self.visit(ast.body)  # ← đúng là .body

        self.exit_scope()
        self.loop_depth -= 1

    def visitBreakStatement(self, ast: BreakStatement):
        if self.loop_depth == 0:
            self.emit(MustInLoop(ast))

    def visitContinueStatement(self, ast: ContinueStatement):
        if self.loop_depth == 0:
            self.emit(MustInLoop(ast))

    # --- Return Statement ---
    def visitReturnStatement(self, ast: ReturnStatement):
        if ast.value is None:
            ret_t = None  # return;
        else:
            ret_t = self.visit(ast.value)  # ← đúng là .value

        expected = self.current_method_return_type
        if expected is None:
            return

        if ret_t is ERROR:
            return

        # nil chỉ được phép nếu expected là class hoặc array
        if isinstance(ast.value, NilLiteral):
            if not (self.is_class_type(expected) or self.is_array_type(expected)):
                self.emit(TypeMismatchInStatement(ast))
            return

        if not self.compatible(expected, ret_t):
            self.emit(TypeMismatchInStatement(ast))

    # --- BinaryOp ---
    def visitBinaryOp(self, ast: BinaryOp, o=None):
        left_t = self.visit(ast.left)
        right_t = self.visit(ast.right)
        op = ast.operator
        if left_t is ERROR or right_t is ERROR:
            return ERROR
        # arithmetic
        if op in ['+', '-', '*', '/', '\\', '%']:
            if (self.is_int_type(left_t) and self.is_int_type(right_t)):
                return PrimitiveType("int")
            if ((self.is_int_type(left_t) or self.is_float_type(left_t)) and
                (self.is_int_type(right_t) or self.is_float_type(right_t))):
                return PrimitiveType("float")
            raise TypeMismatchInExpression(ast)
        # comparisons
        if op in ['<', '>', '<=', '>=']:
            if ( (self.is_int_type(left_t) or self.is_float_type(left_t)) and
                (self.is_int_type(right_t) or self.is_float_type(right_t)) ):
                return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        # equality
        if op in ['==', '!=']:
            if self.same_type(left_t, right_t) or (self.is_int_type(left_t) and self.is_float_type(right_t)) or (self.is_float_type(left_t) and self.is_int_type(right_t)):
                return PrimitiveType("boolean")
            if isinstance(ast.left, NilLiteral) or isinstance(ast.right, NilLiteral):
                if (self.is_class_type(left_t) or self.is_array_type(left_t) or self.is_class_type(right_t) or self.is_array_type(right_t)):
                    return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        # logical
        if op in ['&&', '||']:
            if self.is_bool_type(left_t) and self.is_bool_type(right_t):
                return PrimitiveType("boolean")
            raise TypeMismatchInExpression(ast)
        # string concat
        if op == '^':
            if self.is_string_type(left_t) and self.is_string_type(right_t):
                return PrimitiveType("string")
            raise TypeMismatchInExpression(ast)
        raise TypeMismatchInExpression(ast)

    # --- UnaryOp ---
    def visitUnaryOp(self, ast: UnaryOp, o=None):
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

    # ====================================================================
    #                        OTHER VISITORS (statements/bodies)
    # ====================================================================

    # Generic block visitor (BlockStatement)
    def visitBlockStatement(self, ast: BlockStatement, o=None):
        self.enter_scope()
        for vdecl in getattr(ast, "var_decls", []) or []:
            if vdecl is not None:
                self.visitVariableDecl(vdecl)
        for stmt in getattr(ast, "statements", []) or []:
            if stmt is not None:
                self.safe_visit(stmt) if hasattr(self, "safe_visit") else self.visit(stmt)
        self.exit_scope()

    # Method body visitation: ensure to set current_method_return_type
    def visitMethodBody(self, ast):
        # depending on AST, the method body visit may happen via visitMethodDecl earlier
        # keep as fallback
        self.visit(ast)

    # ParenthesizedExpression
    def visitParenthesizedExpression(self, ast: ParenthesizedExpression):
        return self.visit(ast.expression)

    # PostfixExpression (e.g., ++, -- if supported)
    def visitPostfixExpression(self, ast: PostfixExpression):
        # Bước 1: Lấy kiểu của primary expression (this, id, obj creation, v.v.)
        current_type = self.visit(ast.primary)
        if current_type is ERROR:
            return ERROR

        # Bước 2: Duyệt từng postfix_op trong danh sách postfix_ops
        for op in ast.postfix_ops:
            if isinstance(op, MemberAccess):
                # Xử lý this.PI hoặc obj.field
                member_name = op.member_name
                if not isinstance(current_type, ClassType):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
                cls_name = current_type.class_name
                attr_info = self.lookup_in_class_attrs(cls_name, member_name)
                if attr_info is None:
                    self.emit(UndeclaredAttribute(member_name))
                    return ERROR
                if attr_info.get("isStatic", False):
                    self.emit(IllegalMemberAccess(ast))
                    return ERROR
                # Gán vào final attribute trong constructor thì được phép → sẽ kiểm tra ở Assignment
                current_type = attr_info["type"]

            elif isinstance(op, ArrayAccess):
                idx_type = self.visit(op.index)
                if not self.is_array_type(current_type):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
                if not self.is_int_type(idx_type):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR
                current_type = current_type.element_type

            elif isinstance(op, MethodCall):
                method_name = op.method_name
                arg_types = [self.visit(arg) for arg in op.args]

                # current_type là kiểu của obj (ở đây là A)
                if not isinstance(current_type, ClassType):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR

                cls_name = current_type.class_name  # ← ở đây là "A"

                # DÙNG lookup_method ĐÚNG ĐỂ TÌM TRONG CHUỖI KẾ THỪA
                method_info = self.lookup_method(cls_name, method_name)

                if method_info is None:
                    # ← Đây chính là chỗ phải báo lỗi UndeclaredMethod
                    self.emit(UndeclaredMethod(method_name))
                    return ERROR

                # Nếu tìm thấy nhưng là static mà gọi qua instance → IllegalMemberAccess
                if method_info.get("isStatic", False):
                    self.emit(IllegalMemberAccess(ast))
                    return ERROR

                # Kiểm tra tham số
                params = method_info.get("params", [])
                if len(params) != len(arg_types):
                    self.emit(TypeMismatchInExpression(ast))
                    return ERROR

                for p, a in zip(params, arg_types):
                    if not self.compatible(p.param_type, a):
                        self.emit(TypeMismatchInExpression(ast))
                        return ERROR

                current_type = method_info["returnType"]

        return current_type

    # MethodInvocationStatement (void method call as statement)
    def visitMethodInvocationStatement(self, ast: MethodInvocationStatement):
        call_t = self.visit(ast.method_call)
        if call_t is not ERROR and self.type_name(call_t) != "void":
            self.emit(TypeMismatchInStatement(ast))

    # ====================================================================
    #                          END OF CLASS
    # ====================================================================

    def _call_camel(self, camel_name: str, ast):
        """Helper: call camelCase method if exists, else attempt safe fallback."""
        fn = getattr(self, camel_name, None)
        try:
            if callable(fn):
                return fn(ast)
            # fallback: if ast is ASTNode, try generic visit (may dispatch)
            if hasattr(self, "visit") and callable(getattr(self, "visit")):
                # protect from infinite recursion: if visit would map back to this wrapper,
                # return ERROR to avoid recursion. We detect by checking if camel_name in caller stack is hard;
                # simple safe fallback:
                return self.visit(ast)
        except RecursionError:
            return ERROR
        except Exception:
            # any unexpected issue, avoid crash and return ERROR sentinel
            return ERROR
        return ERROR

    # def visit_array_access(self, ast):
    #     return self.visitArrayAccess(ast)

    # def visit_array_literal(self, ast):
    #     return self.visitArrayLiteral(ast) 

    # def visit_array_type(self, ast):
    #     return self.visitArrayType(ast)

    # def visit_assignment_statement(self, ast):
    #     return self.visitAssignmentStatement(ast)

    # def visit_attribute(self, ast):
    #     return self.visitAttribute(ast)

    # def visit_attribute_decl(self, ast):
    #     return self.visitAttributeDecl(ast)

    # def visit_binary_op(self, ast):
    #     return self.visitBinaryOp(ast)

    # def visit_block_statement(self, ast):
    #     return self.visitBlockStatement(ast) 

    # def visit_bool_literal(self, ast):
    #     return self.visitBoolLiteral(ast)

    # def visit_break_statement(self, ast):
    #     return self.visitBreakStatement(ast)   

    # def visit_class_decl(self, ast):
    #     return self.visitClassDecl(ast)

    # def visit_class_type(self, ast):
    #     return self.visitClassType(ast)

    # def visit_constructor_decl(self, ast):
    #     return self._call_camel("visitConstructorDecl", ast)

    # def visit_continue_statement(self, ast):
    #     return self.visitContinueStatement(ast)

    # def visit_destructor_decl(self, ast):
    #     return self._call_camel("visitDestructorDecl", ast)

    # def visit_float_literal(self, ast):
    #     return self._call_camel("visitFloatLiteral", ast)

    # def visit_for_statement(self, ast):
    #     return self._call_camel("visitForStatement", ast)

    # def visit_id_lhs(self, ast):
    #     return self._call_camel("visitIdLHS", ast)

    # def visit_identifier(self, ast):
    #     return self._call_camel("visitIdentifier", ast)

    # def visit_if_statement(self, ast):
    #     return self._call_camel("visitIfStatement", ast)

    # def visit_int_literal(self, ast):
    #     return self._call_camel("visitIntLiteral", ast)

    # def visit_member_access(self, ast):
    #     return self._call_camel("visitMemberAccess", ast)

    # def visit_method_call(self, ast):
    #     return self._call_camel("visitMethodCall", ast)

    # def visit_method_decl(self, ast):
    #     return self._call_camel("visitMethodDecl", ast)

    # def visit_method_invocation(self, ast):
    #     # many ASTs use MethodInvocation vs MethodCall; try both
    #     r = self._call_camel("visitMethodInvocation", ast)
    #     if r is ERROR:
    #         r = self._call_camel("visitMethodCall", ast)
    #     return r

    # def visit_method_invocation_statement(self, ast):
    #     return self._call_camel("visitMethodInvocationStatement", ast)

    # def visit_nil_literal(self, ast):
    #     return self._call_camel("visitNilLiteral", ast)

    # def visit_object_creation(self, ast):
    #     return self._call_camel("visitObjectCreation", ast)

    # def visit_parameter(self, ast):
    #     return self._call_camel("visitParameter", ast)

    # def visit_parenthesized_expression(self, ast):
    #     return self._call_camel("visitParenthesizedExpression", ast)

    # def visit_postfix_expression(self, ast):
    #     return self._call_camel("visitPostfixExpression", ast)

    # def visit_postfix_lhs(self, ast):
    #     return self._call_camel("visitPostfixLHS", ast)

    # def visit_primitive_type(self, ast):
    #     return self._call_camel("visitPrimitiveType", ast)

    # def visit_program(self, ast):
    #     return self._call_camel("visitProgram", ast)

    # def visit_reference_type(self, ast):
    #     return self._call_camel("visitReferenceType", ast)

    # def visit_return_statement(self, ast):
    #     return self._call_camel("visitReturnStatement", ast)

    # def visit_static_member_access(self, ast):
    #     # static member access may map to MemberAccess or special StaticMemberAccess
    #     r = self._call_camel("visitStaticMemberAccess", ast)
    #     if r is ERROR:
    #         r = self._call_camel("visitMemberAccess", ast)
    #     return r

    # def visit_static_method_invocation(self, ast):
    #     r = self._call_camel("visitStaticMethodInvocation", ast)
    #     if r is ERROR:
    #         r = self._call_camel("visitMethodCall", ast)
    #     return r

    # def visit_string_literal(self, ast):
    #     return self._call_camel("visitStringLiteral", ast)

    # def visit_this_expression(self, ast):
    #     return self._call_camel("visitThisExpression", ast)

    # def visit_unary_op(self, ast):
    #     return self._call_camel("visitUnaryOp", ast)

    # def visit_variable(self, ast):
    #     return self._call_camel("visitVariable", ast)

    # def visit_variable_decl(self, ast):
    #     return self._call_camel("visitVariableDecl", ast)
    
    def visit_array_access(self, ast): return self.visitArrayAccess(ast)
    def visit_array_literal(self, ast): return self.visitArrayLiteral(ast)
    def visit_array_type(self, ast): return self.visitArrayType(ast) if hasattr(self, 'visitArrayType') else None
    def visit_assignment_statement(self, ast): return self.visitAssignmentStatement(ast)
    def visit_attribute(self, ast): return self.visitAttribute(ast) if hasattr(self, 'visitAttribute') else None
    def visit_attribute_decl(self, ast): return self.visitAttributeDecl(ast)
    def visit_binary_op(self, ast): return self.visitBinaryOp(ast)
    def visit_block_statement(self, ast): return self.visitBlockStatement(ast)
    def visit_bool_literal(self, ast): return self.visitBoolLiteral(ast)
    def visit_break_statement(self, ast): return self.visitBreakStatement(ast)
    def visit_class_decl(self, ast): return self.visitClassDecl(ast)
    def visit_class_type(self, ast): return self.visitClassType(ast) if hasattr(self, 'visitClassType') else None
    def visit_constructor_decl(self, ast): return self.visitConstructorDecl(ast)
    def visit_continue_statement(self, ast): return self.visitContinueStatement(ast)
    def visit_destructor_decl(self, ast): return self.visitDestructorDecl(ast)
    def visit_float_literal(self, ast): return self.visitFloatLiteral(ast)
    def visit_for_statement(self, ast): return self.visitForStatement(ast)
    def visit_id_lhs(self, ast): return self.visitIdLHS(ast) if hasattr(self, 'visitIdLHS') else None
    def visit_identifier(self, ast): return self.visitIdentifier(ast)
    def visit_if_statement(self, ast): return self.visitIfStatement(ast)
    def visit_int_literal(self, ast): return self.visitIntLiteral(ast)
    def visit_member_access(self, ast): return self.visitMemberAccess(ast)
    def visit_method_call(self, ast): return self.visitMethodCall(ast)
    def visit_method_decl(self, ast): return self.visitMethodDecl(ast)
    def visit_method_invocation(self, ast): return self.visitMethodCall(ast)  # alias
    def visit_method_invocation_statement(self, ast): return self.visitMethodInvocationStatement(ast)
    def visit_nil_literal(self, ast): return self.visitNilLiteral(ast)
    def visit_object_creation(self, ast): return self.visitObjectCreation(ast)
    def visit_parameter(self, ast): return self.visitParameter(ast)
    def visit_parenthesized_expression(self, ast): return self.visitParenthesizedExpression(ast)
    def visit_postfix_expression(self, ast): return self.visitPostfixExpression(ast)
    def visit_postfix_lhs(self, ast): return self.visitPostfixLHS(ast) if hasattr(self, 'visitPostfixLHS') else None
    def visit_primitive_type(self, ast): return self.visitPrimitiveType(ast) if hasattr(self, 'visitPrimitiveType') else None
    def visit_program(self, ast): return self.visitProgram(ast)
    def visit_reference_type(self, ast): return self.visitReferenceType(ast) if hasattr(self, 'visitReferenceType') else None
    def visit_return_statement(self, ast): return self.visitReturnStatement(ast)
    def visit_static_member_access(self, ast): return self.visitMemberAccess(ast)  # alias
    def visit_static_method_invocation(self, ast): return self.visitMethodCall(ast)  # alias
    def visit_string_literal(self, ast): return self.visitStringLiteral(ast)
    def visit_this_expression(self, ast): return self.visitThisExpression(ast)
    def visit_unary_op(self, ast): return self.visitUnaryOp(ast)
    def visit_variable(self, ast): return self.visitVariable(ast) if hasattr(self, 'visitVariable') else None
    def visit_variable_decl(self, ast): return self.visitVariableDecl(ast)