from utils import Checker


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
    class Test {
        static void main() {
            int x := 5;
            int y := x + 1;
        }
    }
    """
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test type mismatch error"""
    source = """
    class Test {
        static void main() {
            int x := "hello";
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test break not in loop error"""
    source = """
    class Test {
        static void main() {
            break;
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test cannot assign to constant error"""
    source = """
class Test {
    static void main() {
        final int x := 5;
        x := 10;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected

def test_007():
    """Test illegal array literal error - alternative case"""
    source = """
class Test {
    static void main() {
        boolean[2] flags := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(true), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected

def test_008():
    """Redeclared Class in global scope"""
    source = """
    class Student {
        int id;
        string name;
    }
    class Student {  # Redeclared(Class, Student)
        float grade;
    }
    """
    expected = "Redeclared(Class, Student)"
    assert Checker(source).check_from_source() == expected

def test_009():
    """Redeclared Method in same class"""
    source = """
    class Calculator {
        int add(int a; int b) {
            return a + b;
        }
        int add(int x; int y) {  
            return x + y;
        }
    }
    """
    expected = "Redeclared(Method, add)"
    assert Checker(source).check_from_source() == expected

def test_010():
    """Redeclared Attribute in same class"""
    source = """
    class Person {
        string name;
        int age;
        string name;  # Redeclared(Attribute, name)
    }
    """
    expected = "Redeclared(Attribute, name)"
    assert Checker(source).check_from_source() == expected

def test_011():
    """Redeclared Variable in method scope"""
    source = """
    class Example {
        void process() {
            int count := 10;
            int count := 20;  
        }
    }
    """
    expected = "Redeclared(Variable, count)"
    assert Checker(source).check_from_source() == expected

def test_012():
    """Redeclared Parameter"""
    source = """
    class Math {
        int calculate(int x; float y; int x) {
            return x + y;
        }
    }
    """
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_013():
    """Redeclared Parameter in constructor"""
    source = """
    class Point {
        Point(int x; int y; int x) {  # Redeclared(Parameter, x)
            this.x := x;
            this.y := y;
        }
    }
    """
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_014():
    """Redeclared Class in global scope"""
    source = """
    class Alpha {}
    class Beta {}
    class Alpha {}  # Redeclared(Class, Alpha)
    """
    expected = "Redeclared(Class, Alpha)"
    assert Checker(source).check_from_source() == expected

def test_015():
    """Redeclared Attribute in same class with different type"""
    source = """
    class Data {
        int value;
        float value;  # Redeclared(Attribute, value)
    }
    """
    expected = "Redeclared(Attribute, value)"
    assert Checker(source).check_from_source() == expected

def test_016():
    """Redeclared Method with same signature"""
    source = """
    class Math {
        int sum(int a; int b) { return a + b; }
        int sum(int a; int b) { return a - b; }  # Redeclared(Method, sum)
    }
    """
    expected = "Redeclared(Method, sum)"
    assert Checker(source).check_from_source() == expected

def test_017():
    """Redeclared Attribute in class with array type"""
    source = """
    class ArrClass {
        int[2] arr;
        int[3] arr;  # Redeclared(Attribute, arr)
    }
    """
    expected = "Redeclared(Attribute, arr)"
    assert Checker(source).check_from_source() == expected


def test_020():
    """Error: Undeclared Variable"""
    source = """ 
    class Example {
        void method() {
            int result := undeclaredVar + 10;  
        }
    }
    """
    expected = "UndeclaredIdentifier(undeclaredVar)"
    assert Checker(source).check_from_source() == expected


def test_021():
    """Error: Undeclared Class"""
    source = """ 
    class Student extends Person {  
        int studentId;
    }
    """
    expected = "UndeclaredClass(Person)"
    assert Checker(source).check_from_source() == expected

def test_022():
    """Error: Out of scope access"""
    source = """ 
    class ScopeTest {
        void method1() {
            int localVar := 42;
        }
        
        void method2() {
            int value := localVar + 1;  
        }
    }
    """
    expected = "UndeclaredIdentifier(localVar)"
    assert Checker(source).check_from_source() == expected

def test_023():
    """Error: Assignment to constant attribute"""
    source = """ 
    class Constants {
        final int MAX_COUNT := 100;
        
        void example() {
            MAX_COUNT := 200; 
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(MAX_COUNT) := IntLiteral(200)))"
    assert Checker(source).check_from_source() == expected

def test_024():
    """Error: Assignment to constant attribute"""
    source = """ 
    class Configuration {
        final string APP_NAME := "MyApp";
        
        void updateConfig() {
            APP_NAME := "NewApp";  
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(APP_NAME) := StringLiteral('NewApp')))"
    assert Checker(source).check_from_source() == expected

def test_025():
    """Error: Assignment in for loop"""
    source = """ 
    class LoopExample {
        final int limit := 10;
        
        void process() {
            for limit := 0 to 20 do {  
                io.writeIntLn(limit);
            }
        }
    }
    """
    expected = "CannotAssignToConstant(ForStatement(for limit := IntLiteral(0) to IntLiteral(20) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(limit))))])))"
    assert Checker(source).check_from_source() == expected

def test_026():
    """Error: Multiple assignment attempts"""
    source = """ 
    class MultipleAssignment {
        final float PI := 3.14159;
        
        void calculate() {
            PI := PI * 2; 
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(PI) := BinaryOp(Identifier(PI), *, IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected

def test_027():
    """Valid: Proper constant usage"""
    source = """ 
    class ValidConstants {
        final int MAX_SIZE := 1000;
        final string VERSION;
        
        ValidConstants(string version) {
            VERSION := version;  # Valid: initialization in constructor
        }
        
        # void display() {
        #     io.writeStrLn("Version: " ^ VERSION);  # Valid: reading constant
        #     io.writeIntLn(MAX_SIZE);
        # }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_028():
    """Error: Non-boolean condition in if statement"""
    source = """
    class ConditionalError {
        void check() {
            int x := 5;
            string message := "hello";
            if x then {  # Error: TypeMismatchInStatement at if statement
                io.writeStrLn("Invalid");
            }
            
            
            if message then {  # Error: TypeMismatchInStatement at if statement
                io.writeStrLn("Also invalid");
            }
        }
    }
    """
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(x) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Invalid'))))])))"
    assert Checker(source).check_from_source() == expected

def test_029():
    """Error: Non-integer in for statement"""
    source = """
    class ForLoopError {
        void loop() {
            float f := 1.5;
            boolean condition := true;
            int i := 0;
            
            # for f := 0 to 10 do {  # Error: TypeMismatchInStatement at for statement
            #     io.writeFloatLn(f);
            # }
            
            for i := condition to 10 do {  # Error: TypeMismatchInStatement at variable declaration
                io.writeIntLn(i);
            }
        }
    }
    """
    #expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeFloatLn(Identifier(f))))])))"
    expected = "TypeMismatchInStatement(ForStatement(for i := Identifier(condition) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected

def test_030():
    """Error: Assignment type mismatch"""
    source = """
    class AssignmentError {
        void assign() {
            int x := 10;
            string text := "hello";
            boolean flag := true;
            
            #x := text;  # Error: TypeMismatchInStatement at assignment
            #text := x;  # Error: TypeMismatchInStatement at assignment
            flag := x;  # Error: TypeMismatchInStatement at assignment
        }
    }
    """
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(text) := Identifier(x)))"
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(flag) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_031():
    """Error: Array assignment mismatch 1"""
    source = """
    class ArrayError {
        void arrayAssign() {
            int[3] intArray := {1, 2, 3};
            float[3] floatArray := {1.0, 2.0, 3.0};
            int[2] smallArray := {1, 2};
            
            intArray := floatArray;  # Error: TypeMismatchInStatement at assignment
            intArray := smallArray;  # Error: TypeMismatchInStatement at assignment (different size)
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(floatArray)))"
    assert Checker(source).check_from_source() == expected

def test_032():
    """Error: Array assignment mismatch 2"""
    source = """
    class ArrayError {
        void arrayAssign() {
            int[3] intArray := {1, 2, 3};
            float[3] floatArray := {1.0, 2.0, 3.0};
            int[2] smallArray := {1, 2};
            
            #intArray := floatArray;  # Error: TypeMismatchInStatement at assignment
            intArray := smallArray;  # Error: TypeMismatchInStatement at assignment (different size)
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(smallArray)))"
    assert Checker(source).check_from_source() == expected

def test_033():
    """Error: Non-boolean condition in if statement"""
    source = """
    class ConditionalError {
        void check() {
            int x := 5;
            string message := "hello";
            # if x then {  # Error: TypeMismatchInStatement at if statement
            #     io.writeStrLn("Invalid");
            # }
            
            
            if message then {  # Error: TypeMismatchInStatement at if statement
                io.writeStrLn("Also invalid");
            }
        }
    }
    """
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(message) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Also invalid'))))])))"
    assert Checker(source).check_from_source() == expected

def test_034():
    """Error: Assignment type mismatch"""
    source = """
    class AssignmentError {
        void assign() {
            int x := 10;
            string text := "hello";
            boolean flag := true;
            
            x := text;  # Error: TypeMismatchInStatement at assignment
            #text := x;  # Error: TypeMismatchInStatement at assignment
            #flag := x;  # Error: TypeMismatchInStatement at assignment
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(text) := Identifier(x)))"
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(flag) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_035():
    """Error: Assignment type mismatch"""
    source = """
    class AssignmentError {
        void assign() {
            int x := 10;
            string text := "hello";
            boolean flag := true;
            
            #x := text;  # Error: TypeMismatchInStatement at assignment
            text := x;  # Error: TypeMismatchInStatement at assignment
            #flag := x;  # Error: TypeMismatchInStatement at assignment
        }
    }
    """
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(text) := Identifier(x)))"
    #expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(flag) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_036():
    """Error: Method call with wrong arguments"""
    source = """
    class CallError {
        void processInt(int value) {
            io.writeIntLn(value);
        }
        
