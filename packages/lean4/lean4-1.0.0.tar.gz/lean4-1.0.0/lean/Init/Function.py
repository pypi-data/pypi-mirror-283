import re, ast, inspect, sympy, std, types
from sympy import Symbol
from std import __set__, computed
from .Type import *


class CompilerError(Exception):

    def __init__(self, message, inst):
        self.message = message
        self.lineno = inst.lineno
        self.end_lineno = inst.end_lineno
        self.col_offset = inst.col_offset
        self.end_col_offset = inst.end_col_offset


class Function(type):

    @classmethod
    def __prepare__(cls, name, bases, **__dict__):
        return TypedOrderedDict()

    @classmethod
    def create_function(cls, func, __slots__, __annotations__):
        __spec__ = [(var, __annotations__[var], None) for var in __slots__]
        if __kwdefaults__ := func.__kwdefaults__:
            for key, value in __kwdefaults__.items():
                index = __slots__.index(key)
                __spec__[index] = __spec__[index][:-1], value

        __spec__ = tuple(__spec__)

        return_type = __annotations__['return']
        if isinstance(return_type, types.FunctionType):
            co_varnames = return_type.__code__.co_varnames
            indices = []
            for i, (key, dtype, default) in enumerate(__spec__):
                if key in co_varnames:
                    indices.append(i)
            
            indices = tuple(indices)

        def function(*args, **kwargs):
            args = [*args]
            for i, (key, dtype, default) in enumerate(__spec__):
                if i >= len(args):
                    args.append(kwargs.get(key, default))
                if not isinstance(args[i], dtype):
                    args[i] = dtype(args[i])
            ret = func(*args)

            if isinstance(dtype := return_type, types.FunctionType):
                dtype = dtype(*(args[index] for index in indices))

            assert isinstance(ret, dtype), f'Expected {dtype}, got {type(ret)}'
            return ret
        return function

    @classmethod
    def assertion(cls, func):
        assert not Compiler(func).is_infinitely_recursive, f'''
fail to show termination for
{func.__name__}
with errors
structural recursion cannot be used

well-founded recursion cannot be used, '{func.__name__}' does not take any (non-fixed) arguments
'''

    def __new__(cls, name, bases, __dict__):
        cls = super().__new__(cls, name, bases, __dict__)
        if bases:
            func = cls.__new__
            func.__slots__ = func.__code__.co_varnames[1:func.__code__.co_argcount]
            func.__annotations__ = OrderedDict(
                (key, func.__annotations__[key])
                for key in (*func.__slots__, 'return')
            )

            func.__name__ = cls.__name__
            cls = template(func, tuple(value for key, value in cls.__dict__.items() if not key.startswith('__')))
        return cls

    def __call__(cls, func):
        __slots__ = func.__code__.co_varnames[:func.__code__.co_argcount]
        __annotations__ = getattr(func, '__annotations__', {})
        cls.assertion(func)
        return cls.create_function(func, __slots__, __annotations__)


class Function(metaclass=Function):
    ...


# C++ template function
class template:
    '''
    lean4 version of the C++ template function:
    template <typename α, typename β, typename γ>
    auto function(α x, β y) -> γ {
        return static_cast<γ>(std::pow(x, y));
    }
    '''
    def __init__(self, func, __args__):
        self.cache = {}
        self.func = func  # template function
        self.__args__ = __args__  # template arguments
        assert __args__, f'{func.name} has no template arguments'
    
    def __getitem__(self, dtypes):
        if not isinstance(dtypes, tuple):
            dtypes = dtypes,
        
        __args__ = self.__args__
        if len(dtypes) < len(__args__):
            dtypes += __args__[len(dtypes):]

        if function := std.getitem(self.cache, *dtypes):
            return function

        func = self.func
        __annotations__ = OrderedDict(func.__annotations__)
        for key, value in __annotations__.items():
            if isinstance(value, dict):
                (cls, args), = value.items()
                assert isinstance(args, tuple), f'Expected tuple, got {type(args)}'
                args = [*args]
                for name, dtype in zip(__args__, dtypes):
                    for i, arg in enumerate(args):
                        if name == arg:
                            args[i] = dtype

                __annotations__[key] = cls[tuple(args)]
            elif isinstance(value, Type):
                for name, dtype in zip(__args__, dtypes):
                    if name == value:
                        __annotations__[key] = dtype
                        break

        Function.assertion(func)
        cls = std.Object()
        for var, dtype in zip(__args__, dtypes):
            assert isinstance(dtype, type), f'Expected type, got {dtype}'
            cls[var.name] = dtype
        function = Function.create_function(lambda *args: func(cls, *args), func.__slots__, __annotations__)
        std.setitem(self.cache, *dtypes, function)
        return function

    def __call__(self, *args):
        func = self.func
        assert len(args) + 1 == len(func.__annotations__)  # self.__annotations__ has an extra 'return' key!
        # determine the template args automatically
        __args__ = self.__args__
        _Ty = [None] * len(__args__)
        for arg, annotation in zip(args, func.__annotations__.values()):
            if isinstance(annotation, dict):
                (cls, annotated_args), = annotation.items()
                __mro__ = arg.__class__.__mro__
                if realized_annotations := __mro__[0].__annotations__:
                    # template structure types
                    for key, template_arg in __mro__[1].__annotations__.items():
                        if realized_arg := realized_annotations.get(key):
                            if isinstance(template_arg, Type):
                                try:
                                    index = __args__.index(template_arg)
                                    assert template_arg in annotated_args, f'Expected {template_arg} in {annotated_args}'
                                    if _Ty[index]:
                                        assert _Ty[index] == realized_arg, f'Expected {_Ty[index]} == {realized_arg}'
                                    else:
                                        _Ty[index] = realized_arg
                                except ValueError:
                                    ...
                else:
                    realized_annotations = __mro__[1].__annotations__
                    # template inductive types
                    for key, template_annotation in __mro__[2].__annotations__.items():
                        if realized_annotation := realized_annotations.get(key):
                            if isinstance(template_annotation, tuple):
                                template_args_annotation, template_return_annotation = template_annotation
                                if isinstance(template_args_annotation, types.GenericAlias):
                                    assert isinstance(realized_annotation, tuple)
                                    for template_arg, realized_arg in zip(template_args_annotation.__args__, realized_annotation):
                                        try:
                                            index = __args__.index(template_arg)
                                            assert template_arg in annotated_args, f'Expected {template_arg} in {annotated_args}'
                                            if _Ty[index]:
                                                assert _Ty[index] == realized_arg, f'Expected {_Ty[index]} == {realized_arg}'
                                            else:
                                                _Ty[index] = realized_arg
                                        except ValueError:
                                            ...
        try:
            index = _Ty.index(None)
            raise Exception(f"could not deduce template argument for '{__args__[index]}'")
        except ValueError:
            return self[tuple(_Ty)](*args)


