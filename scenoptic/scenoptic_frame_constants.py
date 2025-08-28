from math_rep.expression_types import M_ANY, QualifiedName, MClassType

EXCEL_FRAME_NAME = '*excel*'
EXCEL_AUX_NAME = '*excel-aux*'
EXCEL_ADDITIONS_NAME = '*excel-additions*'
EXCEL_INTERNAL_NAME = '*excel-scenoptic*'
EXCEL_VAR_NAME = '*excel-var*'
WORKSHEET_FRAME_NAME = '*worksheet*'


def excel_name(name, type=M_ANY):
    return QualifiedName(name, type, lexical_path=(EXCEL_FRAME_NAME,))


M_RANGE = MClassType(excel_name('Range'))