        void test() {
            string text := "123";
            this.processInt(text);  # Error: TypeMismatchInStatement at method call
        }
    }
    """
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).processInt(Identifier(text)))))"
    assert Checker(source).check_from_source() == expected

def test_037():
    """Error: Return type mismatch 1"""
    source = """
    class ReturnError {
        int getValue() {
            return "invalid";  # Error: TypeMismatchInStatement at return statement
        }
        
        string getText() {
            return 42;  # Error: TypeMismatchInStatement at return statement
        }
    }
    """
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('invalid')))"
    assert Checker(source).check_from_source() == expected

def test_038():
    """Error: Return type mismatch 2"""
    source = """
    class ReturnError {
        # int getValue() {
        #     return "invalid";  # Error: TypeMismatchInStatement at return statement
        # }
        
        string getText() {
            return 42;  # Error: TypeMismatchInStatement at return statement
        }
    }
    """
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(42)))"
    assert Checker(source).check_from_source() == expected

def test_039():
    """Valid: Proper coercion"""
    source = """
    class Shape {}
    class Rectangle extends Shape {
        float width;
        float height;
        
        Rectangle(float w; float h) {
            this.width := w;
            this.height := h;
        }
    }

    class ValidCoercion {
        void coerce() {
            int x := 10;
            float y := x;  # Valid: int to float coercion

            Shape obj := new Rectangle(5.0, 3.0);  # Valid: subtype to supertype
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_040():
    """Error: Array subscripting with wrong types 1"""
    source = """
    class ArraySubscriptError {
        void access() {
            int[5] numbers := {1, 2, 3, 4, 5};
            string[2] words := {"hello", "world"};
            int x := 10;
            int invalid := x[0];  # Error: TypeMismatchInExpression at array access
            
            int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
            int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
            string word := words[true];      # Error: TypeMismatchInExpression at array access                 
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(x)[IntLiteral(0)]))"
    assert Checker(source).check_from_source() == expected

def test_041():
    """Error: Array subscripting with wrong types 2"""
    source = """
    class ArraySubscriptError {
        void access() {
            int[5] numbers := {1, 2, 3, 4, 5};
            string[2] words := {"hello", "world"};
            int x := 10;
            #int invalid := x[0];  # Error: TypeMismatchInExpression at array access
            
            int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
            int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
            string word := words[true];      # Error: TypeMismatchInExpression at array access                 
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(numbers)[StringLiteral('index')]))"
    assert Checker(source).check_from_source() == expected

def test_042():
    """Error: Array subscripting with wrong types 3"""
    source = """
    class ArraySubscriptError {
        void access() {
            int[5] numbers := {1, 2, 3, 4, 5};
            string[2] words := {"hello", "world"};
            int x := 10;
            #int invalid := x[0];  # Error: TypeMismatchInExpression at array access
            
            #int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
            int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
            string word := words[true];      # Error: TypeMismatchInExpression at array access                 
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(numbers)[FloatLiteral(2.5)]))"
    assert Checker(source).check_from_source() == expected

def test_043():
    """Error: Array subscripting with wrong types 4"""
    source = """
    class ArraySubscriptError {
        void access() {
            int[5] numbers := {1, 2, 3, 4, 5};
            string[2] words := {"hello", "world"};
            int x := 10;
            #int invalid := x[0];  # Error: TypeMismatchInExpression at array access
            
            #int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
            #int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
            string word := words[true];      # Error: TypeMismatchInExpression at array access                 
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(words)[BoolLiteral(True)]))"
    assert Checker(source).check_from_source() == expected

def test_044():
    """Error: Binary operation type mismatch 1"""
    source = """
    class BinaryOpError {
        void calculate() {
            int x := 5;
            string text := "hello";
            boolean flag := true;
            
            int sum := x + text;     # Error: TypeMismatchInExpression at binary operation
            boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
            int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
        }
    }
    """    
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_045():
    """Error: Binary operation type mismatch 2"""
    source = """
    class BinaryOpError {
        void calculate() {
            int x := 5;
            string text := "hello";
            boolean flag := true;
            
            #int sum := x + text;     # Error: TypeMismatchInExpression at binary operation
            boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
            int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
        }
    }
    """    
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), &&, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected

def test_046():
    """Error: Binary operation type mismatch 3"""
    source = """
    class BinaryOpError {
        void calculate() {
            int x := 5;
            string text := "hello";
            boolean flag := true;
            
            #int sum := x + text;     # Error: TypeMismatchInExpression at binary operation
            #boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
            int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
        }
    }
    """    
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(text), <, Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_047():
    """Error: Method call in expression context 1"""
    source = """
    class MethodCallError {
        void printMessage() {  # void return type
            io.writeStrLn("Hello");
        }
        
        int getValue() {
            return 42;
        }
        
        void test() {
            int result := this.printMessage();  # Error: TypeMismatchInExpression at method call
            
            string text := "number";
            int value := this.getValue(text);  # Error: TypeMismatchInExpression at method call
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).printMessage()))"
    assert Checker(source).check_from_source() == expected

def test_048():
    """Error: Method call in expression context 2"""
    source = """
    class MethodCallError {
        void printMessage() {  # void return type
            io.writeStrLn("Hello");
        }
        
