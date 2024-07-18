from pyvnt import *

class TestTensor:
    def setup_method(self, method):
        self.hprop1 = Flt_P('val1', default=1)
        self.hprop2 = Flt_P('val2', default=2)
        self.hprop3 = Flt_P('val3', default=3)
        self.hprop4 = Flt_P('val4', default=4)
        self.hprop5 = Flt_P('val5', default=5)
        self.hprop6 = Flt_P('val6', default=6)
        self.hprop7 = Flt_P('val7', default=7)
        self.hprop8 = Flt_P('val8', default=8)
        self.hprop9 = Flt_P('val9', default=9)

        self.tprop1 = Tensor_P('val1', [self.hprop1, self.hprop2, self.hprop3, self.hprop4, self.hprop5, self.hprop6, self.hprop7, self.hprop8, self.hprop9])
        self.tprop2 = Tensor_P('val2', [self.hprop4, self.hprop5, self.hprop6, self.hprop7, self.hprop8, self.hprop9, self.hprop1, self.hprop2, self.hprop3])
    
    def teardown_method(self, method):
        del self.tprop1
        del self.tprop2
        del self.hprop1
        del self.hprop2
        del self.hprop3
        del self.hprop4
        del self.hprop5
        del self.hprop6
        del self.hprop7
        del self.hprop8
        del self.hprop9
    
    def test_val_returns(self):
        assert self.tprop1.xx() == 1
        assert self.tprop1.xy() == 2
        assert self.tprop1.xz() == 3

        assert self.tprop1.yx() == 4
        assert self.tprop1.yy() == 5
        assert self.tprop1.yz() == 6

        assert self.tprop1.zx() == 7
        assert self.tprop1.zy() == 8
        assert self.tprop1.zz() == 9
    
    def test_tensor_print(self):
        assert str(self.tprop1) == f"Tensor_P(name = val1, xx = 1, xy = 2, xz = 3, yx = 4, yy = 5, yz = 6, zx = 7, zy = 8, zz = 9)"
        assert str(self.tprop2) == f"Tensor_P(name = val2, xx = 4, xy = 5, xz = 6, yx = 7, yy = 8, yz = 9, zx = 1, zy = 2, zz = 3)"
    
    def test_row(self):
        assert str(self.tprop1.row(1)) == f"Vector_P(name = val1_row, x = 1, y = 2, z = 3)"
        assert str(self.tprop1.row(2)) == f"Vector_P(name = val1_row, x = 4, y = 5, z = 6)"
        assert str(self.tprop1.row(3)) == f"Vector_P(name = val1_row, x = 7, y = 8, z = 9)"

    def test_col(self):
        assert str(self.tprop1.col(1)) == f"Vector_P(name = val1_col, x = 1, y = 4, z = 7)"
        assert str(self.tprop1.col(2)) == f"Vector_P(name = val1_col, x = 2, y = 5, z = 8)"
        assert str(self.tprop1.col(3)) == f"Vector_P(name = val1_col, x = 3, y = 6, z = 9)"
    
    def test_give_val(self):
        assert self.tprop1.give_val() == (1, 2, 3, 4, 5, 6, 7, 8, 9)
        assert self.tprop2.give_val() == (4, 5, 6, 7, 8, 9, 1, 2, 3)