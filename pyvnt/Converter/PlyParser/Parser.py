import ply.lex as lex
import ply.yacc as yacc
from pyvnt.Reference.error_classes import ParserError
from pyvnt.Reference.basic import *
from pyvnt.Container.node import *
from pyvnt.Container.list import *
from pyvnt.Container.key import *
from pyvnt.Reference.dimension_set import *
from pyvnt.utils.show_tree import *
from pyvnt.Reference.vector import *
from pyvnt.Reference.tensor import *
import re
import ast
import os
import yaml


'''
Grammer For parser 


file : blocks

blocks : blocks block | block

block : dictionary | listblock | statement | hexEdge_items | coordlists | empty

dictionary : WORD LBRACE blocks RBRACE

listblock : WORD LPAREN blocks RPAREN SEMICOLON

hexEdge_items : hexEdge_items hexEdge_item | hexEdge_item

hexEdge_item : hex_item | edge_item

hex_item : WORD LPAREN NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RPAREN LPAREN NUMBER NUMBER NUMBER RPAREN word gradlist

edge_item : WORD number number gradlist

gradlist : coodlist | LPAREN coordlists RPAREN

coordlists : coordlists coodlist | coodlist

coodlist : LPAREN anylist RPAREN

statement : WORD anylist SEMICOLON

anylist : anylist sitem | sitem

sitem : word | number | dimension | vector | empty

vector : LPAREN NUMBER NUMBER NUMBER RPAREN

dimension : LSQUABRAC NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RSQUABRAC


This is the basic parser which works on our custom datatypes 

Todo: Add macros and code block supports 
      Currently Handling string as enum
      Implementation of tensor pending
      $asa; this pending
      not able to parse snapyHexMeshFile like suzanne.stl{ .... }
                                                key=R    values= tang ,((0 3 2 1)(4 5 6 7));
    
      Improvement of Yamle parser/writer is needed a as for list [[],[]] type 

'''