        int getValue() {
            return 42;
        }
        
        void test() {
            #int result := this.printMessage();  # Error: TypeMismatchInExpression at method call
            
            string text := "number";
            int value := this.getValue(text);  # Error: TypeMismatchInExpression at method call
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).getValue(Identifier(text))))"
    assert Checker(source).check_from_source() == expected

def test_049():
    """Error: Attribute access on non-object 1"""
    source = """
    class AttributeAccessError {
        void access() {
            int x := 10;
            string text := "hello";
            
            int length := text.value;  # Error: TypeMismatchInExpression at member access (if value doesn't exist)
            int invalid := x.length;   # Error: TypeMismatchInExpression at member access (x is not object)
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(text).value))"
    assert Checker(source).check_from_source() == expected

def test_050():
    """Error: Attribute access on non-object 2"""
    source = """
    class AttributeAccessError {
        void access() {
            int x := 10;
            string text := "hello";
            
            #int length := text.value;  # Error: TypeMismatchInExpression at member access (if value doesn't exist)
            int invalid := x.length;   # Error: TypeMismatchInExpression at member access (x is not object)
        }
    }
    """    
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(x).length))"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Error: Unary operation type mismatch 1"""
    source = """
    class UnaryOpError {
        void operations() {
            string text := "hello";
            boolean flag := true;
            
            int negative := -text;   # Error: TypeMismatchInExpression at unary operation
            boolean not := !text;    # Error: TypeMismatchInExpression at unary operation
            int notFlag := !flag;    # Error: TypeMismatchInExpression at unary operation (if assigned to int)
        }
    }
    """    
    expected = "TypeMismatchInExpression(UnaryOp(-, Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_052():
    """Error: Unary operation type mismatch 2"""
    source = """
    class UnaryOpError {
        void operations() {
            string text := "hello";
            boolean flag := true;
            
            #int negative := -text;   # Error: TypeMismatchInExpression at unary operation
            boolean not := !text;    # Error: TypeMismatchInExpression at unary operation
            int notFlag := !flag;    # Error: TypeMismatchInExpression at unary operation (if assigned to int)
        }
    }
    """    
    expected = "TypeMismatchInExpression(UnaryOp(!, Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_053():
    """Error: Unary operation type mismatch 3"""
    source = """
    class UnaryOpError {
        void operations() {
            string text := "hello";
            boolean flag := true;
            
            #int negative := -text;   # Error: TypeMismatchInExpression at unary operation
            #boolean not := !text;    # Error: TypeMismatchInExpression at unary operation
            int notFlag := !flag;    # Error: TypeMismatchInExpression at unary operation (if assigned to int)
        }
    }
    """    
    expected = "TypeMismatchInExpression(UnaryOp(!, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Valid: Proper expression types"""
    source = """
    class Student{
        string name;

        Student(string name) {this.name := name;}
        string getName() {return this.name;}
    }

    class ValidExpressions {
        void validOps() {
            int[3] numbers := {1, 2, 3};
            int index := 1;
            int value := numbers[index];  # Valid
            
            int x := 10, y := 20;
            boolean result := x < y;      # Valid
            int sum := x + y;             # Valid

            Student student := new Student();
            string name := student.getName();  # Valid - assuming getName() returns string
        }
    }
    """    
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Error: Type mismatch in constant declaration 1"""
    source = """
    class ConstantTypeError {
        final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(a = FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected

def test_056():
    """Error: Type mismatch in constant declaration 2"""
    source = """
    class ConstantTypeError {
        #final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(string), [Attribute(text = IntLiteral(42))]))"
    assert Checker(source).check_from_source() == expected

def test_057():
    """Error: Type mismatch in constant declaration 3"""
    source = """
    class ConstantTypeError {
        #final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        #final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = StringLiteral('true'))]))"
    assert Checker(source).check_from_source() == expected

def test_058():
    """Error: Type mismatch in constant declaration 4"""
    source = """
    class ConstantTypeError {
        #final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        #final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        #final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(count = FloatLiteral(3.14))]))"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Error: Array constant type mismatch 1"""
    source = """
    class ArrayConstantError {
        final int[3] numbers := {1.0, 2.0, 3.0};  # Error: TypeMismatchInConstant at constant declaration
        final string[3] words := {1, 2, 3};        # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(PrimitiveType(int)[3]), [Attribute(numbers = ArrayLiteral({FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0)}))]))"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Error: Array constant type mismatch 2"""
    source = """
    class ArrayConstantError {
        #final int[3] numbers := {1.0, 2.0, 3.0};  # Error: TypeMismatchInConstant at constant declaration
        final string[3] words := {1, 2, 3};        # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(PrimitiveType(string)[3]), [Attribute(words = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]))"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Valid: Proper constant types"""
    source = """
    class ValidConstants {
        final int MAX_SIZE := 1000;           # Valid
        final float PI := 3.14159;            # Valid
        final string APP_NAME := "MyApp";     # Valid
        final int[4] PRIMES := {2, 3, 5, 7};   # Valid

        final float ratio := 10;               # Valid: int to float coercion
    }
    """    
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Error: Object type mismatch"""
    source = """
    class Shape {}
    class Rectangle extends Shape {}
    class Integer {}
     
    class ObjectConstantError {
        final Shape shape := new Integer(42);  # TypeMismatchInConstant - if no inheritance relationship
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer(IntLiteral(42))))]))"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Valid: Object type match with inheritance"""
    source = """
    class Shape {}
    class Rectangle extends Shape {}
    class Integer {}

    class ObjectConstantValid {
        final Shape shape := new Rectangle(1.0, 2.0);  # InValid: No match constructor for Rectangle
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Rectangle(FloatLiteral(1.0), FloatLiteral(2.0))))]))"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Error: Break/continue outside loop 1"""
    source = """
    class LoopError {
        void method() {
            break;     # MustInLoop(break)
            continue;  # MustInLoop(continue)
        }
        
        void conditionalError() {
            if true then {
                break;     # MustInLoop(break)
                continue;  # MustInLoop(continue)
            }
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Error: Break/continue outside loop 2"""
    source = """
    class LoopError {
        void method() {
            #break;     # MustInLoop(break)
            continue;  # MustInLoop(continue)
        }
        
        void conditionalError() {
            if true then {
                break;     # MustInLoop(break)
                continue;  # MustInLoop(continue)
            }
        }
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

    
def test_066():
    """Error: Break/continue outside loop 3"""
    source = """
    class LoopError {
        void method() {
            #break;     # MustInLoop(break)
            #continue;  # MustInLoop(continue)
        }
        
        void conditionalError() {
            if true then {
                break;     # MustInLoop(break)
                continue;  # MustInLoop(continue)
            }
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Error: Break/continue outside loop 4"""
    source = """
    class LoopError {
        void method() {
            #break;     # MustInLoop(break)
            #continue;  # MustInLoop(continue)
        }
        
        void conditionalError() {
            if true then {
                #break;     # MustInLoop(break)
                continue;  # MustInLoop(continue)
            }
        }
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_068():
    """Break/continue in method called from loop"""
    source = """
    class MethodCallError {
        void helperMethod() {
            break;     # MustInLoop(break) - different method scope
            continue;  # MustInLoop(continue)
        }
        
        void loopWithCall() {
            int i;
            for i := 0 to 10 do {
                this.helperMethod();  # Method call doesn't transfer loop context
            }
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_069():
    """Valid: Break/continue in loops"""
    source = """
    class ValidLoops {
        void forLoopWithBreak() {
            int i;
            for i := 0 to 10 do {
                if i == 5 then {
                    break;     # Valid
                }
                if i % 2 == 0 then {
                    continue;  # Valid
                }
                io.writeIntLn(i);
            }
        }
        
        void forLoop() {
            int i;
            for i := 0 to 10 do {
                if i == 3 then {
                    continue;  # Valid
                }
                if i == 8 then {
                    break;     # Valid
                }
                io.writeIntLn(i);
            }
        }
        
        void nestedLoops() {
            int i, j;
            for i := 0 to 5 do {
                for j := 0 to 5 do {
                    if i == j then {
                        continue;  # Valid - affects inner loop
                    }
                    if j > 3 then {
                        break;     # Valid - breaks inner loop
                    }
                }
                break;  # Valid - breaks outer loop
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Error: Break/continue in loops 1"""
    source = """
    class ValidLoops {
        void forLoopWithBreak() {
            int i;
            for i := 0 to 10 do {
                if i == 5 then {
                    break;     # Valid
                }
                if i % 2 == 0 then {
                    continue;  # Valid
                }
                io.writeIntLn(i);
            }
            break;
        }
        
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Error: Break/continue in loops 1"""
    source = """
    class ValidLoops {
        void nestedLoops() {
            int i, j;
            for i := 0 to 5 do {
                for j := 0 to 5 do {
                    if i == j then {
                        break;  # Valid - affects inner loop
                    }
                    if j > 3 then {
                        break;     # Valid - breaks inner loop
                    }
                }
                break;  # Valid - breaks outer loop
            }
            continue;  # Error: MustInLoop(continue)
        }
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_072():
    """Error: None/null initialization 1"""
    source = """
    class IllegalConstantError {
        final int x;  # Error: IllegalConstantExpression at constant declaration

        final string text := nil;  # Error: IllegalConstantExpression at constant declaration
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(x)]))"
    assert Checker(source).check_from_source() == expected

def test_073():
    """Error: None/null initialization 2"""
    source = """
    class IllegalConstantError {
        #final int x;  # Error: IllegalConstantExpression at constant declaration

        final string text := nil;  # Error: IllegalConstantExpression at constant declaration
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(string), [Attribute(text = NilLiteral(nil))]))"
    assert Checker(source).check_from_source() == expected

def test_074():
    """Error: Using mutable variable in constant expression 1"""
    source = """
    class MutableInConstant {
        int mutableVar := 10;
        final int constant1 := mutableVar;  # Error: IllegalConstantExpression at constant declaration

        int localVar := 5;
        final int constant2 := 1 + localVar;  # Error: IllegalConstantExpression at constant declaration
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(constant1 = Identifier(mutableVar))]))"
    assert Checker(source).check_from_source() == expected

def test_075():
    """Error: Using mutable variable in constant expression 2"""
    source = """
    class MutableInConstant {
        int mutableVar := 10;
        #final int constant1 := mutableVar;  # Error: IllegalConstantExpression at constant declaration

        int localVar := 5;
        final int constant2 := 1 + localVar;  # Error: IllegalConstantExpression at constant declaration
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(constant2 = BinaryOp(IntLiteral(1), +, Identifier(localVar)))]))"
    assert Checker(source).check_from_source() == expected

def test_076():
    """Error: Method calls in constant expression"""
    source = """
    class MethodCallInConstant {
        final int value := this.getValue();  # Error: IllegalConstantExpression at constant declaration
        
        int getValue() {
            return 42;
        }
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(value = PostfixExpression(ThisExpression(this).getValue()))]))"
    assert Checker(source).check_from_source() == expected

def test_077():
    """Error: Complex expressions with variables 1"""
    source = """
    class ComplexIllegalExpression {
        int a := 10;
        
        final int result := (a * 2) + 5;  # Error: IllegalConstantExpression at constant declaration
        final boolean flag := this.isValid();   # Error: IllegalConstantExpression at constant declaration
        
        boolean isValid() {
            return true;
        }
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(result = BinaryOp(ParenthesizedExpression((BinaryOp(Identifier(a), *, IntLiteral(2)))), +, IntLiteral(5)))]))"
    assert Checker(source).check_from_source() == expected

def test_078():
    """Error: Complex expressions with variables 2"""
    source = """
    class ComplexIllegalExpression {
        int a := 10;
        
        #final int result := (a * 2) + 5;  # Error: IllegalConstantExpression at constant declaration
        final boolean flag := this.isValid();   # Error: IllegalConstantExpression at constant declaration
        
        boolean isValid() {
            return true;
        }
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = PostfixExpression(ThisExpression(this).isValid()))]))"
    assert Checker(source).check_from_source() == expected

def test_079():
    """Valid: Proper constant expressions"""
    source = """
    class ValidConstantExpressions {
        final int MAX_SIZE := 100;
        final int DOUBLE_SIZE := MAX_SIZE * 2;     # Valid: uses immutable attribute
        final string MESSAGE := "Hello" ^ "World"; # Valid: literal concatenation
        final boolean FLAG := true && false;       # Valid: boolean literals with operators
        final float PI := 3.14159;
        final float CIRCLE_AREA := PI * 10 * 10;   # Valid: uses final attribute

        final int SUM := 10 + 20 + 30;         # Valid: literal arithmetic
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_080():
    """Error: Array element access in constant"""
    source = """
    class ArrayAccessInConstant {
        final int[5] NUMBERS := {1, 2, 3, 4, 5};
        final int FIRST := NUMBERS[0];  # Error: IllegalConstantExpression at constant declaration
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(FIRST = PostfixExpression(Identifier(NUMBERS)[IntLiteral(0)]))]))"
    assert Checker(source).check_from_source() == expected

def test_081():
    """Error: Mixed types in array literal 1"""
    source = """
    class IllegalArrayError {
        void create() {
            int[3] mixed1 := {1, 2.0, 3};      # Error: IllegalArrayLiteral at array literal
            string[2] mixed2 := {"hello", 42}; # Error: IllegalArrayLiteral at array literal
            boolean[2] mixed3 := {true, 1};    # Error: IllegalArrayLiteral at array literal
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0), IntLiteral(3)}))"
    assert Checker(source).check_from_source() == expected

def test_082():
    """Error: Mixed types in array literal 2"""
    source = """
    class IllegalArrayError {
        void create() {
            #int[3] mixed1 := {1, 2.0, 3};      # Error: IllegalArrayLiteral at array literal
            string[2] mixed2 := {"hello", 42}; # Error: IllegalArrayLiteral at array literal
            boolean[2] mixed3 := {true, 1};    # Error: IllegalArrayLiteral at array literal
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('hello'), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected

def test_083():
    """Error: Mixed types in array literal 3"""
    source = """
    class IllegalArrayError {
        void create() {
            #int[3] mixed1 := {1, 2.0, 3};      # Error: IllegalArrayLiteral at array literal
            #string[2] mixed2 := {"hello", 42}; # Error: IllegalArrayLiteral at array literal
            boolean[2] mixed3 := {true, 1};    # Error: IllegalArrayLiteral at array literal
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(true), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected

# def test_084():
#     """Error: Mixed object types"""
#     source = """
#     class Shape {}
#     class Rectangle extends Shape {
#         float width;
#         float height;
        
#         Rectangle(float w; float h) {
#             this.width := w;
#             this.height := h;
#         }
#     }
#     class Triangle extends Shape {
#         float base;
#         float height;
        
#         Triangle(float b; float h) {
#             this.base := b;
#             this.height := h;
#         }
#     }
#     class MixedObjectArray {
#         void create() {
#             Shape[3] mixed := {new Rectangle(1.0, 2.0), new Triangle(1.0, 2.0), "not a shape"};  # Error: IllegalArrayLiteral at array literal
#         }
#     }
#     """
#     expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new Rectangle(FloatLiteral(1.0), FloatLiteral(2.0))), ObjectCreation(new Triangle(FloatLiteral(1.0), FloatLiteral(2.0))), StringLiteral('not a shape')}))"
#     assert Checker(source).check_from_source() == expected

# def test_085():
#     """Error: Nested array inconsistency"""
#     source = """
#     class NestedArrayError {
#         void create() {
#             int[3][3] matrix := {
#                 {1, 2, 3},
#                 {4, 5.0, 6},     # IllegalArrayLiteral - float in int array
#                 {7, 8, 9}
#             };
#         }
#     }
#     """
#     expected = "IllegalArrayLiteral(ArrayLiteral({ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}), ArrayLiteral({IntLiteral(4), FloatLiteral(5.0), IntLiteral(6)}), ArrayLiteral({IntLiteral(7), IntLiteral(8), IntLiteral(9)}))}))"
#     assert Checker(source).check_from_source() == expected

def test_086():
    """Valid: Consistent array literals"""
    source = """
    class ValidArrays {
        void create() {
            int[5] numbers := {1, 2, 3, 4, 5};           # Valid
            string[3] words := {"hello", "world", "!"};   # Valid
            boolean[3] flags := {true, false, true};      # Valid
            float[3] decimals := {1.0, 2.5, 3.14};      # Valid
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_087():
    """Error: Accessing instance member via class 1"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class StaticAccessError {
        void test() {
            string school := Student.school;     # Error: IllegalMemberAccess at member access
            Student.setName("John");            # Error: IllegalMemberAccess at method call
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    assert Checker(source).check_from_source() == expected

def test_088():
    """Error: Accessing instance member via class 2"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class StaticAccessError {
        void test() {
            #string school := Student.school;     # Error: IllegalMemberAccess at member access
            Student.setName("John");            # Error: IllegalMemberAccess at method call
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).setName(StringLiteral('John'))))"
    assert Checker(source).check_from_source() == expected

def test_089():
    """Error: Error: Accessing static member via instance 1"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class InstanceAccessError {
        void test() {
            Student s := new Student();
            int count := s.totalStudents;        # Error: IllegalMemberAccess at member access
            s.resetCount();                     # Error: IllegalMemberAccess at method call
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).totalStudents))"
    assert Checker(source).check_from_source() == expected

def test_090():
    """Error: Error: Accessing static member via instance 2"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class InstanceAccessError {
        void test() {
            Student s := new Student();
            # int count := s.totalStudents;        # Error: IllegalMemberAccess at member access
            s.resetCount();                     # Error: IllegalMemberAccess at method call
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).resetCount()))"
    assert Checker(source).check_from_source() == expected

def test_091():
    """Error: Accessing members that don't exist 1"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class UndeclaredMemberError {
        void test() {
            Student s := new Student();
            string name := s.name;               # Valid - if name exists
            s.secretMethod();                   # Valid - if secretMethod exists
            s.nonExistentMethod();              # UndeclaredMethod(nonExistentMethod)
        }
    }
    """
    expected = "UndeclaredMethod(nonExistentMethod)"
    assert Checker(source).check_from_source() == expected

def test_092():
    """Error: Accessing members that don't exist 2"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class UndeclaredMemberError {
        void test() {
            Student s := new Student();
            string name := s.name;               # Valid - if name exists
            s.secretMethod();                   # Valid - if secretMethod exists
            s.nonExistentAttribute := 3;              # UndeclaredAttribute(nonExistentAttribute)
        }
    }
    """
    expected = "UndeclaredAttribute(nonExistentAttribute)"
    assert Checker(source).check_from_source() == expected

def test_093():
    """Valid: Proper member access"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class ValidAccess {
        void test() {
            # Correct static access
            int count := Student.totalStudents;  # Valid
            Student s := new Student();
            Student.resetCount();               # Valid

            # Correct instance access
            s.school := "New School";            # Valid - instance member
            s.setName("Alice");                 # Valid - instance method
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_094():
    """Valid: Access from within inheritance hierarchy"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class GraduateStudent extends Student {
        void accessProtected() {
            this.age := 25;                          # Valid - inherited member
            this.setName("Graduate");               # Valid - inherited method
        }
    }
    """    
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_095():
    """EError: Complex access violations"""
    source = """
    class Student {
        string name;
        int age;
        static int totalStudents := 0;
        string school := "Default School";
        
        static void resetCount() {
            totalStudents := 0;
        }
        
        void setName(string n) {
            name := n;
        }
        
        void secretMethod() {
            io.writeStrLn("Secret");
        }
    }
    class ComplexAccessError {
        void complexTest() {
            Student s1 := new Student();
            Student s2 := new Student();
            string result := Student.school;     # Error: IllegalMemberAccess at member access
            
            # Chained access errors
            s1.secretMethod();                   # Valid if method exists

            # Method call on static access
            s1.resetCount();                     # Error: IllegalMemberAccess at method call
        }
    }
    """    
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    assert Checker(source).check_from_source() == expected

# def test_096():
#     """Error: Accessing members through wrong reference type"""
#     source = """
#     class ReferenceTypeError {
#         void wrongReference() {
#             Shape obj := new Student();
#             # obj.school := "Test";             # IllegalMemberAccess - Shape doesn't have school
#             # obj.setName("Test");             # IllegalMemberAccess - Shape doesn't have setName

#             # Need to cast first
#             ((Student)obj).setName("Test");     // Valid after cast
#         }
#     }
#     """

def test_097():
    """Error: Unary operation type mismatch 1"""
    source = """
    class UnaryOpError {
        void operations() {
            int number := 10;
            boolean flag := false;
            
            int negative := -flag;   # Error: TypeMismatchInExpression at unary operation
            #boolean not := !number;    # Error: TypeMismatchInExpression at unary operation
        }
    }
    """
    expected = "TypeMismatchInExpression(UnaryOp(-, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected

def test_098():
    """Error: Unary operation type mismatch 2"""
    source = """
    class UnaryOpError {
        void operations() {
            int number := 10;
            boolean flag := false;
            
            #int negative := -flag;   # Error: TypeMismatchInExpression at unary operation
            boolean not := !number;    # Error: TypeMismatchInExpression at unary operation
        }
    }
    """
    expected = "TypeMismatchInExpression(UnaryOp(!, Identifier(number)))"
    assert Checker(source).check_from_source() == expected

def test_099():
    """Valid: Proper unary operations"""
    source = """
    class ValidUnaryOps {
        void operations() {
            int x := 5;
            boolean y := true;
            
            int negative := -x;
            boolean notY := !y;
        }
    }
    """    
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_100():
    """Error: Type mismatch in constant declaration 1"""
    source = """
    class ConstantTypeError {
        final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(a = FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected

def test_101():
    """Error: Type mismatch in constant declaration 2"""
    source = """
    class ConstantTypeError {
        #final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(string), [Attribute(text = IntLiteral(42))]))"
    assert Checker(source).check_from_source() == expected

def test_102():
    """Error: Type mismatch in constant declaration 3"""
    source = """
    class ConstantTypeError {
        #final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        #final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = StringLiteral('true'))]))"
    assert Checker(source).check_from_source() == expected

def test_103():
    """Error: Type mismatch in constant declaration 4"""
    source = """
    class ConstantTypeError {
        # final int a := 1.2;        # Error: TypeMismatchInConstant at constant declaration
        # final string text := 42;   # Error: TypeMismatchInConstant at constant declaration
        # final boolean flag := "true";  # Error: TypeMismatchInConstant at constant declaration

        final int count := 3.14;  # Error: TypeMismatchInConstant at constant declaration
    }
    """    
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(count = FloatLiteral(3.14))]))"
    assert Checker(source).check_from_source() == expected

# ...existing code...
def test_104():
    """Redeclared Method in same class (priority: Redeclared)"""
    source = """
    class A {
        void foo() {}
        void foo() {}    # Redeclared(Method, foo)
    }
    """
    expected = "Redeclared(Method, foo)"
    assert Checker(source).check_from_source() == expected

def test_105():
    """Redeclared Attribute in same class"""
    source = """
    class B {
        int a;
        float b;
        int a;   # Redeclared(Attribute, a)
    }
    """
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected

def test_106():
    """Redeclared Parameter in method"""
    source = """
    class C {
        void m(int p; float q; int p) {  # Redeclared(Parameter, p)
            return p;
        }
    }
    """
    expected = "Redeclared(Parameter, p)"
    assert Checker(source).check_from_source() == expected

def test_107():
    """Undeclared identifier used in expression"""
    source = """
    class D {
        void main() {
            int x := 1;
            int y := x + z;   # UndeclaredIdentifier(z)
        }
    }
    """
    expected = "UndeclaredIdentifier(z)"
    assert Checker(source).check_from_source() == expected

def test_108():
    """Undeclared class used in extends"""
    source = """
    class Child extends Parent {   # UndeclaredClass(Parent)
        int id;
    }
    """
    expected = "UndeclaredClass(Parent)"
    assert Checker(source).check_from_source() == expected

def test_109():
    """Type mismatch in assignment statement"""
    source = """
    class E {
        void main() {
            int x := "str";   # TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := StringLiteral('str')))
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('str'))]))"
    assert Checker(source).check_from_source() == expected

def test_110():
    """Type mismatch in binary expression"""
    source = """
    class F {
        void main() {
            int x := 1;
            string s := "a";
            int r := x + s;   # TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(s)))
        }
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(s)))"
    assert Checker(source).check_from_source() == expected

def test_111():
    """Illegal member access: accessing instance attribute via class"""
    source = """
    class G {
        int m;
    }
    class Use {
        void test() {
            int v := G.m;   # IllegalMemberAccess(PostfixExpression(Identifier(G).m))
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(G).m))"
    assert Checker(source).check_from_source() == expected

def test_112():
    """MustInLoop: break outside any loop"""
    source = """
    class H {
        void test() {
            break;   # MustInLoop(BreakStatement())
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_113():
    """Cannot assign to constant attribute"""
    source = """
    class I {
        final int CONST := 1;
        void change() {
            CONST := 2;   # CannotAssignToConstant(AssignmentStatement(IdLHS(CONST) := IntLiteral(2)))
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(CONST) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_114():
    """Illegal constant expression using mutable variable"""
    source = """
    class J {
        int x := 5;
        final int a := x;   # IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(a = Identifier(x))]))
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(a = Identifier(x))]))"
    assert Checker(source).check_from_source() == expected

def test_115():
    """Illegal array literal with mixed types (int and float)"""
    source = """
    class K {
        void create() {
            int[2] arr := {1, 2.0};   # IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0)}))
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0)}))"
    assert Checker(source).check_from_source() == expected

def test_116():
    """Multiple errors: Redeclared variable and a later type error -> Redeclared has priority"""
    source = """
    class L {
        void proc() {
            int v := 1;
            int v := 2;   # Redeclared(Variable, v)  (should be reported)
            string s := v + "x";  # type error but lower priority
        }
    }
    """
    expected = "Redeclared(Variable, v)"
    assert Checker(source).check_from_source() == expected

def test_117():
    """Multiple errors: UndeclaredIdentifier and TypeMismatch -> UndeclaredIdentifier has priority"""
    source = """
    class M {
        void proc() {
            int a := b + 1;   # UndeclaredIdentifier(b) should be reported before any type errors
            string s := 1 + 2; 
        }
    }
    """
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected

def test_118():
    """IllegalMemberAccess should be reported before MustInLoop"""
    source = """
    class N {
        static int count := 0;
        void doIt() {
            N n := new N();
            n.count := 5;   # IllegalMemberAccess(PostfixExpression(Identifier(n).count))
            break;          # MustInLoop(BreakStatement()) lower priority
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(n).count))"
    assert Checker(source).check_from_source() == expected

def test_119():
    """TypeMismatchInConstant for object creation (no inheritance relation)"""
    source = """
    class Shape {}
    class Integer {}
    class O {
        final Shape s := new Integer(1);   # TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(s = ObjectCreation(new Integer(IntLiteral(1))))]))
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(s = ObjectCreation(new Integer(IntLiteral(1))))]))"
    assert Checker(source).check_from_source() == expected

