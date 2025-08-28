from abc import ABC, abstractmethod

from codegen.parameters import ParmKind, POS_AND_KW, REST_PARM, KEYWORDS_PARM, SPECIAL_PARMS, ParameterDescriptor
from codegen.utils import Acceptor, disown
from math_rep.constants import ELEMENT_OF_SYMBOL
from math_rep.expression_types import M_ANY, ATOMIC_PYTHON_TYPES, MClassType, MSetType, MUnionType, MCollectionType, \
    QualifiedName, MMappingType, MTupleType
from validator2solver.python.python_builtins import PYTHON_BUILTIN_NAMES
from validator2solver.python.symbol_default_modules import TOTAL_MAPPING_QN, TUPLE_QN, MAPPING_QN
from validator2solver.python.symbol_table import BindingScope, PYTHON_BUILTIN_FRAME_NAME

TYPING_LEXICAL_PATH = ('typing', PYTHON_BUILTIN_FRAME_NAME)

NEWLINE = '\n'


class VisitorResult:
    pass


class PartialResult(VisitorResult):
    pass


class EmptyContents(PartialResult):
    pass


class Components(PartialResult):
    def __init__(self, components):
        self.components = components


class PythonElement(VisitorResult, ABC, Acceptor):
    @abstractmethod
    def describe(self) -> str:
        pass

    def __repr__(self):
        return self.describe()

    @property
    def starts_on_line(self):
        try:
            return self._starts_on_line
        except AttributeError:
            self._starts_on_line = None
            return None


# DEBUG
class PythonNotImplemented(PythonElement):
    def describe(self) -> str:
        return '**** NOT IMPLEMENTED ****'


class PythonFile(PythonElement, BindingScope):
    def __init__(self, contents):
        self.contents = contents
        self.frame = None

    def describe(self) -> str:
        return f'FILE({NEWLINE.join(c.describe() for c in self.contents)})'


class PythonStatements(PythonElement):
    def __init__(self, statements):
        self.statements = statements

    def describe(self) -> str:
        return f'STMTS({NEWLINE.join(s.describe() for s in self.statements)})'


class PythonPass(PythonElement):
    def describe(self) -> str:
        return 'PASS'


class PythonReturn(PythonElement):
    def __init__(self, retval):
        self.retval = retval

    def describe(self) -> str:
        if (retval := self.retval) is not None:
            return f'RETURN({retval.describe()})'
        else:
            return f'RETURN()'


class PythonIfStatement(PythonElement):
    def __init__(self, conditions, blocks, else_block=None):
        self.conditions = conditions
        self.blocks = blocks
        self.else_block = else_block

    def describe(self) -> str:
        else_text = f'; ELSE {self.else_block.describe()}' if self.else_block else ''
        elifs = zip(self.conditions, self.blocks)
        return f'IF({"; ".join(f"{cond.describe()} → {block.describe()}" for cond, block in elifs)}){else_text}'


class Comprehension(PythonElement, BindingScope):
    kind = 'UNSPECIFIED-COMPREHENSION'

    def as_list(self):
        return PythonListCompr(self.expr, self.control)

    def as_set(self):
        return PythonSetCompr(self.expr, self.control)

    def __init__(self, expr, control):
        self.expr = expr
        self.control = control

    def describe(self) -> str:
        return f'{self.kind}({self.expr.describe()} | {self.control.describe()})'


class PythonListCompr(Comprehension):
    kind = 'LISTCOMPR'


class PythonSetCompr(Comprehension):
    kind = 'SETCOMPR'


class PythonGenExpr(Comprehension):
    kind = 'GEN'


class PythonDictCompr(Comprehension):
    def __init__(self, key_expr, val_expr, control):
        super().__init__(key_expr, control)
        self.val_expr = val_expr

    def describe(self) -> str:
        return f'DICTCOMPR({self.expr.describe()}: {self.val_expr.describe()} | {self.control.describe()})'


class PythonExpressions(PythonElement):
    def __init__(self, expressions):
        self.expressions = expressions

    def describe(self) -> str:
        return f'EXPRS({", ".join(e.describe() for e in self.expressions)})'


