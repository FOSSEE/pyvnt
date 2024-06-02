import pytest

from pyvnt import *

class TestVector:
    def setup_method(self, method):
        self.hprop1 = PropertyFloat('val1', default=1)
        self.hprop2 = PropertyFloat('val2', default=2)
        self.hprop3 = PropertyFloat('val3', default=3)
        self.hprop4 = PropertyFloat('val4', default=4)
        self.hprop5 = PropertyFloat('val5', default=5)
        self.hprop6 = PropertyFloat('val6', default=6)


        self.vprop1 = PropertyVector('val1', self.hprop1, self.hprop2, self.hprop3)
        self.vprop2 = PropertyVector('val2', self.hprop4, self.hprop5, self.hprop6)

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
        assert str(self.vprop1) == f"PropertyVector(name = val1, x = {self.hprop1.giveVal()}, y = {self.hprop2.giveVal()}, z = {self.hprop3.giveVal()})"
        assert str(self.vprop2) == f"PropertyVector(name = val2, x = {self.hprop4.giveVal()}, y = {self.hprop5.giveVal()}, z = {self.hprop6.giveVal()})"
    
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
        self.vprop1.normalise(PropertyFloat('tol', 0.1))
        assert self.vprop1.x() == 1/14**0.5
        assert self.vprop1.y() == 2/14**0.5
        assert self.vprop1.z() == 3/14**0.5