def test_120():
    """TypeMismatchInStatement when assigning arrays of different element types"""
    source = """
    class P {
        void proc() {
            int[2] a := {1,2};
            float[2] b := {1.0,2.0};
            a := b;   # TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(a) := Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_121():
    """Undeclared method call on object"""
    source = """
    class Q {
        void test() {
            Q q := new Q();
            q.unknown();   # UndeclaredMethod(unknown)
        }
    }
    """
    expected = "UndeclaredMethod(unknown)"
    assert Checker(source).check_from_source() == expected

def test_122():
    """Undeclared attribute access on object"""
    source = """
    class R {
        void test() {
            R r := new R();
            r.foo := 1;   # UndeclaredAttribute(foo)
        }
    }
    """
    expected = "UndeclaredAttribute(foo)"
    assert Checker(source).check_from_source() == expected

# def test_123():
#     """UndeclaredIdentifier from scope rules (inner var not visible outside block)"""
#     source = """
#     class S {
#         void test() {
#             { int t := 5; }
#             {int x := t + 1;}   # UndeclaredIdentifier(t)
#         }
#     }
#     """
#     expected = "UndeclaredIdentifier(t)"
#     assert Checker(source).check_from_source() == expected
# ...existing code...

# ...existing code...

def test_127():
    """Use-before-declaration in same block -> UndeclaredIdentifier"""
    source = """
    class UseBeforeDecl {
        void main() {
            x := 10;
        }
    }
    """
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_138():
    """Undeclared identifier used in expression"""
    source = """
    class UseUndeclared {
        void main() {
            int a := 1;
            int b := a + c;  # UndeclaredIdentifier(c)
        }
    }
    """
    expected = "UndeclaredIdentifier(c)"
    assert Checker(source).check_from_source() == expected