class PythonIFTE(PythonElement):
    def __init__(self, cond, pos, neg):
        self.cond = cond
        self.pos = pos
        self.neg = neg

    def describe(self) -> str:
        return f'IFTE({self.cond.describe()}; {self.pos.describe()}, {self.neg.describe()})'


class PythonOp(PythonElement):
    @disown('op')
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def describe(self) -> str:
        return f'OP({self.op}; {", ".join(a.describe() for a in self.args)})'


class PythonComparison(PythonElement):
    @disown('ops')
    def __init__(self, ops, args):
        self.ops = ops
        self.args = args

    def describe(self) -> str:
        return f'COMP({", ".join(self.ops)}; {", ".join(a.describe() for a in self.args)})'


class PythonConstant(PythonElement):
    @disown('value')
    def __init__(self, value):
        self.value = value

    def describe(self) -> str:
        return f'CONST({repr(self.value)})'


class PythonVariable(PythonElement):
    @disown('name')
    def __init__(self, name):
        if name in PYTHON_BUILTIN_NAMES:
            self.name = QualifiedName(name, lexical_path=(PYTHON_BUILTIN_FRAME_NAME,))
        else:
            self.name = QualifiedName(name)
        self.frame = None

    def describe(self) -> str:
        return f'REF({self.name})'


class PythonAttribute(PythonElement):
    @disown('attr')
    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

    def describe(self) -> str:
        return f'GETATTR({self.obj.describe()}, {self.attr})'


class PythonCall(PythonElement):
    def __init__(self, func, arglist):
        self.func = func
        self.arglist = arglist

    def describe(self) -> str:
        return f'CALL({self.func.describe()}; {", ".join(arg.describe() for arg in self.arglist)})'


class PythonKeywordArg(PythonElement):
    @disown('name')
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def describe(self) -> str:
        return f'KWARG({self.name}={self.value.describe()})'


class PythonContainerCons(PythonElement):
    def __init__(self, components):
        self.components = components


class PythonTupleCons(PythonContainerCons):
    def describe(self) -> str:
        return f'TUPLE({", ".join(c.describe() for c in self.components)})'


class PythonListCons(PythonContainerCons):
    def describe(self) -> str:
        return f'LIST({", ".join(c.describe() for c in self.components)})'


class PythonSetCons(PythonContainerCons):
    def describe(self) -> str:
        return f'SET({", ".join(c.describe() for c in self.components)})'


class PythonIncSet(PythonElement):
    def __init__(self, subset):
        self.subset = subset

    def describe(self) -> str:
        return f'INCLUDESET({self.subset.describe()})'


class PythonDictCons(PythonContainerCons):
    def describe(self) -> str:
        return f'DICT({", ".join(c.describe() for c in self.components)})'


class PythonIncDict(PythonElement):
    def __init__(self, subdict):
        self.subdict = subdict

    def describe(self) -> str:
        return f'INCLUDEDICT({self.subdict.describe()})'


class PythonDictPair(PythonElement):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def describe(self) -> str:
        return f'DICTPAIR({self.key.describe()}: {self.value.describe()})'


class PythonUnpack(PythonElement):
    def __init__(self, var):
        self.var = var

    def describe(self) -> str:
        return f'UNPACK({self.var.describe()})'


class PythonDestructure(PythonElement):
    def __init__(self, elements):
        self.elements = elements

    def describe(self) -> str:
        return f'DESTRUCTURE({", ".join(e.describe() for e in self.elements)})'


class PythonForComprehension(PythonElement):
    def __init__(self, vars, container, rest):
        self.vars = vars
        self.container = container
        self.rest = rest

    def describe(self) -> str:
        d_rest = '' if self.rest is None else f'; {self.rest.describe()}'
        return (f'FORC({", ".join(v.describe() for v in self.vars)}{ELEMENT_OF_SYMBOL}{self.container.describe()}'
                f'{d_rest})')


class PythonIfComprehension(PythonElement):
    def __init__(self, condition, rest):
        self.condition = condition
        self.rest = rest

    def describe(self) -> str:
        d_rest = '' if self.rest is None else f'; {self.rest.describe()}'
        return f'IFC({self.condition.describe()}{d_rest})'


