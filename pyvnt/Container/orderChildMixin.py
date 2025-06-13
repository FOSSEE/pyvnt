from anytree import Node, RenderTree, AsciiStyle, NodeMixin
from anytree.search import find_by_attr
from typing import Any, Type
from pyvnt.Container.key import Key_C
from pyvnt.Reference.error_classes import *
from pyvnt.utils.make_indent import make_indent


class OrderedChildMixin:
    """
    A mixin for any class that can be a child of a Node_C.
    It overrides the parent setter to ensure the child is correctly added
    to or removed from its parent's `_ordered_items` list.
    """
    @property
    def parent(self):
        return super().parent

    @parent.setter
    def parent(self, new_parent_node):
        old_parent_node = self.parent
        # print("Parent setter triggerd")
        NodeMixin.parent.fset(self, new_parent_node)

        if hasattr(old_parent_node, '_ordered_items'):
            old_parent_node._ordered_items.remove(self)
        if hasattr(new_parent_node, '_ordered_items'):
            # if self not in new_parent_node._ordered_items:
            new_parent_node._ordered_items.append(self)