# https://en.wikipedia.org/wiki/Halting_problem
class Compiler(ast.NodeVisitor):
    
    def __init__(self, func):
        self.func = func
        # Get the source code of the function
        self.source = inspect.getsource(func)

    @computed
    def indent(self):
        return len(re.match('\s*', self.source)[0]) // 4

    def visit_Call(self, node):
        # Check if the function call is to the function we are analyzing
        if isinstance(node.func, ast.Name) and node.func.id == self.func.__name__:
            self.is_recursive = True
        self.generic_visit(node)

    @computed
    def parsingTree(self):
        # Parse the source code into an AST
        return ast.parse(self.source)

    @computed
    def is_recursive(self):
        if len(re.findall('\\b' + self.func.__name__ + '\\b', self.source)) > 1:
            self.is_recursive = None
            # Visit the AST nodes
            self.visit(self.parsingTree)
            return self.is_recursive
    
    @is_recursive.setter
    def is_recursive(self, is_recursive):
        self.__dict__['is_recursive'] = is_recursive

    @property
    def is_infinitely_recursive(self):
        if self.is_recursive:
            expr = self.sympy_expr(self.locals)
            func = self.sympy_func
            vars = tuple(self.sympy_args.values())
            func.eval = sympy.Lambda(vars, expr)
            return func.is_infinitely_recursive

    @computed
    def sympy_func(self):
        kwargs = {}
        func = self.func
        dtype = func.__annotations__['return']
        match dtype.__name__:
            case 'bool':
                kwargs['bool'] = True
            case 'int':
                kwargs['integer'] = True
            case 'float':
                kwargs['real'] = True
            case 'complex':
                kwargs['complex'] = True
            case _:
                raise TypeError(f"Unsupported type {dtype}")
        return sympy.Function(func.__name__, **kwargs)

    @computed
    def locals(self):
        func = self.func
        if isinstance(func, type):
            return OrderedDict()

        globals = func.__globals__
        locals = OrderedDict(
            (var, globals[var])
            for var in func.__code__.co_names if var in globals
        )
        if self.is_recursive:
            locals[func.__name__] = self.sympy_func
        return locals | self.sympy_args

    @computed
    def sympy_args(self):
        # Extract argument information
        func = self.func
        kwargs = OrderedDict()
        __annotations__ = func.__annotations__
        for var in inspect.signature(func).parameters:
            dtype = __annotations__[var]
            if dtype is type:
                val = var
            elif dtype.is_integer:
                if dtype.is_nonnegative:
                    val = Symbol(var, integer=True, negative=False, domain=dtype)
                else:
                    val = Symbol(var, integer=True)
            elif dtype.is_rational:
                val = Symbol(var, rational=True)
            elif dtype.is_real:
                val = Symbol(var, real=True)
            elif dtype.is_complex:
                val = Symbol(var, complex=True)
            else:
                raise TypeError(f'Unsupported type {dtype}')

            kwargs[var] = val
            # print(val.domain)
        
        return kwargs

    def sympy_expr(self, locals):
        return self.parsingTree.body[0].sympy_expr(locals)


@__set__(ast.Name)
def sympy_vars(self):
    return self.id


@__set__(ast.Tuple)
def sympy_vars(self):
    return tuple(var.sympy_vars() for var in self.elts)