class _OpenFoamParserInternalText:

    # Basic Tokens 
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
    t_ignore = ' \t,'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comm(self,t): # Skips the multiline comment
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        return None

    def t_comments(self,t):
        r'\//.*\n'
        t.lexer.lineno+=1
        pass

    # TODO: Find Better approch for t_WORD (like we can make ast but its too over cooked)
    def t_WORD(self,t):
        r'"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*'

        if t.value.startswith('"') and t.value.endswith('"'):
            t.value = t.value[1:-1].strip()
            return t

        word_part = t.value
        current_pos_after_word = t.lexer.lexpos # Position *after* the  word
        input_stream = t.lexer.lexdata

        # Check if the character immediately after the word is an opening parenthesis
        if current_pos_after_word < len(input_stream) and input_stream[current_pos_after_word] == '(':
            paren_balance = 1
            manual_pos = current_pos_after_word + 1
            consumed_string = word_part + '('

            # Manually scan forward until parentheses are balanced 
            while manual_pos < len(input_stream) and paren_balance > 0:
                char = input_stream[manual_pos]
                consumed_string += char
                if char == '(':
                    paren_balance += 1
                elif char == ')':
                    paren_balance -= 1

                # Check for allowed character 
                allowed_inside = ",()_+-*/<>|:&%. " 

                if not (char.isalnum() or char in allowed_inside):
                     # Found a character not allowed inside
                     print(f"Warning: Invalid character '{char}' found inside potential complex token at {t.lineno}:{self.get_column(input_stream, manual_pos)}.")
                     t.value = word_part
                     t.lexer.lexpos = current_pos_after_word # Set lexer position after the simple word
                     return t

                manual_pos += 1 # Move to the next character
                
            if paren_balance == 0:
                # Successfully found balanced parentheses
                t.value = consumed_string
                t.lexer.lexpos = manual_pos # Advance lexer position past the entire match
                return t
            else:
                 # Loop finished, but parentheses are NOT balanced
                 t.value = word_part
                 t.lexer.lexpos = current_pos_after_word
                 raise ParserError("Unbalanced parentheses",t.lineno,t.lexpos - len(word_part))

        else:
            t.value = word_part
            return t

    def t_NUMBER(self,t):
        r'-?\d+(\.\d+)?([eE][-+]?\d+)?'
        t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
        return t

    def t_error(self,t):
        # print(f"Illegal character '{t.value[0]}'")
        # t.lexer.skip(1)
        column = self.get_column(t.lexer.lexdata, t.lexpos)
        raise ParserError(
            f"Illegal character '{t.value[0]}'",
            lineno=t.lineno,
            column=column
        )

    # Parsing rules

    # object == our custom data type 
    # In many parser functions we are returning object as list beacuse in p_file we are checking object type which finally come from p_blocks


    def p_file(self,p):
        '''file : blocks'''
        node= Node_C("root")
        for value in p[1]: # Geting mixed list of (Key_C,Node_C,List_Cp)
            if isinstance(value,Key_C): # If key add to data in parent node
                node.add_data(value)
            elif isinstance(value,Node_C): # if Node add child to parent Node
                node.add_child(value)
            elif isinstance(value,List_CP): # if list then it definietly will be node then add child to parent node
                node.add_child(value)
        p[0]=node

    def p_blocks(self,p):
        '''blocks : blocks block
                | block'''
        
        # Here p[1] is list and p[2] is object 

        if len(p) == 3:
            isDuplicate = False  # To check for a duplicate key
            for i, item in enumerate(p[1]):
                    if item.name == p[2].name:
                        p[1][i] = p[2]  # Replace old value with new one
                        isDuplicate = True
                        break
            if not isDuplicate:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]  # Ensure p[0] is assigned

        else:
            p[0] = [p[1]] if p[1] is not None else [[]]
        
        
        # if len(p) == 3:
        #     isDuplicate=False # to check the duplicate key
        #     print(isinstance(p[1],list))

        #     if isinstance(p[2],Key_C):
        #         for i,item in enumerate(p[1]):
        #             print(p[2].name)
        #             if item.name == p[2].name:
        #                 p[1][i] = p[2]  # Replace old value with new one
        #                 isDuplicate=True
        #                 break
        #     if isDuplicate==False:
        #         p[0] = p[1] + [p[2]]
        # else:
        #     p[0] = [p[1]] if p[1] is not None else [[]]

    def p_block(self,p):
        '''block : dictionary
                | listblock
                | statement
                | hexEdge_items
                | coordlists
                | empty'''
        p[0] = p[1] # Just returns the object 

    def p_listblock(self,p):
        '''listblock : WORD LPAREN blocks RPAREN SEMICOLON'''
        if isinstance(p[3][0],list): # if its item in list is list returns key_c with data list_cp
            i=0
            if p[3][0] and isinstance(p[3][0][0],list):
                for items in p[3][0]:
                    for item in items:
                        item._Value_P__name=f"v{i}"
                        i+=1
                p[0]= Key_C(p[1],List_CP(p[1],elems=p[3][0]))
            else:
                for items in p[3][0]:
                    items._Value_P__name=f"v{i}"
                    i+=1
                p[0]=Key_C(p[1],List_CP(p[1],elems=[p[3][0]]))
        elif isinstance(p[3][0],Node_C): # If any item is Node_c means List_cp is node 
            p[0]=List_CP(p[1],values=p[3],isNode=True)

    def p_coodlists(self,p): # return [[],[]]
        '''coordlists : coordlists coodlist
                    | coodlist
        '''
        if len(p)==3:
            p[0]=p[1]+[[p[2]]]
        else:
            p[0]=[[p[1]]]

    def p_coordlist(self,p):
        '''
        coodlist : LPAREN anylist RPAREN
        '''
        p[0]=List_CP("v", elems=[p[2]])

    def p_hexEdge_items(self,p):
        '''hexEdge_items : hexEdge_items hexEdge_item
                        | hexEdge_item
        '''
        if len(p)==3:
            p[0]=p[1]+[p[2]]
        else:
            p[0]=[p[1]]

    def p_hexEdge_item(self,p):
        '''hexEdge_item : hex_item 
                        | edge_item'''
        p[0]=p[1]

    def p_hex_item(self,p):
        '''hex_item : WORD LPAREN NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RPAREN LPAREN NUMBER NUMBER NUMBER RPAREN word gradlist'''
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
                ]])]+[p[17]]
        if isinstance(p[18][0],list):
            p[0]+=[List_CP("litsarr",elems=p[18])]
        else:
            p[0]+=p[18]
        
    def p_edge_item(self,p):
        '''edge_item : WORD number number gradlist'''
        p[0]=[Enm_P("type", {p[1]}, p[1]),p[2],p[3]]+p[4]
    
    def p_gradelist(self,p):
        '''gradlist : coodlist 
                    | LPAREN coordlists RPAREN
        '''
        if len(p)==2:
            p[0]=[p[1]]
        else:
            p[0]=p[2]
        # return [[],[]] 

    def p_dictionary(self,p):
        '''dictionary : WORD LBRACE blocks RBRACE'''
        node = Node_C(p[1])
        for value in p[3]:
            if isinstance(value,Key_C):
                node.add_data(value)
            elif isinstance(value,Node_C):
                node.add_child(value)
            elif isinstance(value,List_CP):
                if value.is_a_node():
                    node.add_child(value)
            else:
                raise ParserError(f"Unexpected block type {type(value)} found in dictionary '{p[1]}'.")
        p[0]=node

    def p_statement(self,p):
        '''statement : WORD anylist SEMICOLON'''
        key = Key_C(p[1])
        for value in p[2]:
            key.append_val(value._Value_P__name, value)
        p[0] = key

    def p_anylist(self,p):
        '''anylist : anylist sitem
                | sitem'''
        # Anylist means it can be anything like list of string ,numbers,mixed etc
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_sitem(self,p):
        '''
        sitem : word
            | number
            | dimension
            | vector
            | empty
        '''
        p[0]=p[1]

    def p_word(self,p):
        '''
        word : WORD
        '''
        p[0]=Enm_P(p[1],{p[1]},p[1])

    def p_number(self,p):
        '''
        number : NUMBER
        '''
        if isinstance(p[1],int):
            p[0]=Int_P("value",default=p[1],maximum=max(100000,p[1]),minimum=min(0,p[1]))
        else:
            p[0]=Flt_P("value",default=p[1],maximum=max(1e5,p[1]),minimum=min(0,p[1]))

    def p_vector(self,p):
        '''
        vector : LPAREN NUMBER NUMBER NUMBER RPAREN
        '''
        p[0]=Vector_P("value",Flt_P("x",default=p[2]),Flt_P("y",default=p[3]),Flt_P("z",default=p[4]))

    def p_dimension(self,p):
        '''
        dimension : LSQUABRAC NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RSQUABRAC 
        '''
        p[0]=Dim_Set_P("dim_set",p[2:9])
        #print(p[0])

    def p_empty(self,p):
        'empty :'
        p[0]=None
        
    def get_column(self,text, lexpos):
        """Calculate the column number from lexer position."""
        if text is None:
            return None
        last_newline = text.rfind('\n', 0, lexpos)
        return lexpos - last_newline

    def p_error(self,p):
        """
        Handles parsing errors and raises a structured exception.
        
        Args:
            p: The offending token causing the syntax error.
            lexer: Optional lexer object to extract more details.
        """
        if p:
            column = self.get_column(self.lexer.lexdata, p.lexpos) if self.lexer else None
            error = ParserError(
                f"Unexpected token '{p.value}' of type '{p.type}'",
                lineno=p.lineno,
                column=column,
            )
        else:
            error = ParserError("Unexpected end of file (EOF).")
        # print(error)
        raise error
    
    def parse(self,text):
        """
        Parses the given OpenFOAM text input using the defined lexer and parser.

        Args:
            text (str): The OpenFOAM text input to parse.

        Returns:
            The parsed object(Node_C).
        """
        return self.parser.parse(text, lexer=self.lexer)

