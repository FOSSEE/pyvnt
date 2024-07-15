import pytest

from pyvnt import *

class TestDimm:
    def setup_method(self, method):
        self.dimms = [1, 2, 3, 4, 5, 6, 7]
        self.dset = DimmSet('test', self.dimms)

    def teardown_method(self, method):
        del self.dset
        del self.dimms
    
    def test_dimm_print(self):
        assert str(self.dset) == f"DimmSet(name : test, dimm : {self.dimms})"
    
    def test_dimm_val(self):
        assert self.dset.giveVal() == self.dimms
    
    def test_dimm_edit(self):
        dummy_dimms = [1, 2, 3, 4, 5, 6, 7]
        self.dset.setProperties(*dummy_dimms)
        assert self.dset.giveVal() == dummy_dimms
    
    def test_dimm_edit_fail(self):
        dummy_dimms = [1, 2, 3, 4, 5, 6, 7, 8]
        with pytest.raises(TypeError):
            self.dset.setProperties(*dummy_dimms)
    
