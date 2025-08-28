from collections import namedtuple, defaultdict

import re
from functools import partial
from pathlib import Path
from typing import Tuple, Union

# listener
FROM_RE = re.compile(r'^--- \(lis=(?P<lis>[0-9a-fA-F]+),\s*dir=(?P<dir>[0-9a-fA-F]+),\s*sol=(?P<sol>[0-9a-fA-F]+)\)'
                     r'\s*<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)> changing from '
                     r'(?:(?P<value>[0-9]+)|(?P<null>null))$')

# listener
TO_RE = re.compile(r'^\+\+\+ \(lis=(?P<lis>[0-9a-fA-F]+),\s*dir=(?P<dir>[0-9a-fA-F]+),\s*sol=(?P<sol>[0-9a-fA-F]+)\)'
                   r'\s*<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)> changed to '
                   r'(?:(?P<value>-?[0-9]+)|(?P<null>null))$')

# listener-workaround
IGNORING_RE = re.compile(r'^Ignoring listener (?P<lis>[0-9a-fA-F]+)$')

# cell-prop
ENTERING_RE = re.compile(r'^\*\*\* original values={<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)>'
                         r'=Optional(?:.(?P<empty>empty)|\[(?P<value>-?[0-9]+)\])'
                         r'}; changed=(?P<changed_pairs>{[^}]+})$')

CELL_TO_VALUE_PAIR_RE = re.compile(r'^\s*<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)>='
                                   r'Optional(?:.(?P<empty>empty)|\[(?P<value>-?[0-9]+)\])\s*$')

# inc-phase
ORIGINAL_RE = re.compile(r'^=== using original <CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)>'
                         r'=Optional(?:.(?P<empty>empty)|\[(?P<value>-?[0-9]+)\])$')

# inc-prop
POP_RE = re.compile(r'^Pop:\s+<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)>\s*$')

# inc-prop
UPDATE_RE = re.compile(r'^key=<CellKey (?P<sheet>.+)!(?P<cell>[A-Z]+[0-9]+)>; index=(?P<index>[0-9]+); '
                       r'current=(?:(?P<null>null)|(?P<current>-?[0-9]+)); '
                       r'prev=\[(?P<prev>(?:null|-?[0-9]+|, )+)\]; '
                       r'new=\[(?P<new>(?:null|-?[0-9]+|, )+)\]; '
                       r'final=(?:(?P<new_null>null)|(?P<new_value>-?[0-9]+))$')

VALUE_RE = re.compile(r'^(?P<null>null)|(?P<value>-?[0-9]+)')


def parse_list_of_values(str_list: str) -> Tuple[Union[None, int], ...]:
    return tuple(None if element == 'null' else int(element)
                 for element in str_list.split(', '))


UpdateInfo = namedtuple('UpdateInfo', 'cell, index, old_value, new_value, prev_inputs, new_inputs, line')


def inc_info(lines):
    def close_epoch():
        nonlocal by_var, by_var_index
        for var, info_list in by_var.items():
            if info_list:
                full_by_var[var].append(info_list)
        for var, by_index in by_var_index.items():
            for index, info_list in by_index.items():
                if info_list:
                    full_by_var_index[var][index].append(info_list)
        by_var = defaultdict(list)
        by_var_index = defaultdict(partial(defaultdict, list))

    full_by_var = defaultdict(list)
    full_by_var_index = defaultdict(partial(defaultdict, list))
    by_var = defaultdict(list)
    by_var_index = defaultdict(partial(defaultdict, list))
    ignoring = set()
    all_listeners = set()
    for n, line in enumerate(lines, start=1):
        line = line.rstrip()
        m_from = FROM_RE.match(line)
        if m_from is not None:
            all_listeners.add(m_from.group("lis"))
            continue
        m_to = TO_RE.match(line)
        if m_to is not None:
            all_listeners.add(m_to.group("lis"))
            close_epoch()
            continue
        m_ignore = IGNORING_RE.match(line)
        if m_ignore is not None:
            ignoring.add(m_ignore.group("lis"))
            continue
        m_enter = ENTERING_RE.match(line)
        if m_enter is not None:
            continue
        m_pop = POP_RE.match(line)
        if m_pop is not None:
            continue
        m_orig = ORIGINAL_RE.match(line)
        if m_orig is not None:
            continue
        m_update = UPDATE_RE.match(line)
        if m_update is not None:
            var = m_update.group("cell")
            index = m_update.group("index")
            info = UpdateInfo(var, index,
                              m_update.group("null") or m_update.group("current"),
                              m_update.group("new_null") or m_update.group("new_value"),
                              parse_list_of_values(m_update.group("prev")),
                              parse_list_of_values(m_update.group("new")),
                              n)
            by_var[var].append(info)
            by_var_index[var][index].append(info)
    close_epoch()
    return full_by_var, full_by_var_index, ignoring, all_listeners


def analyze_inc(lines):
    full_by_var, full_by_var_index, ignoring, all_listeners = inc_info(lines)
    # pprint(by_var)
    # pprint(by_var_index)
    # 1. check continuity of values between updates
    print(f'All listeners: {all_listeners}, ignored: {ignoring}')
    print('====== Value checks ======')
    for cell, info_list in full_by_var.items():
        print(f'*** {cell} ***')
        for updates in info_list:
            for u1, u2 in zip(updates, updates[1:]):
                if u1.new_value != u2.old_value:
                    print(f'Value mismatch between lines {u1.line} ({u1.new_value}) and {u2.line} ({u2.old_value})')
    print('====== Input checks ======')
    for cell, indexes in full_by_var_index.items():
        print(f'*** {cell} ***')
        for index, info_list in indexes.items():
            for updates in info_list:
                for u1, u2 in zip(updates, updates[1:]):
                    if u1.new_inputs != u2.prev_inputs:
                        print(f'Input mismatch for index {index} '
                              f'between lines {u1.line} ({u1.new_inputs}) and {u2.line} ({u2.prev_inputs})')


def analyze_inc_file(trace_file):
    with open(trace_file) as inp:
        # parse_inc(inp)
        analyze_inc(inp)


if __name__ == '__main__':
    analyze_inc_file(Path(__file__).parent / 'data' / 'latest-trace.txt')
