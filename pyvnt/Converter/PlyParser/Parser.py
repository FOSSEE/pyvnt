import ply.lex as lex
import ply.yacc as yacc
from pyvnt import *
import os

folder_path = "Demo_case_files/cavity"


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

t_ignore = ' \t\n,'

def t_comm(t):
    r'/\*(.|\n)*?\*/'
    #t.lexer.lineno += t.value.count('\n')
    return None

def t_comments(t):
    r'\//.*'
    pass


def t_WORD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?(e[-+]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
    return t

# def t_COORDINATE(t):
#     r'\(\s*-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s*\)'
#     # Process the coordinate into a tuple of numbers
#     coords = t.value.strip('()').split()
#     t.value = tuple(float(x) if '.' in x or 'e' in x else int(x) for x in coords)
#     return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



# Parsing rules

def p_file(p):
    '''file : blocks'''
    node= Node_C("file")
    for value in p[1]:
        if isinstance(value,Key_C):
            node.add_data(value)
        elif isinstance(value,Node_C):
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
    listcp=List_CP(p[1])
    if isinstance(p[3][0],list):
        i=0
        for coord in p[3][0]:
            coord._Value_P__name=f"v{i}"
            i+=1
    p[0]=Key_C(p[1],List_CP(p[1],elems=[p[3][0]]))
    print(p[0])

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
    '''
    p[0]=List_CP("v", elems=[[Flt_P('x', p[2]), Flt_P('y', p[3]), Flt_P('z', p[4])]])

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
    #print(p[3])
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
    p[0]=Flt_P("value",default=p[1])

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







# def p_statements(p):
#     '''statements : statements block
#                   | block'''
#     if len(p) == 3:
#         p[0] = p[1]+[p[2]]
#     else: 
#         p[0] = [p[1]]

# def p_statement_word_word(p):
#     '''statement : WORD words SEMICOLON
#     '''
#     #print(f"Parsing WORD-WORD: {p[1]}, {p[2]}")
#     p[0]=Key_C(p[1],Enm_P(p[1],set(p[2]),p[2][0]))

# def p_statement_word_words(p):
#     '''words : words WORD
#             | WORD 
#     '''
#     if len(p)==3:
#         p[1].append(p[2])
#         p[0]=p[1]
#     else:
#         p[0] = [p[1]]

# def p_statement_word_number(p):
#     '''statement : WORD NUMBER SEMICOLON'''
#     p[0]=Key_C(p[1],Flt_P('val1', minimum=0, maximum=1000, default=p[2]))

# def p_statement_dollar_word(p):
#     '''statement : DOLLAR WORD SEMICOLON'''
#     p[0] = {"$": p[2]}

# def p_statement_block(p):
#     '''statement : block'''
#     p[0] = p[1]

# def p_statement_word_list(p):
#     '''statement : WORD value_list SEMICOLON'''
#     p[0] = {p[1]: p[2]}

# def p_list_block(p):
#     '''list_block : LPAREN list_items RPAREN SEMICOLON'''
#     p[0] = p[2]
#     #print(p[0])

# def p_list_items(p):
#     '''list_items : list_items list_item
#                   | list_item
#                   | blocks
#                   | empty'''
#     if len(p) == 3:
#         if p[1] is None:
#             p[0] = [p[2]]
#         else:
#             p[0] = p[1] + [p[2]] if p[2] is not None else p[1]
#     elif len(p) == 2 and p[1] is not None:
#         if isinstance(p[1],dict):
#             p[0]=p[1]
#         else:
#             p[0] = [p[1]]
#     else:
#         p[0] = []

# def p_list_item(p):
#     '''list_item : hex_item
#                  | faces_item'''
#     p[0] = p[1]

# def p_faces_item(p):
#     '''faces_item : LPAREN vertex_list RPAREN'''
#     p[0] = p[2]

# def p_vertex_list(p):
#     '''vertex_list : vertex_list NUMBER
#                    | NUMBER'''
#     if len(p) == 3:
#         p[0] = p[1] + [p[2]]
#     else:
#         p[0] = [p[1]]

# def p_number_list(p):
#     '''number_list : number_list NUMBER
#                    | NUMBER'''
#     if len(p) == 3:
#         p[0] = p[1] + [p[2]]
#     else:
#         p[0] = [p[1]]

def p_empty(p):
    'empty :'
    p[0]=None

# def p_value_list(p):
#     '''value_list : value_list COMMA value_list
#                   | value'''
#     if len(p)==4:
#         p[0]=p[1]+p[3]
#     else:
#         p[0]=[p[1]]

# def p_value(p):
    '''value : WORD
             | NUMBER'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse_fvsolutions(text):
    return parser.parse(text, lexer=lexer)

#Traverse through the folder
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     for file in os.listdir(file_path):
#         with open(os.path.join(file_path, file)) as tF:
#             text =tF.read()
#         tt=parse_fvsolutions(text)
#         #print(tt)
#         show_tree(tt)

tt= parse_fvsolutions(r'''/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  9
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 0.1;

vertices
(
    (0 0 0)
    (1 0 0)
    (1 1 0)
    (0 1 0)
    (0 0 0.1)
    (1 0 0.1)
    (1 1 0.1)
    (0 1 0.1)
);

blocks
(
    hex (0 1 2 3 4 5 6 7) (20 20 1) simpleGrading (1 1 1)
);



// ************************************************************************* //
''')

print (tt)
show_tree(tt)
