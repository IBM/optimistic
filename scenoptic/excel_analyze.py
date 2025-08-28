from __future__ import annotations

from io import StringIO
from typing import Tuple, Dict, Union, Literal, Sequence

from antlr4 import ParserRuleContext, RuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from ExcelParser import ExcelParser
from scenoptic.excel_analyze_variability import VariabilityTree, bind_cell_variability_by_tree
from scenoptic.excel_data import CellReference
from scenoptic.excel_to_math import Scenario, CellSpec
from scenoptic.parse_excel import get_excel_parser
from scenoptic.xl_utils import range_to_cells, cell_to_coords, column_to_index, get_cell_re_dict


class FormulaMatchException(Exception):
    pass


def get_cell(xl_range: str) -> CellSpec:
    cell1, _, sheet = range_to_cells(xl_range)
    row, col = cell_to_coords(cell1)
    return dict(sheet=sheet, row=row, col=col)


def get_adjacent_cell(cell: str, direction: str = 'down') -> CellSpec:
    spec = get_cell(cell)
    if direction == 'down':
        return dict(sheet=spec['sheet'], row=spec['row'] + 1, col=spec['col'])


def get_content(cell_spec: CellSpec, scenario: Scenario) -> str:
    return scenario.cell_value(cell_spec['row'], cell_spec['col'], sheet=cell_spec['sheet'])


def get_parser(spec: CellSpec, scenario: Scenario, verbose=False):
    content = get_content(spec, scenario)
    if isinstance(content, str):
        content = content.strip()
        if content.startswith('='):
            parser = get_excel_parser(content)
            if verbose:
                print(f'Cell{spec}  {content}')
            return parser
    return None


def is_compatible_cell(origin_child_cell: str,
                       candidate_child_cell: str,
                       cur_sheet: str,
                       distance: Tuple[int, int]) -> Union[CellReference, Literal[False, True]]:
    origin_info = get_cell_re_dict(origin_child_cell)
    candidate_info = get_cell_re_dict(candidate_child_cell)

    result = True
    if origin_info['col_fix']:
        result = result and origin_info['col'] == candidate_info['col']
    else:
        result = result and column_to_index(candidate_info['col']) - column_to_index(origin_info['col']) == distance[1]

    if origin_info['row_fix']:
        result = result and origin_info['row'] == candidate_info['row']
    else:
        result = result and int(candidate_info['row']) - int(origin_info['row']) == distance[0]

    if result and not (origin_info['col_fix'] and origin_info['row_fix']):
        # Compatible and cell are variable, not totally fixed
        return CellReference(int(origin_info['row']),
                             origin_info['row_fix'],
                             column_to_index(origin_info['col']),
                             origin_info['col_fix'],
                             cur_sheet)
    elif not result:
        # Not Compatible
        return False
    else:
        # Compatible but all cells are fixed
        return True


def terminal_description(terminal: Union[TerminalNodeImpl, RuleContext]):
    symbol = terminal.getSymbol()
    with StringIO() as buf:
        buf.write(symbol.text)
        buf.write("@")
        buf.write(str(symbol.start))
        buf.write(":")
        buf.write(str(symbol.stop))
        return buf.getvalue()


def determine_terminal_cell_node_sheet(cell: RuleContext, cur_sheet: str):
    parent_ctx = cell.parentCtx.parentCtx
    if isinstance(parent_ctx, ExcelParser.SimpleRefContext):
        return cur_sheet
    if isinstance(parent_ctx, ExcelParser.PrefixedRefContext):
        return parent_ctx.prefix().getText()[:-1]


def check_compatibility_recursive(origin: RuleContext,
                                  candidate: RuleContext,
                                  origin_sheet: str,
                                  distance: Tuple[int, int],
                                  indexes: Tuple[int, ...],
                                  child_path_to_cell_ref: Dict[Tuple[int, ...], str],
                                  indent='') -> None:
    # print(f'{indent}{type(first)}={first.getText()}')

    if type(origin) != type(candidate):
        raise FormulaMatchException(f'RuleNode with different parser context '
                                    f'{type(origin).__name__} vs {type(candidate).__name__}')

    if isinstance(origin, TerminalNodeImpl):
        # The following check any TerminalNode leaf:
        #  1. If it is CELL leaf, check (row, col) distance compatibility
        #  2. otherwise, validate same expression predicate value
        if origin.getSymbol().type == ExcelParser.CELL:
            origin_cell_name = origin.getText()
            candidate_cell_name = candidate.getText()
            sheet = determine_terminal_cell_node_sheet(origin, cur_sheet=origin_sheet)
            cell_reference = is_compatible_cell(origin_cell_name, candidate_cell_name, cur_sheet=sheet,
                                                distance=distance)
            if cell_reference is True:
                # Compatible but fixed
                pass
            elif cell_reference is False:
                raise FormulaMatchException(
                    f'Cells are not compatible '
                    f'"{terminal_description(origin)}" and "{terminal_description(candidate)}"')
            else:
                # Compatible and not fixed
                child_path_to_cell_ref[indexes] = cell_reference
        else:
            if origin.getText() != candidate.getText():
                raise FormulaMatchException(
                    f'Nodes of "{type(origin.getParent()).__name__}" have different '
                    f'values "{terminal_description(origin)}" and "{terminal_description(candidate)}"')
    else:
        # The following checks parse three RuleNodes, having :
        # 1. the same context type
        # 2. same number of children
        if origin.getChildCount() != candidate.getChildCount():
            raise FormulaMatchException(f'Nodes has different number of children')

        for i in range(origin.getChildCount()):
            origin_child = origin.getChild(i)
            candidate_child = candidate.getChild(i)

            check_compatibility_recursive(origin_child,
                                          candidate_child,
                                          origin_sheet=origin_sheet,
                                          distance=distance,
                                          indexes=(*indexes, i),
                                          child_path_to_cell_ref=child_path_to_cell_ref,
                                          indent=indent + " ")


