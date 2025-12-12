# OPLang Compiler - Static Semantic Analysis

## Overview
This project implements Assignment 3: Static Semantic Analysis for the OPLang programming language compiler. The static checker analyzes the Abstract Syntax Tree (AST) to detect semantic errors before runtime.

## Project Status
**Completed** - All 100 test cases in `tests/viet.py` pass successfully.

## Error Types Implemented
The static checker detects the following 10 semantic error types:

1. **Redeclared** - Duplicate declarations of classes, methods, attributes, variables, constants, parameters
2. **UndeclaredIdentifier/UndeclaredClass/UndeclaredAttribute/UndeclaredMethod** - Using undefined identifiers
3. **CannotAssignToConstant** - Attempting to modify final/constant values
4. **TypeMismatchInStatement** - Type errors in statements (assignments, if conditions, for loops, returns)
5. **TypeMismatchInExpression** - Type errors in expressions (operators, method calls, array access)
6. **TypeMismatchInConstant** - Type errors in constant declarations
7. **MustInLoop** - break/continue statements outside of loop constructs
8. **IllegalConstantExpression** - Non-constant expressions in constant declarations
9. **IllegalArrayLiteral** - Array literals with mixed element types
10. **IllegalMemberAccess** - Static/instance member access violations

## Project Structure
```
├── src/
│   ├── grammar/
│   │   └── OPLang.g4           # ANTLR4 grammar definition
│   ├── astgen/
│   │   └── ast_generation.py   # AST generation from parse tree
│   ├── semantics/
│   │   ├── static_checker.py   # Static semantic analyzer
│   │   └── static_error.py     # Error class definitions
│   └── utils/
│       ├── nodes.py            # AST node definitions
│       └── visitor.py          # Visitor pattern base class
├── tests/
│   ├── viet.py                 # 100 test cases (10 per error type)
│   ├── test_checker.py         # Original test suite
│   └── utils.py                # Test utilities
├── build/                      # Generated ANTLR parser/lexer
└── external/
    └── antlr-4.13.2-complete.jar
```

## Key Implementation Details

### Static Checker (src/semantics/static_checker.py)
- Uses visitor pattern to traverse AST
- Maintains class table with attributes, methods, constructors, destructors
- Tracks variable scopes with stack-based approach
- Validates type compatibility for assignments and expressions
- Enforces static/instance member access rules

### Recent Changes (December 2025)
- Added `_require_class_defined()` for validating class types in declarations
- Updated grammar to support nested block statements
- Fixed constructor/destructor redeclaration detection
- Improved BoolLiteral string formatting (True/False)
- Added class type validation for parameters and variables

## Running Tests
```bash
cd /home/runner/workspace
PYTHONPATH=. python -m pytest tests/viet.py -v --timeout=10
```

## Building Grammar
```bash
java -jar external/antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -no-listener -o build src/grammar/OPLang.g4
```

## Dependencies
- Python 3.12
- antlr4-python3-runtime
- pytest
- pytest-html
- pytest-timeout
- Java (for ANTLR grammar compilation)