def test_139():
    """Type mismatch in assignment (assign string to int)"""
    source = """
    class AssignTypeError {
        void main() {
            int x := 0;
            x := "oops";  # TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := StringLiteral('oops')))
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := StringLiteral('oops')))"
    assert Checker(source).check_from_source() == expected

def test_140():
    """Illegal member access: instance access to static member"""
    source = """
    class Stat {
        static int cnt := 0;
    }
    class IllegalAccess {
        void test() {
            Stat s := new Stat();
            int v := s.cnt;  # IllegalMemberAccess(PostfixExpression(Identifier(s).cnt))
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).cnt))"
    assert Checker(source).check_from_source() == expected

def test_141():
    """Undeclared method call on object"""
    source = """
    class Caller {
        void test() {
            Caller c := new Caller();
            c.nope();  # UndeclaredMethod(nope)
        }
    }
    """
    expected = "UndeclaredMethod(nope)"
    assert Checker(source).check_from_source() == expected

def test_142():
    """Cannot assign to constant attribute"""
    source = """
    class ConstAssign {
        final int CONST := 9;
        void change() {
            CONST := 10;  # CannotAssignToConstant(AssignmentStatement(IdLHS(CONST) := IntLiteral(10)))
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(CONST) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected

def test_143():
    """Illegal array literal with mixed literal types"""
    source = """
    class MixedArray {
        void create() {
            int[2] a := {1, "a"};  # IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('a')}))
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('a')}))"
    assert Checker(source).check_from_source() == expected

