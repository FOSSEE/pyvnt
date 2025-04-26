import pytest
from pathlib import Path
from pyvnt import *

DICT_PATH = Path("tests/dicts")

@pytest.fixture
def parser():
    return OpenFoamParser()

class TestOpenFoamParser:

    def test_empty_file(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "emptyFile"))
        assert isinstance(tt, Node_C)
        assert tt.name == "emptyFile"
        assert tt.data == []
        assert tt.children == ()

    def test_single_dict(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "singleDict"))
        val = parser.get_value(tt, "key1", "key1")
        assert isinstance(val, Key_C)
        keys = list(val.get_keys())
        items = list(val.get_items())
        assert keys[0] == "value"
        assert items[0][1]._Enm_P__default == "value"

    def test_single_empty_dict(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "singleEmptyDict"))
        block = parser.get_value(tt, "key1")
        assert isinstance(block, Node_C)
        assert block.children == ()
        assert block.data == []

    def test_duplicate_entry_dict(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "duplicateEntryDict"))
        key1_val = parser.get_value(tt, "key1")
        assert isinstance(key1_val, Key_C)
        assert list(key1_val.get_keys())[0] == "value3"
        assert list(key1_val.get_items())[0][1]._Enm_P__default == "value3"

        key2_val = parser.get_value(tt, "key2")
        assert isinstance(key2_val, Key_C)
        assert list(key2_val.get_keys()) == ["value1", "value2"]

    def test_all_possible_values(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "allPossibleValuesDict"))

        key1 = parser.get_value(tt, "key1")
        assert isinstance(key1, Key_C)
        assert set(key1.get_keys()) == {"word1", "word2", "string1"}

        key2 = parser.get_value(tt, "key2")
        assert isinstance(key2, Key_C)
        assert list(key2.get_items())[0][1].give_val() == 12

        key3 = parser.get_value(tt, "key3")
        assert isinstance(key3, Key_C)
        assert list(key3.get_items())[0][1].give_val() == 1.23

        key4 = parser.get_value(tt, "key4")
        assert isinstance(key4, Key_C)
        assert list(key4.get_items())[0][1].give_val() == (4, 2, 5)

        key5 = parser.get_value(tt, "key5")
        assert isinstance(key5, Key_C)
        assert list(key5.get_items())[0][1].give_val() == [0, 1, 0, 0, 0, 0, 0]

        key5 = parser.get_value(tt, "key6")
        assert isinstance(key5, Key_C)
        assert list(key5.get_items())[0][1].give_val() == 1e-256

        key5 = parser.get_value(tt, "key7")
        assert isinstance(key5, Key_C)
        assert list(key5.get_items())[0][1].give_val() == 1e+256

    def test_nested_dict_parsing(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "nestedDictWithKeys"))

        nod1 = parser.get_value(tt, "key9")
        assert isinstance(nod1, Node_C)

        val1 = parser.get_value(tt, "key9", "key1")
        assert isinstance(val1, Key_C)
        assert list(val1.get_keys())[0] == "value1"
        assert list(val1.get_items())[0][1]._Enm_P__default == "value1"

        val2 = parser.get_value(tt, "key9", "key2")
        assert isinstance(val2, Key_C)
        assert list(val2.get_keys())[0] == "value2"
        assert list(val2.get_items())[0][1]._Enm_P__default == "value2"

        key3 = parser.get_value(tt, "key9", "key3")
        assert isinstance(key3, Node_C)

        key3_val1 = parser.get_value(key3, "key1")
        assert isinstance(key3_val1, Key_C)
        assert list(key3_val1.get_keys())[0] == "value1"
        assert list(key3_val1.get_items())[0][1]._Enm_P__default == "value1"

        key3_key2 = parser.get_value(key3, "key2")
        assert isinstance(key3_key2, Node_C)

        key3_key2_val1 = parser.get_value(key3_key2, "key1")
        assert isinstance(key3_key2_val1, Key_C)
        assert list(key3_key2_val1.get_keys())[0] == "value1"
        assert list(key3_key2_val1.get_items())[0][1]._Enm_P__default == "value1"

        key3_key2_val2 = parser.get_value(key3_key2, "key2")
        assert isinstance(key3_key2_val2, Key_C)
        assert list(key3_key2_val2.get_keys())[0] == "value2"
        assert list(key3_key2_val2.get_items())[0][1]._Enm_P__default == "value2"

    def test_vertices_list(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "verticesList"))
        vertices = parser.get_value(tt, "vertices")
        assert isinstance(vertices, Key_C)
        assert not isinstance(vertices, Node_C)
        assert len(list(vertices.get_items())[0][1].get_elems()) == 8

    def test_list_of_dicts(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "nodeList"))
        key1_list = parser.get_value(tt, "key1")
        assert isinstance(key1_list, List_CP)
        assert key1_list.is_a_node()

        first_dict = key1_list.children[0]
        type_key = parser.get_value(first_dict, "key2", "type")
        assert isinstance(type_key, Key_C)
        assert list(type_key.get_items())[0][0] == "wall"

    def test_fvSchemes(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "fvSchemes"))

        ddt_scheme = parser.get_value(tt, "ddtSchemes", "default")
        assert isinstance(ddt_scheme, Key_C)
        assert list(ddt_scheme.get_items())[0][0] == "Euler"

        grad_default = parser.get_value(tt, "gradSchemes", "default")
        assert isinstance(grad_default, Key_C)
        assert list(grad_default.get_keys()) == ["Gauss", "linear"]

        for field in ["div(phi,U)", "div(phi,k)", "div(phi,epsilon)", "div(phi,Yi_h)"]:
            div_scheme = parser.get_value(tt, "divSchemes", field)
            assert isinstance(div_scheme, Key_C)
            assert list(div_scheme.get_keys()) == ["Gauss", "upwind"]

        for field in ["div(U)", "div(((rho*nuEff)*dev2(T(grad(U)))))"]:
            div_scheme = parser.get_value(tt, "divSchemes", field)
            assert isinstance(div_scheme, Key_C)
            assert list(div_scheme.get_keys()) == ["Gauss", "linear"]

        laplacian = parser.get_value(tt, "laplacianSchemes", "default")
        assert isinstance(laplacian, Key_C)
        assert list(laplacian.get_keys()) == ["Gauss", "linear", "orthogonal"]

        non_existent = parser.get_value(tt, "divSchemes", "nonExistentDiv")
        assert non_existent is None

    def test_simple_dict(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "simpleDict"))

        key1 = parser.get_value(tt, "key1")
        assert isinstance(key1, Key_C)
        assert list(key1.get_items())[0][1].give_val() == 25

        key2 = parser.get_value(tt, "key2")
        assert isinstance(key2, Key_C)
        assert list(key2.get_items())[0][1].give_val() == 35.8

        key3 = parser.get_value(tt, "key3")
        assert isinstance(key3, Key_C)
        assert list(key3.get_items())[0][1].give_val() == "value1"

        node_key4 = parser.get_value(tt, "key4")
        assert isinstance(node_key4, Node_C)

        nested_key = parser.get_value(node_key4, "key41")
        assert isinstance(nested_key, Key_C)
        assert list(nested_key.get_items())[0][1].give_val() == "value1"

        node_key5 = parser.get_value(tt, "key5")
        assert isinstance(node_key5, List_CP)

        nested_deep = parser.get_value(node_key5, "key30", "key31")
        assert isinstance(nested_deep, Key_C)
        assert list(nested_deep.get_items())[0][1].give_val() == "value1"

        key6_list = parser.get_value(tt, "key6")
        assert isinstance(key6_list, Key_C)
        assert isinstance(list(key6_list.get_items())[0][1], List_CP)

    def test_fvSchemes(self, parser):
        tt = parser.parse_file(path=str(DICT_PATH / "fvSchemes"))
        dd = parser.parse_file(path=str(DICT_PATH/"listnode"))
        assert [name.name for name in tt._ordered_items]==['FoamFile', 'ddtSchemes', 'gradSchemes', 'divSchemes', 'laplacianSchemes']
        assert [name.name for name in dd._ordered_items]==['key1', 'FoamFile', 'blocks', 'key2', 'boundary']
        assert list(parser.get_value(dd,'boundary','movingWall','faces').get_items())[0][1].get_elems()[0][0]==List_CP('v0',elems=[[Int_P("value", default = 3, minimum = 0, maximum = 100000), 
                                                                                                                                    Int_P("value", default = 7, minimum = 0, maximum = 100000), 
                                                                                                                                    Int_P("value", default = 6, minimum = 0, maximum = 100000), 
                                                                                                                                    Int_P("value", default = 2, minimum = 0, maximum = 100000)]])