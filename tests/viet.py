"""
viet.py - 100 test cases for OPLang static semantic analysis
Covers all 10 error types: Redeclared, Undeclared, CannotAssignToConstant,
TypeMismatchInStatement, TypeMismatchInExpression, TypeMismatchInConstant,
MustInLoop, IllegalConstantExpression, IllegalArrayLiteral, IllegalMemberAccess
"""

from utils import Checker


# ==================== REDECLARED TESTS (10) ====================

def test_viet_001():
    """Redeclared Class"""
    source = """
class Animal {}
class Animal {}
"""
    expected = "Redeclared(Class, Animal)"
    assert Checker(source).check_from_source() == expected


def test_viet_002():
    """Redeclared Attribute"""
    source = """
class Test {
    int count;
    float count;
    static void main() {}
}
"""
    expected = "Redeclared(Attribute, count)"
    assert Checker(source).check_from_source() == expected


def test_viet_003():
    """Redeclared Method"""
    source = """
class Test {
    void process() {}
    int process() { return 0; }
    static void main() {}
}
"""
    expected = "Redeclared(Method, process)"
    assert Checker(source).check_from_source() == expected


def test_viet_004():
    """Redeclared Variable"""
    source = """
class Test {
    static void main() {
        int x := 1;
        int x := 2;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_viet_005():
    """Redeclared Constant"""
    source = """
class Test {
    static final int PI := 3;
    static final int PI := 4;
    static void main() {}
}
"""
    expected = "Redeclared(Constant, PI)"
    assert Checker(source).check_from_source() == expected


def test_viet_006():
    """Redeclared Parameter"""
    source = """
class Test {
    void calc(int a; int a) {}
    static void main() {}
}
"""
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected


def test_viet_007():
    """Redeclared Constant with same name as variable"""
    source = """
class Test {
    static void main() {
        int num := 1;
        final int num := 2;
    }
}
"""
    expected = "Redeclared(Constant, num)"
    assert Checker(source).check_from_source() == expected


def test_viet_008():
    """Redeclared Method with same name as attribute"""
    source = """
class Test {
    string data;
    string data() { return ""; }
    static void main() {}
}
"""
    expected = "Redeclared(Method, data)"
    assert Checker(source).check_from_source() == expected


def test_viet_009():
    """Redeclared Attribute with same name as method"""
    source = """
class Test {
    void getValue() {}
    int getValue;
    static void main() {}
}
"""
    expected = "Redeclared(Attribute, getValue)"
    assert Checker(source).check_from_source() == expected


def test_viet_010():
    """Redeclared Variable in same scope"""
    source = """
class Test {
    void process() {
        int count := 10;
        int count := 20;
    }
    static void main() {}
}
"""
    expected = "Redeclared(Variable, count)"
    assert Checker(source).check_from_source() == expected


# ==================== UNDECLARED TESTS (10) ====================

def test_viet_011():
    """Undeclared Identifier"""
    source = """
class Test {
    static void main() {
        int x := unknownVar;
    }
}
"""
    expected = "UndeclaredIdentifier(unknownVar)"
    assert Checker(source).check_from_source() == expected


def test_viet_012():
    """Undeclared Class in extends"""
    source = """
class Child extends Parent {}
class Main { static void main() {} }
"""
    expected = "UndeclaredClass(Parent)"
    assert Checker(source).check_from_source() == expected


def test_viet_013():
    """Undeclared Attribute access"""
    source = """
class Foo {
    int x;
    static void main() {}
}
class Test {
    void run() {
        Foo f;
        int y := f.nonExistent;
    }
    static void main() {}
}
"""
    expected = "UndeclaredAttribute(nonExistent)"
    assert Checker(source).check_from_source() == expected


def test_viet_014():
    """Undeclared Method call"""
    source = """
class Foo {
    static void main() {}
}
class Test {
    void run() {
        Foo f;
        f.nonExistentMethod();
    }
    static void main() {}
}
"""
    expected = "UndeclaredMethod(nonExistentMethod)"
    assert Checker(source).check_from_source() == expected


def test_viet_015():
    """Undeclared Class in variable declaration"""
    source = """