class PythonSubscripted(PythonElement):
    def __init__(self, obj, subscripts):
        self.obj = obj
        self.subscripts = subscripts

    def describe(self) -> str:
        return f'SUB({self.obj.describe()}; {", ".join(s.describe() for s in self.subscripts)})'


class PythonSlice(PythonElement):
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step

    def describe(self) -> str:
        start = self.start.describe() if self.start else ''
        stop = self.stop.describe() if self.stop else ''
        step = self.step.describe() if self.step else ''
        return f'SLICE({start}:{stop}:{step})'


class PythonFuncDef(PythonElement, BindingScope):
    @disown('name')
    def __init__(self, name, pars, res_type, body):
        self.name = name
        self.pars = pars
        self.res_type = res_type
        self.body = body
        self.frame = None
        self.decorators = []

    def describe(self) -> str:
        res_type = f'→{self.res_type.describe()}' if self.res_type else ''
        return f'DEF({self.name}; {self.pars.describe()}{res_type}: {self.body.describe()})'


class PythonParmlist(PythonElement):
    def __init__(self, args):
        self.args = args

    def describe(self) -> str:
        return f'PARMS({", ".join(a.describe() for a in self.args)})'


# FIXME: replace by correct value when following function is fixed
SET_TYPE = MClassType(QualifiedName('Set', lexical_path=TYPING_LEXICAL_PATH))
MAPPING_TYPE = MClassType(QualifiedName('Mapping', lexical_path=TYPING_LEXICAL_PATH))
MAPPING_BUILTIN_TYPE = MClassType(MAPPING_QN)
TOTAL_MAPPING_TYPE = MClassType(TOTAL_MAPPING_QN)
TUPLE_TYPE = MClassType(QualifiedName('Tuple', lexical_path=TYPING_LEXICAL_PATH))
TUPLE_BUILTIN_TYPE = MClassType(TUPLE_QN)

UNION_TYPE = MClassType(QualifiedName('Union', lexical_path=TYPING_LEXICAL_PATH))
COLLECTION_TYPE = MClassType(QualifiedName('Collection', lexical_path=TYPING_LEXICAL_PATH))
SEQUENCE_TYPE = MClassType(QualifiedName('Sequence', lexical_path=TYPING_LEXICAL_PATH))

PARTIAL_MAPPING_TYPES_GROUP = {MAPPING_BUILTIN_TYPE, MAPPING_TYPE}
TUPLE_TYPES_GROUP = {TUPLE_BUILTIN_TYPE, TUPLE_TYPE}


def python_type_to_abstract(python_type):
    """
    Convert an expression describing a Python type to an MType object.
    :param python_type: a PythonElement describing a type
    :return: the corresponding MType
    """
    if not python_type:
        return M_ANY
    if isinstance(python_type, PythonVariable):
        # FIXME: restore condition once fixes below are implemented
        # and (is_python_builtin(name := python_type.name) or is_unknown_name(name)):
        result = ATOMIC_PYTHON_TYPES.get(python_type.name.name)
        if result:
            return result
        # FIXME! temporary workaround: just use the name
        return MClassType(python_type.name)
    # FIXME! deal with other types, including variables defined as types; need to treat imports
    # FIXME! temporary workaround: just use the name
    if isinstance(python_type, PythonSubscripted):
        obj_type = python_type_to_abstract(python_type.obj)
        if obj_type == SET_TYPE:
            assert len(python_type.subscripts) == 1
            return MSetType(python_type_to_abstract(python_type.subscripts[0]))
        elif obj_type in PARTIAL_MAPPING_TYPES_GROUP:
            assert len(python_type.subscripts) == 2
            return MMappingType(*map(python_type_to_abstract, python_type.subscripts), total=False)
        elif obj_type == TOTAL_MAPPING_TYPE:
            assert len(python_type.subscripts) == 2
            return MMappingType(*map(python_type_to_abstract, python_type.subscripts), total=True)
        elif obj_type in TUPLE_TYPES_GROUP:
            return MTupleType(map(python_type_to_abstract, python_type.subscripts))
        elif obj_type == UNION_TYPE:
            return MUnionType(set(map(python_type_to_abstract, python_type.subscripts)))
        elif obj_type in (COLLECTION_TYPE, SEQUENCE_TYPE):
            assert len(python_type.subscripts) == 1
            return MCollectionType(python_type_to_abstract(python_type.subscripts[0]))
    raise Exception('Complete implementation of python_type_to_abstract!')


