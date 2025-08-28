from numbers import Number
from typing import Sequence, Optional, Union

from codegen.abstract_rep import VariableAccess, Expression, FunctionApplExpr, StringExpr, NumberExpr, Assignment, \
    DataConstant
from math_rep.expression_types import QualifiedName, M_ANY, MType
from validator2solver.python.python_frame_constants import PYTHON_USER_FRAME_NAME
from validator2solver.python.symbol_table import PYTHON_BUILTIN_FRAME_NAME

NAME_TYPE = Union[QualifiedName, VariableAccess, str]


class ProgramFactory:
    """
    Factory for abstract representation of program (`CodeElement` subclasses)
    """

    def __init__(self, default_lexical_path: str):
        self.default_lexical_path = (*reversed(default_lexical_path.split('.')), PYTHON_BUILTIN_FRAME_NAME)
        self.user_lexical_path = PYTHON_USER_FRAME_NAME
        self._fresh_vars = {}

    def var(self, name: str, type: MType = M_ANY, additional_lexical_components: Sequence[str] = (),
            override_lexical_path: Optional[Sequence[str]] = None) -> VariableAccess:
        lexical_path = (override_lexical_path if override_lexical_path is not None
                        else (*additional_lexical_components, *self.default_lexical_path))
        return VariableAccess(QualifiedName(name, type=type, lexical_path=lexical_path))

    def fresh_var(self, prefix: str, type: MType = M_ANY):
        next_index = self._fresh_vars.get(prefix, 1)
        self._fresh_vars[prefix] = next_index + 1
        return VariableAccess(QualifiedName(f'{prefix}{next_index}', type=type, lexical_path=self.user_lexical_path))

    def user_var(self, name: str, type: MType = M_ANY):
        return VariableAccess(QualifiedName(name, type=type, lexical_path=self.user_lexical_path))

    def constant(self, value):
        if isinstance(value, str):
            return StringExpr(value)
        if isinstance(value, Number):
            return NumberExpr(value)
        return DataConstant(value)

    def _to_qn(self, name: NAME_TYPE):
        if isinstance(name, QualifiedName):
            return name
        if isinstance(name, VariableAccess):
            return name.name
        if isinstance(name, str):
            return QualifiedName(name, lexical_path=self.default_lexical_path)
        raise ValueError(f'Cannot convert {name} to a QualifiedName')

    def assign(self, var: NAME_TYPE, value: Expression, comment: Optional[str] = None):
        return Assignment(self._to_qn(var), value, comment=comment)

    def function_call(self, function: NAME_TYPE, *args: Expression, comment: Optional[str] = None,
                      **named_args: Expression):
        return FunctionApplExpr(self._to_qn(function), args, named_args=named_args.items(), comment=comment)

    def method_call(self, target: Expression, function: NAME_TYPE, *args: Expression, comment: Optional[str] = None,
                    **named_args: Expression):
        return FunctionApplExpr(self._to_qn(function), args, named_args=named_args.items(), method_target=target,
                                comment=comment)
