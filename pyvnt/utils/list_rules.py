'''
ListProperty stores a list of elements internally. 

Th elements are decided by the name of the list

While printing, the elementa are printed vertically, while the content of the element is printed horizontally.

TODO: How to place restriction on the contents of the elements of the list based on the name of the list. 

Example:

blocks --> list
(
    hex (0 1 2 3 4 5 6 7) (100 150 1) simpleGrading (1 1 1) --> element
    hex (8 9 10 11 12 13 14) (100 150 1) simpleGrading (1 1 1) --> element
);

Data: can be a python dictionary. 
Key: name of the list
Value: format of the element

TODO: How to set the format of the element?

The element internally stores the data in it in a list and does not print the brackets while writing out. 

'''

(
    (a, b, c),
    (d, e, f),
)