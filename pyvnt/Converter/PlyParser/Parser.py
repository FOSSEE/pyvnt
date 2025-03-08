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
            'COORDINATE',
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
    r'\d+(\.\d+)?(e[-+]?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
    return t

def t_COORDINATE(t):
    r'\(\s*-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s+-?\d+(\.\d+)?(e[-+]?\d+)?\s*\)'
    # Process the coordinate into a tuple of numbers
    coords = t.value.strip('()').split()
    t.value = tuple(float(x) if '.' in x or 'e' in x else int(x) for x in coords)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



# Parsing rules


# def p_file(p):
#     '''file : blocks'''
#     p[0]=Node_C("file",None,children=p[1])
#     print(p[0])



def p_file(p):
    '''file : blocks'''
    p[0] = Node_C("file", None, children=p[1][0])
    for data in p[1][1]:
        p[0].add_data(data)
    #print(p[0])


def p_blocks(p):
    '''blocks : blocks block
               | block'''
    
    if len(p) == 3:
        if p[2][0]:
            p[1][0].append(p[2][0])
        if p[2][1]:
            p[1][1].append(p[2][1])
        p[0] = p[1]
        #print(p[2])
    else:
        p[0] = [[], []]
        if p[1][0]:
            p[0][0].append(p[1][0])
        if p[1][1]:
            p[0][1].append(p[1][1])
    #print(p[0])
    

def p_block(p):
    '''block : WORD dimension
             | WORD dictbody
             | WORD list_block
    '''

    #print(p[2])

    p[0] = [None, None]
    
    # Check if second element is Dim_Set_P (dimension)
    if len(p) == 3 and isinstance(p[2], Dim_Set_P):
        p[0][1] = Key_C("Dimension", p[2])
    else:
        # Create a new node with the word as name
        node = Node_C(p[1])
        
        # Process the dictbody or list_block
        if len(p) >= 3:
            # Handle node children (Node_C objects)
            if isinstance(p[2][0], Node_C):
                for child in p[2]:
                    node.add_child(child)
            # Handle node data (Key_C objects)
            elif isinstance(p[2][0], Key_C):
                #print(p[2])
                for data in p[2]:
                    node.add_data(data)
            elif isinstance(p[2][0],list):
                for pair in p[2]:
                    for element in pair:
                        if isinstance(element, Node_C):
                            node.add_child(element)
                        elif isinstance(element, Key_C):
                            #print(p[2])
                            node.add_data(element)


        #print(node)
        p[0][0] = node

def p_dictionaries(p):
    '''dictionaries :
    '''    

def p_dimension(p):
    '''
    dimension : LSQUABRAC NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RSQUABRAC SEMICOLON
    '''
    p[0]=Dim_Set_P("dim_set",p[2:9])

def p_dictbody(p):
    '''
    dictbody : LBRACE statements RBRACE
    '''
    p[0]=p[2]
    # print("statements ===========================")
    # print(p[0])
    

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1]+[p[2]]
    else: 
        p[0] = [p[1]]
    

    #print(p[0])

def p_statement_word_word(p):
    '''statement : WORD words SEMICOLON
    '''
    #print(f"Parsing WORD-WORD: {p[1]}, {p[2]}")
    p[0]=Key_C(p[1],Enm_P(p[1],set(p[2]),p[2][0]))

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
    p[0]=Key_C(p[1],Flt_P('val1', minimum=0, maximum=1000, default=p[2]))

def p_statement_dollar_word(p):
    '''statement : DOLLAR WORD SEMICOLON'''
    p[0] = {"$": p[2]}

def p_statement_block(p):
    '''statement : block'''
    p[0] = p[1]

def p_statement_word_list(p):
    '''statement : WORD value_list SEMICOLON'''
    p[0] = {p[1]: p[2]}


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


# Traverse through the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    for file in os.listdir(file_path):
        with open(os.path.join(file_path, file)) as tF:
            text =tF.read()
        tt=parse_fvsolutions(text)
        #print(tt)
        show_tree(tt)

