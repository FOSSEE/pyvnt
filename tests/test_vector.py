import pytest

from pyvnt import *

class TestVector:
    def setup_method(self, method):
        self.hprop1 = Flt_P('val1', default=1)
        self.hprop2 = Flt_P('val2', default=2)
        self.hprop3 = Flt_P('val3', default=3)
        self.hprop4 = Flt_P('val4', default=4)
        self.hprop5 = Flt_P('val5', default=5)
        self.hprop6 = Flt_P('val6', default=6)


        self.vprop1 = Vector_P('val1', self.hprop1, self.hprop2, self.hprop3)
        self.vprop2 = Vector_P('val2', self.hprop4, self.hprop5, self.hprop6)

    def teardown_method(self, method):
        del self.vprop1
        del self.vprop2
        del self.hprop1
        del self.hprop2
        del self.hprop3
        del self.hprop4
        del self.hprop5
        del self.hprop6

    def test_vector_print(self):
        assert str(self.vprop1) == f"Vector_P(name = val1, x = {self.hprop1.give_val()}, y = {self.hprop2.give_val()}, z = {self.hprop3.give_val()})"
        assert str(self.vprop2) == f"Vector_P(name = val2, x = {self.hprop4.give_val()}, y = {self.hprop5.give_val()}, z = {self.hprop6.give_val()})"
    
    def test_vector_x(self):
        assert self.vprop1.x() == 1
        assert self.vprop2.x() == 4
    
    def test_vector_y(self):
        assert self.vprop1.y() == 2
        assert self.vprop2.y() == 5
    
    def test_vector_z(self):
        assert self.vprop1.z() == 3
        assert self.vprop2.z() == 6
    
    def test_vector_magnitude(self):
        assert self.vprop1.magnitude() == 14**0.5
        assert self.vprop2.magnitude() == 77**0.5
    
    def test_vector_normalise(self):
        self.vprop1.normalise(Flt_P('tol', 0.1))
        assert self.vprop1.x() == 1/14**0.5
        assert self.vprop1.y() == 2/14**0.5
        assert self.vprop1.z() == 3/14**0.5
    
    def test_vector_give_val(self):
        assert self.vprop1.give_val() == (1, 2, 3)
        assert self.vprop2.give_val() == (4, 5, 6)