def compute_distance(origin_cell_spec, candidate_cell_spec) -> Tuple[int, int]:  # row, column
    return (candidate_cell_spec['row'] - origin_cell_spec['row'],
            candidate_cell_spec['col'] - origin_cell_spec['col'])


def cell_parse_tree(spec: CellSpec, scenario: Scenario, verbose=False) -> Union[ParserRuleContext, None]:
    parse = get_parser(spec, scenario, verbose)
    if parse:
        parse_tree = parse.start()
        # TODO fetch forumula instead
        if not any(isinstance(e, ExcelParser.FormulaContext) for e in parse_tree.getChildren()):
            print(f'Cell "{spec}" does not contain a formula')
            return None
        return parse_tree
    return None


def extract_variability(child_path_to_cell_ref, verbose=False) -> Tuple[VariabilityTree, Sequence[CellReference]]:
    cell_references = []
    variability = set(child_path_to_cell_ref.keys())
    if verbose:
        print(f'Results = {child_path_to_cell_ref if child_path_to_cell_ref is not False else "No Match"}')
        print(f'variability = {variability}')

    variability = VariabilityTree()
    for key in child_path_to_cell_ref.keys():
        cur = variability
        for e in key:
            node = cur.exists(e)
            if node is False:
                child = VariabilityTree(e)
                cur.add_child(child)
                cur = child
            else:
                cur = node
        child.add_cell_reference(child_path_to_cell_ref[key])
        cell_references.append(child_path_to_cell_ref[key])

    cell_references = sorted(set(cell_references))

    # if verbose:
    #     print(f'variability = {variability}')
    #     print(f'Cell Reference = {cell_references}')

    return variability, cell_references


def check_compatible_formula(origin_cell: str,
                             candidate_cell: str,
                             scenario: Scenario,
                             verbose=False) -> Union[Tuple[VariabilityTree, Sequence[CellReference]], Literal[False]]:
    """
    Check formula's compatibility between any two cells on the same worksheet,

    Compatible input cells are such that according to distance (candidate_row - origin_row, candidate_col - origin_col)
    between the "origin" and "candidate" input cells, for any Cell Reference that exists in the "origin"
    formula there is a corresponding cell reference in the "candidate" formula, and these cell references are
    at the same designated distance of the input cells.
    Yet, if the cell reference is fixed, i.e. $col$row notation (e.g $A$2), the formulas in both input cells
    are compatible only if they use the same cell reference value.
    In addition for them to be compatible, we require that any other expression predicate exists
    in both input cells at the same position and have the same value

    :param origin_cell: origin input cell string representation, may be prefixed with sheet name
    :param candidate_cell: second input cell string representation
    :param scenario: pointer to the requesting excel Scenario
    :param verbose: Set to True when logging is requested for testing or debugging purposes

    :return: on completion we get a variability tree representing the traversal path from root down to each cell reference
    that is not fixed and is compatible, the path is specified by the node's child order.
    """
    origin_cell_spec = get_cell(origin_cell)
    candidate_cell_spec = get_cell(candidate_cell)

    origin_parse_tree = cell_parse_tree(origin_cell_spec, scenario, verbose)
    candidate_parse_tree = cell_parse_tree(candidate_cell_spec, scenario, verbose)
    if origin_parse_tree is None or candidate_parse_tree is None:
        return False

    distance = compute_distance(origin_cell_spec, candidate_cell_spec)
    try:
        child_path_to_cell_ref = dict()
        check_compatibility_recursive(origin_parse_tree,
                                      candidate_parse_tree,
                                      origin_sheet=origin_cell_spec['sheet'],
                                      distance=distance,
                                      indexes=(),
                                      child_path_to_cell_ref=child_path_to_cell_ref)
    except FormulaMatchException as e:
        if verbose:
            msg = f'FormulaMatchException: {e}'
            print(msg)
        return False

    variability, cell_references = extract_variability(child_path_to_cell_ref, verbose=verbose)
    return variability, cell_references


def bind_cell_variability(origin_cell: str,
                          variability: VariabilityTree,
                          scenario: Scenario,
                          verbose: bool = False) -> Union[Sequence[int], Literal[False]]:
    if variability is False:
        return False

    origin_cell_spec = get_cell(origin_cell)
    origin_parse_tree = cell_parse_tree(origin_cell_spec, scenario, verbose)

    return bind_cell_variability_by_tree(origin_parse_tree, variability, verbose=verbose)
