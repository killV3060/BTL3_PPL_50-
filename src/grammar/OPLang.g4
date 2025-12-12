grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text[1:]);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text[1:]);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: class_decl_list EOF; // write for program rule here using vardecl and funcdecl
//ASCIIZ:
    //Newline
    // BLANK: [ \t\f\r];
    // NEWLINE: '\n';

//Comment:
COMMENT: ('/*' .*? ('*/' | EOF) | '#' ~[\r\n]* ('\n' | EOF)) -> skip;
// ILLEGAL_COMMENT_ESCAPE: '/*' .*? {raise UncloseString(result.text[1:])} ;

//Reserved Key Word: NOT in this project


//Special TOKEN must precced "ID", if not -> error
    CLASS: 'class';
    EXTEND: 'extends';
    INT: 'int';
    FLOAT: 'float';
    STRING: 'string';
    BOOL: 'boolean';
    VOID: 'void';
    MAIN: 'main';
    THIS: 'this';
    STA: 'static';
    FIN: 'final';
    IF: 'if';
    THEN: 'then';
    ELSE: 'else';
    FOR: 'for';
    TO: 'to';
    DO: 'do';
    BREAK: 'break';
    CON: 'continue';
    DOWNTO: 'downto';
    RETURN: 'return';
    NIL: 'nil';
    

