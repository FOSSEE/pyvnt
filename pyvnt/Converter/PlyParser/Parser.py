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
import yaml

class _OpenFoamParserInternalText:

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
    t_ignore = ' \t,"'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comm(self,t):
        r'/\*(.|\n)*?\*/'
        return None

    def t_comments(self,t):
        r'\//.*'
        pass

    def t_WORD(self,t):
        r'[a-zA-Z_][+\-<>(),.\*|a-zA-Z_0-9&%:]*'
        return t

    def t_NUMBER(self,t):
        r'-?\d+(\.\d+)?([eE][-+]?\d+)?'
        t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
        return t

    def t_error(self,t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Parsing rules

    def p_file(self,p):
        '''file : blocks'''
        node= Node_C("File")
        for value in p[1]:
            if isinstance(value,Key_C):
                node.add_data(value)
            elif isinstance(value,Node_C):
                node.add_child(value)
            elif isinstance(value,List_CP):
                node.add_child(value)
        p[0]=node

    def p_blocks(self,p):
        '''blocks : blocks block
                | block'''
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
        '''block : dictnary
                | listblock
                | statement
                | hex_item
                | coordlists
                | empty'''
        p[0] = p[1]

    def p_listblock(self,p):
        '''listblock : WORD LPAREN blocks RPAREN SEMICOLON'''
        if isinstance(p[3][0],list):
            i=0
            for coord in p[3][0]:
                coord._Value_P__name=f"v{i}"
                i+=1
            p[0]=Key_C(p[1],List_CP(p[1],elems=[p[3][0]]))
        elif isinstance(p[3][0],Node_C):
            p[0]=List_CP(p[1],values=p[3],isNode=True)

    def p_coodlists(self,p):
        '''coordlists : coordlists coodlist
                    | coodlist
        '''
        if len(p)==3:
            p[0]=p[1]+[p[2]]
        else:
            p[0]=[p[1]]

    def p_coordlist(self,p):
        '''
        coodlist : LPAREN NUMBER NUMBER NUMBER RPAREN
                | LPAREN NUMBER NUMBER NUMBER NUMBER RPAREN
        '''
        if len(p)==6:
            p[0]=List_CP("v", elems=[[Flt_P('x', p[2]), Flt_P('y', p[3]), Flt_P('z', p[4])]])
        else:
            p[0]=List_CP("v", elems=[[Flt_P('x', p[2]), Flt_P('y', p[3]), Flt_P('z', p[4]),Flt_P('k', p[5])]])

    def p_hex_item(self,p):
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
        
    def p_dictnary(self,p):
        '''dictnary : WORD LBRACE blocks RBRACE'''
        node = Node_C(p[1])
        for value in p[3]:
            if isinstance(value,Key_C):
                node.add_data(value)
            elif isinstance(value,Node_C):
                node.add_child(value)
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
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_sitem(self,p):
        '''
        sitem : word
            | number
            | vector
            | dimension
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
        max=1e5
        min=0
        if p[1]>max:
            max=p[1]
        if p[1]<min:
            min=p[1]
        p[0]=Flt_P("value",default=p[1],maximum=max,minimum=min)

    def p_vector(self,p):
        '''
        vector : LPAREN NUMBER NUMBER NUMBER RPAREN
        '''
        p[0]=Vector_P("value",Flt_P("int_prop",default=p[2]),Flt_P("int_prop",default=p[3]),Flt_P("int_prop",default=p[4]))

    def p_dimension(self,p):
        '''
        dimension : LSQUABRAC NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER RSQUABRAC 
        '''
        p[0]=Dim_Set_P("dim_set",p[2:9])
        #print(p[0])

    def p_empty(self,p):
        'empty :'
        p[0]=None
        
    def p_error(self,p):
        if p:
            print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
        else:
            print("Syntax error at EOF")

    def parse(self,text):
        return self.parser.parse(text, lexer=self.lexer)

class _OpenFoamParserInternalYaml:
    def __init__(self):
        self.data=None
        self.tt=None

    # def traverse_dict(self, d, name="root"):
    #     """ Recursively build a tree structure from the dictionary """
    #     node = Node_C(name)
    #     print(d)
    #     for key, value in d.items():
    #         if isinstance(value, dict):                # If value is a dictionary, create a new node and recurse
    #             child_node = self.traverse_dict(value, key)
    #             node.add_child(child_node)
    #         elif isinstance(value,list):
    #             if any(isinstance(v, dict) for v in value):                # If there is a dictionary in list, create a new list node and  recurse the dictionaries
    #                 dictlist=[]
    #                 for v in value:
    #                     for sub_key, sub_value in v.items():
    #                         child_node = self.traverse_dict(sub_value, sub_key)
    #                         dictlist.append(child_node)
    #                 listnode = List_CP(key,values=dictlist, isNode=True)
    #                 node.add_child(listnode)
    #             else:
    #                 # For normal list
    #                 cordslist=[]
    #                 for item in value:
    #                     vallist=[]
    #                     if isinstance(item,list):
    #                         i=0
    #                         for val in item:
    #                             vallist.append(Flt_P(f'v{i}',val))
    #                             i+=1
    #                         tt=List_CP(f'V',elems=[vallist])
    #                         cordslist.append(tt)
    #                     elif isinstance(item,str):
    #                         enp=Enm_P(item,{item},item)
    #                         cordslist.append(enp)
    #                     elif isinstance(item,(float,int)):
    #                         cordslist.append(Flt_P(f'v',item))

    #                 listcp=List_CP(key,elems=[cordslist])
    #                 key_obj=Key_C(str(key),listcp)
    #                 node.add_data(key_obj)
    #         else:
    #             # If value is not a dictionary, create a Key_C object
    #             key_obj = Key_C(str(key))
    #             if isinstance(value,str):
    #                 enmpList=value.split()
    #                 if(len(enmpList)>1):
    #                     for value in enmpList:
    #                         enp=Enm_P(value,{value},value)
    #                         key_obj.append_val(enp._Value_P__name, enp)
    #                 else :
    #                     enp=Enm_P(enmpList[0],{enmpList[0]},enmpList[0])
    #                     key_obj.append_val(enp._Value_P__name, enp)
    #             elif isinstance(value ,(float,int)):
    #                 flt=Flt_P('v',value)
    #                 key_obj.append_val(flt._Value_P__name,flt)

    #             node.add_data(key_obj)

    #     return node
    
    def traverse_dict(self, d, name="root"):
        """ Recursively build a tree structure from the dictionary """
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
        """ Handle Node list and key List """
        if any(isinstance(v, dict) for v in values):
            dict_list = [self.traverse_dict(sub_value, sub_key) for v in values for sub_key,sub_value in v.items()]
            return List_CP(key, values=dict_list, isNode=True)
        
        if self.check_list(values,(int,float),7):
            dims=Dim_Set_P("dim_set",values)
            return Key_C(str(key),dims)
        
        processed_items = [self.process_list_item(item) for item in values]
        
        return Key_C(str(key),List_CP(key, elems=[processed_items]))

    def process_list_item(self, item):
        """ Process list items """
        if isinstance(item, list):
            elments=[]
            for val in item:
                elments.append(self.strOrintOrfloat(val))
            return List_CP("V", elems=[elments])
        elif isinstance(item, str):
            return self.strOrintOrfloat(item)
        elif isinstance(item, (float, int)):
            return self.strOrintOrfloat(item)
        return item

    def check_list(self,lst, data_type, expected_length):
        return all(isinstance(item, data_type) for item in lst) and len(lst) == expected_length

    def handle_value(self, key, value):
        """ Handle individual non-list/non-dictionary values """
        key_obj = Key_C(str(key))
        if isinstance(value, str):
            for val in value.split():
                key_obj.append_val(val, self.strOrintOrfloat(val))
        elif isinstance(value, (float, int)):
            key_obj.append_val("v", self.strOrintOrfloat(value))
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

        max=1e5
        min=0
        if val>max:
            max=val
        if val<min:
            min=val
        if isinstance(val,float):
            return Flt_P("v", val,minimum=min,maximum=max)
        elif isinstance(val,int):
            return Int_P("v", val,minimum=int(min),maximum=int(max))

    def parseYaml(self,text:str):
        self.data=yaml.safe_load(text)
        return self.traverse_dict(d=self.data)

class OpenFoamParser:
    def __init__(self):
        self._parseInternalText=_OpenFoamParserInternalText()
        self._parseInternalYaml=_OpenFoamParserInternalYaml()

    def parse_file(self,text :str=None,fileType :str='txt',path:str=None):
        """
        Parse OpenFoam file and return the resulting object.
        
        Args:
            text (str): The input text to parse
            
        Returns:
            The parsed object structure
        """
        if path!=None:
            ext = os.path.splitext(path)[1]
            filename=os.path.basename(path)
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
            parsed.name=filename
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
        Parse OpenFoam Case File and return the resulting object.
        
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
