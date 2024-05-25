import pytest

import pyvnt.DictionaryElement.keyData as keyData
from pyvnt.Reference.basic import *

class TestKeyData:
    def setup_method(self, method):
        self.items = {'PCG', 'PBiCG', 'PBiCGStab'}
        self.prop2 = EnumProp('val2', items=self.items, default='PBiCG')
        self.prop1 = EnumProp('val1', items=self.items, default='PCG')
        self.key1 = keyData.KeyData('solver', self.prop1, self.prop2)
    
    def teardown_method(self, method):
        del self.key1
        del self.prop1
        del self.prop2
        del self.items
    
    def test_keyData_print(self):
        assert str(self.key1) == f"KeyData(val1 : {str(self.prop1)}, val2 : {str(self.prop2)})"
    
    def test_keyData_val(self):
        assert self.key1.giveVal() == f"solver : {self.prop1.giveVal()}, {self.prop2.giveVal()}"
    
    def test_keyData_edit(self):
        tmp_prop1 = PropertyInt('tmpval1', 2, 1, 10)
        tmp_prop2 = PropertyInt('tmpval2', 3, 1, 10)

        self.key1.replaceVal('val1', tmp_prop1)
        assert self.key1.giveVal() == f"solver : {tmp_prop1.giveVal()}, {self.prop2.giveVal()}"

        self.key1.replaceVal(self.prop2, tmp_prop2)
        assert self.key1.giveVal() == f"solver : {tmp_prop1.giveVal()}, {tmp_prop2.giveVal()}"

        tmp_prop3 = PropertyInt('tmpval2', 4, 1, 10)

        self.key1.replaceVal(tmp_prop2, tmp_prop3)
        assert self.key1.giveVal() == f"solver : {tmp_prop1.giveVal()}, {tmp_prop3.giveVal()}"
    
    def test_keyData_edit_fail(self):
        tmp_prop1 = PropertyInt('tmpval1', 2, 1, 10)
        tmp_prop2 = PropertyInt('tmpval2', 3, 1, 10)
        tmp_prop3 = PropertyInt('tmpval2', 4, 1, 10)

        with pytest.raises(keyData.KeyRepeatError):
            self.key1.replaceVal('val1', tmp_prop1)
            self.key1.replaceVal('val2', tmp_prop1)
        
        with pytest.raises(keyData.KeyRepeatError):
            self.key1.replaceVal('val2', tmp_prop2)
            self.key1.replaceVal('val2', tmp_prop3)
    
    def test_keyData_del(self):
        self.key1.delVal('val1')
        assert self.key1.giveVal() == f"solver : {self.prop2.giveVal()}"

        