class _OpenFoamParserInternalYaml:
    """
    Internal class for parsing OpenFOAM YAML files.
    Provides methods to traverse and process YAML data into a tree structure.
    """
    def __init__(self):
        self.data=None

    def traverse_dict(self, d, name="root"):
        """ Recursively build a tree structure from the dictionary 
        Args:
            d (dict): The dictionary to traverse.
            name (str): The name of the root node.

        Returns:
            Node_C: A tree structure representing the dictionary.
        """
        node = Node_C(name)
        for key, value in d.items():
            if isinstance(value, dict):
                node.add_child(self.traverse_dict(value, key))
            elif isinstance(value, list):
                listdata=self.handle_list(value, key)
                if isinstance(listdata,Key_C):
                    node.add_data(listdata)
                elif isinstance(listdata,List_CP):
                    node.add_child(listdata)
            else:
                node.add_data(self.handle_value(key, value))
        
        return node

    def handle_list(self, values, key):
        """ Handle Node list and key List 
        Args:
            values (list): The list to process.
            key (str): The key associated with the list.

        Returns:
            Key_C or List_CP: A processed representation of the list.
        """
        if not values:
            Key_C(str(key),List_CP(key, elems=[[]]))
            
        if any(isinstance(v, dict) for v in values): # Check if the list contains dictionaries
            dict_list = [self.traverse_dict(sub_value, sub_key) for v in values for sub_key,sub_value in v.items()]
            return List_CP(key, values=dict_list, isNode=True)
        
        if self.check_list(values,(int,float),7):
            dims=Dim_Set_P("dim_set",values)
            return Key_C(str(key),dims)
        

        # Process individual items in the list
        processed_items=[]
        for item in values:
            processed_items.append([self.process_list_item(item)])
        if processed_items ==[]:
            processed_items=[[]]

        return Key_C(str(key),List_CP(key, elems=processed_items))

    def process_list_item(self, item):
        """ Process list items 
        Args:
            item: The item to process.

        Returns:
            Processed representation of the item.
        """
        # print("Processsing list item : "+str(item))
        if isinstance(item, list) or item==[]: # If the item is a nested list
            elements=[]
            for val in item:
                elements.append(self.process_list_item(val))
            if self.check_list(elements,(Int_P,Flt_P),7):
                dim_values = [e.give_val() for e in elements]
                return Dim_Set_P("dim_set", dim_values)
            return List_CP("V", elems=[elements])
        elif isinstance(item, (str, float, int)):
            return self.strOrintOrfloat(item)
        return item

    def check_list(self,lst, data_type, expected_length):
        """
        Checks if a list matches a specific data type and length.

        Args:
            lst (list): The list to check.
            data_type (type): The expected data type of the elements.
            expected_length (int): The expected length of the list.

        Returns:
            bool: True if the list matches the criteria, False otherwise.
        """
        return all(isinstance(item, data_type) for item in lst) and len(lst) == expected_length

    def handle_value(self, key, value):
        """ Handle individual non-list/non-dictionary values 
        Args:
            key (str): The key associated with the value.
            value: The value to process.

        Returns:
            Key_C: A key-value representation of the value.
        """
        key_obj = Key_C(str(key))
        if isinstance(value,str):
            value=self.parse_openfoam_entries(value)
            for i in value:
                if isinstance(i,tuple):
                    i=list(i)
                i=self.process_list_item(i)
                key_obj.append_val(i._Value_P__name,i)
            return key_obj
        val=self.process_list_item(value)
        key_obj.append_val(val._Value_P__name,val)
        return key_obj

    def strOrintOrfloat(self,value):
        """
        Parse OpenFoam Case File and return the resulting object.
        
        Args:
            path (str): Path to the Case File Or a single
            
        Returns:
            if string returns Enm_p
            if Scientific notation return Flt_p
        """
        val=value
        try:
            if isinstance(value,str):
                val=float(value)
        except ValueError:
            return Enm_P(val, {val}, val)


        # Define min and max bounds for numerical values
        max=1e5
        min=0
        if val>max:
            max=val
        if val<min:
            min=val

        # Return the value as a float or integer with bounds
        if isinstance(val,float):
            return Flt_P("v", val,minimum=min,maximum=max)
        elif isinstance(val,int):
            return Int_P("v", val,minimum=int(min),maximum=int(max))

    def preprocess_openfoam_literals(self,s): # Replace space separated values inside brackets or parentheses with comma-separated values
        def replacer(match):
            open_bracket = match.group(1)
            content = match.group(2)
            close_bracket = match.group(3)
            # Insert commas between elements
            return f"{open_bracket}{', '.join(content.split())}{close_bracket}"
        
        # Regex matches either [ ... ] or ( ... )
        pattern = r'(\[|\()([^\[\]\(\)]+)(\]|\))'
        
        # Replace all matches in the string
        return re.sub(pattern, replacer, s)

    def parse_openfoam_entries(self,s):
        s_processed = self.preprocess_openfoam_literals(s)
    
        # Tokenize by matching lists, tuples, or other non-space sequences
        tokens = re.findall(r'\[.*?\]|\(.*?\)|\S+', s_processed)
        parsed = []
        for token in tokens:
            try:
                # Safely evaluate Python literals
                parsed.append(ast.literal_eval(token))
            except Exception:
                # If evaluation fails, keep as string
                parsed.append(token)
        return parsed

    def parseYaml(self,text:str):
        """
        Parses YAML file and returns the resulting tree structure.

        Args:
            text (str): The YAML to parse.

        Returns:
            Node_C: A tree structure representing the parsed YAML data.
        """
        self.data=yaml.safe_load(text)
        return self.traverse_dict(d=self.data)

