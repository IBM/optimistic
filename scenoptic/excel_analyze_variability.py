from __future__ import annotations

from antlr4 import RuleContext
from antlr4.tree.Tree import TerminalNodeImpl
from typing import Union, Sequence, Literal, Dict

from ExcelParser import ExcelParser
from scenoptic.excel_data import CellReference


class VariabilityTree:

    def __init__(self, val: Union[int, str] = 'Start'):
        self.name = val
        self.bind_id = None
        self.cell = None
        self.children: Sequence[VariabilityTree] = None

    def add_child(self, child: VariabilityTree):
        if self.children is None:
            self.children = []
        self.children.append(child)
        return child

    def add_cell_reference(self, cell_ref: CellReference):
        self.cell = cell_ref

    def exists(self, child: int) -> Union[VariabilityTree, Literal[False]]:
        if self.children is not None:
            for c in self.children:
                if c.name == child:
                    return c
        return False

    def get_child(self, i: int):
        return self.children[i] if len(self.children) > i else None

    def get_children(self):
        if self.children is not None:
            for child in self.children:
                yield child

    def get_child_count(self):
        return len(self.children) if self.children else 0

    def describe(self, indent=""):
        nl = f'\n'
        return f'{self.name}{f": ({self.bind_id})" if self.bind_id else ""}{f": ({self.cell})" if self.cell else ""} -> ' \
               f'{"(" if self.get_child_count() > 0 else ""}' \
               f'{",".join(c.describe(indent=indent + " ") for c in self.get_children()) if self.get_child_count() > 0 else "()"}' \
               f'{")" if self.get_child_count() > 0 else ""}'

    def __repr__(self):
        return self.describe()


def bind_cell_variability_by_tree(tree_node: RuleContext,
                                  variability: VariabilityTree,
                                  verbose: bool = False) -> Union[Dict[int, CellReference], Literal[False]]:
    """
    return
     binding between
      int - the cell parent ID that is the CellRefContext node id
      CellReference - the leaf cell
     or,
       False - if there is no compatibility
    """
    if variability is False:
        return False

    binding = {}
    for i in range(variability.get_child_count()):
        variability_child = variability.get_child(i)
        cell_child = tree_node.getChild(variability_child.name)

        bind_cell_recursive(cell_child, variability_child, binding=binding, verbose=verbose)
    return binding


def bind_cell_recursive(cell: RuleContext,
                        variability: VariabilityTree,
                        binding: Dict[int, CellReference],
                        verbose: bool = False,
                        indent=''):
    if isinstance(cell, TerminalNodeImpl):
        # The following checks any TerminalNode leaf:
        #  1. If it is CELL leaf, add to binding the parent cell ID that is the of the CellRefContext node
        #  2. otherwise,  skip, we do not handle miss match, here, we expect the variability to belong to the cell
        if cell.getSymbol().type == ExcelParser.CELL:
            variability.bind_id = id(cell.getParent())
            binding[id(cell.getParent())] = variability.cell
            # binding.append(id(cell.getParent()))
    else:
        for i in range(variability.get_child_count()):
            variability_child = variability.get_child(i)
            cell_child = cell.getChild(variability_child.name)

            bind_cell_recursive(cell_child,
                                variability_child,
                                binding=binding,
                                verbose=verbose,
                                indent=indent + " ")
