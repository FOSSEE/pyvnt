import pytest

from pyvnt import *

class TestList:
    def setup_method(self, method):
        self.hprop1 = Flt_P('val1', default=1)
        self.hprop2 = Flt_P('val2', default=2)
        self.hprop3 = Flt_P('val3', default=3)
        self.hprop4 = Flt_P('val4', default=4)
        self.hprop5 = Flt_P('val5', default=5)
        self.hprop6 = Flt_P('val6', default=6)

        self.lp1 = List_CP('list1', 3, elems = [[self.hprop1, self.hprop2, self.hprop3]])
        self.lp2 = List_CP('list2', 3, elems = [[self.hprop4, self.hprop5, self.hprop6]])

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
        
        
    def test_list_give_val(self):
        assert self.lp1.give_val() == (self.hprop1.give_val(), self.hprop2.give_val(), self.hprop3.give_val())
        assert self.lp2.give_val() == (self.hprop4.give_val(), self.hprop5.give_val(), self.hprop6.give_val())
    
    def test_list_get_item(self):
        assert self.lp1.get_item(0, 0) == self.hprop1
        assert self.lp1.get_item(0, 1) == self.hprop2
        assert self.lp1.get_item(0, 2) == self.hprop3
        
        assert self.lp2.get_item(0, 0) == self.hprop4
        assert self.lp2.get_item(0, 1) == self.hprop5
        assert self.lp2.get_item(0, 2) == self.hprop6
    
    def test_list_append_value(self):
        self.lp1.append_value(0, self.hprop4)
        assert self.lp1.get_item(0, 3) == self.hprop4
    
    def test_list_append_uniq_value(self):
        self.lp1.append_uniq_value(0, self.hprop4)
        assert self.lp1.get_item(0, 3) == self.hprop4
        
        with pytest.raises(KeyRepeatError):
            self.lp1.append_uniq_value(0, self.hprop4)
    
    def test_list_append_elem(self):
        self.lp1.append_elem([self.hprop4, self.hprop5, self.hprop6])
        self.lp1.get_item(1, 0)
        assert self.lp1.get_item(1, 0) == self.hprop4
        assert self.lp1.get_item(1, 1) == self.hprop5
        assert self.lp1.get_item(1, 2) == self.hprop6
        
    
    def test_list_append_uniq_elem(self):
        self.lp1.append_uniq_elem([self.hprop4, self.hprop5, self.hprop6])
        assert self.lp1.get_item(1, 0) == self.hprop4
        assert self.lp1.get_item(1, 1) == self.hprop5
        assert self.lp1.get_item(1, 2) == self.hprop6
        
        with pytest.raises(KeyRepeatError):
            self.lp1.append_uniq_elem([self.hprop4, self.hprop5, self.hprop6])
    
    