class Test {
    static void main() {
        UnknownClass obj;
    }
}
"""
    expected = "UndeclaredClass(UnknownClass)"
    assert Checker(source).check_from_source() == expected


def test_viet_016():
    """Undeclared Identifier in for loop"""
    source = """
class Test {
    static void main() {
        for undeclaredVar := 0 to 10 do {}
    }
}
"""
    expected = "UndeclaredIdentifier(undeclaredVar)"
    assert Checker(source).check_from_source() == expected


def test_viet_017():
    """Undeclared Identifier in assignment"""
    source = """
class Test {
    static void main() {
        int x := 1;
        unknownVar := x + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(unknownVar)"
    assert Checker(source).check_from_source() == expected


def test_viet_018():
    """Undeclared Identifier in condition"""
    source = """
class Test {
    static void main() {
        if undeclaredFlag then {}
    }
}
"""
    expected = "UndeclaredIdentifier(undeclaredFlag)"
    assert Checker(source).check_from_source() == expected


def test_viet_019():
    """Undeclared Identifier in return"""
    source = """
class Test {
    int getValue() {
        return undeclaredResult;
    }
    static void main() {}
}
"""
    expected = "UndeclaredIdentifier(undeclaredResult)"
    assert Checker(source).check_from_source() == expected


def test_viet_020():
    """Undeclared Class for parameter type"""
    source = """
class Test {
    void process(UnknownType x) {}
    static void main() {}
}
"""
    expected = "UndeclaredClass(UnknownType)"
    assert Checker(source).check_from_source() == expected


# ==================== CANNOT ASSIGN TO CONSTANT TESTS (10) ====================

def test_viet_021():
    """Cannot assign to local constant"""
    source = """
class Test {
    static void main() {
        final int x := 10;
        x := 20;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(20)))"
    assert Checker(source).check_from_source() == expected


def test_viet_022():
    """Cannot assign to class constant attribute"""
    source = """
class Config {
    static final int MAX := 100;
    static void main() {
        Config.MAX := 200;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(Config).MAX)) := IntLiteral(200)))"
    assert Checker(source).check_from_source() == expected


def test_viet_023():
    """Cannot assign to constant in for loop"""
    source = """
class Test {
    static void main() {
        final int i := 0;
        for i := 0 to 10 do {}
    }
}
"""
    expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_viet_024():
    """Cannot assign to final attribute via this"""
    source = """
class Test {
    final int value;
    void setValue() {
        this.value := 10;
    }
    static void main() {}
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).value)) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected


def test_viet_025():
    """Cannot assign to constant inside if statement"""
    source = """
class Test {
    static void main() {
        final int flag := 1;
        if true then {
            flag := 0;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(flag) := IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected


def test_viet_026():
    """Cannot assign to constant string"""
    source = """
class Test {
    static void main() {
        final string msg := "hello";
        msg := "world";
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(msg) := StringLiteral('world')))"
    assert Checker(source).check_from_source() == expected


def test_viet_027():
    """Cannot assign to constant float"""
    source = """
class Test {
    static void main() {
        final float pi := 3.14;
        pi := 3.14159;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(pi) := FloatLiteral(3.14159)))"
    assert Checker(source).check_from_source() == expected


def test_viet_028():
    """Cannot assign to constant boolean"""
    source = """
class Test {
    static void main() {
        final boolean active := true;
        active := false;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(active) := BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected


def test_viet_029():
    """Cannot assign to static final attribute"""
    source = """
class Config {
    static final string VERSION := "1.0";
    void update() {
        Config.VERSION := "2.0";
    }
    static void main() {}
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(Config).VERSION)) := StringLiteral('2.0')))"
    assert Checker(source).check_from_source() == expected


