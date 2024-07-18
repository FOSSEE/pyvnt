import pytest

from pyvnt.Container.key import Key_C
from pyvnt.Reference.basic import *
from pyvnt.Reference.error_classes import *

class TestKey_C:
    def setup_method(self, method):
        self.items = {'PCG', 'PBiCG', 'PBiCGStab'}
        self.prop2 = Enm_P('val2', items=self.items, default='PBiCG')
        self.prop1 = Enm_P('val1', items=self.items, default='PCG')
        self.key1 = Key_C('solver', self.prop1, self.prop2)
    
    def teardown_method(self, method):
        del self.key1
        del self.prop1
        del self.prop2
        del self.items
    
    def test_Key_C_print(self):
        assert str(self.key1) == f"Key_C(val1 : {str(self.prop1)}, val2 : {str(self.prop2)})"
    
    def test_Key_C_val(self):
        assert self.key1.give_val() == f"solver : {self.prop1.give_val()}, {self.prop2.give_val()}"
    
    def test_Key_C_edit(self):
        tmp_prop1 = Int_P('tmpval1', 2, 1, 10)
        tmp_prop2 = Int_P('tmpval2', 3, 1, 10)

        self.key1.replace_val('val1', tmp_prop1)
        assert self.key1.give_val() == f"solver : {tmp_prop1.give_val()}, {self.prop2.give_val()}"

        self.key1.replace_val(self.prop2, tmp_prop2)
        assert self.key1.give_val() == f"solver : {tmp_prop1.give_val()}, {tmp_prop2.give_val()}"

        tmp_prop3 = Int_P('tmpval2', 4, 1, 10)

        self.key1.replace_val(tmp_prop2, tmp_prop3)
        assert self.key1.give_val() == f"solver : {tmp_prop1.give_val()}, {tmp_prop3.give_val()}"
    
    def test_Key_C_edit_fail(self):
        tmp_prop1 = Int_P('tmpval1', 2, 1, 10)
        tmp_prop2 = Int_P('tmpval2', 3, 1, 10)
        tmp_prop3 = Int_P('tmpval2', 4, 1, 10)

        with pytest.raises(KeyRepeatError):
            self.key1.replace_val('val1', tmp_prop1)
            self.key1.replace_val('val2', tmp_prop1)
        
        with pytest.raises(KeyRepeatError):
            self.key1.replace_val('val2', tmp_prop2)
            self.key1.replace_val('val2', tmp_prop3)
    
    def test_Key_C_del(self):
        self.key1.delete_val('val1')
        assert self.key1.give_val() == f"solver : {self.prop2.give_val()}"

        