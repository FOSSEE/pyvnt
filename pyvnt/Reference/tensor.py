from pyvnt.Reference.basic import *

class PropertyTensor(ValueProperty):
    '''
    A property that holds a tensor value.

    Tensor is stored in the following manner:
    [[xx, xy, xz],
    [yx, yy, yz],
    [zx, zy, zz]]

    Constructor Parameters:
        name: The name of the property.
        value: list
    '''

    __slots__ = ('_PropertyTensor__name', '_PropertyTensor__values')

    def instance_restricted(self):
        pass

    def __init__(self, name, value: [PropertyFloat]):
        super(PropertyTensor, self).__init__()
        self.setProperties(name, *value)

    def setProperties(self, name: str, xx: PropertyFloat = None, xy: PropertyFloat = None, xz: PropertyFloat = None, yx: PropertyFloat = None, yy: PropertyFloat = None, yz: PropertyFloat = None, zx: PropertyFloat = None, zy: PropertyFloat = None, zz: PropertyFloat = None) -> None:
        '''
        Function to edit the values stored in the object

        Parameters:
        name: The name of the property.
        value: list
        '''
        self._ValueProperty__name = name

        self.__values = [[xx, xy, xz],
                         [yx, yy, yz],
                         [zx, zy, zz]]
    
    def xx(self) -> float:
        '''
        Returns the xx value of the tensor
        '''
        return self.__values[0][0].giveVal()
    
    def xy(self) -> float:
        '''
        Returns the xy value of the tensor
        '''
        return self.__values[0][1].giveVal()
    
    def xz(self) -> float:
        '''
        Returns the xz value of the tensor
        '''
        return self.__values[0][2].giveVal()
    
    def yx(self) -> float:
        '''
        Returns the yx value of the tensor
        '''
        return self.__values[1][0].giveVal()
    
    def yy(self) -> float:
        '''
        Returns the yy value of the tensor
        '''
        return self.__values[1][1].giveVal()
    
    def yz(self) -> float:
        '''
        Returns the yz value of the tensor
        '''
        return self.__values[1][2].giveVal()
    
    def zx(self) -> float:
        '''
        Returns the zx value of the tensor
        '''
        return self.__values[2][0].giveVal()
    
    def zy(self) -> float:
        '''
        Returns the zy value of the tensor
        '''
        return self.__values[2][1].giveVal()
    
    def zz(self) -> float:
        '''
        Returns the zz value of the tensor
        '''
        return self.__values[2][2].giveVal()
    
    def __repr__(self):
        return f"PropertyTensor(name = {self._ValueProperty__name}, xx = {self.xx()}, xy = {self.xy()}, xz = {self.xz()}, yx = {self.yx()}, yy = {self.yy()}, yz = {self.yz()}, zx = {self.zx()}, zy = {self.zy()}, zz = {self.zz()})"


        
        