@__set__(ast.FunctionDef)
def sympy_expr(self, locals):
    *statement, last = self.body
    for statement in statement:
        locals = statement.sympy_expr(locals)
    return last.sympy_expr(locals)


@__set__(ast.ClassDef)
def sympy_expr(self, locals):
    *statement, last = self.body
    for statement in statement:
        locals = statement.sympy_expr(locals)

    if isinstance(last, ast.FunctionDef) and last.name == '__new__':
        args = last.args.sympy_expr(locals)
        args['return'] = last.returns.sympy_expr(locals)
        return args
    else:
        return last.sympy_expr(locals)


@__set__(ast.arguments)
def sympy_expr(self, locals):
    return OrderedDict(
        arg.sympy_expr(locals)
        for arg in self.args
    )


@__set__(ast.arg)
def sympy_expr(self, locals):
    if annotation := self.annotation:
        annotation = annotation.sympy_expr(locals)
    return self.arg, annotation


@__set__(ast.Subscript)
def sympy_expr(self, locals):
    return self.value.sympy_expr(locals)[self.slice.sympy_expr(locals)]


@__set__(ast.Tuple)
def sympy_expr(self, locals):
    return tuple(elt.sympy_expr(locals) for elt in self.elts)


@__set__(ast.Match)
def sympy_expr(self, locals):
    subject = self.subject.sympy_expr(locals)
    conds = []
    for case in self.cases:
        pattern, value = case.sympy_expr(locals)

        func = sympy.Element if pattern.etype and subject.dtype in pattern.etype else sympy.Equal
        conds.append([value, func(subject, pattern)])
    conds[-1][-1] = True
    return sympy.Piecewise(*conds)


@__set__(ast.Name)
def sympy_expr(self, locals):
    id = self.id
    if id not in locals:
        try:
            return eval(id)
        except NameError:
            raise CompilerError(f'Variable {id} not declared', self)
    
    return locals[id]


@__set__(ast.match_case)
def sympy_expr(self, locals):
    *statement, value = self.body
    for statement in statement:
        locals = statement.sympy_expr(locals)
    
    return self.pattern.sympy_expr(locals), value.sympy_expr(locals)


@__set__(ast.MatchValue)
def sympy_expr(self, locals):
    return self.value.sympy_expr(locals)


@__set__(ast.MatchClass)
def sympy_expr(self, locals):
    return self.cls.sympy_expr(locals)


@__set__(ast.Return)
def sympy_expr(self, locals):
    return self.value.sympy_expr(locals)


@__set__(ast.Attribute)
def sympy_expr(self, locals):
    value = self.value.sympy_expr(locals)
    attr = self.attr
    if isinstance(value, Symbol):
        from .Prelude import Nat
        if value.domain is Nat:
            if attr == 'args':
                return value - 1,

    value = getattr(value, attr)
    return sympy.sympify(value)


@__set__(ast.Constant)
def sympy_expr(self, locals):
    return sympy.sympify(self.value)


@__set__(ast.Assign)
def sympy_expr(self, locals):
    var = [target.sympy_vars() for target in self.targets]
    if len(var) == 1:
        var, = var
    val = self.value.sympy_expr(locals)
    locals = OrderedDict(locals)
    if isinstance(var, tuple):
        for var, val in zip(var, val):
            locals[var] = val
    elif val is type:
        locals[var] = {var: val}
    else:
        locals[var] = val

    return locals


@__set__(ast.AnnAssign)
def sympy_expr(self, locals):
    var = self.target.sympy_vars()
    annotation = self.annotation.sympy_expr(locals)
    val = self.value.sympy_expr(locals)
    locals = OrderedDict(locals)
    if isinstance(var, tuple):
        for var, val in zip(var, val):
            locals[var] = val
    elif annotation is type:
        locals[var] = {var: val}
    else:
        locals[var] = {var: (annotation, val)}

    return locals


@__set__(ast.UnaryOp)
def sympy_expr(self, locals):
    operand = self.operand.sympy_expr(locals)
    match self.op:
        case ast.Invert():
            return ~operand
        case ast.Not():
            return sympy.Not(operand)
        case ast.UAdd():
            return +operand
        case ast.USub():
            return -operand


@__set__(ast.BinOp)
def sympy_expr(self, locals):
    left = self.left.sympy_expr(locals)
    right = self.right.sympy_expr(locals)
    match self.op:
        case ast.Add():
            return left + right
        case ast.BitAnd():
            return left & right
        case ast.BitOr():
            return left | right
        case ast.BitXor():
            return left ^ right
        case ast.Div():
            return left / right
        case ast.FloorDiv():
            return left // right
        case ast.LShift():
            return left << right
        case ast.Mod():
            return left % right
        case ast.Mult():
            return left * right
        case ast.MatMult():
            return left @ right
        case ast.Pow():
            return left ** right
        case ast.RShift():
            return left >> right


@__set__(ast.Call)
def sympy_expr(self, locals):
    return self.func.sympy_expr(locals)(*(arg.sympy_expr(locals) for arg in self.args))


__all__ = 'Function',