
from utils import Checker

def test_001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;  # valid usage
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
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected


def test_008():
    """Redeclared Class Student"""
    source = """
class Student {
    int id;
    string name;
}

class Student {  
    float grade;
}
"""
    expected = "Redeclared(Class, Student)"
    assert Checker(source).check_from_source() == expected

def test_009():
    """ Redeclared Attribute in same class """
    source = """ 
class Person {
    string name;
    int age;
    string name(){} 
}
"""
    expected = "Redeclared(Method, name)"
    assert Checker(source).check_from_source() == expected

def test_010():
    """ Redeclared Variable in method scope """
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

def test_011():
    """ Redeclared Parameter"""
    source = """ 
class Math {
    int calculate(int x; float y; int x) { 
        return x + y;
    }
}
"""
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_012():
    """ Redeclared Constant """
    source = """ 
class Constants {
    static final int MAX_SIZE := 100;
    static final int MAX_SIZE := 200;  
}
"""
    expected = "Redeclared(Constant, MAX_SIZE)"
    assert Checker(source).check_from_source() == expected

def test_013():
    """ Valid: Method overriding (inheritance) """
    source = """ 
class Animal {
    void makeSound() {
        io.writeStrLn("Some sound");
    }
}
class Dog extends Animal {
    void makeSound() { 
        io.writeStrLn("Woof!");
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_014():
    """ Valid: Shadowing in different scopes"""
    source = """ 
class ShadowExample {
    int value := 100;  
    