class OpenFoamParser:
    """
    Main class for parsing OpenFOAM files and directories.
    Provides methods to parse individual files or entire case directories.
    """
    def __init__(self):
        self._parseInternalText=_OpenFoamParserInternalText()
        self._parseInternalYaml=_OpenFoamParserInternalYaml()

    def parse_file(self,text :str=None,fileType :str='txt',path:str=None):
        """
        Parses an OpenFOAM file and returns the resulting object.

        Args:
            text (str): The input text to parse. Defaults to None.
            fileType (str): The type of file ('txt' or 'yaml'). Defaults to 'txt'.
            path (str): The path to the file. Defaults to None.

        Returns:
            The parsed object structure(Node tree) or None if the file is invalid.
        """
        if path!=None:
            filename=os.path.basename(path)
            filename_root, ext = os.path.splitext(filename)
            if os.path.isfile(path):
                with open(path, 'r') as tF:
                    text = tF.read()
            else:
                print("Path does not to file")
                return None
            if ext in ('','.txt'):
                parsed=self._parseInternalText.parse(text)
            elif ext=='.yaml':
                parsed=self._parseInternalYaml.parseYaml(text)
            parsed.name=filename_root
        elif text!=None:
            if text==None:
                print("Please enter filetype")
            if fileType=='txt':
                parsed=self._parseInternalText.parse(text)
            elif fileType=='yaml':
                parsed=self._parseInternalYaml.parseYaml(text)
            else:
                print("This File Formate supported")
        return parsed

    def parse_case(self,path :str):
        """
        Parse OpenFoam Case File and return the entire case tree.
        
        Args:
            path (str): Path to the Case File Or a single
            
        Returns:
            The parsed node object 
        """
        masterNode = Node_C(os.path.basename(os.path.normpath(path)))
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):  # If it's a folder, process it recursively
                folderNode = self.parse_case(file_path)
                masterNode.add_child(folderNode)
            elif os.path.isfile(file_path):  # If it's a file, process it
                filnode = self.parse_file(path=file_path)
                filnode.name=filename
                masterNode.add_child(filnode)
        return masterNode

    def get_value(self,node:Node_C,*keys):
        """
        Retrieves a value from the parsed tree structure using a sequence of keys.

        Args:
            node (Node_C): The root node of the tree.
            keys (str): Sequence of keys to traverse the tree.

        Returns:
            The value corresponding to the keys .
        """
        result = node  # Start with the root object
        for key in keys:
            found = False  # Flag to check if key is found
            datas=None
            if (isinstance(result,(Key_C, Node_C))):
                datas=result.get_data() + [result.get_child(key)]
            elif isinstance(result,List_CP):
                datas=result.get_elems() + list(result.children)
            for data in datas:
                if isinstance(data, (Key_C, Node_C)) and data.name == key:
                    result = data
                    found = True
                    break
                elif isinstance(data,List_CP) and data.is_a_node() and data.name:
                    result = data
                    found = True
                    break
            if not found:
                return None  # Return None if any key in the Parsed Tree is not found
        return result
