from math_rep.expression_types import QualifiedName
from scenoptic.scenoptic_frame_constants import WORKSHEET_FRAME_NAME
from opl_repr.opl_frame_constants import OPL_USER_FRAME_NAME, PARAMETER_FRAME_NAME, INVENTED_VARS_FRAME_NAME


def is_opl_user_name(qname: QualifiedName):
    return (len(qname.lexical_path) > 0
            and qname.lexical_path[-1] in (OPL_USER_FRAME_NAME, INVENTED_VARS_FRAME_NAME, PARAMETER_FRAME_NAME,
                                           WORKSHEET_FRAME_NAME))