    void method() {
        int value := 200;  
        {
            int value := 300; 
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_015():
    """  """
    source = """
        class Outer {
            int a := 10;
            int a() {
            }
        }
        """
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected

def test_016():
    """  """
    source = """
        class Outer {
            int a := 10;
            void method() {
                int a := 20;
                int a := 30;
            }
        }
        """
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_017():
    """  """
    source = """
        class Outer {
            int a := 10;
            void method(int a; float b; float a) {
            }
        }
        """
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected

def test_018():
    """  """
    source = """
        class Outer {
            static final int A := 100;
            static final int A := 200;
        }
        """
    expected = "Redeclared(Constant, A)"
    assert Checker(source).check_from_source() == expected

def test_019():
    """  """
    source = """
        class A {
            A() {}
            A() {}
            }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected

def test_020():
    """  """
    source = """
        class A {
            ~A() {}
            ~A() {}
            }
    """
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected

def test_021():
    """  """
    source = """
        class A {
            void foo() {}
            ~foo() {}
            }
    """
    expected = "Redeclared(Destructor, foo)"
    assert Checker(source).check_from_source() == expected
def test_021b():
    """  """
    source = """
        class A {
            ~foo() {}
            }
    """
    expected = "TypeMismatchInStatement(DestructorDecl(~foo(), BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected
def test_021a():
    """  """
    source = """
        class A {
            void foo() {}
            foo() {}
            }
    """
    expected = "Redeclared(Constructor, foo)"
    assert Checker(source).check_from_source() == expected
def test_021c():
    """  """
    source = """
        class A {
            foo() {}
            }
    """
    expected = "TypeMismatchInStatement(ConstructorDecl(foo([]), BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected
def test_022():
    """  """
    source = """
        class A {
            void foo() {}
            A() {}
            int A() {}
            ~A() {}
            }
    """
    expected = "Redeclared(Method, A)"
    assert Checker(source).check_from_source() == expected

def test_023():
    """  """
    source = """
        class A {
            void foo() {}
            ~A() {}
            A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_024():
    """  """
    source = """
        class A {
            A() {}
            ~A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_025():
    """  """
    source = """
        class A {
            ~A() {}
            A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_026():
    """  """
    source = """
        class A {
            int A;
            A() {}
            }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected
def test_026a():
    """  """
    source = """
        class A {
            int A(){}
            A() {}
            }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected
def test_027():
    """  """
    source = """
        class A {
            A() {}
            int A;
            }
    """
    expected = "Redeclared(Attribute, A)"
    assert Checker(source).check_from_source() == expected
def test_027a():
    """  """
    source = """
        class A {
            A() {}
            int A(){}
            }
    """
    expected = "Redeclared(Method, A)"
    assert Checker(source).check_from_source() == expected
def test_028():
    """  """
    source = """
        class A {
            ~A() {}
            int A;
            }
    """
    expected = "Redeclared(Attribute, A)"
    assert Checker(source).check_from_source() == expected
def test_028a():
    """  """
    source = """
        class A {
            int A;
            ~A() {}
            }
    """
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected
def test_029():
    """  """
    source = """
        class A {
            int A() {}
            ~A() {}
            }
    """
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected
def test_029a():
    """  """
    source = """
        class A {
            int A(){}
            ~A() {}
            }
    """
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected
def test_030():
    """  """
    source = """
        class A {
            ~A() {}
            int A() {}
            }
    """
    expected = "Redeclared(Method, A)"
    assert Checker(source).check_from_source() == expected

def test_031():
    """  """
    source = """
        class A {
            int A;
            ~A() {}
            int A() {}
            }
    """
    expected = "Redeclared(Destructor, A)"
    assert Checker(source).check_from_source() == expected

def test_032():
    """  """
    source = """
        class A {
            int A;
            int x;
            }
        class B extends A {
            ~A() {}
            }
    """
    expected = "TypeMismatchInStatement(DestructorDecl(~A(), BlockStatement(stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_033():
    """  """
    source = """
        class A {
            int A;
            int x;
            }
        class B extends A {
            int A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_034():
    """  """
    source = """
        class A {
            final int A;
            final int A;
            int add (int x; int y) {
                float A;
            }
        }
    """
    expected = "Redeclared(Constant, A)"
    assert Checker(source).check_from_source() == expected

def test_035():
    """  """
    source = """
        class A {
            int A;
            int add (int x; int y) {
                int x;
                }
            }
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_036():
    """  """
    source = """
        class A {
            int add (int x) {
                    {
                        int x;
                    }
                }
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_037():
    """  """
    source = """
        class A {
            A(int x){
                int x;
            }
        }
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_038():
    """  """
    source = """
        class A {
            A(int x){
                final int x;
            }
        }
    """
    expected = "Redeclared(Constant, x)"
    assert Checker(source).check_from_source() == expected

def test_039():
    """  """
    source = """
        class A {
            A(int x){
                final int y;
                int y;
            }
        }
    """
    expected = "Redeclared(Variable, y)"
    assert Checker(source).check_from_source() == expected

def test_040():
    """  """
    source = """
        class A {
            A(int x; int x){
                final int y;
                final int y;
            }
        }
    """
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_041():
    """  """
    source = """
        class A {
            A(){}
            A(int x; int y){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_041a():
    """  """
    source = """
        class A {
            A(int x; float y){}
            A(int x; float y){}
        }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected
def test_041b():
    """  """
    source = """
        class A {
            A(int x; float y){}
            A(int a; float b){}
        }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected
def test_041c():
    """  """
    source = """
        class A {
            A(int x, y){}
            A(int x; int y){}
        }
    """
    expected = "Redeclared(Constructor, A)"
    assert Checker(source).check_from_source() == expected
def test_041d():
    """  """
    source = """
        class A {
            A(int x, y){}
            A(){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_041e():
    """  """
    source = """
        class A {
            A(int x; float y){}
            A(int x; int y){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_041f():
    """  """
    source = """
        class A {
            A(int x; float y){}
            A(int x, y){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_042():
    """  """
    source = """
        class A {
            A(){}
            A(int x; float y){}
            ~A(){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_043():
    """  """
    source = """
        class A {
            int x(int y){
            {
                {
                int y;
                }
            }
        }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_044():
    """  """
    source = """
        class A {
            int x(int y){
                int y;
        }
        }
    """
    expected = "Redeclared(Variable, y)"
    assert Checker(source).check_from_source() == expected

def test_045():
    """ Error: Undeclared Class """
    source = """
class Student extends Person {  
    int studentId;
}
"""
    expected = "UndeclaredClass(Person)" 
    assert Checker(source).check_from_source() == expected

def test_046():
    """ Error: Undeclared Attribute"""
    source= """
class Car {
    string brand;
    int year;
    
    void display() {
        io.writeStrLn(this.brand);
        io.writeIntLn(this.e);
        io.writeStrLn(model); 
    }
}
"""
    expected = "UndeclaredAttribute(e)"
    assert Checker(source).check_from_source() == expected

def test_047():
    """Error: Undeclared Method """ 
    source = """
class Calculator {
    int add(int a; int b) {
        return a + b;
    }
    
    void test() {
        int result := this.multiply(5, 3); 
    }
}
"""
    expected = "UndeclaredMethod(multiply)"
    assert Checker(source).check_from_source() == expected

def test_048():
    """ Error: Method called on wrong class"""
    source = """
class Calculator {
    int add(int a; int b) {
        return a + b;
    }
}

class MathUtils {
    static int factorial(int n) {
        if n <= 1 then return 1; else return n ;
    }
}

class Main {
    void run() {
        Calculator calc := new Calculator();
        int fact := calc.factorial(5);  
    }
}
"""
    expected = "UndeclaredMethod(factorial)"
    assert Checker(source).check_from_source() == expected

def test_049():
    """ Valid: Inherited member access"""
    source = """
class Animal {
    string species;
    
    void setSpecies(string s) {
        this.species := s;
    }
}

class Dog extends Animal {
    void identify() {
        io.writeStrLn(this.species);  
        this.setSpecies("Canine");  
    }
}
"""

    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_050():
    """ Error: Out of scope access """
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

def test_051():
    """ Valid: Accessing inherited attributes and methods """
    source = """
class Vehicle {
    string model;
}
class Car extends Vehicle {
    void displayInfo() {
        this.model := "Sedan";
        io.writeStrLn(this.model);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_052():
    """ Error: Accessing non-existent inherited member """
    source = """
class Vehicle {
    string model;
}
class Car extends Vehicle {
    void displayInfo() {
        this.year := 2020;
    }
}
"""
    expected = "UndeclaredAttribute(year)"
    assert Checker(source).check_from_source() == expected

def test_053():
    """ """
    source = """
class Parent {
    void greet() {
        io.writeStrLn("Hello from Parent");
    }
}
class Child extends Parent {
    void greet() {
        io.writeStrLn("Hello from Child");
    }
}
class GrandChild extends Child {
    void greet() {
        io.writeStrLn("Hello from GrandChild");
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Undeclared class """
    source = """
class A extends B {
    int x;
}
"""
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Undeclared attribute in inherited class"""
    source = """
class A {
    int x;
}
class B extends A {
    void foo() {
        io.writeIntLn(this.y);
    }
}
"""
    expected = "UndeclaredAttribute(y)"
    assert Checker(source).check_from_source() == expected

def test_056():
    """Undeclared method in inherited class"""
    source = """
class A {
    void foo() {
        io.writeStrLn("foo in A");
    }
}
class B extends A {
    void bar() {
        this.baz();
    }
}
"""
    expected = "UndeclaredMethod(baz)"
    assert Checker(source).check_from_source() == expected

def test_057():
    """Valid access to inherited members"""
    source = """
class A {
    int x;
    void foo() {
        io.writeIntLn(this.x);
    }
}
class B extends A {
    void bar() {
        this.foo();
        this.x := 10;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_058():
    """Valid multi-level inheritance"""
    source = """
class A {
    int x;
}
class B extends A {
    int y;
}
class C extends B {
    void display() {
        io.writeIntLn(this.x);
        io.writeIntLn(this.y);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Undeclared attribute in multi-level inheritance"""
    source = """
class A {
    int x;
}
class B extends A {
    int y;
}
class C extends B {
    void display() {
        io.writeIntLn(this.z);
    }
}
"""
    expected = "UndeclaredAttribute(z)"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Undeclared method in multi-level inheritance"""
    source = """
class A {
    void foo() {
        io.writeStrLn("foo in A");
    }
}
class B extends A {
    void bar() {
        this.baz();
    }
}
class C extends B {
    void qux() {
        this.baz();
    }
}
"""
    expected = "UndeclaredMethod(baz)"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Valid access to inherited members in multi-level inheritance"""
    source = """
class A {
    int x;
    void foo() {
        io.writeIntLn(this.x);
    }
}
class B extends A {
    int y;
    void bar() {
        this.foo();
        io.writeIntLn(this.y);
    }
}
class C extends B {
    void display() {
        this.bar();
        io.writeIntLn(this.x);
        io.writeIntLn(this.y);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Undeclared class in multi-level inheritance"""
    source = """
class A extends X {
    int x;
}
class B extends A {
    int y;
}
class C extends B {
    void display() {
        io.writeIntLn(this.x);
        io.writeIntLn(this.y);
    }
}
"""
    expected = "UndeclaredClass(X)"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Undeclared variable in method"""
    source = """
class Test {
    void method() {
        int x := 10;
        int y := x + z;
    }
}
"""
    expected = "UndeclaredIdentifier(z)"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Valid variable scopes in nested blocks"""
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int y := 20;
            {
                int z := x + y;
                io.writeIntLn(z);
            }
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Undeclared variable in nested block"""
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int y := 20;
            {
                int z := x + y + w;
                io.writeIntLn(z);
            }
        }
    }
}
"""
    expected = "UndeclaredIdentifier(w)"
    assert Checker(source).check_from_source() == expected

def test_066():
    """Variable shadowing in nested blocks"""
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int x := 20;
            {
                int y := x + 5;
                io.writeIntLn(y);
            }
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Undeclared class in variable declaration"""
    source = """
class Test { Animal animal := new Animal(); }
class Animal {}
"""
    expected = "UndeclaredClass(Animal)"
    assert Checker(source).check_from_source() == expected

def test_067a():
    source = """
    class Test { Animal animal; }
    class Animal {}
"""
    expected = "UndeclaredClass(Animal)"
    assert Checker(source).check_from_source() == expected
def test_068():
    """Valid variable usage across methods"""
    source = """
class Test {
    void method1() {
        int x := 10;
        this.method2(x);
    }
    int method2(int y) {
        io.writeIntLn(y);
        return y + 5;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_069():
    """Undeclared variable across methods"""
    source = """
class Test {
    void method1() {
        int x := 10;
        this.method2();
    }
    void method2() {
        io.writeIntLn(x);
    }
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Undeclared variable in attribute initialization"""
    source = """
class Test {
    int x := x + 1;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected

def test_071():
    """ """
    source = """
class Test {
void method() {
    int x := x + 1;
}
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected
    

def test_072():
    """ """
    source = """
class Test {
    int x := 10;
    void method() {
        int y := this.x + 5;
        io.writeIntLn(y);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_073():
    """ """
    source = """
class Test {
    void method() {
        int x := y;
        {
            int y := 20;}
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_074():
    """ """
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int y := x;
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_075():
    """ Error: Assignment to constant attribute """
    source = """ 
class Constants {
    final int MAX_COUNT := 100;
    
    void example() {
        this.MAX_COUNT := 200;  #Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).MAX_COUNT)) := IntLiteral(200)))"
    assert Checker(source).check_from_source() == expected  

def test_076():
    """ Assignment to constant attribute """
    source = """ 
class Configuration {
    final string APP_NAME := "MyApp";
    
    void updateConfig() {
        this.APP_NAME := "NewApp";  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).APP_NAME)) := StringLiteral('NewApp')))"
    assert Checker(source).check_from_source() == expected

def test_077():
    """ Assignment in for loop """
    source = """
class LoopExample {
    final int limit := 10;
    
    void process() {
        for limit := 0 to 20 do {  # Error: CannotAssignToConstant at for statement
            io.writeIntLn(this.limit);
        }
    }
}
"""
    expected = "UndeclaredIdentifier(limit)"
    assert Checker(source).check_from_source() == expected
def test_077a():
    """ Assignment in for loop """
    source = """
class LoopExample {
    void process() {
        final int limit := 10;
        for limit := 0 to 20 do {  # Error: CannotAssignToConstant at for statement
            io.writeIntLn(this.limit);
        }
    }
}
"""
    expected = "CannotAssignToConstant(ForStatement(for limit := IntLiteral(0) to IntLiteral(20) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(PostfixExpression(ThisExpression(this).limit))))])))"
    assert Checker(source).check_from_source() == expected
def test_078():
    """ Multiple assignment attempts """
    source = """
class MultipleAssignment {
    final float PI := 3.14159;
    
    void calculate() {
        this.PI := this.PI * 2;  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).PI)) := BinaryOp(PostfixExpression(ThisExpression(this).PI), *, IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected

def test_079():
    """ Proper constant usage """
    source = """
class ValidConstants {
    final int MAX_SIZE := 1000;
    final string VERSION;
    
    ValidConstants(string version) {
        VERSION := version;  # Valid: initialization in constructor
    }
    
    void display() {
        io.writeStrLn(this.VERSION);  # Valid: reading constant
        io.writeIntLn(this.MAX_SIZE);
    }
}
"""
    expected = "UndeclaredIdentifier(VERSION)"
    assert Checker(source).check_from_source() == expected
def test_079a():
    """ Proper constant usage """
    source = """
class ValidConstants {
    final int MAX_SIZE := 1000;
    final string VERSION;
    
    ValidConstants(string version) {
        this.VERSION := version;  # Valid: initialization in constructor
    }
    
    void display() {
        io.writeStrLn(this.VERSION);  # Valid: reading constant
        io.writeIntLn(this.MAX_SIZE);
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).VERSION)) := Identifier(version)))"
    assert Checker(source).check_from_source() == expected
def test_080():
    """ Constant initialization outside constructor """
    source = """
class InvalidConstants {
    final int MAX_SIZE := 1000;
    final string VERSION := "1.0"; 
    
    InvalidConstants(string version) {
    }
    void display() {
        io.writeStrLn(this.VERSION);
        io.writeIntLn(this.MAX_SIZE);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_081():
    source = """
class Test {
    void method() {
        final int x := 10;
        x := 20;  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(20)))"
    assert Checker(source).check_from_source() == expected

def test_082():
    source = """
class Test {
    void method() {
        final string msg := "Hello";
        msg := "World";  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(msg) := StringLiteral('World')))"
    assert Checker(source).check_from_source() == expected

def test_083():
    source = """
    class Test{
        final int CONST_VAL;
        Test(){
            this.CONST_VAL := 1;  # Valid: initialization in constructor
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).CONST_VAL)) := IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_084():
    source = """
    class Test{
        final int CONST_VAL;
        Test(){
        }
        void method(){
            this.CONST_VAL := 2;  # Error: CannotAssignToConstant at assignment statement
        }
    }
    """
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).CONST_VAL)) := IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_085():
    source = """
class Test {
    void method() {
        final float PI := 3.14;
        PI := 3.14159;  # Error: CannotAssignToConstant at assignment statement
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(PI) := FloatLiteral(3.14159)))"
    assert Checker(source).check_from_source() == expected

def test_086():
    source = """
class Test {
    void method() {
        final boolean FLAG := true;
        if FLAG then {
            FLAG := false;  # Error: CannotAssignToConstant at assignment statement
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(FLAG) := BoolLiteral(False)))"
    assert Checker(source).check_from_source() == expected

def test_087():
    source = """
class Test {
    void method() {
        final int LIMIT := 100;
        int i;
        for i := 0 to 50 do { 
            LIMIT := LIMIT - 1;
        }
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(LIMIT) := BinaryOp(Identifier(LIMIT), -, IntLiteral(1))))"
    assert Checker(source).check_from_source() == expected

def test_088():
    source = """
class Test{
void method(){
    for i := 0 to 10 do {
        io.writeIntLn(i);
    }
}
}
"""
    expected = "UndeclaredIdentifier(i)"
    assert Checker(source).check_from_source() == expected

def test_089():
    source = """
class Test{
void method(){
    int i ;
    for i := 0 to 10 do {
        z := i * 2;
    }
}
}
"""
    expected = "UndeclaredIdentifier(z)"
    assert Checker(source).check_from_source() == expected

def test_090():
    source = """
class Test{
void method(){
    int i ;
    for i := 0 to 10 do {
        int i ;
        i := i + 1;
    }
}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected



def test_091():
    """Non-boolean condition in if statement"""
    source = """
class ConditionalError {
void check() {
    int x := 5;
    string message := "hello";
    if x then {  
        io.writeStrLn("Invalid");
    }
    
    if message then { 
        io.writeStrLn("Invalid");
    }
}
}
    """
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(x) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Invalid'))))])))"
    assert Checker(source).check_from_source() == expected

def test_092():
    """"""
    source = """
class ConditionalError {
void check() {
    string message := "hello";
    if message then { 
        io.writeStrLn("Invalid");
    }
}
}
    """
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(message) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Invalid'))))])))"
    assert Checker(source).check_from_source() == expected

def test_093():
    """Valid boolean conditions in if statements"""
    source = """
class Conditional
{
void check() {
    boolean flag := true;
    if flag then {  
        io.writeStrLn("Valid");
    }
    
    if !flag then { 
        io.writeStrLn("Also Valid");
    }
}
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_094():
    """Valid boolean conditions in if-else statements"""
    source = """
class Conditional
{
void check() {
    boolean flag := false;
    if flag then {  
        io.writeStrLn("Valid");
    } else {
        io.writeStrLn("Else Valid");
    }
}
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_095():
    """Valid relational conditions in if statements"""
    source = """
class Conditional
{  
void check() {
    int x := 10;
    if x > 5 then {  
        io.writeStrLn("Valid");
    } else {
        io.writeStrLn("Also Valid");
    }
}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_095a():
    """Valid relational conditions in if statements"""
    source = """
class Conditional
{  
void check() {
    int x := 10;
    if (x > 5) && (true) then {  
        io.writeStrLn("Valid");
    } else {
        io.writeStrLn("Also Valid");
    }
}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_096():
    """Non-boolean condition in if statement with relational operator"""
    source = """
class Conditional
{
void check() {
    string message := "hello";
    if message > "a" then {  
        io.writeStrLn("Invalid");
    }
}
}
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(message), >, StringLiteral('a')))"
    assert Checker(source).check_from_source() == expected
def test_097():
    """Valid logical conditions in if statements"""
    source = """
class Conditional
{
void check() {
    boolean flag1 := true;
    boolean flag2 := false;
    if flag1 && !flag2 then {  
        io.writeStrLn("Valid");
    }
}
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_098():
    """Non-boolean condition in if statement with logical operator"""
    source = """
class Conditional
{
void check() {
    int x := 10;
    boolean flag := true;
    if x && flag then {  
        io.writeStrLn("Invalid");
    }
}
}
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), &&, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected
def test_099():
    """Valid nested if statements with boolean conditions"""
    source = """
class Conditional
{
void check() {
    boolean outerFlag := true;
    boolean innerFlag := false;
    if outerFlag then {  
        if !innerFlag then {
            io.writeStrLn("Valid Nested");
        }
    }
}
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_100():
    """Non-boolean condition in nested if statement"""
    source = """
class Conditional
{
void check() {
    boolean outerFlag := true;
    int innerValue := 5;
    if outerFlag then {  
        if innerValue then {
            io.writeStrLn("Invalid Nested");
        }
    }
}
}
    """
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(innerValue) then BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeStrLn(StringLiteral('Invalid Nested'))))])))"
    assert Checker(source).check_from_source() == expected
def test_101():
    source = """
    class ForLoopError {
    void loop() {
        float f := 1.5;
        boolean condition := true;
        
        for f := 0 to 10 do { 
            io.writeFloatLn(f);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeFloatLn(Identifier(f))))])))"
    assert Checker(source).check_from_source() == expected

def test_102():
    source = """
    class ForLoopError {
    void loop() {
        boolean condition := true;
        
        for condition := 0 to 10 do {  
            io.writeIntLn(condition);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for condition := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(condition))))])))"
    assert Checker(source).check_from_source() == expected
def test_103():
    source = """
    class ForLoopValid {
    void loop() {
        int i;
        
        for i := 0 to 10 do {  
            io.writeIntLn(i);
        }
        
        for i := -5 to 5 do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_104():
    source = """
    class ForLoopValid {
    void loop() {
        int start := -10;
        int end := 10;
        int i;
        
        for i := start to end do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_105():
    source = """
    class ForLoopValid {
    void loop() {
        int i;
        
        for i := 10 to 0 do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_106():
    source = """
    class ForLoopValid {
    void loop() {
        int i;
        
        for i := 0 to 10 do {  
            int i;
            i := i + 1;
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_107():
    source = """
    class ForLoopError {
    void loop() {
        int i;
        boolean flag := true;
        for i := flag to 10 do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := Identifier(flag) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected
def test_108():
    source = """
    class ForLoopError {
    void loop() {
        int i;
        float f := 5.5;
        for i := 0 to f do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to Identifier(f) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected

def test_109():
    source = """
    class ForLoopError {
    void loop() {
        int i;
        for i := "ss" to 10 do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := StringLiteral('ss') to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected
def test_110():
    source = """
    class ForLoopError {
    void loop() {
        int i;
        for i := 0 to "end" do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for i := IntLiteral(0) to StringLiteral('end') do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeIntLn(Identifier(i))))])))"
    assert Checker(source).check_from_source() == expected
def test_111():
    source = """
    class ForLoopError {
    void loop() {
        float f;
        for f := 0 to 10 do {  
            io.writeFloatLn(f);
        }
    }
}
    """
    expected = "TypeMismatchInStatement(ForStatement(for f := IntLiteral(0) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(PostfixExpression(Identifier(io).writeFloatLn(Identifier(f))))])))"
    assert Checker(source).check_from_source() == expected

def test_112():
    source = """
class AssignmentError {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        x := text;  
        text := x;  
        flag := x;  
    }
}
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_113():
    source = """
class AssignmentError {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        text := x;  
        flag := text;  
    }
}
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(text) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_114():
    source = """
class AssignmentError {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        flag := x;  
    }
}
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(flag) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_115():
    source = """
class AssignmentValid {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        x := 20;  
        text := "world";  
        flag := false;  
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_116():
    source = """
class AssignmentValid {
    void assign() {
        string text := "hello";
        boolean flag := true;
          
        text := text ^ " world";  
        flag := !flag;  
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_117():
    """  """
    source = """
        class A {
            void foo() {
            int x := 10;
            float y := 5.5;
            y := x;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_118():
    """  """
    source = """
        class A {
            void foo() {
            int x := 10;
            float y := 5.5;
            x := y;
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := Identifier(y)))"
    assert Checker(source).check_from_source() == expected
def test_119():
    """ Subtype can coerce to supertype """
    source = """
        class A {
            A() {}
        }
        class B extends A {
            B() {}
            void foo() {
                A a;
                B b;
                a := b;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_120():
    """ Supertype cannot coerce to subtype """
    source = """
        class A {
            A() {}
        }
        class B extends A {
            B() {}
            void foo() {
                A a;
                B b;
                b := a;
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := Identifier(a)))"
    assert Checker(source).check_from_source() == expected

def test_121():
    """  """
    source = """
        class A {
            void foo() {
            float x;
            x := 3;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_122():
    """  """
    source = """
        class A {
            void foo() {
            int x;
            x := 3.5;
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := FloatLiteral(3.5)))"
    assert Checker(source).check_from_source() == expected
def test_123():
    """  """
    source = """
        class A {
            void foo() {
            float x;
            int y := 3;
            x := 3.5 + y;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_124():
    """  """
    source = """
        class A {
            void foo() {
            int x;
            float y := 3.5;
            x := y + 2;
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := BinaryOp(Identifier(y), +, IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected
def test_125():
    """  """
    source = """
        class A {
            void foo() {
            float x;
            x := 3 + 2.5 * 4 - 1.0 / 2;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_126():
    """  """
    source = """
        class A {
            void foo() {
            int x;
            x := 3 + 2.5 * 4 - 1 / 2;
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(x) := BinaryOp(BinaryOp(IntLiteral(3), +, BinaryOp(FloatLiteral(2.5), *, IntLiteral(4))), -, BinaryOp(IntLiteral(1), /, IntLiteral(2)))))"
    assert Checker(source).check_from_source() == expected
    print(Checker(source).check_from_source())
def test_127():
    """  """
    source = """
        class A {
            A() {}
        }
        class B extends A {
            B() {}
            void foo() {
                A a;
                B b;
                a := new B();
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_128():
    """  """
    source = """
        class A {
            A() {}
        }
        class B extends A {
            B() {}
            void foo() {
                A a;
                B b;
                b := new A();
            }
        }
    """
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(b) := ObjectCreation(new A())))"
    assert Checker(source).check_from_source() == expected
def test_129():
    """ """
    source = """
class A{
    }
class B extends A{
    }
class C extends B{
    void foo(){
        A a;
        C c;
        a := new C();
    }
    }
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_130():
    """ """
    source = """
class A{
    }
class B extends A{
    }
class C extends B{
    void foo(){
        A a;
        C c;
        c := new A();
    }
    }
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(c) := ObjectCreation(new A())))"
    assert Checker(source).check_from_source() == expected
def test_131():
    """ """
    source = """
class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        int[2] smallArray := {1, 2};
        
        intArray := floatArray;
        floatArray := smallArray;
        intArray := smallArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(floatArray)))"
    assert Checker(source).check_from_source() == expected
def test_131a():
    """ """
    source = """
class Rectangle {
}
class ArrayError {
    void arrayAssign() {
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        int[3] intArray := {1, 2, 3};
        rectArray := intArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(rectArray) := Identifier(intArray)))"
    assert Checker(source).check_from_source() == expected
def test_131b():
    """ """
    source = """
class Rectangle {
}
class ArrayError {
    void arrayAssign() {
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        float[3] floatArray := {1.0, 2.0, 3.0};
        rectArray := floatArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(rectArray) := Identifier(floatArray)))"
    assert Checker(source).check_from_source() == expected
def test_131c():
    """ """
    source = """
class Rectangle {
}
class ArrayError {
    void arrayAssign() {
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        Rectangle[2] smallRectArray := {new Rectangle(), new Rectangle()};
        rectArray := smallRectArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(rectArray) := Identifier(smallRectArray)))"
    assert Checker(source).check_from_source() == expected
def test_131d():
    """ """
    source = """
class Rectangle {
}
class ArrayValid {
    void arrayAssign() {
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        Rectangle[3] anotherRectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        rectArray := anotherRectArray;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_132():
    """ """
    source = """
class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        int[2] smallArray := {1, 2};
        
        floatArray := intArray;
        smallArray := floatArray;
        smallArray := intArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(floatArray) := Identifier(intArray)))"
    assert Checker(source).check_from_source() == expected
def test_132a():
    """ """
    source = """
class Shape {
}
class Rectangle extends Shape {
}
class ArrayError {
    void arrayAssign() {
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        Shape[3] shapeArray := {new Shape(), new Shape(), new Shape()};
        rectArray := shapeArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(rectArray) := Identifier(shapeArray)))"
    assert Checker(source).check_from_source() == expected
def test_132b():
    """ """
    source = """
class Shape {
}
class Rectangle extends Shape {
}
class ArrayError {
    void arrayAssign() {
        Shape[3] shapeArray := {new Shape(), new Shape(), new Shape()};
        Rectangle[3] rectArray := {new Rectangle(), new Rectangle(), new Rectangle()};
        shapeArray := rectArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(shapeArray) := Identifier(rectArray)))"
    assert Checker(source).check_from_source() == expected
def test_133():
    """ """
    source = """
class ArrayValid {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        int[3] anotherIntArray := {4, 5, 6};
        
        intArray := anotherIntArray;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_134():
    """ """
    source = """
class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        int[2] smallArray := {1, 2};
        
        floatArray := smallArray;
        intArray := floatArray;
        intArray := smallArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(floatArray) := Identifier(smallArray)))"
    assert Checker(source).check_from_source() == expected
def test_135():
    """ """
    source = """
class ArrayError {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        float[3] floatArray := {1.0, 2.0, 3.0};
        int[2] smallArray := {1, 2};
        
        intArray := smallArray;
        intArray := floatArray;
        floatArray := smallArray;
    }
}
"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(intArray) := Identifier(smallArray)))"
    assert Checker(source).check_from_source() == expected
def test_136():
    """"""
    source = """
class ArrayValid {
    void arrayAssign() {
        float[3] floatArray := {1.0, 2.0, 3.0};
        float[3] anotherFloatArray := {4.0, 5.0, 6.0};
        
        floatArray := anotherFloatArray;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_137():
    """ """
    source = """
class ArrayValid {
    void arrayAssign() {
        int[2] smallArray := {1, 2};
        int[2] anotherSmallArray := {3, 4};
        
        smallArray := anotherSmallArray;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_138():
    """ """
    source = """
class CallError {
    void processInt(int value) {
        io.writeIntLn(value);
    }
    
    void test() {
        string text := "123";
        this.processInt(text);  
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).processInt(Identifier(text)))))"
    assert Checker(source).check_from_source() == expected

def test_139():
    """ """
    source = """
    class A{
        void foo(){
            this.a:=3;
        }
        int a;
    }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_140():
    """ """
    source = """
class CallError {
    void processInt(int value) {
        io.writeIntLn(value);
    }
    
    void test() {
        string text := "123";
        this.processInt();  
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).processInt())))"
    assert Checker(source).check_from_source() == expected
def test_141():
    """ """
    source = """
class CallValid {
    void processInt(int value) {
        io.writeIntLn(value);
    }
    
    void test() {
        int num := 123;
        this.processInt(num);  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_142():
    """ """
    source = """
class CallValid {
    int processFloat(float value) {
        io.writeFloatLn(value);
    }
    
    void test() {
        float num := 123.45;
        this.processFloat(num);  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_143():
    """ """
    source = """
class CallError {
    void processFloat(float value) {
        io.writeFloatLn(value);
    }
}
class Test extends CallError {
    void test() {
        int num := 123;
        this.processFloat(num);  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_144():
    """ """
    source = """
class CallError {
    void processFloat(float value) {
        io.writeFloatLn(value);
    }
    void test() {
        float b := 12.34;
        a.processFloat(b);  
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_145():
    """ """
    source = """
class CallValid {
    void processString(string value) {
        io.writeStrLn(value);
    }
    
    void test() {
        string msg := "Hello, World!";
        this.processString(msg);  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_146():
    """ """
    source = """
class CallError {
    void processString(string value) {
        io.writeStrLn(value);
    }
    
    void test() {
        this.processString("abc");  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_147():
    """ """
    source = """
class CallError {
    void processString(string value) {
        io.writeStrLn(value);
    }
    
    void test() {
        int num := 100;
        float result := 0.0;
        this.processString(num, result);  
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).processString(Identifier(num), Identifier(result)))))"
    assert Checker(source).check_from_source() == expected
def test_148():
    """ """
    source = """
    class Test {
    void method() {
        int x := 10;
        {
            int x := 20;
            io.writeIntLn(x);
        }
        io.writeIntLn(x);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_149():
    source = """
class ReturnError {
    int getValue() {
        return "invalid";  
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('invalid')))"
    assert Checker(source).check_from_source() == expected
def test_150():
    source = """
class ReturnError {
    float getValue() {
        return 42;  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_151():
    source = """
class ReturnError {
    string getValue() {
        return 100;  
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(100)))"
    assert Checker(source).check_from_source() == expected
def test_152():
    source = """
class ReturnValid {
    boolean isTrue() {
        return true;  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_153():
    source = """
class ReturnValid {
    int computeSum(int a; int b) {
        return a + b;  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_153a():
    source = """
class ReturnValid {
    int computeSum(int a; float b) {
        return a + b;  
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return BinaryOp(Identifier(a), +, Identifier(b))))"
    assert Checker(source).check_from_source() == expected
def test_154():
    source = """
class Test {
    void method() {
        return "done";  # Error: TypeMismatchInStatement
    }
}

"""
    expected = "TypeMismatchInStatement(ReturnStatement(return StringLiteral('done')))"
    assert Checker(source).check_from_source() == expected
def test_155():
    source = """
class Test {
    void method() {
        return 5;  # Error: TypeMismatchInStatement
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_156():
    """ Return subtype to supertype """
    source = """ 
class A{

    }
class B extends A{

    }
class Test extends B{
    A getInstance() {
        return new B();  # Valid: returning subtype
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_157():
    """ Return supertype to subtype """
    source = """
class A{

    }
class B extends A{

    }
class Test extends B{
    B getInstance() {
        return new A();  # Error: TypeMismatchInStatement
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return ObjectCreation(new A())))"
    assert Checker(source).check_from_source() == expected

def test_158():
    """  """
    source = """
class A{

    }
class B extends A{

    }
class Test extends B{
    B getInstance() {
        return new B();  # Error: TypeMismatchInStatement
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_159():
    """"""
    source = """
class ArraySubscriptError {
    void access() { 
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
        int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
        string word := words[true];      # Error: TypeMismatchInExpression at array access
        
        int x := 10;
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([StringLiteral('index')])"
    assert Checker(source).check_from_source() == expected
def test_159a():
    """  """
    source = """
class A{}
class ArraySubscriptError {
    void access() {
        A a;
        int invalid := a[0];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(a)[IntLiteral(0)]))"
    assert Checker(source).check_from_source() == expected
def test_159b():
    """  """
    source = """
class A{}
class ArraySubscriptError {
    void access() {
        A[3] a:= {new A(), new A(), new A()};
        int invalid := a["index"];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([StringLiteral('index')])"
    assert Checker(source).check_from_source() == expected
def test_159c():
    """  """
    source = """
class A{}
class ArraySubscriptError {
    void access() {
        A[3] a:= {new A(), new A(), new A()};
        int invalid := a[1.5];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([FloatLiteral(1.5)])"
    assert Checker(source).check_from_source() == expected
def test_159d():
    """  """
    source = """
class A{}
class ArraySubscriptError {
    void access() {
        A[3] a:= {new A(), new A(), new A()};
        int invalid := a[true];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected
def test_159e():
    """  """
    source = """
class A{}
class Array {
    void access() {
        A[3] a:= {new A(), new A(), new A()};
        int invalid := a[0]; 
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(invalid = PostfixExpression(Identifier(a)[IntLiteral(0)]))]))"
    assert Checker(source).check_from_source() == expected
def test_159f():
    """  """
    source = """
class A{}
class Array {
    void access() {
        A[3] a:= {new A(), new A(), new A()};
        A valid := a[1];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_160():
    source = """
class ArraySubscriptError {
    void access() { 
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
        int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
        string word := words[true];      # Error: TypeMismatchInExpression at array access
        
        int x := 10;
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([FloatLiteral(2.5)])"
    assert Checker(source).check_from_source() == expected

def test_161():
    source = """
class ArraySubscriptError {
    void access() { 
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        string word := words[true];      # Error: TypeMismatchInExpression at array access
        int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
        int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
        
        int x := 10;
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access
    }
}
"""
    expected = "TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected
def test_162():
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
def test_163():
    source = """
class ArraySubscriptValid {
    void access() { 
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        int value1 := numbers[0];  
        int value2 := numbers[4];      
        string word := words[1];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_164():
    source = """
class ArraySubscriptValid {
    void access() { 
        int[3] arr := {10, 20, 30};
        int index := 1;
        
        int value := arr[index];  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_165():
    source = """
class ArraySubscriptValid {
    void access() { 
        string[2] words := {"hello", "world"};
        int i := 0;
        
        string firstWord := words[i];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_165a():
    source = """
class ArraySubscriptValid {
    void access() { 
        string[2] words := {"hello", "world"};
        int i := -1;
        
        string firstWord := words[i];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_165b():
    source = """
    class A{
}
class ArraySubscriptValid {
    void access() {
        A[3] arr := {new A(), new A(), new A()};
        int i := 2;
        A element := arr[i];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_165c():
    source = """
    class A{
}
class ArraySubscriptValid {
    void access() {
        A[3] arr := {new A(), new A(), new A()};
        int i := 99;
        A element := arr[i];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_166():
    source = """
class ArraySubscriptValid {
    void access() { 
        float[4] values := {1.1, 2.2, 3.3, 4.4};
        int idx := 2;
        
        float val := values[idx];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_167():
    source = """
class ArraySubscriptValid {
    void access() { 
        boolean[3] flags := {true, false, true};
        int position := 0;
        
        boolean flag := flags[position];
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_168():
    source = """
class ArraySubscriptValid {
    void access() { 
        int[5] numbers := {1, 2, 3, 4, 5};
        int i;
        for i := 0 to 4 do {
            io.writeIntLn(numbers[i]);
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_169():
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
def test_170():
    source = """
class BinaryOpError {
    void calculate() {
        int x := 5;
        string text := "hello";
        boolean flag := true;
        
        boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
        int sum := x + text;     # Error: TypeMismatchInExpression at binary operation
        int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), &&, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected
def test_171():
    source = """
class BinaryOpError {
    void calculate() {
        int x := 5;
        string text := "hello";
        boolean flag := true;
        
        int comparison := text < x;   # Error: TypeMismatchInExpression at binary operation
        int sum := x + text;     # Error: TypeMismatchInExpression at binary operation
        boolean result := x && flag;  # Error: TypeMismatchInExpression at binary operation
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(text), <, Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_172():
    source = """
class BinaryOpError {
    void calculate() {
        int x := 5;
        string text := "hello";
        boolean flag := true;
        
        int sum := x + 10;     
        boolean result := flag || false;  
        boolean comparison := x > 3;   
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_173():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        
        float result1 := a * str;  # Error: TypeMismatchInExpression at binary operation
        boolean result2 := str && true;  # Error: TypeMismatchInExpression at binary operation
        int result3 := b + 3;     # Error: TypeMismatchInExpression at binary operation
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), *, Identifier(str)))"
    assert Checker(source).check_from_source() == expected
def test_174():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        
        int result3 := b + 3;     # Error: TypeMismatchInExpression at binary operation
        float result1 := a * str;  # Error: TypeMismatchInExpression at binary operation
        boolean result2 := str && true;  # Error: TypeMismatchInExpression at binary operation
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(result3 = BinaryOp(Identifier(b), +, IntLiteral(3)))]))"
    assert Checker(source).check_from_source() == expected

def test_175():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        int e := 4;
        b := e + 2.0;
        str := "value" ^ str;
        a := a * b;
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_176():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        int e := 4;
        int f := e \\ 2;
        boolean c;
        f := e \\ 2;
        f := e % 2;
        a := a * b;
        a := e + 2;
        a := e / b;
        c := a == b;
        c := e != f;
        c := (a > b) && (e < 10);
    }
}"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), ==, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_177():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        int e := 4;
        int f := e \\ 2;
        boolean c;
        c := a > b;
        c := a > e;
        c := e > f;
        a := e + f;
        a := a * e;
        a := b / e;
        e := a - 2;
    }
}"""
    expected = "TypeMismatchInStatement(AssignmentStatement(IdLHS(e) := BinaryOp(Identifier(a), -, IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected

def test_178():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        int e := 4;
        int f := e \\ 2;
        boolean c;
        e := (e - 2) * 3;
        c := (a > b) && (e < 10);
        c := e != f;
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_179():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        string str := "test";
        int e := 4;
        int f := e \\ 2;
        boolean c;
        e := (e - 2) * 3;
        c := (a > b) && (e < 10);
        c := (e != f) || (a < b);
        a := (a + b) / 2.0;
        a := (e * 1.5) + (b - 0.5);
        b := (e % 2) + (a * 1);
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_180():
    source = """
class BinaryOpError {
    void calculate() {
        float a := 2.5;
        float b := 4.0;
        int e := 4;
        e := (a ^ b) + 2;
    }
}"""
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), ^, Identifier(b)))"
    assert Checker(source).check_from_source() == expected
def test_181():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        
        int negX := -text;          # Error: TypeMismatchInExpression at unary operation
        float negY := -flag;        # Error: TypeMismatchInExpression at unary operation
        boolean notFlag := !x;      # Error: TypeMismatchInExpression at unary operation
    }
}
    """
    expected = "TypeMismatchInExpression(UnaryOp(-, Identifier(text)))"
    assert Checker(source).check_from_source() == expected

def test_182():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        
        float negY := -flag;        # Error: TypeMismatchInExpression at unary operation
        int negX := -text;          # Error: TypeMismatchInExpression at unary operation
        boolean notFlag := !x;      # Error: TypeMismatchInExpression at unary operation
    }
}
    """
    expected = "TypeMismatchInExpression(UnaryOp(-, Identifier(flag)))"
    assert Checker(source).check_from_source() == expected

def test_183():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        
        boolean notFlag := !x;      # Error: TypeMismatchInExpression at unary operation
        int negX := -text;          # Error: TypeMismatchInExpression at unary operation
        float negY := -flag;        # Error: TypeMismatchInExpression at unary operation
    }
}
    """
    expected = "TypeMismatchInExpression(UnaryOp(!, Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_184():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        
        int negX := -x;          
        float negY := -y;        
        boolean notFlag := !flag;      
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_184a():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        
        int negX := -x;          
        float negY := -y;        
        float notFlag := !flag;      
    }
}"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(float), [Variable(notFlag = UnaryOp(!, Identifier(flag)))]))"
    assert Checker(source).check_from_source() == expected
def test_185():
    source = """
class UnaryOpError {
    void evaluate() {
        int x := 10;
        float y := 5.5;
        boolean flag := true;
        string text := "hello";
        int negX := -x;          
        float negY := +y;        
        boolean notFlag := !flag;
        boolean check := !(x > 5);
        int doubleX := -(-x);
        int sum := -x + 20;
        float adjustedY := -y * 2.0;
        int complex := -(-(-x)) + 5;
        int combined := -x + -(-x);
        float finalY := -(-y) / 2.0;
        boolean finalCheck := !(flag || false);
        boolean nestedNot := !!flag;
        boolean logic := !((x < 15) && !flag);
        boolean logic2 := !((x >= 10) || flag);
        int arithmetic := -x * (-x + 10);
        int arithmetic2 := -(-x / 2) + 5;
        int arithmetic3 := +x % 3;
        int arithmetic4 := -x \\ 4;
        float arithmetic5 := +y + (-y * 3.0);
        float arithmetic6 := +(-y + 2.0) / 4.0;
        boolean logic3 := !((x != 0) && (flag == true));
        boolean logic4 := !((x == 10) || (flag != false));
        boolean logic5 := !( ( (x < 20) && (x > 5) ) || (!flag) );
        boolean logic6 := !((x <= 15) && !(flag || true));
    }
}"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(arithmetic2 = BinaryOp(UnaryOp(-, ParenthesizedExpression((BinaryOp(UnaryOp(-, Identifier(x)), /, IntLiteral(2))))), +, IntLiteral(5)))]))"
    assert Checker(source).check_from_source() == expected

def test_186():
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
    expected = "TypeMismatchInExpression(Identifier(text))"
    assert Checker(source).check_from_source() == expected
def test_187():
    source = """
class AttributeAccessError {
    void access() {
        int x := 10;
        string text := "hello";
        
        int invalid := x.length;   # Error: TypeMismatchInExpression at member access (x is not object)
        int length := text.value;  # Error: TypeMismatchInExpression at member access (if value doesn't exist)
    }
}
    """
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected
def test_188():
    source = """
class A {
    int length;
    void access() {
        int x := 10;
        string text := "hello";
        int validLength := this.length;
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_189():
    source = """
        class A {
            int length;
            void foo() {
                string text := "hello";
                int len := text.length;
            }
        }
    """
    expected = "TypeMismatchInExpression(Identifier(text))"
    assert Checker(source).check_from_source() == expected
def test_190():
    source = """
        class A {
            int length;
            void foo() {
                A a;
                int len := a.length;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_191():
    """ Subtype can coerce to supertype """
    source = """
        class A {
            int length;
        }
        class B extends A {
            B() {}
            void foo() {
                A a;
                B b;
                int len:= b.length;
                int len2:= a.length;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_191a():
    """ """
    source = """
        class C {
            int code;
        }
        class B {
            C c;
            int b;
        }
        class A extends B {
            A() {}
            void foo() {
                B b;
                A a;
                int len:= a.c.code;
                int len2:= b.c.code;
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_191b():
    """ """
    source = """
        class C {
            int code;
        }
        class B {
            C c;
            int b;
        }
        class A extends B {
            A() {}
            void foo() {
                B b;
                int a;
                int len:= a.c.code;
                int len2:= b.c.code;
            }
        }
    """
    expected = "TypeMismatchInExpression(Identifier(a))"
    assert Checker(source).check_from_source() == expected
def test_192():
    """ Supertype cannot coerce to subtype """
    source = """
        class A {
            int length;
        }
        class B extends A {
            boolean flag;
            void foo() {
                A a;
                B b;
                float len:= a.length;
                int len2:= b.length;
                boolean g:= b.flag;
                float o:= this.length;
                # boolean h:= a.flag; # object of type A has no attribute flag
            }
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_193():
    """  """
    source = """
        class A {
            int length;
        }
        class B extends A {
            B() {}
            boolean flag;
            void foo() {
                A a;
                B b;
                int len:= a.length;
                int len2:= b.length;
                }
        }
        class C extends B {
            C() {}
            void bar() {
                A a;
                B b;
                C c;
                int len:= a.length;
                int len2:= b.length;
                int len3:= c.length;
                boolean j:= this.flag;
                int i:= this.length;
                boolean h:= c.flag;
                boolean g:= b.flag;
                boolean f:= a.flag;
            }
        }
    """
    expected = "UndeclaredAttribute(flag)"
    assert Checker(source).check_from_source() == expected
def test_194():
    """  """
    source = """
        class A {
            int length;
        }
        class B extends A {
            B() {}
            boolean flag;
            void foo() {
                A a;
                B b;
                int len:= a.length;
                int len2:= b.length;
                }
        }
        class C extends B {
            C() {}
            void bar() {
                A a;
                B b;
                C c;
                int x;
                int len:= a.length;
                int len2:= b.length;
                int len3:= c.length;
                boolean j:= this.flag;
                int i:= this.length;
                boolean h:= c.flag;
                boolean g:= b.flag;
                int y:= x.length;
            }
        }
    """
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected
def test_195():
    """  """
    source = """
        class A {
            int length;
        }
        class B extends A {
            B() {}
            boolean flag;
            void foo() {
                A a;
                B b;
                int len:= a.length;
                int len2:= b.length;
                }
        }
        class C extends B {
            C() {}
            void bar() {
                A a;
                B b;
                C c;
                int x;
                int len:= a.length;
                int len2:= b.length;
                int len3:= c.length;
                boolean j:= this.flag;
                int i:= this.length;
                boolean h:= c.flag;
                boolean g:= b.flag;
                boolean f:= x.flag;
            }
        }
    """
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_196():
    source = """
    class MethodCallError {
    void printMessage() {  
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

def test_197():
    source = """
    class MethodCallError {
    void printMessage() {  
        io.writeStrLn("Hello");
    }
    
    int getValue() {
        return 42;
    }
    
    void test() {
        string text := "number";
        int value := this.getValue(text);  # Error: TypeMismatchInExpression at method call
        int result := this.printMessage();  # Error: TypeMismatchInExpression at method call
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).getValue(Identifier(text))))"
    assert Checker(source).check_from_source() == expected

def test_198():
    source = """
    class MethodCallValid {
    int printMessage() {  
        io.writeStrLn("Hello");
    }
    
    int getValue() {
        return 42;
    }
    
    void test() {
        int value := this.getValue();  
        this.printMessage();  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_199():
    source = """
    class MethodCallValid {
    void printMessage(string msg) {  
        io.writeStrLn(msg);
    }
    
    int getValue(int multiplier) {
        return 42 * multiplier;
    }
    
    void test() {
        int value := this.getValue(2);
        this.printMessage("Test Message");  
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_200():
    source = """
    class MethodCallValid {
    void printMessage(string msg) {  
        io.writeStrLn(msg);
    }
    
    int getValue(int multiplier) {
        return 42 * multiplier;
    }
    
    void test() {
        MethodCallValid mc := new MethodCallValid();
        int value := this.getValue(2);
        int value2 := mc.getValue(3);
        mc.printMessage("Test Message");
        this.printMessage("Value is: " + value);
    }
}"""
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('Value is: '), +, Identifier(value)))"
    assert Checker(source).check_from_source() == expected

def test_201():
    source = """
class A{
    final int a;
    final int a;
}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected
def test_202():
    source = """
class A{
    void foo(){
        final int a;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_203():
    source = """
class A{
    final int a;
    int a;
}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected

def test_204():
    source = """
    class MethodCallValid {
    void printMessage(string msg) {  
        io.writeStrLn(msg);
    }
    
    int getValue(int multiplier) {
        return 42 * multiplier;
    }
    
    void test() {
        MethodCallValid mc := new MethodCallValid();
        int value := this.getValue(2);
        int value2 := mc.getValue(3);
        mc.printMessage("Test Message");
        this.printMessage(value, value2);
    }
}"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).printMessage(Identifier(value), Identifier(value2)))))"
    assert Checker(source).check_from_source() == expected

def test_205():
    source = """
    class MethodCallValid {
    void printMessage(string msg) {  
        io.writeStrLn(msg);
    }
    
    int getValue(int multiplier) {
        return 42 * multiplier;
    }
    
    void test() {
        MethodCallValid mc := new MethodCallValid();
        string text := "number";
        int value := this.getValue(2);
        int value2 := mc.getValue(3);
        mc.printMessage("Test Message");
        this.printMessage("value is: " ^ text);
        value := mc.getValue(1 + 2);
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_206():
    """ """
    source = """
class CallValid {
    float processFloat(float value) {
        io.writeFloatLn(value);
        return value;
    }
    
    void test() {
        float num := 123.45;
        num := this.processFloat(67);
        num := this.processFloat(num);
        num := this.processFloat(78.9);
        num := this.processFloat(100 + 23.45);
        num := this.processFloat(num * 2);
        num := this.processFloat(50 \\ 3);
        num := this.processFloat(10.0 - 2.5);
        num := this.processFloat((1 + 2) / 3.4 );
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_207():
    source = """
class Student {
    string getName(){
        return "a";
    }
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
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_208():
    source = """
class CallError {
    void processString(string value) {
        io.writeStrLn(value);
    }
    void test() {
        string msg := "Hello World";
        this.processString(msg);  
        this.processString(100);
    }
}
"""
    expected = "TypeMismatchInStatement(MethodInvocationStatement(PostfixExpression(ThisExpression(this).processString(IntLiteral(100)))))"
    assert Checker(source).check_from_source() == expected
def test_209():
    source = """
class ConstantTypeError {
    final int a := 1.2;        
    final string text := 42;  
    final boolean flag := "true"; 
    
    final int count := 3.14;  
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(a = FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected
def test_210():
    source = """
class ConstantTypeError {
    void foo() {
        final float pi := 3.14;
        final string greeting := "Hello";
        final boolean check := "false";
        final boolean isValid := 100;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(boolean), [Variable(check = StringLiteral('false'))]))"
    assert Checker(source).check_from_source() == expected
def test_211():
    source = """
class ConstantTypeError {
    void foo() {
        final float pi := 3.14;
        final string greeting := "Hello";
        final boolean check := true;
        final int number := 100;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_212():
    source = """
class ConstantTypeError {
    void foo() {
        final float pi := 3;
        final string greeting := "Hello";
        final boolean check := (3 > 2) && false || true;
        final int number := "e";
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(int), [Variable(number = StringLiteral('e'))]))"
    assert Checker(source).check_from_source() == expected

def test_213():
    source = """
class A{
}
class B extends A{
}
class C extends B{
    final C c := new C();
    final B b := new C();
    final A a := new B();
    final A a2 := new A();
    final B b2 := new B();
    final C c2 := new C();
    final A a3 := 2;
}

"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(A), [Attribute(a3 = IntLiteral(2))]))"
    assert Checker(source).check_from_source() == expected

def test_214():
    source = """
class A{
}
class B extends A{
}
class C extends B{
    final A a := new C();
    final B b := new A();
    final C c := new B();
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(B), [Attribute(b = ObjectCreation(new A()))]))"
    assert Checker(source).check_from_source() == expected
def test_215():
    source = """
class Test {
    final int a := 10 + 10;
    final float b := 20 + this.a - 20.45;
    final string c := "hello" ^ " world";
    void foo() {
        final int a := (50 \\ 3) * 2;
        final float b:= 15.5 + a / 2.0 - 5.5;
        final string c:= "world";
    }
}
"""    
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_216():
    source = """
class Test {
    final int a := 10 + 10;
    final float b := 20 + this.a - 20.45;
    final string c := "hello" ^ " world";
    void foo() {
        this.a:= (50 \\ 3) * 2;
        this.b:= 15.5 + this.a / 2.0 - 5.5;
        this.c:= "world";
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).a)) := BinaryOp(ParenthesizedExpression((BinaryOp(IntLiteral(50), \\, IntLiteral(3)))), *, IntLiteral(2))))"
    assert Checker(source).check_from_source() == expected
def test_217():
    """ Supertype cannot coerce to subtype """
    source = """
class A{
}
class B extends A{
}
class Test extends B{
    A getInstance() {
        return new A();
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_218():
    source = """
class ArrayConstantError {
    final int[3] numbers := {1.0, 2.0, 3.0};  
    final string[3] words := {1, 2, 3};        
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(PrimitiveType(int)[3]), [Attribute(numbers = ArrayLiteral({FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0)}))]))"
    assert Checker(source).check_from_source() == expected
def test_218a():
    source = """
    class A{}
class ArrayConstantError {
    final A[3] arr := {new A(), new A(), 42};
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new A()), ObjectCreation(new A()), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected
def test_218b():
    source = """
    class A{}
class ArrayConstantError {
    final A[3] arr := {3.14, 2.14, 3.44};
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(ClassType(A)[3]), [Attribute(arr = ArrayLiteral({FloatLiteral(3.14), FloatLiteral(2.14), FloatLiteral(3.44)}))]))"
    assert Checker(source).check_from_source() == expected
def test_218c():
    source = """
    class A{}
    class B extends A{}
class ArrayConstantError {
    final A[3] arr := {new B(), new B(), new B()};
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ArrayType(ClassType(A)[3]), [Attribute(arr = ArrayLiteral({ObjectCreation(new B()), ObjectCreation(new B()), ObjectCreation(new B())}))]))"
    assert Checker(source).check_from_source() == expected
def test_219():
    source = """
class ArrayConstantError {
    void foo() {
        final int[3] numbers := {1, 2, 3};  
        final string[3] words := {23, 42, 343};        
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final ArrayType(PrimitiveType(string)[3]), [Variable(words = ArrayLiteral({IntLiteral(23), IntLiteral(42), IntLiteral(343)}))]))"
    assert Checker(source).check_from_source() == expected

def test_220():
    source = """
class ArrayConstantError {
    void foo() {
        final int[3] numbers := {1, 2, 3};  
        final string[3] words := {"hello", "world", "!"};
        int[3] numbers := {1, 2, 3};     
    }
}
"""
    expected = "Redeclared(Variable, numbers)"
    assert Checker(source).check_from_source() == expected
def test_220a():
    source = """
class ArrayConstantError {
    void foo() {
        final int[3] numbers := {1, 2, 3};  
        final string[3] words := {"hello", "world", "!"};
        int[3] abc := {1, 2, 3};     
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_220b():
    source = """
class ArrayConstantError {
    void foo() {
        final float[3] numbers := {1, 2, 3};  
        final string[3] words := {"hello", "world", "!"};
        int[3] abc := {1, 2, 3};     
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final ArrayType(PrimitiveType(float)[3]), [Variable(numbers = ArrayLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)}))]))"
    assert Checker(source).check_from_source() == expected
def test_221():
    source = """
class Test {
    void foo() {
        final int x := 0;
        {
            int x := 5;
            x := 3;
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_222():
    source = """
class Test {
    void foo() {
        final int x := 0;
        {
            final int x := 5;
            x := 3;
        }
    }
}
"""    
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(3)))"
    assert Checker(source).check_from_source() == expected

def test_223():
    source = """
class ValidConstants {
    final int MAX_SIZE := 1000;           
    final float PI := 3.14159;            
    final string APP_NAME := "MyApp";     
    final int[4] PRIMES := {2, 3, 5, 7};  
    final float ratio := 10;          
}
"""    
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_224():
    source = """
class Shape {
}
class Integer {
    Integer(int value) {}
}
class ObjectConstantError {
    final Shape shape := new Integer(42);  
}
"""
    expected = "TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer(IntLiteral(42))))]))"
    assert Checker(source).check_from_source() == expected
def test_224a():
    source = """
class Shape {
}
class Integer {
    Integer(int value) {}
}
class ObjectConstantError {
    final Shape shape := new Shape(42);  
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_224b():
    source = """
class Shape {
}
class Integer {
    Integer(int value) {}
}
class ObjectConstantError {
    final Shape shape := new Shape();  
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_224c():
    source = """
class Shape {
}
class Integer extends Shape{
    Integer(int value) {}
}
class ObjectConstantError {
    final Shape shape := new Integer();  
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_224d():
    source = """
class Shape {
}
class Integer extends Shape{
    Integer(int value) {}
}
class ObjectConstantError {
    final Shape shape := new Integer(1);  
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_225():
    source = """
class LoopError {
    void method() {
        break;    
        continue; 
    }
    
    void conditionalError() {
        if true then {
            break;     
            continue; 
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_226():
    source = """
class LoopError {
    void method() {
        continue; 
        break;    
    }
    
    void conditionalError() {
        if true then {
            break;     
            continue; 
        }
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected
def test_227():
    source = """
class LoopError {
    void method() {
        int i;
        for i := 0 to 10 do {
            break;     
            continue;
            break;
            continue;
            if true then {
                break;
                continue;
            }
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_228():
    source = """
    class LoopError {
    void conditionalError() {
        if true then {
            break;     
            continue; 
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected
def test_229():
    source = """
    class LoopError {
    void conditionalError() {
        if true then {
            continue; 
            break;
        }
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected
def test_230():
    source = """
class MethodCallError {
    void helperMethod() {
        break;    
        continue; 
    }

    void loopWithCall() {
        int i;
        for i := 0 to 10 do {
            this.helperMethod();  
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected
def test_231():
    source = """
class MethodCallError {
    void helperMethod() {
        continue;  
        break;     
    }
    
    void loopWithCall() {
        int i;
        for i := 0 to 10 do {
            this.helperMethod();  
        }
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected
def test_232():
    source = """
class ValidLoops {
    void forLoopWithBreak() {
        int i;
        for i := 0 to 10 do {
            if i == 5 then {
                break;    
            }
            if i % 2 == 0 then {
                continue; 
            }
            io.writeIntLn(i);
        }
    }
    
    void forLoop() {
        int i;
        for i := 0 to 10 do {
            if i == 3 then {
                continue;  
            }
            if i == 8 then {
                break;    
            }
            io.writeIntLn(i);
        }
    }
    
    void nestedLoops() {
        int i, j;
        for i := 0 to 5 do {
            for j := 0 to 5 do {
                if i == j then {
                    continue;  
                }
                if j > 3 then {
                    break;     
                }
            }
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

 
def test_234():
    source = """
class IllegalConstantError {
    final string text := nil; 
    final int x;
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(string), [Attribute(text = NilLiteral(nil))]))"
    assert Checker(source).check_from_source() == expected
def test_234a():
    source = """
class IllegalConstantError {
    final int x;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_234b():
    source = """
class IllegalConstantError {
    void foo() {
        final int x;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_234c():
    source = """
class IllegalConstantError {
    void foo() {
        final int x;
        {
            final string text;
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_235():
    source = """
class MutableInConstant {
    int mutableVar := 10;
    final int constant1 := this.mutableVar;  
    
    int localVar := 5;
    final int constant2 := 1 + localVar;  
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(constant1 = PostfixExpression(ThisExpression(this).mutableVar))]))"
    assert Checker(source).check_from_source() == expected
def test_235a():
    source = """
class MutableInConstant {
    int mutableVar := 10;
    final int constant1 := mutableVar;  
    
    int localVar := 5;
    final int constant2 := 1 + localVar;  
}
"""
    expected = "UndeclaredIdentifier(mutableVar)"
    assert Checker(source).check_from_source() == expected
def test_236():
    source = """
class MutableInConstant {
    int localVar := 5;
    final int constant2 := 1 + this.localVar;  
    int mutableVar := 10;
    final int constant1 := mutableVar;  
    
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(constant2 = BinaryOp(IntLiteral(1), +, PostfixExpression(ThisExpression(this).localVar)))]))"
    assert Checker(source).check_from_source() == expected
def test_236a():
    source = """
class MutableInConstant {
    int localVar := 5;
    final int constant2 := 1 + localVar;  
    int mutableVar := 10;
    final int constant1 := mutableVar;  
    
}
"""
    expected = "UndeclaredIdentifier(localVar)"
    assert Checker(source).check_from_source() == expected

def test_237():
    source = """
class MethodCallInConstant {
    final int value := this.getValue();  
    
    int getValue() {
        return 42;
    }
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(value = PostfixExpression(ThisExpression(this).getValue()))]))"
    assert Checker(source).check_from_source() == expected

def test_238():
    source = """
class ComplexIllegalExpression {
    int a := 10;
    
    final int result := (this.a * 2) + 5;  
    final boolean flag := this.isValid();  
    
    boolean isValid() {
        return true;
    }
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(result = BinaryOp(ParenthesizedExpression((BinaryOp(PostfixExpression(ThisExpression(this).a), *, IntLiteral(2)))), +, IntLiteral(5)))]))"
    assert Checker(source).check_from_source() == expected
def test_238a():
    source = """
class ComplexIllegalExpression {
    int a := 10;
    
    final int result := (a * 2) + 5;  
    final boolean flag := this.isValid();  
    
    boolean isValid() {
        return true;
    }
}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected
def test_239():
    source = """
class ComplexIllegalExpression {
    int a := 10;
    
    final boolean flag := this.isValid();  
    final int result := (a * 2) + 5;  
    
    boolean isValid() {
        return true;
    }
}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(boolean), [Attribute(flag = PostfixExpression(ThisExpression(this).isValid()))]))"
    assert Checker(source).check_from_source() == expected
def test_240():
    source = """
class ValidConstantExpressions {
    final int MAX_SIZE := 100;
    final int DOUBLE_SIZE := this.MAX_SIZE * 2;     
    final string MESSAGE := "Hello" ^ "World"; 
    final boolean FLAG := true && false;       
    final float PI := 3.14159;
    final float CIRCLE_AREA := this.PI * 10 * 10;   
    final int SUM := 10 + 20 + 30;         
}

"""    
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_240a():
    source = """
class ValidConstantExpressions {
    final int MAX_SIZE;
    final int DOUBLE_SIZE := this.MAX_SIZE * 2;     
    final string MESSAGE := "Hello" ^ "World"; 
    final boolean FLAG := true && false;       
    final float PI := 3.14159;
    final float CIRCLE_AREA := this.PI * 10 * 10;   
    final int SUM := 10 + 20 + 30;
    final int a;
    final int b := this.a + 10;    
}

"""    
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_241():
    source = """
class ArrayAccessInConstant {
    final int[5] NUMBERS := {1, 2, 3, 4, 5};
    final int FIRST := this.NUMBERS[0];  
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_241a():
    source = """
class ArrayAccessInConstant {
void foo() {
    final int[5] NUMBERS := {1, 2, 3, 4, 5};
    final int FIRST := NUMBERS[0];  
}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_241b():
    source = """
class ArrayAccessInConstant {
    final int[5] NUMBERS := {1, 2, 3, 4, 5};
    final int FIRST := NUMBERS[0];  
}
"""
    expected = "UndeclaredIdentifier(NUMBERS)"
    assert Checker(source).check_from_source() == expected
def test_242():
    source = """
class IllegalArrayError {
    void create() {
        int[3] mixed1 := {1, 2.0, 3};     
        string[2] mixed2 := {"hello", 42}; 
        boolean[2] mixed3 := {true, 1};    
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), FloatLiteral(2.0), IntLiteral(3)}))"
    assert Checker(source).check_from_source() == expected
def test_243():
    source = """
class IllegalArrayError {
    void create() {
        string[2] mixed2 := {"hello", 42}; 
        int[3] mixed1 := {1, 2.0, 3};     
        boolean[2] mixed3 := {true, 1};    
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({StringLiteral('hello'), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected
def test_244():
    source = """
class IllegalArrayError {
    boolean[2] mixed3 := {true, 1};    
    int[3] mixed1 := {1, 2.0, 3};     
    string[2] mixed2 := {"hello", 42}; 
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected
def test_245():
    source = """
class ComplexIllegalExpression {
void foo() {
    int a := 10;
    
    final int result := (a * 2) + 5;  
    final boolean flag := this.isValid();  
    }
    boolean isValid() {
        return true;
    }
}
"""
    expected = "IllegalConstantExpression(VariableDecl(final PrimitiveType(int), [Variable(result = BinaryOp(ParenthesizedExpression((BinaryOp(Identifier(a), *, IntLiteral(2)))), +, IntLiteral(5)))]))"
    assert Checker(source).check_from_source() == expected
def test_246():
    source = """
class ValidArrays {
    void create() {
        int[5] numbers := {1, 2, 3, 4, 5};          
        string[3] words := {"hello", "world", "!"};  
        boolean[3] flags := {true, false, true};      
        float[3] decimals := {1.0, 2.5, 3.14};      
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_246a():
    source = """
class Rectangle {
}
class ValidArrays {
    void create() {
        Rectangle[2] shapes := {new Rectangle(1.0, 2.0), new Rectangle(3.0, 4.0)};
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_246b():
    source = """
class Rectangle {
    void foo(){
        Rectangle[2] shapes := {1, new Rectangle(3.0, 4.0)};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), ObjectCreation(new Rectangle(FloatLiteral(3.0), FloatLiteral(4.0)))}))"
    assert Checker(source).check_from_source() == expected
def test_246c():
    source = """
class Rectangle {
}
class ValidArrays {
    void create() {
        Rectangle[2] shapes := {new Rectangle(), new Rectangle()};
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_246d():
    source = """
class Rectangle {
    Rectangle(float width; float height) {}
}
class ValidArrays {
    void create() {
        Rectangle[3] shapes := {new Rectangle(1.0, 2.0), new Rectangle(3.0, 4.0), "new Rectangle(5.0, 6.0)"};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({ObjectCreation(new Rectangle(FloatLiteral(1.0), FloatLiteral(2.0))), ObjectCreation(new Rectangle(FloatLiteral(3.0), FloatLiteral(4.0))), StringLiteral('new Rectangle(5.0, 6.0)')}))"
    assert Checker(source).check_from_source() == expected
def test_247():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class StaticAccessError {
    void test() {
        string school := Student.school;    
        Student.setName("John");            
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    assert Checker(source).check_from_source() == expected
def test_248():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class StaticAccessError {
    void test() {
        Student.setName("John");                
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).setName(StringLiteral('John'))))"
    assert Checker(source).check_from_source() == expected
def test_249():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class StaticAccessValid {
    void test() {
        int count := Student.totalStudents;    
        Student s := new Student();
        string schoolName := s.school;               
        Student.resetCount();
        s.setName("John");
        s.secretMethod();
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_250():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        this.totalStudents := 0;
    }
    
    void setName(string n) {
        Student.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class StaticAccessValid {
    void test() {
        int count := Student.totalStudents;    
        string schoolName := s.school;               
        Student s := new Student();
        Student.resetCount();
        s.setName("John");
        this.secretMethod();
    }
}"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_251():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    void setName(string n) {
        Student.name := n;
    }
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class StaticAccessValid {
    void test() {
        int count := Student.totalStudents;    
        string schoolName := s.school;               
        Student s := new Student();
        Student.resetCount();
        s.setName("John");
        this.secretMethod();
    }
}"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).name))"
    assert Checker(source).check_from_source() == expected

def test_252():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class InstanceAccessError {
    void test() {
        Student s := new Student();
        int count := s.totalStudents;        
        s.resetCount();                     
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).totalStudents))"
    assert Checker(source).check_from_source() == expected
def test_253():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class InstanceAccessError {
    void test() {
        Student s := new Student();
        s.resetCount();                     
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).resetCount()))"
    assert Checker(source).check_from_source() == expected
def test_254():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class UndeclaredMemberError {
    void test() {
        Student s := new Student();
        string name := s.name;               
        s.secretMethod();                  
        s.nonExistentMethod();              
    }
}
"""
    expected = "UndeclaredMethod(nonExistentMethod)"
    assert Checker(source).check_from_source() == expected
def test_255():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ValidAccess {
    void test() {
        int count := Student.totalStudents;  
        Student s := new Student();
        Student.resetCount();               
        s.school := "New School";            
        s.setName("Alice");                 
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_256():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class GraduateStudent extends Student {
    void accessProtected() {
        this.age := 25;                          
        this.setName("Graduate");               
    }
}
class AccessError {
    void test() {
        GraduateStudent gs := new GraduateStudent();
        gs.age := 30;                          
        gs.setName("pass");                    
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_257():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class GraduateStudent extends Student {
    void accessProtected() {
        this.age := 25;                          
        this.setName("Graduate");               
    }
}
class AccessError {
    void test() {
        GraduateStudent gs := new GraduateStudent();
        gs.age := 30;                          
        gs.setName("pass");                    
        gs.secretMethod();
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_258():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ComplexAccessError {
    void complexTest() {
        Student s1 := new Student();
        Student s2 := new Student();
        
        string result := Student.school;     
        s1.secretMethod();                   
        
        s1.resetCount();                    
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(Student).school))"
    assert Checker(source).check_from_source() == expected
def test_259():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ComplexAccessError {
    void complexTest() {
        Student s1 := new Student();
        Student s2 := new Student();
        
        s1.secretMethod();                   
        
        s1.resetCount();                    
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s1).resetCount()))"
    assert Checker(source).check_from_source() == expected
def test_260():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ComplexAccessValid {
    void complexTest() {
        Student s1 := new Student();
        Student s2 := new Student();
        
        int count := Student.totalStudents;  
        string schoolName := s1.school;      
        Student.resetCount();                
        s1.setName("Alice");                 
        s2.secretMethod();
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_261():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ReferenceTypeError {
    void wrongReference() {
        Shape obj := new Student();
        #((Student)obj).setName("Test");     
    }
}
"""
    expected = "UndeclaredClass(Shape)"
    assert Checker(source).check_from_source() == expected
def test_262():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class Shape {
}
class ReferenceTypeError {
    void wrongReference() {
        Shape obj := new Student();
        #((Student)obj).setName("Test");     
    }

}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(Shape), [Variable(obj = ObjectCreation(new Student()))]))"
    assert Checker(source).check_from_source() == expected
def test_263():
    source = """
class A{
    int x := 10;
    int & ref := x;       
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected
def test_264():
    source = """
class A{
    void foo() {
        int x := 10;
        int & ref := x;       
        ref := 20;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_265():
    source = """
class A{
    void foo() {
        int x := 10;
        int & ref := x;        # ref is an alias for x
        float & ref2 := x;  
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ReferenceType(PrimitiveType(float) &), [Variable(ref2 = Identifier(x))]))"
    assert Checker(source).check_from_source() == expected
def test_266():
    source = """
class A{
void foo() {
    Rectangle r := new Rectangle(5.0, 3.0);
    Rectangle & rectRef := r;  # rectRef is an alias for r
    rectRef.length := 10.0;    # r.length also becomes 10.0
}
}
class Rectangle {
    float length;
    float width;
    
    Rectangle(float l; float w) {
        this.length := l;
        this.width := w;
    }
}"""
    expected = "UndeclaredClass(Rectangle)"
    assert Checker(source).check_from_source() == expected

def test_267():
    source = """
class Example1 {
    int factorial(int n){
        if n == 0 then return 1; else return n * this.factorial(n - 1);
    }

    void main(){
        int x;
        x := io.readInt();
        io.writeIntLn(this.factorial(x));
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_268():
    source = """
class Shape {
    float length, width;
    float getArea() {}
    Shape(float length, width){
        this.length := length;
        this.width := width;
    }
}

class Rectangle extends Shape {
    float getArea(){
        return this.length * this.width;
    }
}

class Triangle extends Shape {
    float getArea(){
        return this.length * this.width / 2;
    }
}

class Example2 {
    void main(){
        Shape s; 
        s := new Rectangle(3,4);
        io.writeFloatLn(s.getArea());
        s := new Triangle(3,4);
        io.writeFloatLn(s.getArea());
    }
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_269():
    source = """
class Rectangle {
    float length, width;
    static int count;
    
    # Default constructor
    Rectangle() {
        this.length := 1.0;
        this.width := 1.0;
        Rectangle.count := Rectangle.count + 1;
    }
    
    # Copy constructor
    # Rectangle(Rectangle other) {
    #     this.length := other.length;
    #     this.width := other.width;
    #     Rectangle.count := Rectangle.count + 1;
    # }
    
    # User-defined constructor
    Rectangle(float length; float width) {
        this.length := length;
        this.width := width;
        Rectangle.count := Rectangle.count + 1;
    }
    
    # Destructor
    ~Rectangle() {
        Rectangle.count := Rectangle.count - 1;
        io.writeStrLn("Rectangle destroyed");
    }
    
    float getArea() {
        return this.length * this.width;
    }
    
    static int getCount() {
        return Rectangle.count;
    }
}

class Example3 {
    void main() {
        # Using different constructors
        Rectangle r1 := new Rectangle();           # Default constructor
        Rectangle r2 := new Rectangle(5.0, 3.0);  # User-defined constructor
        # Rectangle r3 := new Rectangle(r2);        # Copy constructor
        
        io.writeFloatLn(r1.getArea());  # 1.0
        io.writeFloatLn(r2.getArea());  # 15.0
        # io.writeFloatLn(r3.getArea());  # 15.0
        io.writeIntLn(Rectangle.getCount());  # 3
        
        # Destructors will be called automatically when objects go out of scope
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_270():
    source = """
class ConstantTypeError {
    void foo() {
        final float pi := 3;
        final string greeting := "Hello";
        final boolean check := false;
        final int number := 100;
        pi := 3.14;
        greeting := "Hi";
        check := true;
        number := 200;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(pi) := FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_271():
    source = """
class A{
    final int a := 10;
    int a := 20;
}
"""
    expected = "Redeclared(Attribute, a)"
    assert Checker(source).check_from_source() == expected
def test_272():
    source = """
class A{
    int a := 20;
    final int a := 10;
}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected
def test_273():
    source = """
class A{
    int a(){}
    final int a := 10;
}
"""
    expected = "Redeclared(Constant, a)"
    assert Checker(source).check_from_source() == expected
def test_274():
    source = """
class A{
    final int a := 10;
    int a(){}
}
"""
    expected = "Redeclared(Method, a)"
    assert Checker(source).check_from_source() == expected
def test_275():
    source = """
class A{
}
class B extends A{
}
class C extends B{
    final A a1 := new B();
    final B b1 := new C();
}
class D extends C{
    final C c1 := new D();
    final A a2 := new C();
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_276():
    source = """
        class Test { 
                static void main() { 
                    int[3] arr := {1, 2, 3};
                    int first;
                    first := arr[0];
                    arr[1] := 42;
                }
            }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_277():
    source = """
        class Test { 
                static void main() { 
                    int[3] arr := {1, 2, 3};
                    float first;
                    first := arr[0];
                    arr[1] := 42.0;
                }
            }
        """
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(1)])) := FloatLiteral(42.0)))"
    assert Checker(source).check_from_source() == expected
def test_278():
    source = """
class Test { 
        static void main() { 
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_279():
    source = """
class Vit{ final int My1stCons := 1 + 5, My2ndCons := 2;
    float foo(){ return (3.0 + 4.0) * 2.0 / 7.0; }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_280():
    source = """
    class Vit{ final int My1stCons := vit.foo(), My2ndCons := 2;}
"""
    expected = "UndeclaredIdentifier(vit)"
    assert Checker(source).check_from_source() == expected
def test_281():
    source = """
class Vit{ final int My1stCons := 4; 
         static final string Vit;}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_282():
    source = """
class Vit{ static int x, y := 0;}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_283():
    source = """
class Vit{ final int x, y := 0;}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_284():
    source = """
        class T { void m(){ R r := new R(); } }
        """
    expected = "UndeclaredClass(R)"
    assert Checker(source).check_from_source() == expected

def test_285():
    source = """
        class R{}
        class T { void m(){ R r := new R(); } }
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_286():
    source = """
        class T { void m(){ R r := new R(); } }
        class R extends S{}
        class S{}
"""
    expected = "UndeclaredClass(R)"
    assert Checker(source).check_from_source() == expected
def test_287():
    source = """
        class T{
            int x:= 0.0;
            int x := 5;
            }
        """
    expected = "Redeclared(Attribute, x)"
    assert Checker(source).check_from_source() == expected
def test_288():
    source = """
class T{
    void m(){
        final int x := true;
        int x := 5;
    }
}
"""
    expected = "TypeMismatchInConstant(VariableDecl(final PrimitiveType(int), [Variable(x = BoolLiteral(True))]))"
    assert Checker(source).check_from_source() == expected
def test_289():
    source = """
class T{
    void m(){
        int x := true;
        int x := 5;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = BoolLiteral(True))]))"
    assert Checker(source).check_from_source() == expected

def test_290():
    source = """
class T{
    int a := 10;
    final int b := this.a;}
"""
    expected = "IllegalConstantExpression(AttributeDecl(final PrimitiveType(int), [Attribute(b = PostfixExpression(ThisExpression(this).a))]))"
    assert Checker(source).check_from_source() == expected
def test_290a():
    source = """
class T{
    int a := 10;
    final int b := a;}
"""
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected
def test_291():
    source = """
class T{
    void m(){
        int a := Student.totalStudents;
    }
}
"""
    expected = "UndeclaredIdentifier(Student)"
    assert Checker(source).check_from_source() == expected
def test_292():
    source = """
class T{
    void m(){
        int a := this.totalStudents;
    }
}
"""
    expected = "UndeclaredAttribute(totalStudents)"
    assert Checker(source).check_from_source() == expected
def test_293():
    source = """
class T{
    void m(){
        int a := this.totalStudents();
    }
}
    """
    expected = "UndeclaredMethod(totalStudents)"
    assert Checker(source).check_from_source() == expected

def test_294():
    source = """
    class T{
    void m(){
        int & ref := nil;
    }
    }
"""
    expected = "TypeMismatchInStatement(VariableDecl(ReferenceType(PrimitiveType(int) &), [Variable(ref = NilLiteral(nil))]))"
    assert Checker(source).check_from_source() == expected

def test_295():
    source = """
class MathUtils {
    static void swap(int & a; int & b) {
        int temp := a;
        a := b;
        b := temp;
    }
    
    static void modifyArray(int[5] & arr; int index; int value) {
        arr[index] := value;
    }
    
    static int & findMax(int[5] & arr) {
        int & max := arr[0];
        int i;
        for i := 1 to 4 do {
            if (arr[i] > max) then {
                max := arr[i];
            }
        }
        return max;
    }
}
class Test {
    static void main() {
        int x := 10;
        int y := 20;
        int[5] numbers := {1, 2, 3, 4, 5};
        MathUtils.swap(x, y);
        io.writeIntLn(x);  
        io.writeIntLn(y);  
        
        MathUtils.modifyArray(numbers, 2, 42);
        io.writeIntLn(numbers[2]);  
        io.writeIntLn(MathUtils.findMax(numbers));  
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_296():
    source = """
class C { int & pick(int & a) { return a; } }
class T{
    void m(){
        C c := new C();
        int x := 10;
        int & ref := c.pick(x);
        io.writeIntLn(x);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_297():
    source = """
class C { int pick(int & a) { return a; } }
class T{
    void m(){
        C c := new C();
        int x := 10;
        int ref := c.pick(x);
        io.writeIntLn(x);
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_298():
    source = """
class A{
    boolean isEven(int n){
        if n % 2 == 0 then return true; else return false;
    }
    static void main(){
        A a := new A();
        int num := 10;
        if a.isEven(num) then
            io.writeStrLn("Even");
        else
            io.writeStrLn("Odd");
    } 
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_299():
    """ Test No Entry Point based on test_013 (Inheritance) """
    source = """ 
class Animal {
    void makeSound() {
        io.writeStrLn("Some sound");
    }
}
class Dog extends Animal {
    void makeSound() { 
        io.writeStrLn("Woof!");
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_300():
    """ Test Entry Point added to test_013 """
    source = """ 
class Animal {
    void makeSound() {
        io.writeStrLn("Some sound");
    }
}
class Dog extends Animal {
    void makeSound() { 
        io.writeStrLn("Woof!");
    }
    static void main() {
        Dog d := new Dog();
        d.makeSound();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_301():
    """ Test No Entry Point based on test_014 (Shadowing) """
    source = """ 
class ShadowExample {
    int value := 100;  
    
    void method() {
        int value := 200;  
        {
            int value := 300; 
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_302():
    """ Test Entry Point added to test_014 """
    source = """ 
class ShadowExample {
    int value := 100;  
    
    void method() {
        int value := 200;  
        {
            int value := 300; 
        }
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_303():
    """ Test No Entry Point based on test_023 (Constructor/Destructor) """
    source = """
        class A {
            void foo() {}
            ~A() {}
            A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_304():
    """ Test Entry Point added to test_023 """
    source = """
        class A {
            void foo() {}
            ~A() {}
            A() {}
            static void main() {}
            }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_305():
    """ Test No Entry Point based on test_033 (Inheritance/Override) """
    source = """
        class A {
            int A;
            int x;
            }
        class B extends A {
            int A() {}
            }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_306():
    """ Test Entry Point added to test_033 """
    source = """
        class A {
            int A;
            int x;
            }
        class B extends A {
            int A() {}
            static void main() {}
            }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_307():
    """ Test No Entry Point based on test_041 (Constructor Overload) """
    source = """
        class A {
            A(){}
            A(int x; int y){}
        }
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_308():
    """ Test Entry Point added to test_041 """
    source = """
        class A {
            A(){}
            A(int x; int y){}
            static void main() {
                A a := new A();
            }
        }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_309():
    """ Test No Entry Point based on test_049 (Inherited Access) """
    source = """
class Animal {
    string species;
    
    void setSpecies(string s) {
        this.species := s;
    }
}

class Dog extends Animal {
    void identify() {
        io.writeStrLn(this.species);  
        this.setSpecies("Canine");  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_310():
    """ Test Entry Point added to test_049 """
    source = """
class Animal {
    string species;
    
    void setSpecies(string s) {
        this.species := s;
    }
}

class Dog extends Animal {
    void identify() {
        io.writeStrLn(this.species);  
        this.setSpecies("Canine");  
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_311():
    """ Test No Entry Point based on test_053 (Multi-level Inheritance) """
    source = """
class Parent {
    void greet() {
        io.writeStrLn("Hello from Parent");
    }
}
class Child extends Parent {
    void greet() {
        io.writeStrLn("Hello from Child");
    }
}
class GrandChild extends Child {
    void greet() {
        io.writeStrLn("Hello from GrandChild");
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_312():
    """ Test Entry Point added to test_053 """
    source = """
class Parent {
    void greet() {
        io.writeStrLn("Hello from Parent");
    }
}
class Child extends Parent {
    void greet() {
        io.writeStrLn("Hello from Child");
    }
}
class GrandChild extends Child {
    void greet() {
        io.writeStrLn("Hello from GrandChild");
    }
    static void main() {
        GrandChild g := new GrandChild();
        g.greet();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_313():
    """ Test No Entry Point based on test_064 (Nested Blocks) """
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int y := 20;
            {
                int z := x + y;
                io.writeIntLn(z);
            }
        }
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_314():
    """ Test Entry Point added to test_064 """
    source = """
class Test {
    void method() {
        int x := 10;
        {
            int y := 20;
            {
                int z := x + y;
                io.writeIntLn(z);
            }
        }
    }
    static void main() {
        Test t := new Test();
        t.method();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_315():
    """ Test No Entry Point based on test_093 (If Statements) """
    source = """
class Conditional
{
void check() {
    boolean flag := true;
    if flag then {  
        io.writeStrLn("Valid");
    }
    
    if !flag then { 
        io.writeStrLn("Also Valid");
    }
}
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_316():
    """ Test Entry Point added to test_093 """
    source = """
class Conditional
{
void check() {
    boolean flag := true;
    if flag then {  
        io.writeStrLn("Valid");
    }
    
    if !flag then { 
        io.writeStrLn("Also Valid");
    }
}
static void main() {}
}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_317():
    """ Test No Entry Point based on test_103 (For Loops) """
    source = """
    class ForLoopValid {
    void loop() {
        int i;
        
        for i := 0 to 10 do {  
            io.writeIntLn(i);
        }
        
        for i := -5 to 5 do {  
            io.writeIntLn(i);
        }
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_318():
    """ Test Entry Point added to test_103 """
    source = """
    class ForLoopValid {
    void loop() {
        int i;
        
        for i := 0 to 10 do {  
            io.writeIntLn(i);
        }
        
        for i := -5 to 5 do {  
            io.writeIntLn(i);
        }
    }
    static void main() {}
}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_319():
    """ Test No Entry Point based on test_115 (Assignment) """
    source = """
class AssignmentValid {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        x := 20;  
        text := "world";  
        flag := false;  
    }
}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_320():
    """ Test Entry Point added to test_115 """
    source = """
class AssignmentValid {
    void assign() {
        int x := 10;
        string text := "hello";
        boolean flag := true;
        
        x := 20;  
        text := "world";  
        flag := false;  
    }
    static void main() {}
}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_321():
    """ Test No Entry Point based on test_133 (Array Assign) """
    source = """
class ArrayValid {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        int[3] anotherIntArray := {4, 5, 6};
        
        intArray := anotherIntArray;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_322():
    """ Test Entry Point added to test_133 """
    source = """
class ArrayValid {
    void arrayAssign() {
        int[3] intArray := {1, 2, 3};
        int[3] anotherIntArray := {4, 5, 6};
        
        intArray := anotherIntArray;
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_323():
    """ Test No Entry Point based on test_145 (Method Call) """
    source = """
class CallValid {
    void processString(string value) {
        io.writeStrLn(value);
    }
    
    void test() {
        string msg := "Hello, World!";
        this.processString(msg);  
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_324():
    """ Test Entry Point added to test_145 """
    source = """
class CallValid {
    void processString(string value) {
        io.writeStrLn(value);
    }
    
    void test() {
        string msg := "Hello, World!";
        this.processString(msg);  
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_325():
    """ Test No Entry Point based on test_240 (Constants) """
    source = """
class ValidConstantExpressions {
    final int MAX_SIZE := 100;
    final int DOUBLE_SIZE := this.MAX_SIZE * 2;     
    final string MESSAGE := "Hello" ^ "World"; 
    final boolean FLAG := true && false;       
    final float PI := 3.14159;
    final float CIRCLE_AREA := this.PI * 10 * 10;   
    final int SUM := 10 + 20 + 30;         
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_326():
    """ Test Entry Point added to test_240 """
    source = """
class ValidConstantExpressions {
    final int MAX_SIZE := 100;
    final int DOUBLE_SIZE := this.MAX_SIZE * 2;     
    final string MESSAGE := "Hello" ^ "World"; 
    final boolean FLAG := true && false;       
    final float PI := 3.14159;
    final float CIRCLE_AREA := this.PI * 10 * 10;   
    final int SUM := 10 + 20 + 30;
    static void main() {
        ValidConstantExpressions v := new ValidConstantExpressions();
        io.writeIntLn(v.SUM);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_327():
    """ Test No Entry Point based on test_255 (Static Access) """
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ValidAccess {
    void test() {
        int count := Student.totalStudents;  
        Student s := new Student();
        Student.resetCount();               
        s.school := "New School";            
        s.setName("Alice");                 
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_328():
    """ Test Entry Point added to test_255 """
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
    
    static void resetCount() {
        Student.totalStudents := 0;
    }
    
    void setName(string n) {
        this.name := n;
    }
    
    void secretMethod() {
        io.writeStrLn("Secret");
    }
}
class ValidAccess {
    void test() {
        int count := Student.totalStudents;  
        Student s := new Student();
        Student.resetCount();               
        s.school := "New School";            
        s.setName("Alice");                 
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_329():
    source = """
    class A{
    static void main(){}
    static void main(){}
    }
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected
def test_330():
    source = """
    class A{
    static void main(){}
    void main(){}
    }
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected
def test_331():
    source = """
class A {
    static void main(){}
    static void main(int x; float y){}
}
"""
    expected = "Redeclared(Method, main)"
    assert Checker(source).check_from_source() == expected
def test_332():
    source = """
class A {
    static void main(){}
    static int main;
}"""
    expected = "Redeclared(Attribute, main)"
    assert Checker(source).check_from_source() == expected
def test_333():
    source = """
class A {
    static void main(int x){}
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_334():
    source = """
class A {
    static void main(float x){}
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_335():
    source = """
class A {
    static void main(int x; float y){}
}"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_336():
    source = """
class Test {
        int attr;
        static void main() {
           this.attr := 10;
        }
    }
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_337():
    source = """
class Test {
        static int attr;
        static void main() {
           this.attr := 10;
        }
    }
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_338():
    source = """
class MethodCallError {
    void printMessage() {  
        io.writeStrLn("Hello");
    }   
    int getValue() {
        return 42;
    }   
    void test() {
        int result := this.printMessage();  
}
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(ThisExpression(this).printMessage()))"
    assert Checker(source).check_from_source() == expected

def test_339():
    source = """
class C {}
class B {
    C(){
        int a;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInStatement(ConstructorDecl(C([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(a)])], stmts=[])))"
    assert Checker(source).check_from_source() == expected

def test_340():
    source = """
class C {}
class B {
    C(){
        int a;
    }
}
"""
    expected = "TypeMismatchInStatement(ConstructorDecl(C([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(a)])], stmts=[])))"
    assert Checker(source).check_from_source() == expected
def test_341():
    source = """
class Test {
    int atrr;
    static void main() {
        this.atrr := 10;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_342():
    source = """
class Test {
    static int atrr;
    void main() {
        this.atrr := 10;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).atrr))"
    assert Checker(source).check_from_source() == expected
def test_343():
    source = """
class Test {
    static int atrr;
    static void main() {
        this.atrr := 10;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_344():
    source = """
class Test{
    static int atrr;
    void main() {
        Test.atrr := 10;
    }
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_345():
    source = """
class A {static int a; int b;}
class Test{
    A a;
    static void main(){
        A.a := 1;
        A.b := 2;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).b))"
    assert Checker(source).check_from_source() == expected

def test_346():
    source = """
class Student {
    static int totalStudents := 0;
    static void resetCount() {
        this.totalStudents := 0;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_347():
    source = """
class Student {
    string name;
    int age;
    static int totalStudents := 0;
    string school := "Default School";
   
    static void resetCount() {
        Student.totalStudents := 0;
    }
}
class InstanceAccessError {
    void test() {
        Student s := new Student();
        s.resetCount();                    
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(s).resetCount()))"
    assert Checker(source).check_from_source() == expected

def test_348():
    source = """
class A extends B{
    static void main(){}
}

class B {}
"""
    expected = "UndeclaredClass(B)"
    assert Checker(source).check_from_source() == expected
def test_349():
    source = """
class B {}
class A extends B{
    static void main(){}
} 
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_350():
    source = """
class A{
    int attr;
    void foo() {
        int x := 10;
        int a := x.attr;
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_351():
    source = """
class Test {
    void main() {
        Rectangle r;
        r := new Rectangle(10.0, 5.0);
    }
}
class Rectangle {
    float length, width;
    Rectangle(float l;
    float w){
            this.length := l;
            this.width := w;
    }
    float getArea() {
        return this.length * this.width;
    }
}
"""
    expected = "UndeclaredClass(Rectangle)"
    assert Checker(source).check_from_source() == expected

def test_352():
        source = """
class A{
    int attr;
    void foo() {
        int x := 10;
        int a := this.attr;
    }
}
"""
        expected = "No Entry Point"
        assert Checker(source).check_from_source() == expected
def test_353():
        source = """
class A{
    int attr;
    void foo() {
        int x := 10;
        int f;
        int a := this.f;
    }
}
"""
        expected = "UndeclaredAttribute(f)"
        assert Checker(source).check_from_source() == expected
def test_353a():
    source = """
class A{
    int attr;
    void foo() {
        int x := 10;
        int a := this.f;
    }
}
"""
    expected = "UndeclaredAttribute(f)"
    assert Checker(source).check_from_source() == expected
def test_354():
        source = """
class A{
    float attr;
    void foo() {
        int x := 10;
        int a := this.attr;
    }
}
"""
        expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(a = PostfixExpression(ThisExpression(this).attr))]))"
        assert Checker(source).check_from_source() == expected

def test_355():
    source = """
class A{}
class B{
    A a;
    void foo() {
        int x := 10;
        A b := this.a;
    }
    static void main() {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_356():
    source = """
class C {}
class B {C c;}
class A {B b;}
class Test {
    static void main() {
        A a := new A();
        C c := a.b.c;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_357():
    source = """
class C {}
class B {C c;}
class A {B b;}
class Test {
    static void main() {
        A a := new A();
        C c := this.b.c;
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_358():
    source = """
class C {}
class B {C c;}
class A {B b;}
class Test {
    static void main() {
        int a ;
        C c := a.b.c;
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(a))"
    assert Checker(source).check_from_source() == expected

def test_359():
    source = """
class C {}
class A {} /* A không có thuộc tính b */
class Test {
    static void main() {
        A a := new A();
        C c := a.b.c; /* Lỗi: Không tìm thấy b trong A */
    }
}
"""
    # Tên lỗi phụ thuộc vào message của Checker, thường là UndeclaredAttribute("b")
    expected = "UndeclaredAttribute(b)" 
    assert Checker(source).check_from_source() == expected

def test_360():
    source = """
class C {}
class A {
    int b; /* b là int, không thể truy cập .c từ int */
}
class Test {
    static void main() {
        A a := new A();
        C c := a.b.c; /* Lỗi: a.b là int -> TypeMismatch */
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(a).b))"
    assert Checker(source).check_from_source() == expected

def test_361():
    source = """
class B {} /* B không có thuộc tính c */
class A {B b;}
class Test {
    static void main() {
        A a := new A();
        int temp := a.b.c; /* Lỗi: Không tìm thấy c trong B */
    }
}
"""
    expected = "UndeclaredAttribute(c)"
    assert Checker(source).check_from_source() == expected

def test_priority_001():
    """ Priority 1 (Redeclared) vs Priority 2 (TypeMismatch)
    Tình huống: Khai báo lại biến 'x', đồng thời gán giá trị sai kiểu (string cho int).
    Kỳ vọng: Lỗi Redeclared (1) được báo trước TypeMismatch (2).
    """
    source = """
class Test {
    void main() {
        int x := 1;
        int x := "string"; 
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_priority_002():
    """ Priority 1 (Undeclared) vs Priority 3 (IllegalMemberAccess)
    Tình huống: Sử dụng biến chưa khai báo 'undeclared' trong biểu thức có chứa lỗi truy cập 'this' trong static.
    Kỳ vọng: Lỗi Undeclared (1) được báo trước IllegalMemberAccess (3).
    """
    source = """
class Test {
    static void main() {
        int x := undeclared + this.toString(); 
    }
}
"""
    expected = "UndeclaredIdentifier(undeclared)"
    assert Checker(source).check_from_source() == expected

def test_priority_003():
    """ Priority 2 (TypeMismatch) vs Priority 3 (IllegalMemberAccess)
    Tình huống: Điều kiện IF bị sai kiểu (TypeMismatch), thân hàm chứa lỗi truy cập (IllegalMemberAccess).
    Kỳ vọng: Lỗi TypeMismatch (2) trong biểu thức điều kiện được báo trước.
    """
    source = """
class Test {
    static void main() {
        if (1 > "s") then {         # TypeMismatch (2)
            this.toString();   # IllegalMemberAccess (3)
        }
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), >, StringLiteral('s')))"
    assert Checker(source).check_from_source() == expected

def test_priority_004():
    """ Priority 3 (IllegalMemberAccess) vs Priority 4 (MustInLoop)
    Tình huống: Truy cập 'this' trong static (IllegalMemberAccess) làm điều kiện cho lệnh break (MustInLoop).
    Kỳ vọng: Lỗi IllegalMemberAccess (3) trong biểu thức được báo trước lỗi MustInLoop (4).
    """
    source = """
class Test {
    int attr;
    static void main() {
        if (this.attr > 0) then {  # IllegalMemberAccess (3)
            break;            # MustInLoop (4)
        }
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_priority_005():
    """ Priority 3 (IllegalMemberAccess) vs Priority 5 (CannotAssignToConstant)
    Tình huống: Gán giá trị vào hằng số (CannotAssignToConstant), giá trị bên phải gây lỗi truy cập (IllegalMemberAccess).
    Kỳ vọng: Lỗi IllegalMemberAccess (3) (ưu tiên cao hơn) được báo thay vì lỗi gán hằng số (5).
    """
    source = """
class Test {
    int attr;
    static void main() {
    final int C := 10;
    C := this.attr; # AssignToConst (5) vs IllegalMemberAccess (3)
    }
}
"""
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

def test_priority_006():
    """ Priority 4 (MustInLoop) vs Priority 5 (CannotAssignToConstant)
    Tình huống: Lệnh break (MustInLoop) đứng trước lệnh gán hằng số (CannotAssignToConstant) trong cùng một khối.
    Lưu ý: Do tính chất tuần tự, lỗi ở lệnh đầu tiên thường được báo trước.
    """
    source = """
class Test {
    void main() {
        final int x := 1;
        if (true) then {
            break;  # MustInLoop (4)
            x := 2; # CannotAssignToConstant (5)
        }
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_priority_007():
    """ Priority 5 (CannotAssignToConstant) vs Priority 6 (IllegalArrayLiteral)
    Tình huống: Gán một mảng literal bị lỗi (IllegalArrayLiteral) vào một biến final (CannotAssignToConstant).
    Kỳ vọng: Lỗi CannotAssignToConstant (5) được báo trước IllegalArrayLiteral (6).
    """
    source = """
class Test {
    void main() {
        final int[2] arr := {1, 2};
        arr := {1, "string"}; # AssignToConst (5) vs IllegalArrayLiteral (6)
    }
}
"""
    # Lưu ý: Kết quả này phụ thuộc vào việc trình biên dịch kiểm tra tính hợp lệ của lệnh gán (LHS) trước hay kiểm tra biểu thức (RHS) trước.
    # Theo bảng ưu tiên, expected là CannotAssignToConstant.
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(arr) := ArrayLiteral({IntLiteral(1), StringLiteral('string')})))"
    assert Checker(source).check_from_source() == expected

def test_priority_008():
    """ Priority 6 (IllegalArrayLiteral) vs Priority 7 (No Entry Point)
    Tình huống: Chương trình không có main (No Entry Point), nhưng có lỗi Array Literal trong khai báo thuộc tính.
    Kỳ vọng: Lỗi IllegalArrayLiteral (6) được báo trước No Entry Point (7).
    """
    source = """
class Test {
    int[2] arr := {1, "error"}; # IllegalArrayLiteral (6)
    # Missing main method (7)
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({IntLiteral(1), StringLiteral('error')}))"
    assert Checker(source).check_from_source() == expected

def test_priority_009():
    """ Priority 1 (Declaration) vs Priority 5 (Constant)
    Tình huống: Gán biến chưa khai báo vào hằng số.
    Kỳ vọng: Undeclared (1) > CannotAssignToConstant (5).
    """
    source = """
class Test {
    void main() {
        final int x := 10;
        x := undeclared; # AssignToConst (5) vs Undeclared (1)
    }
}
"""
    expected = "UndeclaredIdentifier(undeclared)"
    assert Checker(source).check_from_source() == expected

def test_priority_010():
    """ Priority 2 (TypeMismatch) vs Priority 4 (MustInLoop)
    Tình huống: Biểu thức điều kiện IF bị sai kiểu, bên trong có break.
    Kỳ vọng: TypeMismatch (2) > MustInLoop (4).
    """
    source = """
class Test {
    void main() {
        if (10 + "s") then { # TypeMismatch (2)
            break;      # MustInLoop (4)
        }
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(10), +, StringLiteral('s')))"
    assert Checker(source).check_from_source() == expected

def test_lms_017(): 
    source = """
class A {
    A(int x){
        final int y, z := 123;
    }
}
# final kh dc phep := -> vi la gan
# ma no chi dc la := 

"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected
def test_lms_007(): 
    """
        Kiểm tra mảng chứa biểu thức tạo đối tượng (new A()).
        Thầy xác nhận: ArrayLiteral là tập các expression.
        """
    source = """
        class A {}
        class Program {
            static void main() {
                # Mảng đối tượng được khởi tạo bằng new
                A[2] arr := {new A(), new A()}; 
            }
        }
        """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_lms_038(): 
    source = """
    class AttributeAccessError {
        void access() {
            int x := 10;
            string text := "hello";
            
            int length := text.value;  # Error: TypeMismatchInExpression at member access (if value doesn't exist)
        }
    }
"""
    expected = "TypeMismatchInExpression(Identifier(text))"
    assert Checker(source).check_from_source() == expected
def test_lms_039(): 
    source = """
class AttributeAccessError {
    void access() {
        int x := 10;
        string text := "hello";
        
        int invalid := x.length;   # Error: TypeMismatchInExpression at member access (x is not object)
    }
}

"""
    expected = "TypeMismatchInExpression(Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_2142():
    """Error: Undeclared Variable"""
    source = """
    class Example {
        void method() {
            int result := undeclaredVar + 10;  
        }
    }
"""
    expected = "UndeclaredAttribute(undeclaredVar)"


def test_5112():
    """Type mismatch in array access: E2 is int, E1 must be array"""
    source = """
class Test {
    static void main() {
        int x;
        int y := x[1];
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(x)[IntLiteral(1)]))"
    assert Checker(source).check_from_source() == expected
def test_512():
    """Type mismatch in array index: E2 is not be int"""
    source = """
class Test {
    static void main() {
        int[3] a;
        int x := a[true];
    }
}
"""
    expected = "TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected
def test_513():
    # Error: Array subscripting with wrong types
    source ="""class ArraySubscriptError {
    static void access() {
        int[5] numbers := {1, 2, 3, 4, 5};
        string[2] words := {"hello", "world"};
        
        #int value1 := numbers["index"];  # Error: TypeMismatchInExpression at array access
        #int value2 := numbers[2.5];      # Error: TypeMismatchInExpression at array access
        string word := words[true];      # Error: TypeMismatchInExpression at array access
        
        # Non-array subscripting
        int x := 10;
        int invalid := x[0];  # Error: TypeMismatchInExpression at array access
    }
}"""
    expected ="TypeMismatchInExpression([BoolLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_532_1():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static void foo() {}
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInExpression(PostfixExpression(Identifier(A).foo()))"
    assert Checker(source).check_from_source() == expected
def test_532_2():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static void foo() { return 1; }
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "TypeMismatchInStatement(ReturnStatement(return IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_532_4():
    """Type mismatch in expression: use void method in value context"""
    source = """
class A {
    static int foo() {  }
}
class Test {
    static void main() {
        int x := A.foo(); 
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_541():
    """Type mismatch in expression: attribute access on non-class"""
    source = """

class Test {
    static void main() {
        int x;
        string text := "hello";
        int y := text.value;
    }
}
"""
    expected = "TypeMismatchInExpression(Identifier(text))"
    assert Checker(source).check_from_source() == expected
def test_611():
    # Error: Type mismatch in constant declaration
    source ="""
class ConstantTypeError {
    static void main(){
        #final int a := 1.2;              # Error: TypeMismatchInConstant at constant declaration
        #final string text := 42;         # Error: TypeMismatchInConstant at constant declaration
        #final boolean flag := "true";    # Error: TypeMismatchInConstant at constant declaration
    }
    final int count := 3.14;       # TypeMismatchInConstant at constant declaration
}"""
    #expected = "TypeMismatchInConstant(Variable(a = FloatLiteral(1.2)))"
    #expected = "TypeMismatchInConstant(Variable(text = IntLiteral(42)))"
    #expected = "TypeMismatchInConstant(Variable(flag = StringLiteral('true')))"
    expected = "TypeMismatchInConstant(AttributeDecl(final PrimitiveType(int), [Attribute(count = FloatLiteral(3.14))]))"
    assert Checker(source).check_from_source() == expected 
def test_613():
    #Error: Object type mismatch
    source ="""
    class Shape{
    }
    class Integer{
        int value;
        Integer(int value){
            this.value := value;
        }
    }
    class ObjectConstantError {
        final Shape shape := new Integer(42);  #TypeMismatchInConstant - if no inheritance relationship
    }
"""
    expected ="TypeMismatchInConstant(AttributeDecl(final ClassType(Shape), [Attribute(shape = ObjectCreation(new Integer(IntLiteral(42))))]))"
    assert Checker(source).check_from_source() == expected 
def test_1042():
    source = """
class A {int coo() {return 1;} static int foo() {return 1;}}
class example{
    A a;
    static void main(){
        int x := A.foo() + A.coo();
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).coo()))"
    assert Checker(source).check_from_source() == expected
def test_1043():
    source = """
class A {static int a; int b;}
class example{
    A a;
    static void main(){
        A.a := 1;
        A.b := 2;
    }
}
"""
    expected = "IllegalMemberAccess(PostfixExpression(Identifier(A).b))"
    assert Checker(source).check_from_source() == expected
def test_1047():
        source = """
    class example{
        final int MAX_SIZE;
        static void main(){}
    }
    """
        expected = "Static checking passed"
        assert Checker(source).check_from_source() == expected
def test_this_type_check():
    """Verify 'this' has the type of the enclosing class"""
    source = """
    class B {}
    class A {
        void check() {
            A x := this;    # Hợp lệ: this có kiểu A -> gán cho biến A
            B y := this;    # Lỗi: this có kiểu A -> không thể gán cho biến B
        }
    }
    """
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(B), [Variable(y = ThisExpression(this))]))"
    assert Checker(source).check_from_source() == expected


def test_this_as_return_value():
    """Verify 'this' can be returned when return type is the class itself"""
    source = """
    class A {
        A getMe() {
            return this; # Hợp lệ: return type là A, this cũng là A
        }
        
        int getWrong() {
            return this; # Lỗi: return type là int, this là A
        }
    }
    """
    # Mong đợi lỗi ở hàm getWrong
    expected = "TypeMismatchInStatement(ReturnStatement(return ThisExpression(this)))"
    assert Checker(source).check_from_source() == expected
def test_this_as_return_value():
    """Verify 'this' can be returned when return type is the class itself"""
    source = """
    class A {
        A getMe() {
            return this; # Hợp lệ: return type là A, this cũng là A
        }
        
        int getWrong() {
            return this; # Lỗi: return type là int, this là A
        }
    }
    """
    # Mong đợi lỗi ở hàm getWrong
    expected = "TypeMismatchInStatement(ReturnStatement(return ThisExpression(this)))"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing():
    """Verify 'this.x' refers to attribute, distinguishing from parameter 'x'"""
    source = """
    class A {
        int x;
        void setX(float x) {
            # x ở đây là float (param)
            # this.x là int (attribute)
            
            this.x := x;      # Lỗi: gán float (param x) vào int (attribute this.x) -> TypeMismatch
        }
    }
    """
    # Lưu ý: OPLang thường không cho gán float vào int (coercion chỉ cho int -> float)
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)))"
    assert Checker(source).check_from_source() == expected
def test_this_access_in_static():
    """Test using 'this.x' inside a static method"""
    source = """
    class A {
        int x;
        static void main() {
            # Lỗi: Không thể dùng 'this' trong static main
            # Checker sẽ bắt lỗi ngay tại từ khóa 'this'
            io.writeInt(this.x); 
        }
    }
    """
    # Checker ném lỗi IllegalMemberAccess chứa node ThisExpression
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_assignment_in_static():
    """Test assigning 'this' to a variable inside static method"""
    source = """
    class A {
        static void main() {
            # Lỗi: 'this' không tồn tại trong ngữ cảnh static
            A a := this; 
        }
    }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_method_call_in_static():
    """Test calling 'this.foo()' inside static method"""
    source = """
    class A {
        void foo() {}
        static void main() {
            # Lỗi: Không thể dùng 'this' để gọi hàm
            this.foo();
        }
    }
    """
    # Checker vẫn báo lỗi tại 'this', không phải tại MethodCall
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing_resolution():
    """Verify 'this.x' refers to int attribute, while 'x' refers to float param"""
    source = """
    class ShadowTest {
        int x; # Attribute là INT
        
        void setX(float x) { # Parameter là FLOAT
            this.x := x;     # Lỗi: Không thể gán float (param) vào int (attribute)
        }
    }
    """
    # Lưu ý: Cấu trúc lỗi phụ thuộc vào cách bạn __str__ AST
    # Node gây lỗi là AssignmentStatement
    expected = "TypeMismatchInStatement(AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x)))"
    
    # Nếu Checker của bạn báo lỗi AssignmentStatement chứ không phải từng phần tử
    # Bạn cần điều chỉnh chuỗi expected cho khớp với thực tế chạy
    assert Checker(source).check_from_source() == expected
def test_this_method_invocation():
    """Test calling another instance method using 'this'"""
    source = """
    class Calculator {
        int result;
        
        void reset() {
            this.result := 0;
        }
        
        void compute() {
            this.reset(); # Gọi method khác qua this
            this.result := 100;
        }
        
        static void main() {
            Calculator c := new Calculator();
            c.compute();
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_this_shadowing_valid():
    """Test valid shadowing: assigning param to this.attr"""
    source = """
    class Rectangle {
        int width;
        int height;
        
        # Constructor có tham số trùng tên với attribute
        Rectangle(int width; int height) {
            this.width := width;   # Hợp lệ: gán int vào int
            this.height := height; # Hợp lệ: gán int vào int
        }
        
        static void main() {
            Rectangle r := new Rectangle(10, 20);
        }
    }
    """
    # Nếu checker đúng, nó sẽ trả về None hoặc list rỗng (tuỳ implementation của bạn)
    # Hoặc bạn có thể assert nó không raise exception
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_shadowing_behavior():
    """
    Verify that parameter shadows attribute.
    Implicit 'this' is disabled here.
    """
    source = """
    class Shadow {
        int val; # Attribute là INT
        
        # Parameter là FLOAT -> Nó sẽ che khuất attribute
        void test(float val) {
            
            # Ở đây 'val' là parameter (float)
            # Phép gán này HỢP LỆ (float := float)
            # Nếu checker nhầm 'val' là attribute (int), nó sẽ báo lỗi.
            val := 10.5; 
            
            # Để gán vào attribute, BẮT BUỘC dùng this
            # this.val := val; # Dòng này sẽ lỗi (int := float) nhưng ta đang test dòng trên
        }
        static void main(){}
    }

    """
    # Mong đợi: Không có lỗi (Static checking passed)
    # Vì val := 10.5 là gán vào parameter float
    assert Checker(source).check_from_source() == "Static checking passed"


def test_this_102():
    source = """
class Person {
    string name;
    static void abc(){
        int a := b; 
    }
}
"""
    expected = "UndeclaredIdentifier(b)"
    assert Checker(source).check_from_source() == expected
def test_this_access_static_member_error():
    """
    Test Point 6: 'this' cannot be used to access static attributes.
    Spec requires: ClassName.member for static.
    """
    source = """
    class MathUtil {
        static float PI;
        
        void setup() {
            # LỖI: PI là static, không được gọi qua 'this' (instance)
            # Đúng phải là: MathUtil.PI := 3.14;
            this.PI := 3.14; 
        }
    }
    """
    # Checker sẽ báo lỗi IllegalMemberAccess vì PI là static mà lại bị truy cập kiểu instance
    # Node lỗi là FieldAccess (this.PI) hoặc toán hạng postfix
    expected = "IllegalMemberAccess(PostfixExpression(ThisExpression(this).PI))" 
    
    # Lưu ý: Nếu checker của bạn báo lỗi cả cụm gán, hãy điều chỉnh expected
    # Dựa trên code của bạn: raise IllegalMemberAccess(op) -> FieldAccess/MemberAccess
    assert Checker(source).check_from_source() == expected
def test_polymorphism_validity():
    """
    Test Point 7: Verify static checker allows polymorphism structures.
    1. Upcasting (Subtype := Supertype)
    2. Calling inherited/overridden methods via 'this'
    """
    source = """
    class Shape {
        float getArea() { return 0.0; }
    }
    
    class Rectangle extends Shape {
        float width, height;
        
        # Override method
        float getArea() { 
            return this.width * this.height; 
        }
        
        void printArea() {
            # Gọi method qua this.
            # Static Checker chỉ cần biết getArea() tồn tại trong Rectangle (hoặc cha của nó)
            io.writeFloat(this.getArea()); 
        }
    }
    
    class Main {
        static void main() {
            # 1. Test Upcasting (Dynamic Dispatch setup)
            # Biến s kiểu Shape, nhưng giữ object Rectangle
            Shape s := new Rectangle(); 
            
            # 2. Test gọi hàm
            # Static check: Kiểm tra xem class 'Shape' có hàm getArea không? -> Có -> OK.
            s.getArea(); 
        }
    }
    """
    expect = "Static checking passed" 
    assert Checker(source).check_from_source() == expect

def test_this_inherited_members():
    """Verify 'this' can access members defined in parent class"""
    source = """
    class Parent {
        int id;
        void setId(int id) {
            this.id := id;
        }
    }
    
    class Child extends Parent {
        void update() {
            # 'id' được khai báo ở Parent.
            # 'this.id' ở Child phải hợp lệ và trỏ lên Parent.id
            this.id := 100; 
            
            # 'setId' được khai báo ở Parent
            # 'this.setId' phải hợp lệ
            this.setId(200);
        }
        static void main(){}
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_scope_block_variable_visibility():
    """
    Block scope: Variables declared in a block are only visible 
    from declaration to the end of that block.
    """
    source = """
    class BlockScopeTest {
        void main() {
            if (true) then{
                int local := 10;
                # Trong block: local hợp lệ
                local := 20; 
            }
            # Ra khỏi block: local biến mất
            # Checker phải báo lỗi UndeclaredIdentifier tại đây
            local := 30; 
        }
    }
    """
    expected = "UndeclaredIdentifier(local)"
    assert Checker(source).check_from_source() == expected

def test_scope_class_inheritance():
    """
    Class scope: Attributes are visible in subclasses.
    """
    source = """
    class Parent {
        int inheritedVar;
    }
    
    class Child extends Parent {
        void test() {
            # inheritedVar được khai báo ở Parent
            # Child phải nhìn thấy nó (thông qua this hoặc implicit)
            this.inheritedVar := 100; 
        }
        
        static void main() {
            Child c := new Child();
            c.test();
        }
    }
    """
    # Mong đợi: Không có lỗi
    assert Checker(source).check_from_source() == "Static checking passed"
def test_scope_global_static():
    """
    Global scope: Static attributes/methods are visible everywhere via ClassName.
    """
    source = """
    class GlobalConfig {
        static int MAX_USERS;
    }
    
    class UserManager {
        void check() {
            # Truy cập biến static của class khác
            # Nếu Global scope đúng, Checker sẽ tìm thấy GlobalConfig -> MAX_USERS
            GlobalConfig.MAX_USERS := 500;
        }
        static void main(){}
    }
    """
    # Mong đợi: Không có lỗi
    assert Checker(source).check_from_source() == "Static checking passed"
def test_scope_method_parameter_visibility():
    """
    Method scope: Parameters are visible throughout the method body.
    Check valid access inside nested blocks.
    """
    source = """
    class MethodScopeTest {
        void process(int param) {
            # param visible ở cấp cao nhất của method
            int y := param; 
            
            if (y > 0) then {
                # param vẫn phải visible trong block con (nested scope)
                y := param + 1;
            }
        }
        static void main(){}
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_scope_independent_blocks():
    """
    Verify two parallel blocks can declare the same variable name 
    without conflict (because the first one exits before the second enters).
    """
    source = """
    class IndependentBlocks {
        void test() {
            if (true) then {
                int temp := 1; # temp của block 1
            }
            
            if (false) then {
                int temp := 2; # temp của block 2 (độc lập)
                # Nếu logic scope sai, checker sẽ báo lỗi Redeclared tại đây
            }
        }
        static void main(){}
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"
def test_entry_point_invalid():
    """Test various invalid main signatures"""
    # 1. Main with params
    source1 = """class Program { static void main(int x) {} }"""
    assert Checker(source1).check_from_source() == "No Entry Point"

    # 2. Main not static
    source2 = """class Program { void main() {} }"""
    assert Checker(source2).check_from_source() == "No Entry Point"
    
    # 3. Main returns int
    source3 = """class Program { static int main() { return 1; } }"""
    assert Checker(source3).check_from_source() == "No Entry Point"

def test_abc():
    source = """
class Test {
void foo() {
Test test := this;
}
static void main(){}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_xyx():
    source = """
class Test {
    void foo() {
    int test := this;
    }
    static void main(){}
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(test = ThisExpression(this))]))"
    assert Checker(source).check_from_source() == expected

def test_vinh():
    source = """
        class T{
            static void main(){
                final int a := this.foo();
            }
            int foo(){return 1;}
        }
    """
    expected = "IllegalMemberAccess(ThisExpression(this))"
    assert Checker(source).check_from_source() == expected