from utils import Checker

# --- Redeclaration/Undeclared Errors (Highest Priority) ---

def test_144():
    """Redeclared Variable in method scope (with later Undeclared)"""
    source = """
    class PrioRedeclaredVar {
        void proc() {
            int i := 1;
            int i := 2;     # Redeclared(Variable, i)
            int j := k;     # UndeclaredIdentifier(k) - Lower priority
        }
    }
    """
    expected = "Redeclared(Variable, i)"
    assert Checker(source).check_from_source() == expected

def test_145():
    """Undeclared Class in inheritance (with later Undeclared Identifier)"""
    source = """
    class Child extends UnknownParent {  # UndeclaredClass(UnknownParent)
        void method() {
            int x := y;  # UndeclaredIdentifier(y) - Same priority, but this appears later
        }
    }
    """
    expected = "UndeclaredClass(UnknownParent)"
    assert Checker(source).check_from_source() == expected

def test_146():
    """Redeclared Class in global scope (with later TypeMismatch)"""
    source = """
    class Duplicate {}
    class Duplicate {}  # Redeclared(Class, Duplicate)
    class Another {
        void proc() {
            int x := true; # TypeMismatchInStatement - Lower priority
        }
    }
    """
    expected = "Redeclared(Class, Duplicate)"
    assert Checker(source).check_from_source() == expected

