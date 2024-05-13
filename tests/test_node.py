import pytest

from pyvnt import *

class TestNode:
    def setup_method(self, method):
        self.items = {'PCG', 'PBiCG', 'PBiCGStab'}

        self.eprop2 = EnumProp('val2', items=self.items, default='PBiCG')
        self.eprop1 = EnumProp('val1', items=self.items, default='PCG') 

        self.key1 = KeyData('solver', self.eprop1, self.eprop2)
        self.key2 = KeyData('solver2', self.eprop2, self.eprop1)

        self.head = Foam("test_head", None, None)
        self.chld1 = Foam("test_child", self.head, None, self.key2)
        self.chld2 = Foam("test_child2", None, None)
    
    def teardown_method(self, method):
        del self.head
        del self.key1
        del self.eprop1
        del self.eprop2
        del self.items
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_node_print(self):
        assert str(self.head) == f"Foam(name : test_head, parent : None, children : ({self.chld1}, {self.chld2}, ), data : ({self.key1}, ), )"

    def test_node_add_child(self):
        self.head.addChild(self.chld2)
        assert self.head.children == (self.chld1, self.chld2, )
    
    def test_node_set_parent(self):
        self.chld2.setParent(self.head)
        assert self.chld2.parent == self.head
    
    def test_node_get_child(self):
        assert self.head.getChild('test_child') == self.chld1
    
    def test_node_add_data(self):
        self.chld2.addData(self.key2)
        assert self.chld2.data == [self.key2]

        self.chld2.addData(self.key1, 0)
        assert self.chld2.data == [self.key1, self.key2]
    
    def test_node_remove_data(self):
        self.chld1.removeData(self.key2)
        assert self.chld1.data == []
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_node_terminal_display(self):
        pass
    
    