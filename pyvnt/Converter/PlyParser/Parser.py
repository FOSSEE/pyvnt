import ply.lex as lex
import ply.yacc as yacc
from pyvnt.Reference.error_classes import IncorrectLengthError
from pyvnt.Reference.basic import *
from pyvnt.Container.node import *
from pyvnt.Container.list import *
from pyvnt.Container.key import *
from pyvnt.Reference.dimension_set import *
from pyvnt.utils.show_tree import *
from pyvnt.Reference.vector import *
from pyvnt.Reference.tensor import *
import os


tokens = (
            'WORD', 
            'NUMBER',
            'LBRACE',
            'RBRACE',
            'SEMICOLON',
            'DOLLAR',
            'COMMA',
            'LPAREN',
            'RPAREN',
            'LSQUABRAC',
            'RSQUABRAC'
            )

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_DOLLAR = r'\$'
t_COMMA = r','
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LSQUABRAC=r'\['
t_RSQUABRAC=r'\]'

t_ignore = ' \t\n,"'

def t_comm(t):
    r'/\*(.|\n)*?\*/'
    return None

def t_comments(t):
    r'\//.*'
    pass

def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(\(\s*([a-zA-Z_][a-zA-Z0-9_]*\s*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)?\s*\))?'
    return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?(e[-+]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parsing rules

def p_file(p):
    '''file : blocks'''
    node= None
    for data in p[1][0].get_data():
        if data.name=="object":
            k,p1=list(data.get_items())[0]
            node=Node_C(str(k))

    for value in p[1]:
        if isinstance(value,Key_C):
            node.add_data(value)
        elif isinstance(value,Node_C):
            node.add_child(value)
        elif isinstance(value,List_CP):
            node.add_child(value)
    p[0]=node

def p_blocks(p):
    '''blocks : blocks block
              | block'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]] if p[1] is not None else [[]]

def p_block(p):
    '''block : dictnary
            | listblock
            | statement
            | hex_item
            | coordlists
            | empty'''
    p[0] = p[1]

def p_listblock(p):
    '''listblock : WORD LPAREN blocks RPAREN SEMICOLON'''
    if isinstance(p[3][0],list):
        i=0
        for coord in p[3][0]:
            coord._Value_P__name=f"v{i}"
            i+=1
        p[0]=Key_C(p[1],List_CP(p[1],elems=[p[3][0]]))
    elif isinstance(p[3][0],Node_C):
        p[0]=List_CP(p[1],values=p[3],isNode=True)

def p_coodlists(p):
    '''coordlists : coordlists coodlist
                  | coodlist
    '''
    if len(p)==3:
        p[0]=p[1]+[p[2]]
    else:
        p[0]=[p[1]]

def p_coordlist(p):
    '''
    coodlist : LPAREN NUMBER NUMBER NUMBER RPAREN
             | LPAREN NUMBER NUMBER NUMBER NUMBER RPAREN
    '''
    if len(p)==6:
        p[0]=List_CP("v", elems=[[Flt_P('x', p[2]), Flt_P('y', p[3]), Flt_P('z', p[4])]])
    else:
        p[0]=List_CP("v", elems=[[Flt_P('x', p[2]), Flt_P('y', p[3]), Flt_P('z', p[4]),Flt_P('z', p[5])]])

def p_hex_item(p):
    '''hex_item : WORD LPAREN NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RPAREN LPAREN  NUMBER NUMBER NUMBER RPAREN WORD LPAREN  NUMBER NUMBER NUMBER RPAREN'''
    p[0]=[Enm_P("type", {p[1]}, p[1]),
            List_CP("faces", elems=[[
                Int_P("v0", p[3]),
                Int_P("v1", p[4]),
                Int_P("v2", p[5]),
                Int_P("v3", p[6]),
                Int_P("v4", p[7]),
                Int_P("v5", p[8]),
                Int_P("v6", p[9]),
                Int_P("v7", p[10])
            ]]),
            List_CP("res", elems=[[
                Int_P("nx", p[13]),
                Int_P("ny", p[14]),
                Int_P("nz", p[15])
            ]]),
            Enm_P("grading", {"simpleGrading"}, "simpleGrading"),
            List_CP("simpleGrading", elems=[[
                Int_P("x", p[19]),
                Int_P("y", p[20]),
                Int_P("z", p[21])
            ]])]
    
def p_dictnary(p):
    '''dictnary : WORD LBRACE blocks RBRACE'''
    node = Node_C(p[1])
    for value in p[3]:
        if isinstance(value,Key_C):
            node.add_data(value)
        elif isinstance(value,Node_C):
            node.add_child(value)
    p[0]=node

def p_statement(p):
    '''statement : WORD anylist SEMICOLON'''
    key = Key_C(p[1])
    for value in p[2]:
        key.append_val(value._Value_P__name, value)
    p[0] = key

def p_anylist(p):
    '''anylist : anylist sitem
               | sitem'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_sitem(p):
    '''
    sitem : word
          | number
          | vector
          | dimension
    '''
    p[0]=p[1]

def p_word(p):
    '''
    word : WORD
    '''
    p[0]=Enm_P(p[1],{p[1]},p[1])

def p_number(p):
    '''
    number : NUMBER
    '''
    p[0]=Flt_P("value",default=p[1],maximum=1e5)

def p_vector(p):
    '''
    vector : LPAREN NUMBER NUMBER NUMBER RPAREN
    '''
    p[0]=Vector_P("value",Flt_P("int_prop",default=p[2]),Flt_P("int_prop",default=p[3]),Flt_P("int_prop",default=p[4]))

def p_dimension(p):
    '''
    dimension : LSQUABRAC NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RSQUABRAC 
    '''
    p[0]=Dim_Set_P("dim_set",p[2:9])
    #print(p[0])

def p_empty(p):
    'empty :'
    p[0]=None
    
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer=lexer)


def parse_file(text :str):
    """
    Parse OpenFoam file and return the resulting object.
    
    Args:
        text (str): The input text to parse
        
    Returns:
        The parsed object structure
    """
    return parse(text)

def parse_case(path :str):
    """
    Parse OpenFoam Case File and return the resulting object.
    
    Args:
        path (str): Path to the Case File
        
    Returns:
        The parsed node object
    """
    masterNode = Node_C(os.path.basename(os.path.normpath(path)))

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):  # If it's a folder, process it recursively
            folderNode = parse_case(file_path)
            masterNode.add_child(folderNode)
        elif os.path.isfile(file_path):  # If it's a file, process it
            with open(file_path, 'r') as tF:
                text = tF.read()
            tempText = parse(text)
            masterNode.add_child(tempText)
    return masterNode