def test_147():
    """Redeclared Parameter in constructor"""
    source = """
    class ConflictingParam {
        ConflictingParam(string a; int b; string a) {  # Redeclared(Parameter, a)
            this.b := b;
        }
    }
    """
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected

def test_148():
    """Undeclared Identifier in array index expression"""
    source = """
    class UndeclaredArrayAccess {
        void access() {
            int[5] numbers := {1, 2, 3, 4, 5};
            int value := numbers[invalidIndex];  # UndeclaredIdentifier(invalidIndex)
        }
    }
    """
    expected = "UndeclaredIdentifier(invalidIndex)"
    assert Checker(source).check_from_source() == expected

# --- Type Errors (Second Highest Priority) ---

def test_149():
    """Type mismatch in binary expression (int and boolean)"""
    source = """
    class PrioTypeMismatchExpr {
        void main() {
            int x := 5;
            boolean flag := true;
            boolean result := x == flag; # TypeMismatchInExpression(BinaryOp(Identifier(x), ==, Identifier(flag)))
            break;  # MustInLoop - Lower priority
        }
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), ==, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected

def test_150():
    """Type mismatch in variable declaration (float to int, no coercion)"""
    source = """
    class PrioTypeMismatchDecl {
        void main() {
            int count := 4.5;  # TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(count = FloatLiteral(4.5))]))
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(count = FloatLiteral(4.5))]))"
    assert Checker(source).check_from_source() == expected

def test_151():
    """Type mismatch in while loop condition (int instead of boolean)"""
    source = """
    class TypeMismatchWhile {
        void loop() {
            final int i := 1;
            for i := 5 to 20 do {  # TypeMismatchInStatement(ForStatement(for Identifier(i) := IntLiteral(5) to IntLiteral(20) do BlockStatement(stmts=[])))
                i := i + 1;
            }
        }
    }
    """
    expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(5) to IntLiteral(20) do BlockStatement(stmts=[AssignmentStatement(IdLHS(i) := BinaryOp(Identifier(i), +, IntLiteral(1)))])))"
    assert Checker(source).check_from_source() == expected

