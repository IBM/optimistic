import time
import datetime

from enum import Enum
from typing import Union, Tuple



class Report(Enum):
    FAILURE = 'Failure'
    WARNING = 'Warning'
    SUCCESS = 'Success'
    SUMMARY = 'Summary'
    STATS = 'Stats'
    LOG = 'LOG'


class ReportLogger:
    def __init__(self):
        self.report = {kind: [] for kind in Report}

    def add(self, of: Union[Tuple['Report', ...], 'Report'], msg: str):
        add = of
        if not isinstance(of, (tuple, list)):
            add = (of,)
        for e in add:
            self.report[e].append(msg)

    def get_report(self, kind=(Report.SUCCESS, Report.FAILURE, Report.SUMMARY)):
        kind_as_tuple = kind if isinstance(kind, tuple) else tuple([kind])
        report = ''.join(f'\n{key}:\n {msg if msg else "None"}' for key, msg in
                         ((k.name, '\n'.join(f'\t{entry}' for entry in self.report[k])) for k in kind_as_tuple))
        # report = ''
        # for k in kind_as_tuple:
        #     msg = '\n'.join(f'\t{msg}' for msg in self.report[k])
        #     if not msg:
        #         msg = 'None'
        #     report += f'\n{k.name}: \n {msg}'
        return report


def timeit(start):
    build_time = time.time() - start
    return f'Duration - {build_time:.3f} sec. = {datetime.timedelta(seconds=build_time)}'
