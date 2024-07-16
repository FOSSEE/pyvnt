import pytest

from pyvnt import *

class TestList:
    def setup_method(self, method):
        self.hprop1 = PropertyFloat('val1', default=1)
        self.hprop2 = PropertyFloat('val2', default=2)
        self.hprop3 = PropertyFloat('val3', default=3)
        self.hprop4 = PropertyFloat('val4', default=4)
        self.hprop5 = PropertyFloat('val5', default=5)
        self.hprop6 = PropertyFloat('val6', default=6)

        self.lp1 = PropertyList('list1', 3, elems = [[self.hprop1, self.hprop2, self.hprop3]])
        self.lp2 = PropertyList('list2', 3, elems = [[self.hprop4, self.hprop5, self.hprop6]])

    def teardown_method(self, method):
        del self.hprop1
        del self.hprop2
        del self.hprop3
        del self.hprop4
        del self.hprop5
        del self.hprop6
        
        del self.lp1
        del self.lp2

    def list_print(self):
        assert str(self.lp1) == f"(name: 'list1', values: {[self.hprop1, self.hprop2, self.hprop3]})"
        assert self.lp1.size() == 3
        
        
    def test_list_giveVal(self):
        assert self.lp1.giveVal() == (self.hprop1.giveVal(), self.hprop2.giveVal(), self.hprop3.giveVal())
        assert self.lp2.giveVal() == (self.hprop4.giveVal(), self.hprop5.giveVal(), self.hprop6.giveVal())
    
    def test_list_getItem(self):
        assert self.lp1.getItem(0, 0) == self.hprop1
        assert self.lp1.getItem(0, 1) == self.hprop2
        assert self.lp1.getItem(0, 2) == self.hprop3
        
        assert self.lp2.getItem(0, 0) == self.hprop4
        assert self.lp2.getItem(0, 1) == self.hprop5
        assert self.lp2.getItem(0, 2) == self.hprop6
    
    def test_list_append_value(self):
        self.lp1.append_value(0, self.hprop4)
        assert self.lp1.getItem(0, 3) == self.hprop4
    
    def test_list_append_uniq_value(self):
        self.lp1.append_uniq_value(0, self.hprop4)
        assert self.lp1.getItem(0, 3) == self.hprop4
        
        with pytest.raises(KeyRepeatError):
            self.lp1.append_uniq_value(0, self.hprop4)
    
    def test_list_append_elem(self):
        self.lp1.append_elem([self.hprop4, self.hprop5, self.hprop6])
        self.lp1.getItem(1, 0)
        assert self.lp1.getItem(1, 0) == self.hprop4
        assert self.lp1.getItem(1, 1) == self.hprop5
        assert self.lp1.getItem(1, 2) == self.hprop6
        
    
    def test_list_append_uniq_elem(self):
        self.lp1.append_uniq_elem([self.hprop4, self.hprop5, self.hprop6])
        assert self.lp1.getItem(1, 0) == self.hprop4
        assert self.lp1.getItem(1, 1) == self.hprop5
        assert self.lp1.getItem(1, 2) == self.hprop6
        
        with pytest.raises(KeyRepeatError):
            self.lp1.append_uniq_elem([self.hprop4, self.hprop5, self.hprop6])
    
    