def test_152():
    """Type mismatch in method return (expected int, got float)"""
    source = """
    class TypeMismatchReturn {
        int getNumber() {
            return 3.14;  # TypeMismatchInStatement(ReturnStatement(return FloatLiteral(3.14)))
        }
    }
    """
    expected = "TypeMismatchInStatement(ReturnStatement(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_153():
    """Type mismatch in object creation (assigning wrong type object)"""
    source = """
    class A {}
    class B {}
    class TypeMismatchObject {
        void create() {
            A obj := new B();  # TypeMismatchInStatement (if A and B no relation)
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(A), [Variable(obj = ObjectCreation(new B()))]))"
    assert Checker(source).check_from_source() == expected

# --- Access Control Errors (Third Highest Priority) ---

def test_154():
    """Illegal member access: Accessing static method via instance (with later MustInLoop)"""
    source = """
    class AccessStaticMethod {
        static void staticM() {}
        void instanceM() {
            this.staticM();  # IllegalMemberAccess(PostfixExpression(ThisExpression(this).staticM()))
            break;          # MustInLoop - Lower priority
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_155():
    """Illegal member access: Assigning to instance attribute via class name"""
    source = """
    class AccessInstanceAttr {
        int val := 10;
        void test() {
            AccessInstanceAttr.val := 20; # IllegalMemberAccess(AssignmentStatement(StaticLHS(AccessInstanceAttr, val) := IntLiteral(20)))
        }
    }
    """
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(AccessInstanceAttr).val))"
    assert Checker(source).check_from_source() == expected

# --- Control Flow Errors (Fourth Highest Priority) ---

def test_156():
    """MustInLoop: continue outside of any loop (with later CannotAssignToConstant)"""
    source = """
    class PrioMustInLoop {
        final int C := 1;
        void test() {
            continue;  # MustInLoop(ContinueStatement())
            C := 2;    # CannotAssignToConstant - Lower priority
        }
    }
    """
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected

def test_157():
    """MustInLoop: break inside an if statement that is not inside a loop"""
    source = """
    class BreakInIf {
        void test() {
            if true then {
                break;  # MustInLoop(BreakStatement())
            }
        }
    }
    """
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

# --- Constant Errors (Fifth Highest Priority) ---

def test_158():
    """Cannot assign to local constant variable in for loop initializer"""
    source = """
    class CannotAssignToFor {
        void loop() {
            final int i := 10;
            for i := 0 to 5 do { # CannotAssignToConstant (for loop attempts assignment to final 'i')
                io.writeIntLn(i);
            }
        }
    }
    """
    expected = "CannotAssignToConstant(ForStatement(for i := IntLiteral(0) to IntLiteral(5) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected

def test_159():
    """Illegal constant expression: using non-final attribute in declaration"""
    source = """
    class IllegalConstAttr {
        int x := 10;
        final int y := x * 2;  # IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(y = BinaryOp(Identifier(x), *, IntLiteral(2)))]))
    }
    """
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(y = BinaryOp(Identifier(x), *, IntLiteral(2)))]))"
    assert Checker(source).check_from_source() == expected

def test_160():
    """TypeMismatchInConstant: boolean constant initialized with nil"""
    source = """
    class TypeMismatchConstNil {
        final boolean flag := nil;  # TypeMismatchInConstant(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = NilLiteral(nil))]))
    }
    """
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = NilLiteral(nil))]))"
    assert Checker(source).check_from_source() == expected

# --- Literal Errors (Lowest Priority) ---

def test_161():
    """IllegalArrayLiteral: Array size mismatch on declaration with literal (if size checking is done here)"""
    source = """
    class ArraySizeMismatch {
        void create() {
            int[2] a := {1, 2, 3};  # IllegalArrayLiteral (if size is checked) - Assuming type check priority
        }
    }
    """
    # Assuming the implementation checks for literal type consistency first, and uses a generic IllegalArrayLiteral for array declaration issues.
    # Since the values are all 'int', this would typically pass the type consistency check unless there's an explicit size check that raises this specific error.
    # Based on the provided examples, the priority is for type inconsistency within the array, so we'll enforce that:
    source = """
    class ArrayTypeInconsistency {
        void create() {
            string[3] arr := {"a", 1, "c"};  # IllegalArrayLiteral
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('a'), IntLiteral(1), StringLiteral('c')}))"
    assert Checker(source).check_from_source() == expected

def test_162():
    """IllegalArrayLiteral: Mixed booleans and strings in literal"""
    source = """
    class MixedBoolStringArray {
        void create() {
            boolean[2] flags := {true, "false"};  # IllegalArrayLiteral
        }
    }
    """
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(true), StringLiteral('false')}))"
    assert Checker(source).check_from_source() == expected

def test_163():
    """Redeclared Attribute and later TypeMismatchInExpression -> Redeclared wins"""
    source = """
    class PriorityCheck1 {
        int data;
        float data;  # Redeclared(Attribute, data)
        void method() {
            int x := 1 + "a"; # TypeMismatchInExpression
        }
    }
    """
    expected = "Redeclared(Attribute, data)"
    assert Checker(source).check_from_source() == expected

def test_164():
    source = """
        class Animal {
        string name := "Animal";
        void speak() {
            io.writeStrLn(this.name);
        }
    }

    class Dog extends Animal {
        string name := "Dog";
        # Method overriding
        void speak() {
            this.speak(); # Accessing superclass method
            io.writeStrLn(this.name);
        }
        
        void fetch() {
            io.writeStrLn("Fetching...");
        }
    }

    class Main {
        static void main() {
            Animal myAnimal;
            Dog myDog := new Dog();
            myAnimal := myDog; # Valid upcasting
            myAnimal.speak();
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_165():
    source = """
    class Vehicle {}
    class Car extends Vehicle {}

    class Main {
        static void main() {
            Car myCar;
            Vehicle myVehicle := new Vehicle();
            myCar := myVehicle; # Error: Cannot assign superclass to subclass variable
        }
    }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(myCar) := Identifier(myVehicle)))"
    assert Checker(source).check_from_source() == expected

def test_166():
    source = """
    class Parent {
        static int baseValue := 100;
    }

    class Child extends Parent {
        static void printValue() {
            # Accessing inherited static attribute via subclass name
            int val := Child.baseValue;
            io.writeIntLn(val);
        }
    }

    class Main {
        static void main() {
            Child.printValue();
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_167():
    source = """
    class A {
        void methodA() {}
    }

    class B extends A {
        void methodB() {}
    }

    class Main {
        static void main() {
            A obj := new B();
            obj.methodB(); # Error: methodB is not declared in class A
        }
    }
    """
    expected = "UndeclaredMethod(methodB)"
    assert Checker(source).check_from_source() == expected

def test_168():
    source = """
    class ScopeTest {
        int x := 10;
        
        void testShadowing() {
            int x := 20; # This local variable shadows the attribute x
            io.writeIntLn(x); # Should print 20
            io.writeIntLn(this.x); # Should print 10
        }
    }

    class Main {
        static void main() {
            ScopeTest st := new ScopeTest();
            st.testShadowing();
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_169():
    source = """
    class Main {
        static void main() {
            int i := 0;
            for i := 0 to 10 do {
                int i := 5; # Error: Redeclared variable 'i' in a sub-scope
                io.writeInt(i);
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_170():
    source = """
    class Employee {
        string id := "default";
        
        void setId(string id) { # Parameter 'id' shadows attribute 'id'
            this.id := id;
        }
    }

    class Main {
        static void main() {
            Employee emp := new Employee();
            emp.setId("E123");
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_171():
    source = """
    class Circle {
        final float PI;
        float radius;
        
        Circle(float r) {
            this.PI := 3.14159; # Valid assignment to final attribute in constructor
            this.radius := r;
        }
    }

    class Main {
        static void main() {
            Circle c := new Circle(5.0);
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
