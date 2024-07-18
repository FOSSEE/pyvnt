import pytest

from pyvnt import *

class TestDimm:
    def setup_method(self, method):
        self.dimms = [1, 2, 3, 4, 5, 6, 7]
        self.dset = Dim_Set_P('test', self.dimms)

    def teardown_method(self, method):
        del self.dset
        del self.dimms
    
    def test_dimm_print(self):
        assert str(self.dset) == f"Dim_Set_P(name : test, dimm : {self.dimms})"
    
    def test_dimm_val(self):
        assert self.dset.give_val() == self.dimms
    
    def test_dimm_edit(self):
        dummy_dimms = [1, 2, 3, 4, 5, 6, 7]
        self.dset.set_properties(*dummy_dimms)
        assert self.dset.give_val() == dummy_dimms
    
    def test_dimm_edit_fail(self):
        dummy_dimms = [1, 2, 3, 4, 5, 6, 7, 8]
        with pytest.raises(TypeError):
            self.dset.set_properties(*dummy_dimms)
    
