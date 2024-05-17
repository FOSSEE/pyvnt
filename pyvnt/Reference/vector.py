from pyvnt.Reference.basic import *

class PropertyVector(ValueProperty):
    '''
    Property Class to store vector values

    Constructor Parameters:
        name: Name of the property of which vector value is to be stored
        x: PropertyFloat object to store x value of the vector
        y: PropertyFloat object to store y value of the vector
        z: PropertyFloat object to store z value of the vector
    '''

    __slots__ = ('_PropertyVector__name', '_PropertyVector__x', '_PropertyVector__y', '_PropertyVector__z')

    def instance_restricted(self):
        pass

    def __init__(self, name: str, x: PropertyFloat, y: PropertyFloat, z: PropertyFloat):
        super(PropertyVector, self).__init__()
        self.setProperties(name, x, y, z)
    
    def setProperties(self, name: str = None, x: PropertyFloat = None, y: PropertyFloat = None, z: PropertyFloat = None) -> None:
        '''
        Function to edit the values stored in the object

        Parameters:
        name: Name of the property of which vector value is to be stored
        x: PropertyFloat object to store x value of the vector
        y: PropertyFloat object to store y value of the vector
        z: PropertyFloat object to store z value of the vector
        '''
        if name:
            self._ValueProperty__name = name
        
        if x:
            self.__x = x
        
        if y:
            self.__y = y
        
        if z:
            self.__z = z
    
    def x(self) -> float:
        '''
        Returns the x value of the vector
        '''

        return self.__x.giveVal()
    
    def y(self) -> float:
        '''
        Returns the y value of the vector
        '''
        return self.__y.giveVal()
    
    def z(self) -> float:
        '''
        Returns the z value of the vector
        '''
        return self.__z.giveVal()
    
    def __repr__(self):
        return f"PropertyVector(name = {self.__name}, x = {self.__x.giveVal()}, y = {self.__y.giveVal()}, z = {self.__z.giveVal()})"