//Literal type:
    BOOLLIT: 'true' | 'false'; 
    INTLIT: [0-9]+;
    

    FLOATLIT: [0-9]+ '.' [0-9]*
            | [0-9]+ '.' [0-9]+ ('E' | 'e') ('+'|'-'| ) [0-9]+
            | [0-9]+ ('E' | 'e') ('+'|'-'| ) [0-9]+;//Replaced '.' and '+,-' to TOKEN

    // ILLEGAL_INITLIT: ([0-9]+ [A-Za-z_]+)+ {raise ErrorToken(self.text);} ;
    // ILLEGAL_FLOATLIT: ('.'* [0-9]+ '.'*)+ ([A-Za-z_]+ '.'* ('+'|'-'| ) '.'* [0-9]*)* '.'* {raise ErrorToken(self.text);}; //
    
    
    // number: INTLIT | FLOATLIT;

    STRINGLIT: '"' (ESCAPE | ~[\\"\r\n])* '"'{self.text = self.text[1:-1]}; //Add more Unclosed or Illegal Escape
    fragment ESCAPE: '\\' [bft"\\];

    // string: STRINGLIT;


//Array:
    array: LB (arraylist_intlit | arraylist_floatlit | arraylist_stringlit | arraylist_nillit) RB;

    arraylist_intlit: INTLIT COMMA arraylist_intlit | INTLIT;
    arraylist_floatlit: FLOATLIT COMMA arraylist_floatlit | FLOATLIT;
    arraylist_stringlit: STRINGLIT COMMA arraylist_stringlit | STRINGLIT;
    arraylist_nillit: NIL COMMA arraylist_nillit | NIL;
//Other special character:
    SEMI: ';';
    LB: '{';
    RB: '}';
    REF: '&';
    LRB: '(';
    RRB: ')';
    LSB: '[';
    RSB: ']';
    COMMA: ',';
    DOT: '.';
    COLON: ':';

//Operator:
    //Regular
    ADD: '+';
    SUB: '-';
    MUL: '*';
    INTDIV: '\\';
    FLOATDIV: '/';
    MOD: '%';

    //Compare
    EQ: '==';
    NEQ: '!=';
    LESST: '<';
    LESSEQ: '<=';
    MORET: '>';
    MOREEQ: '>=';

    //Logic
    OR: '||';
    AND: '&&';
    NOT: '!';

    //Other
    NEW: 'new';
    CONCAT: '^';
    ASSIGN: ':=';
//Type:
    func_type: type | VOID;
    type: primitivetype | arraytype | classtype;
    primitivetype: INT|FLOAT|STRING|BOOL;
    arraytype: arraytype_primitive | arraytype_non_primitive;
    arraytype_primitive: primitivetype LSB INTLIT RSB;
    arraytype_non_primitive: ID LSB INTLIT RSB;
    referencetype: (primitivetype | classtype | arraytype) REF;
    classtype: ID;

//Main:
    main_func: VOID MAIN;

//Statement:
    //Block statement:
    blockstm: LB var_decl_stm stmlist RB;
    stmlist: stm stmlist| ; //Note: Added stmlist to have recursive
    stm: assingstm | ifstm | forstm | breakstm | continuestm | returnstm | invocationstm;

        //Assign statement
        assingstm: (ID | ID LSB expr RSB | invocationstm_frame) vardecl_assign SEMI; //Added SEMI
        vardecl_assign: ASSIGN expr; //Seperate for assignment of initiated variable

        //If statement
        ifstm: IF (LRB expr RRB | expr) THEN (stm | blockstm) elsestm; //Review //Added LRB, RRB
        elsestm: ELSE (stm | blockstm) | ;
        //For statement
        forstm: FOR ID ASSIGN (LRB expr RRB | expr) (TO|DOWNTO) (LRB expr RRB | expr) DO (blockstm | stm); //Review

        //Break + Continue + Return statement
        breakstm: BREAK SEMI; //Review
        continuestm: CON SEMI; //Review
        returnstm: RETURN expr SEMI; //Review

        //Invocation statement
        invocationstm: invocationstm_frame SEMI;
        invocationstm_frame: expr dotting; //(in_attribute_access | sta_attribute_access | in_method | sta_method);//Copy from expression
        // in_attribute_access: expr DOT ID;
        // sta_attribute_access: ID DOT ID;
        // in_method: expr DOT callfuncstm;
        // sta_method: ID DOT callfuncstm;

        //Call function statement:
        callfuncstm: ID LRB input_func_param_list RRB;
        input_func_param_list: input_func_param_prime | ; //nullable 4, YES sep SEMI
        input_func_param_prime: input_func_param COMMA input_func_param_prime | input_func_param;
        input_func_param: INTLIT | FLOATLIT | STRINGLIT | ID | expr;

//Declare:
    decl : (attr_decl|func_decl) decl| ;
//Class Declaration:
class_decl_list: class_decl class_decl_list| class_decl; // non-nullable 1 class
    class_decl: CLASS ID LB class_member RB //Replaced ID -> class_type
                | CLASS ID EXTEND ID LB class_member RB; //
    //NOT in this Project: Check duplicate
        ID: [a-zA-Z_][a-zA-Z0-9_]*;
        

    attr_decl: stafin type attr_decl_list SEMI | stafin referencetype attr_decl_list_ref SEMI; 
    attr_decl_list: attr_name (vardecl_assign| ) COMMA attr_decl_list | attr_name (vardecl_assign| ); //non-nullable 3, YES sep COMMA
    attr_decl_list_ref: attr_name vardecl_assign COMMA attr_decl_list_ref | attr_name vardecl_assign;
    attr_name: ID ; //(assign_stm | )

    class_member: decl; //null-able var or fun 2, NO sep
//Function/Method Declaration:
func_decl: normal_func | constructor | destructor; 
    normal_func: (STA | ) main_func LRB RRB blockstm 
                | (STA | ) (func_type | referencetype) ID LRB func_param_list RRB blockstm;
    //NOT in this Project: Check duplicate?
        // ID: [a-zA-Z_][a-zA-Z0-9_]*;
        //Block Statement:

    constructor: default_constructor | copy_constructor | user_constructor;
    //YES:
    // - Have no return type
    //NOT in this Project about Constructor:
    // - Have the same name as the class
    // - Cannot contain return statements in the body
    // - Are automatically called when creating objects with `new`
        default_constructor: ID LRB RRB blockstm;
        copy_constructor: ID LRB ID ID RRB blockstm;
        user_constructor: ID LRB func_param_list RRB blockstm;
    
    destructor: '~' ID LRB RRB blockstm;
    //YES: 
    // - Has the same name as the class preceded by `~`
    // - Takes no parameters
    // - Has no return type
    ///NOT in this Project about Constructor:
    // - Cannot contain return statements in the body
    // - Is automatically called when the object goes out of scope or is garbage collected
    // - Is used primarily for cleanup operations, not memory deallocation (since OPLang uses garbage collection)
        
        // RETYPE: TYPE | VOID;

    func_param_list: func_param_prime | ; //nullable 4, YES sep SEMI
    func_param_prime: (type | referencetype) func_param SEMI func_param_prime | (type | referencetype) func_param;
    func_param: var_name COMMA func_param | var_name;
    
        
//Variable/Attribute Declaration:
var_decl_stm: var_decl_no_stafin var_decl_stm | ;

var_decl_no_stafin: (FIN | ) type var_decl_list SEMI | (FIN | ) referencetype var_decl_list_ref SEMI; 

var_decl: stafin type var_decl_list SEMI | stafin referencetype var_decl_list_ref SEMI; 

    //Check duplicate: Not in this Project ?
        stafin: STA FIN|FIN STA|STA|FIN| ;
    var_decl_list: var_name (vardecl_assign| ) COMMA var_decl_list | var_name (vardecl_assign| ); //non-nullable 3, YES sep COMMA
    var_decl_list_ref: var_name vardecl_assign COMMA var_decl_list_ref | var_name vardecl_assign;
    var_name: ID ; //(assign_stm | )




//Expression:
    expr: expr1 (LESST | LESSEQ | MORET | MOREEQ) expr1 | expr1;
    expr1: expr2 (EQ | NEQ) expr2 | expr2;
    expr2: expr2 (AND | OR) expr3 | expr3;
    expr3: expr3 (ADD | SUB) expr4 | expr4;
    expr4: expr4 (MUL | INTDIV | FLOATDIV | MOD) expr5 | expr5;
    expr5: expr5 CONCAT expr6 | expr6;
    expr6: NOT expr6 | expr7;
    expr7: (ADD|SUB) expr7 | expr8;
    expr8: expr8 LSB expr RSB | expr9;
    dotting: DOT (ID | callfuncstm | ID LSB expr RSB) dotting | DOT (ID | callfuncstm| ID LSB expr RSB);
    expr9: expr9 dotting | expr10;
    expr10: NEW expr10 | expr11;
    expr11: INTLIT | FLOATLIT | STRINGLIT | BOOLLIT | ID | callfuncstm | array | THIS | NIL | LRB expr RRB;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: .; //TODO
ILLEGAL_ESCAPE: '"' (ESCAPE | ~[\\"\r\n])* '\\' ~[bft"\\];
UNCLOSE_STRING: '"' (ESCAPE | ~[\\"\r\n])* ('\r' | '\n' | EOF);