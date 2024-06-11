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

        self.lp1 = PropertyList('list1', 3, [self.hprop1, self.hprop2, self.hprop3])
        self.lp2 = PropertyList('list2', 3, [self.hprop4, self.hprop5, self.hprop6])

    def teardown_method(self, method):
        del self.hprop1
        del self.hprop2
        del self.hprop3
        del self.hprop4
        del self.hprop5
        del self.hprop6
        del self.lp1
        del self.lp2

    def test_list_print(self):
        assert str(self.lp1) == f"PropertyList(name : list1, values : [{self.hprop1}, {self.hprop2}, {self.hprop3}])"
        assert str(self.lp2) == f"PropertyList(name : list2, values : [{self.hprop4}, {self.hprop5}, {self.hprop6}])"
    
    def test_list_size(self):
        assert self.lp1.size() == 3
        assert self.lp2.size() == 3
    
    def test_list_getItem(self):
        assert self.lp1.getItem(0) == self.hprop1
        assert self.lp1.getItem(1) == self.hprop2
        assert self.lp1.getItem(2) == self.hprop3
        assert self.lp2.getItem(0) == self.hprop4
        assert self.lp2.getItem(1) == self.hprop5
        assert self.lp2.getItem(2) == self.hprop6
    
    def test_list_giveVal(self):
        assert self.lp1.giveVal() == (1, 2, 3)
        assert self.lp2.giveVal() == (4, 5, 6)
    
    def test_list_append_value(self):
        self.lp1.append_value(self.hprop4)
        assert self.lp1.size() == 4
        assert self.lp1.getItem(3) == self.hprop4
    
    def test_list_append_uniq_value(self):
        self.lp1.append_uniq_value(self.hprop4)
        assert self.lp1.size() == 4
        assert self.lp1.getItem(3) == self.hprop4
        with pytest.raises(KeyRepeatError):
            self.lp1.append_uniq_value(self.hprop4)
        
    def test_list_checkSimilarData(self):
        assert self.lp1.checkSimilarData() == True
        assert self.lp2.checkSimilarData() == True
        self.lp1.append_value(PropertyInt('val', default=1))
        assert self.lp1.checkSimilarData() == False
        self.lp1.append_value(PropertyFloat('val', default=1))
        assert self.lp1.checkSimilarData() == False
        self.lp2.append_value(PropertyFloat('val', default=1))
        assert self.lp2.checkSimilarData() == True
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_list_writeOut(self):
        with open('test.txt', 'w') as f:
            self.lp1.writeOut(f)
        with open('test.txt', 'r') as f:
            assert f.read() == f"{self.lp1._PropertyList__values}\n"
        import os
        os.remove('test.txt')
    
    @pytest.mark.skip(reason = 'Complex to test')
    def test_list_writeOut_wrong_type(self):
        with pytest.raises(TypeError):
            self.lp1.writeOut('test.txt')
    
    def test_list_eq(self):
        assert self.lp1 == self.lp1
        assert self.lp1 != self.lp2