class PythonParm(PythonElement):
    @disown('name', 'kind')
    def __init__(self, name, *, init=None, ptype=None, kind: ParmKind = POS_AND_KW):
        self.name = name
        self.init = init
        self.ptype = ptype
        self.kind = kind
        self.frame = None

    def as_parameter_descriptor(self):
        return ParameterDescriptor(self.name, python_type_to_abstract(self.ptype), self.kind)

    def with_init(self, init):
        return PythonParm(self.name, init=init, ptype=self.ptype, kind=self.kind)

    def with_kind(self, kind: ParmKind):
        return PythonParm(self.name, init=self.init, ptype=self.ptype, kind=kind)

    def describe(self) -> str:
        special_kind = '*' if self.kind == REST_PARM else '**' if self.kind == KEYWORDS_PARM else ''
        init = f'={self.init.describe()}' if self.init else ''
        type_desc = f': {self.ptype.describe()}' if self.ptype else ''
        kind = f'/{self.kind.kind}' if self.kind not in SPECIAL_PARMS else ''
        return f'PARM({special_kind}{self.name}{type_desc}{init}{kind})'


class PythonRestParm(PythonElement):
    def __init__(self, arg):
        self.arg = arg.with_kind(REST_PARM)

    def describe(self) -> str:
        return f'RESTPARM({self.arg.describe()})'


class PythonKeywordParm(PythonElement):
    def __init__(self, arg):
        self.arg = arg.with_kind(KEYWORDS_PARM)

    def describe(self) -> str:
        return f'KWPARM({self.arg.describe()})'


class PythonClass(PythonElement, BindingScope):
    @disown('name')
    def __init__(self, name, superclasses, members):
        self.name = name
        self.superclasses = superclasses
        self.members = members
        self.frame = None
        self.decorators = []

    def describe(self) -> str:
        superclasses = f'({", ".join(s.describe() for s in self.superclasses)})' if self.superclasses else ''
        return f'CLASS({self.name}{superclasses}: {self.members.describe()})'


class PythonDecorated(PythonElement):
    def __init__(self, decorators, decorated):
        self.decorators = decorators
        self.decorated = decorated
        # stick decorators directly onto decorated object
        decorated.decorators = decorators

    def describe(self) -> str:
        return (f'DECORATED({", ".join(d.describe() for d in self.decorators)}: '
                f'{self.decorated.describe()})')


class PythonAssignment(PythonElement):
    @disown('operator')
    def __init__(self, lhs, operator, rhs):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def describe(self) -> str:
        return f'ASSIGN({self.operator}; {self.lhs.describe()}, {self.rhs.describe()})'


class PythonTypedExpr(PythonElement):
    def __init__(self, expr, type_decl):
        self.expr = expr
        self.type_decl = type_decl

    def describe(self) -> str:
        return f'TYPED({self.expr.describe()}: {self.type_decl.describe()})'


class PythonImport(PythonElement):
    def __init__(self, names):
        self.names = names

    def describe(self) -> str:
        return f'IMPORT({", ".join(name.describe() for name in self.names)})'


class PythonImportFrom(PythonElement):
    def __init__(self, package, names):
        self.package = package
        self.names = names

    def describe(self) -> str:
        return f'IMPORT-FROM({self.package.describe()}: {", ".join(name.describe() for name in self.names)})'


class PythonImportAs(PythonElement):
    def __init__(self, name, new_name):
        self.name = name
        self.new_name = new_name

    def describe(self) -> str:
        as_name = f'→{self.new_name})' if self.new_name is not None else ''
        return f'AS({self.name}{as_name}'


class PythonImportAll(PythonElement):
    def describe(self) -> str:
        return f'*'


class PythonAssert(PythonElement):
    def __init__(self, test, doc=None):
        self.test = test
        self.doc = doc

    def describe(self) -> str:
        doc = f'; {self.doc.describe()}' if self.doc else ''
        return f'ASSERT({self.test.describe()}{doc})'


# Visitor abstract class

# @visitor_for(PythonElement)
class AbstractPythonVisitor:
    pass