def test_viet_030():
    """Cannot assign to constant array"""
    source = """
class Test {
    static void main() {
        final int[3] arr := {1, 2, 3};
        arr := {4, 5, 6};
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(arr) := ArrayLiteral({IntLiteral(4), IntLiteral(5), IntLiteral(6)})))"
    assert Checker(source).check_from_source() == expected


# ==================== TYPE MISMATCH IN STATEMENT TESTS (10) ====================

def test_viet_031():
    """Type mismatch in variable declaration"""
    source = """
class Test {
    static void main() {
        int x := "hello";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_032():
    """Type mismatch in assignment"""
    source = """
class Test {
    static void main() {
        int x := 1;
        x := "string";
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := StringLiteral('string')))"
    assert Checker(source).check_from_source() == expected


def test_viet_033():
    """Type mismatch in if condition"""
    source = """
class Test {
    static void main() {
        if 42 then {}
    }
}
"""
    expected = "TypeMismatchInStatement(IfStatement(if IntLiteral(42) then BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_viet_034():
    """Type mismatch in for loop variable type"""
    source = """
class Test {
    static void main() {
        float f := 1.0;
        for f := 0 to 10 do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_viet_035():
    """Type mismatch in return statement"""
    source = """
class Test {
    int getValue() {
        return "not an int";
    }
    static void main() {}
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('not an int')))"
    assert Checker(source).check_from_source() == expected


def test_viet_036():
    """Type mismatch in assignment string to int"""
    source = """
class Test {
    static void main() {
        string s := 123;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(string), [Variable(s = IntLiteral(123))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_037():
    """Type mismatch in for start expression"""
    source = """
class Test {
    static void main() {
        int i := 0;
        for i := "zero" to 10 do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := StringLiteral('zero') to IntLiteral(10) do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_viet_038():
    """Type mismatch in for end expression"""
    source = """
class Test {
    static void main() {
        int i := 0;
        for i := 0 to "ten" do {}
    }
}
"""
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to StringLiteral('ten') do BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_viet_039():
    """Type mismatch void return with value"""
    source = """
class Test {
    void doNothing() {
        return 42;
    }
    static void main() {}
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(42)))"
    assert Checker(source).check_from_source() == expected


def test_viet_040():
    """Type mismatch boolean to int"""
    source = """
class Test {
    static void main() {
        int x := true;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = BoolLiteral(True))]))"
    assert Checker(source).check_from_source() == expected


# ==================== TYPE MISMATCH IN EXPRESSION TESTS (10) ====================

def test_viet_041():
    """Type mismatch in binary operator"""
    source = """
class Test {
    static void main() {
        int x := 1 + "hello";
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), +, StringLiteral('hello')))"
    assert Checker(source).check_from_source() == expected


def test_viet_042():
    """Type mismatch in logical AND"""
    source = """
class Test {
    static void main() {
        boolean b := true && 1;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(BoolLiteral(True), &&, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected


def test_viet_043():
    """Type mismatch in unary minus with string"""
    source = """
class Test {
    static void main() {
        int x := -"hello";
    }
}
"""
    expected = "TypeMismatchInExpression(UnaryOp(-, StringLiteral('hello')))"
    assert Checker(source).check_from_source() == expected


def test_viet_044():
    """Type mismatch in unary NOT with int"""
    source = """
class Test {
    static void main() {
        boolean b := !42;
    }
}
"""
    expected = "TypeMismatchInExpression(UnaryOp(!, IntLiteral(42)))"
    assert Checker(source).check_from_source() == expected


def test_viet_045():
    """Type mismatch in array index"""
    source = """
class Test {
    static void main() {
        int[5] arr := {1, 2, 3, 4, 5};
        int x := arr["zero"];
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(arr)[StringLiteral('zero')]))"
    assert Checker(source).check_from_source() == expected


def test_viet_046():
    """Type mismatch in comparison"""
    source = """
class Test {
    static void main() {
        boolean b := "abc" < 123;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('abc'), <, IntLiteral(123)))"
    assert Checker(source).check_from_source() == expected


def test_viet_047():
    """Type mismatch in multiplication"""
    source = """
class Test {
    static void main() {
        int x := "a" * "b";
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('a'), *, StringLiteral('b')))"
    assert Checker(source).check_from_source() == expected


def test_viet_048():
    """Type mismatch in method arguments"""
    source = """
class Math {
    int add(int a; int b) {
        return a + b;
    }
    static void main() {}
}
class Test {
    void run() {
        Math m;
        int result := m.add("one", 2);
    }
    static void main() {}
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(m).add(StringLiteral('one'), IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected


def test_viet_049():
    """Type mismatch in logical OR"""
    source = """
class Test {
    static void main() {
        boolean b := "yes" || false;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('yes'), ||, BoolLiteral(True)))"
    assert Checker(source).check_from_source() == expected


def test_viet_050():
    """Type mismatch in string concatenation with int"""
    source = """
class Test {
    static void main() {
        string s := "hello" ^ 123;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('hello'), ^, IntLiteral(123)))"
    assert Checker(source).check_from_source() == expected


# ==================== TYPE MISMATCH IN CONSTANT TESTS (10) ====================

def test_viet_051():
    """Type mismatch in constant declaration"""
    source = """
class Test {
    static void main() {
        final int x := "hello";
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_052():
    """Type mismatch in class constant attribute"""
    source = """
class Config {
    static final int MAX := "not a number";
    static void main() {}
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(static final PrimitiveType(int), [Attribute(MAX = StringLiteral('not a number'))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_053():
    """Type mismatch in final string constant"""
    source = """
class Test {
    static void main() {
        final string s := 123;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(string), [Variable(s = IntLiteral(123))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_054():
    """Type mismatch in final boolean constant"""
    source = """
class Test {
    static void main() {
        final boolean flag := "yes";
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(boolean), [Variable(flag = StringLiteral('yes'))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_055():
    """Type mismatch in final float constant"""
    source = """
class Test {
    static void main() {
        final float pi := "3.14";
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(float), [Variable(pi = StringLiteral('3.14'))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_056():
    """Type mismatch in class final boolean attribute"""
    source = """
class Settings {
    static final boolean ENABLED := 1;
    static void main() {}
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(static final PrimitiveType(boolean), [Attribute(ENABLED = IntLiteral(1))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_057():
    """Type mismatch in final array constant"""
    source = """
class Test {
    static void main() {
        final int[2] arr := {"a", "b"};
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final ArrayType(PrimitiveType(int)[2]), [Variable(arr = ArrayLiteral({StringLiteral('a'), StringLiteral('b')}))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_058():
    """Type mismatch in constant from expression"""
    source = """
class Test {
    static void main() {
        final int x := 1 + 2;
        final string s := x;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(string), [Variable(s = Identifier(x))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_059():
    """Type mismatch in class static final float attribute"""
    source = """
class MathConst {
    static final float E := true;
    static void main() {}
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(static final PrimitiveType(float), [Attribute(E = BoolLiteral(True))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_060():
    """Type mismatch in final with binary expression"""
    source = """
class Test {
    static void main() {
        final boolean b := 1 + 2;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(boolean), [Variable(b = BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))"
    assert Checker(source).check_from_source() == expected


# ==================== MUST IN LOOP TESTS (10) ====================

def test_viet_061():
    """Break outside of loop"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_062():
    """Continue outside of loop"""
    source = """
class Test {
    static void main() {
        continue;
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_063():
    """Break in if statement outside loop"""
    source = """
class Test {
    static void main() {
        if true then {
            break;
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_064():
    """Continue in if-else outside loop"""
    source = """
class Test {
    static void main() {
        if false then {} else {
            continue;
        }
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_065():
    """Break in method without loop"""
    source = """
class Test {
    void doSomething() {
        break;
    }
    static void main() {}
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_066():
    """Continue in method without loop"""
    source = """
class Test {
    void process() {
        continue;
    }
    static void main() {}
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_067():
    """Break after for loop ends"""
    source = """
class Test {
    static void main() {
        int i := 0;
        for i := 0 to 5 do {}
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_068():
    """Continue after for loop ends"""
    source = """
class Test {
    static void main() {
        int i := 0;
        for i := 0 to 5 do {}
        continue;
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_069():
    """Break in constructor without loop"""
    source = """
class Test {
    Test() {
        break;
    }
    static void main() {}
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected


def test_viet_070():
    """Continue in destructor without loop"""
    source = """
class Test {
    ~Test() {
        continue;
    }
    static void main() {}
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


# ==================== ILLEGAL CONSTANT EXPRESSION TESTS (10) ====================

def test_viet_071():
    """Illegal constant expression with method call"""
    source = """
class Helper {
    static int getValue() { return 5; }
    static void main() {}
}
class Test {
    static final int X := Helper.getValue();
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(static final PrimitiveType(int), [Attribute(X = PostfixExpression(Identifier(Helper).getValue()))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_072():
    """Illegal constant expression with variable"""
    source = """
class Test {
    static void main() {
        int y := 5;
        final int x := y;
    }
}
"""
    expected = "IllegalConstantExpression(Identifier(y))"
    assert Checker(source).check_from_source() == expected


def test_viet_073():
    """Illegal constant expression with nil"""
    source = """
class Test {
    static final Test obj := nil;
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(NilLiteral(nil))"
    assert Checker(source).check_from_source() == expected


def test_viet_074():
    """Illegal constant expression with new object"""
    source = """
class Helper {
    static void main() {}
}
class Test {
    static void main() {
        final Helper h := new Helper();
    }
}
"""
    expected = "IllegalConstantExpression(ObjectCreation(new Helper()))"
    assert Checker(source).check_from_source() == expected


def test_viet_075():
    """Illegal constant expression with attribute access"""
    source = """
class Data {
    static int value := 10;
    static void main() {}
}
class Test {
    static final int X := Data.value;
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(static final PrimitiveType(int), [Attribute(X = PostfixExpression(Identifier(Data).value))]))"
    assert Checker(source).check_from_source() == expected


def test_viet_076():
    """Illegal constant expression with this"""
    source = """
class Test {
    int value;
    void init() {
        final int x := this.value;
    }
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(ThisExpression(this).value))"
    assert Checker(source).check_from_source() == expected


def test_viet_077():
    """Illegal constant expression with array access"""
    source = """
class Test {
    static void main() {
        int[3] arr := {1, 2, 3};
        final int x := arr[0];
    }
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(arr)[IntLiteral(0)]))"
    assert Checker(source).check_from_source() == expected


def test_viet_078():
    """Illegal constant expression with non-final variable in expression"""
    source = """
class Test {
    static void main() {
        int a := 1;
        final int b := a + 1;
    }
}
"""
    expected = "IllegalConstantExpression(BinaryOp(Identifier(a), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected


def test_viet_079():
    """Illegal constant expression with parameter"""
    source = """
class Test {
    void process(int param) {
        final int x := param;
    }
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(Identifier(param))"
    assert Checker(source).check_from_source() == expected


def test_viet_080():
    """Illegal constant expression with object field"""
    source = """
class Point {
    int x;
    int y;
    static void main() {}
}
class Test {
    void run() {
        Point p;
        final int val := p.x;
    }
    static void main() {}
}
"""
    expected = "IllegalConstantExpression(PostfixExpression(Identifier(p).x))"
    assert Checker(source).check_from_source() == expected


# ==================== ILLEGAL ARRAY LITERAL TESTS (10) ====================

def test_viet_081():
    """Illegal array literal with mixed types int and string"""
    source = """
class Test {
    static void main() {
        int[2] arr := {1, "two"};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('two')}))"
    assert Checker(source).check_from_source() == expected


def test_viet_082():
    """Illegal array literal with mixed bool and int"""
    source = """
class Test {
    static void main() {
        boolean[2] arr := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_083():
    """Illegal array literal with mixed float and string"""
    source = """
class Test {
    static void main() {
        float[2] arr := {1.5, "hello"};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({FloatLiteral(1.5), StringLiteral('hello')}))"
    assert Checker(source).check_from_source() == expected


def test_viet_084():
    """Illegal array literal with mixed string and bool"""
    source = """
class Test {
    static void main() {
        string[2] arr := {"yes", false};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('yes'), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_085():
    """Illegal array literal with mixed int and float"""
    source = """
class Test {
    static void main() {
        int[2] arr := {1, 2.5};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.5)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_086():
    """Illegal array literal with int and bool"""
    source = """
class Test {
    static void main() {
        int[3] arr := {1, 2, true};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), IntLiteral(2), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_087():
    """Illegal array literal with float and boolean"""
    source = """
class Test {
    static void main() {
        float[2] arr := {3.14, false};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({FloatLiteral(3.14), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_088():
    """Illegal array literal with string and int"""
    source = """
class Test {
    static void main() {
        string[2] arr := {"one", 1};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('one'), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected


def test_viet_089():
    """Illegal array literal with bool and string"""
    source = """
class Test {
    static void main() {
        boolean[2] arr := {true, "true"};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), StringLiteral('true')}))"
    assert Checker(source).check_from_source() == expected


def test_viet_090():
    """Illegal array literal with multiple mixed types"""
    source = """
class Test {
    static void main() {
        int[3] arr := {1, "two", true};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('two'), BoolLiteral(True)}))"
    assert Checker(source).check_from_source() == expected


# ==================== ILLEGAL MEMBER ACCESS TESTS (10) ====================

def test_viet_091():
    """Illegal member access non-static via class name"""
    source = """
class Data {
    int value;
    static void main() {}
}
class Test {
    void run() {
        int x := Data.value;
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Data).value))"
    assert Checker(source).check_from_source() == expected


def test_viet_092():
    """Illegal member access non-static method via class name"""
    source = """
class Helper {
    int getValue() { return 5; }
    static void main() {}
}
class Test {
    void run() {
        int x := Helper.getValue();
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Helper).getValue()))"
    assert Checker(source).check_from_source() == expected


def test_viet_093():
    """Illegal member access static attribute via instance"""
    source = """
class Config {
    static int MAX := 100;
    static void main() {}
}
class Test {
    void run() {
        Config c;
        int x := c.MAX;
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(c).MAX))"
    assert Checker(source).check_from_source() == expected


def test_viet_094():
    """Illegal member access static method via instance"""
    source = """
class Utils {
    static int compute() { return 42; }
    static void main() {}
}
class Test {
    void run() {
        Utils u;
        int x := u.compute();
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(u).compute()))"
    assert Checker(source).check_from_source() == expected


def test_viet_095():
    """Illegal member access non-static in static context"""
    source = """
class Test {
    int instanceValue;
    static void main() {
        int x := Test.instanceValue;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Test).instanceValue))"
    assert Checker(source).check_from_source() == expected


def test_viet_096():
    """Illegal member access non-static method in static context"""
    source = """
class Test {
    int getValue() { return 10; }
    static void main() {
        int x := Test.getValue();
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Test).getValue()))"
    assert Checker(source).check_from_source() == expected


def test_viet_097():
    """Illegal access static via object assignment"""
    source = """
class Counter {
    static int count := 0;
    static void main() {}
}
class Test {
    void run() {
        Counter c;
        c.count := 5;
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(c).count))"
    assert Checker(source).check_from_source() == expected


def test_viet_098():
    """Illegal member access non-static from class in expression"""
    source = """
class Box {
    int size;
    static void main() {}
}
class Test {
    void run() {
        int total := Box.size + 10;
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Box).size))"
    assert Checker(source).check_from_source() == expected


def test_viet_099():
    """Illegal member access static via instance in method call"""
    source = """
class Math {
    static int add(int a; int b) { return a + b; }
    static void main() {}
}
class Test {
    void run() {
        Math m;
        int result := m.add(1, 2);
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(m).add(IntLiteral(1), IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected


def test_viet_100():
    """Illegal member access non-static void method via class"""
    source = """
class Printer {
    void print() {}
    static void main() {}
}
class Test {
    void run() {
        Printer.print();
    }
    static void main() {}
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Printer).print()))"
    assert Checker(source).check_from_source() == expected
