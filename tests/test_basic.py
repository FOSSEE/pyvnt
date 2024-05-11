import pytest

import pyvnt.Reference.basic as basic

class TestEnum:
    def setup_method(self, method):
        self.items = {'PCG', 'PBiCG', 'PBiCGStab'}
        self.eprop2 = basic.EnumProp('val2', items=self.items, default='PBiCG')
        self.eprop1 = basic.EnumProp('val1', items=self.items, default='PCG')
    
    def teardown_method(self, method):
        del self.eprop1
        del self.eprop2
        del self.items
    
    def test_enum_print(self):
        assert str(self.eprop1) == f"EnumProp(name = val1, items = {self.items}, default = PCG)"
        assert str(self.eprop2) == f"EnumProp(name = val2, items = {self.items}, default = PBiCG)"
    
    def test_enum_val(self):
        assert self.eprop1.giveVal() == 'PCG'
        assert self.eprop2.giveVal() == 'PBiCG'

    def test_enum_items(self):
        assert self.eprop1.get_items() == self.items
        assert self.eprop2.get_items() == self.items

    def test_enum_edit(self):
        dummy_items = {'PCG', 'PBiCG', 'GMRES'}
        self.eprop1.setProperties('val1', dummy_items, 'PCG')
        assert self.eprop1.get_items() == dummy_items
        assert self.eprop1.giveVal() == 'PCG'
    
    def test_enum_edit_fail(self):
        dummy_items = {'PCG', 'PBiCG', 'GMRES'}
        with pytest.raises(basic.DefaultOutofRangeError):
            self.eprop1.setProperties('val1', dummy_items, 'PBiCGStab')
        
        with pytest.raises(basic.NotSetType):
            self.eprop1.setProperties('val1', 'PCG', 'PCG')
        
        with pytest.raises(basic.NotStringType):
            self.eprop1.setProperties('val1', {1, 2, 3}, 'PCG')
    
    def test_enum_change(self):
        self.eprop1.set_default('PBiCG')
        assert self.eprop1.giveVal() == 'PBiCG'
    
    def test_enum_change_fail(self):
        with pytest.raises(basic.ValueOutofRangeError):
            self.eprop1.set_default('GMRES')
    
    def test_enum_remove(self):
        self.eprop1.remove_item('PBiCGStab')
        assert self.eprop1.get_items() == {'PCG', 'PBiCG'}
    
    def test_enum_remove_fail(self):
        with pytest.raises(basic.IsDefaultError):
            self.eprop1.remove_item('PCG')

class TestInt:
    def setup_method(self, method):
        self.iprop1 = basic.PropertyInt('val1', 5, 1, 10)
        self.iprop2 = basic.PropertyInt('val2', 100, -100, 1000)
    
    def teardown_method(self, method):
        del self.iprop1
        del self.iprop2
    
    def test_int_print(self):
        assert str(self.iprop1) == f"PropertyInt(name = val1, default = 5, minimum = 1, maximum = 10)"
        assert str(self.iprop2) == f"PropertyInt(name = val2, default = 100, minimum = -100, maximum = 1000)"
    
    def test_int_edit(self):
        self.iprop1.setProperties('val1', 10, 1, 10)
        assert self.iprop1.giveVal() == 10
    
    def test_int_edit_fail(self):
        with pytest.raises(basic.DefaultOutofRangeError):
            self.iprop1.setProperties('val1', 0, 1, 10)
        
        with pytest.raises(basic.InvalidRangeError):
            self.iprop1.setProperties('val1', 2, 5, 1)
    
    def test_int_val(self):
        assert self.iprop1.giveVal() == 5
        assert self.iprop2.giveVal() == 100

class TestFloat:
    def setup_method(self, method):
        self.fprop1 = basic.PropertyFloat('val1', 5.0, 1.0, 10.0)
        self.fprop2 = basic.PropertyFloat('val2', 100.0, -100.0, 1000.0)
    
    def teardown_method(self, method):
        del self.fprop1
        del self.fprop2
    
    def test_float_print(self):
        assert str(self.fprop1) == f"PropertyFloat(name = val1, default = 5.0, minimum = 1.0, maximum = 10.0)"
        assert str(self.fprop2) == f"PropertyFloat(name = val2, default = 100.0, minimum = -100.0, maximum = 1000.0)"
    
    def test_float_edit(self):
        self.fprop1.setProperties('val1', 10.0, 1.0, 10.0)
        assert self.fprop1.giveVal() == 10.0
    
    def test_float_edit_fail(self):
        with pytest.raises(basic.DefaultOutofRangeError):
            self.fprop1.setProperties('val1', 0.0, 1.0, 10.0)
        
        with pytest.raises(basic.InvalidRangeError):
            self.fprop1.setProperties('val1', 2.0, 5.0, 1.0)
    
    def test_float_val(self):
        assert self.fprop1.giveVal() == 5.0
        assert self.fprop2.giveVal() == 100.0