import pytest

from pyvnt import *

class TestNode:
    def setup_method(self, method):
        self.items = {'PCG', 'PBiCG', 'PBiCGStab'}

        self.eprop2 = Enm_P('val2', items=self.items, default='PBiCG')
        self.eprop1 = Enm_P('val1', items=self.items, default='PCG') 

        self.key1 = Key_C('solver', self.eprop1, self.eprop2)
        self.key2 = Key_C('solver2', self.eprop2, self.eprop1)

        self.head = Node_C("test_head", None, None)
        self.chld1 = Node_C("test_child", self.head, None, self.key2)
        self.chld2 = Node_C("test_child2", None, None)
    
    def teardown_method(self, method):
        del self.head
        del self.key1
        del self.eprop1
        del self.eprop2
        del self.items
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_node_print(self):
        assert str(self.head) == f"Node_C(name : test_head, parent : None, children : ({self.chld1}, {self.chld2}, ), data : ({self.key1}, ), )"

    def test_node_add_child(self):
        self.head.add_child(self.chld2)
        assert self.head.children == (self.chld1, self.chld2, )
    
    def test_node_set_parent(self):
        self.chld2.set_Parent(self.head)
        assert self.chld2.parent == self.head
    
    def test_node_get_child(self):
        assert self.head.get_child('test_child') == self.chld1
    
    def test_node_add_data(self):
        self.chld2.add_data(self.key2)
        assert self.chld2.data == [self.key2]

        self.chld2.add_data(self.key1, 0)
        assert self.chld2.data == [self.key1, self.key2]
    
    def test_node_remove_data(self):
        self.chld1.remove_data(self.key2)
        assert self.chld1.data == []
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_node_terminal_display(self):
        pass
    
    