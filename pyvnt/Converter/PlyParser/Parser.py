
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
            'COORDINATE')

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_DOLLAR = r'\$'
t_COMMA = r','
t_LPAREN=r'\('
t_RPAREN=r'\)'

t_ignore = ' \t\n'

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
    r'\d+(\.\d+)?(e[-+]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
    return t


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



# Parsing rules


def p_file(p):
    '''file : blocks'''
    p[0] = p[1]
    #print(str(lexer.lineno)+"--=================-------")

def p_blocks(p):
    '''blocks : blocks block
              | block'''
    p[0] = {**p[1] , **p[2]} if len(p) == 3 else p[1]

def p_block(p):
    '''block : WORD LBRACE statements RBRACE
             | WORD WORD SEMICOLON
             | WORD NUMBER SEMICOLON
             | WORD list_block
    '''
    if len(p) == 5:
        p[0] = {p[1]: p[3]}
    elif len(p) == 4:
        p[0] = {p[1]: p[2]}
    elif len(p) == 3:
        p[0] = {p[1]: p[2]}
    #print(p[0])



def p_list_block(p):
    '''list_block : LPAREN list_items RPAREN SEMICOLON'''
    p[0] = p[2]
    #print(p[0])

def p_list_items(p):
    '''list_items : list_items list_item
                  | list_item
                  | blocks
                  | empty'''
    if len(p) == 3:
        if p[1] is None:
            p[0] = [p[2]]
        else:
            p[0] = p[1] + [p[2]] if p[2] is not None else p[1]
    elif len(p) == 2 and p[1] is not None:
        if isinstance(p[1],dict):
            p[0]=p[1]
        else:
            p[0] = [p[1]]
    else:
        p[0] = []


def t_COORDINATE(t):
    r'\(\s*-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s*\)'
    # Process the coordinate into a tuple of numbers
    coords = t.value.strip('()').split()
    t.value = tuple(float(x) if '.' in x or 'e' in x else int(x) for x in coords)
    return t

def p_list_item(p):
    '''list_item : COORDINATE
                 | hex_item
                 | faces_item'''
    p[0] = p[1]

def p_hex_item(p):
    '''hex_item : WORD LPAREN vertex_list RPAREN LPAREN number_list RPAREN WORD LPAREN number_list RPAREN'''
    # Specifically for the 'hex' block format
    p[0] = {'type': p[1], 'vertices': p[3], 'dimensions': p[6], 'grading_type': p[8], 'gradings': p[10]}

def p_faces_item(p):
    '''faces_item : LPAREN vertex_list RPAREN'''
    p[0] = p[2]

def p_vertex_list(p):
    '''vertex_list : vertex_list NUMBER
                   | NUMBER'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_number_list(p):
    '''number_list : number_list NUMBER
                   | NUMBER'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_empty(p):
    'empty :'
    pass


def p_statements(p):
    '''statements : statements statement
                  | statement
                  | list_block'''
    if len(p) == 3:
        p[1].update(p[2])  # Merge statements
        p[0] = p[1]
    else:
        p[0] = p[1]
    #print(p[1])

def p_statement_word_word(p):
    '''statement : WORD words SEMICOLON
    '''
    p[0] = {p[1]: p[2]}

def p_statement_word_words(p):
    '''words : words WORD
            | WORD 
    '''
    if len(p)==3:
        p[1].append(p[2])
        p[0]=p[1]
    else:
        p[0] = [p[1]]

def p_statement_word_number(p):
    '''statement : WORD NUMBER SEMICOLON'''
    p[0] = {p[1]: p[2]}

def p_statement_dollar_word(p):
    '''statement : DOLLAR WORD SEMICOLON'''
    p[0] = {"$": p[2]}

def p_statement_block(p):
    '''statement : block'''
    p[0] = p[1]

def p_statement_word_list(p):
    '''statement : WORD value_list SEMICOLON'''
    p[0] = {p[1]: p[2]}

def p_value_list(p):
    '''value_list : value_list COMMA value_list
                  | value'''
    if len(p)==4:
        p[0]=p[1]+p[3]
    else:
        p[0]=[p[1]]

def p_value(p):
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



def build_tree(parent, data):
    """ Recursively builds a Foam tree from parsed fvSolution data. """
    for key, value in data.items():
        if(key=='FoamFile' or key=='$'):
            continue
        if isinstance(value, dict):
            node = Node_C(key, parent)
            build_tree(node, value)
            
        else:
            cam=None
            print(value)
            if isinstance(value,list):
                cam=value[0]
            else:
                cam=value
            prop = Key_C(key, Flt_P('val1', minimum=0, maximum=1000, default=value) 
                           if isinstance(value, float) else
                           Flt_P('val1', minimum=0, maximum=100, default=value) 
                           if isinstance(value, int) else
                           Enm_P('val1', items={cam}, default=cam))
            #print(prop)  # Add property to the parent Foam node
            parent.addData(prop)




# parsed_data_fv = parse_fvsolutions(fvsolutions_text)
# parsed_data_dic=parse_fvsolutions(control_dict_text)
# parsed_data_sch=parse_fvsolutions(fvscheme_text)
# parsed_data_block=parse_fvsolutions(blockmesh_dict)




# complete_parse_data={parsed_data_dic['FoamFile']['object']:parsed_data_dic,parsed_data_fv['FoamFile']['object']:parsed_data_fv,parsed_data_sch['FoamFile']['object']:parsed_data_sch}
# print (parsed_data_block)

# showTree(head)





# check=['p','U','transportProperties','blockMeshDict', 'controlDict', 'fvSchemes', 'fvSolution']

# complete_parse_data={}


# # Traverse through the folder
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     for file in os.listdir(file_path):
#         with open(os.path.join(file_path, file)) as tF:
#             text =tF.read()
#         complete_parse_data+={}
#         print(parse_fvsolutions(text))
#         print(file+"----------------------")


# head = Node_C('Project')
# build_tree(head,complete_parse_data)