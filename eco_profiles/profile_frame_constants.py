from __future__ import annotations

from math_rep.expression_types import QualifiedName, M_ANY

PROFILE_FRAME_NAME = '*profiles*'


# PROFILE_FRAME = Frame(PROFILE_FRAME_NAME)
def is_profile_name(qname: QualifiedName):
    return qname.lexical_path == (PROFILE_FRAME_NAME,)


QualifiedName.add_lexical_scope_predicate(is_profile_name)


def profile_name(name, type=M_ANY):
    return QualifiedName(name, type, lexical_path=(PROFILE_FRAME_NAME,))
