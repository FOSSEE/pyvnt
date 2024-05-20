from pyvnt.Reference.basic import *
from pyvnt.Reference.errorClasses import InvalidTupleError
from pyvnt.Reference.vector import PropertyVector

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

        inputs = []

        for i in range(3):
            for j in range(3):
                inputs.append((i, j, value[i*3+j]))
        self.setProperties(name, *inputs)

    # TODO: Implement matrix operations for tensors, refer to the OpenFOAM team for details

    # TODO: Change the way input is taken in this method, refer Matlab's matrix slicing --done
    def setProperties(self, name: str, *args: (int, int, PropertyFloat)) -> None:
        '''
        Function to edit the values stored in the object

        Parameters:
        name: The name of the property.
        *args: The values of the tensor in the form of tuples.

        The tuples should be in the form of (i, j, PropertyFloat) where i and j are the indices of the tensor in 1-based indexing.
        In order to set the value for an entire row or column, set the index to 0 for the row or column respectively.

        Example: 
        To set the value of the entire row 1 to 5, the tuple should be (1, 0, PropertyFloat(name, 5))
        To set the value of the entire column 2 to 5, the tuple should be (0, 2, PropertyFloat(name, 5))
        To set the value of the element at row 1 and column 2 to 5, the tuple should be (1, 2, PropertyFloat(name, 5))

        '''
        self._ValueProperty__name = name

        inputs = list(args)
        self.__values = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]]

        for t in inputs:
            if len(t) != 3 or type(t[0]) != int or type(t[1]) != int or type(t[2]) != PropertyFloat:
                raise InvalidTupleError(t)
            else:
                if t[0] == 0 and t[1] == 0:
                    val = t[2]
                    self.__values = [[val, val, val], 
                                     [val, val, val], 
                                     [val, val, val]]
                elif t[0] == 0:
                    for i in range(3):
                        self.__values[i][t[1]-1] = t[2]
                elif t[1] == 0:
                    for i in range(3):
                        self.__values[t[0]-1][i] = t[2]
                elif t[0] != 0 and t[1] != 0:
                    self.__values[t[0]-1][t[1]-1] = t[2]
                else:
                    raise InvalidTupleError(t)
    
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
    
    def row(self, r: int) -> PropertyVector:
        '''
        Returns the row vector of the tensor

        Parameters:
        r: The row number of the tensor
        '''
        return PropertyVector(self._ValueProperty__name + "_row", self.__values[r][0], self.__values[r][1], self.__values[r][2])
    
    def col(self, c: int) -> PropertyVector:
        '''
        Returns the column vector of the tensor

        Parameters:
        c: The column number of the tensor
        '''
        return PropertyVector(self._ValueProperty__name + "_col", self.__values[0][c], self.__values[1][c], self.__values[2][c])
    
    def diag(self) -> PropertyVector:
        '''
        Returns the diagonal vector of the tensor
        '''
        return PropertyVector(self._ValueProperty__name + "_diag", self.__values[0][0], self.__values[1][1], self.__values[2][2])

    def T(self) -> PropertyTensor:
        '''
        Return non-Hermitian transpose of the tensor
        '''
        return PropertyTensor(self._ValueProperty__name + "_T", [self.__values[0][0], self.__values[1][0], self.__values[2][0],
                                                                 self.__values[0][1], self.__values[1][1], self.__values[2][1],
                                                                 self.__values[0][2], self.__values[1][2], self.__values[2][2]])

    def inv(self) -> PropertyTensor:
        '''
        Returns the inverse of the tensor
        '''
        pass

    def inner(self, t) -> PropertyTensor:
        '''
        Returns the inner product of the tensor with another tensor
        '''
        pass

    def schur(self, t) -> PropertyTensor:
        '''
        Returns the Schur product of the tensor with another tensor
        '''
        pass
    
    def __repr__(self):
        return f"PropertyTensor(name = {self._ValueProperty__name}, xx = {self.xx()}, xy = {self.xy()}, xz = {self.xz()}, yx = {self.yx()}, yy = {self.yy()}, yz = {self.yz()}, zx = {self.zx()}, zy = {self.zy()}, zz = {self.zz()})"


        
        