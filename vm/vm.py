import dis
import operator


suppress = False
verbose = 0

UNARY_OPERATORS = {
    'POSITIVE': operator.pos,
    'NEGATIVE': operator.neg,
    'NOT':      operator.not_,
}

BINARY_OPERATORS = {
    'POWER':    pow,
    'MULTIPLY': operator.mul,
    'DIVIDE':   operator.div,
    'MODULO':   operator.mod,
    'ADD':      operator.add,
    'SUBTRACT': operator.sub,
    'SUBSCR':   operator.getitem,
    'LSHIFT':   operator.lshift,
    'RSHIFT':   operator.rshift,
    'AND':      operator.and_,
    'XOR':      operator.xor,
    'OR':       operator.or_,
}

COMPARE_OPERATORS = [
    operator.lt,
    operator.le,
    operator.eq,
    operator.ne,
    operator.gt,
    operator.ge,
]

class Cell:

    def __init__(self):
        self._deref = None

    def set(self, deref):
        self._deref = deref

    def get(self):
        return self._deref


class Frame:

    def __init__(self, f_code, f_globals, f_locals, vm):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_locals = f_locals
        self.f_back = vm.frame()
        if self.f_back:
            self.f_builtins = self.f_back.f_builtins
        else:
            self.f_builtins = f_locals['__builtins__']
            if hasattr(self.f_builtins, '__dict__'):
                self.f_builtins = self.f_builtins.__dict__

        self.f_restricted = 1
        self.f_lineno = f_code.co_firstlineno
        self.f_lasti = 0

        if f_code.co_cellvars:
            self._cells = {}
            if not self.f_back._cells:
                self.f_back._cells = {}
            for var in f_code.co_cellvars:
                self.f_back._cells[var] = self._cells[var] = Cell()
                if self.f_locals.has_key(var):
                    self._cells[var].set(self.f_locals[var])
        else:
            self._cells = None

        if f_code.co_freevars:
            if not self._cells:
                self._cells = {}
            for var in f_code.co_freevars:
                self._cells[var] = self.f_back._cells[var]

        self.blockstack = []

        if verbose == 2:
            print self
            print '    f_locals: %s' % f_locals

    def __str__(self):
        return '<frame at 0x%s>' % hex(id(self))[2:]


class Function:

    def __init__(self, func_code, func_doc, func_defaults, func_closure, vm):
        self._vm = vm
        self.func_code = func_code
        self.func_name = func_code.co_name
        self.func_doc = func_doc
        self.func_defaults = func_defaults
        self.func_globals = vm.frame().f_globals
        self.func_dict = vm.frame().f_locals
        self.func_closure = func_closure

    def __str__(self):
        return '<function %s at 0x%s>' % (self.func_name, hex(id(self))[2:])

    def __call__(self, *args, **kw):
        if len(args) < self.func_code.co_argcount:
            if not self.func_defaults:
                if self.func_code.co_argcount == 0:
                    argCount = 'no arguments'
                elif self.func_code.co_argcount == 1:
                    argCount = 'exactly 1 argument'
                else:
                    argCount = ('exactly %i arguments' %
                                self.func_code.co_argcount)
                raise TypeError('%s() takes %s (%s given)' % (
                        self.func_name, argCount, len(args)))
            else:
                defArgCount = len(self.func_defaults)
                args.extend(self.func_defaults[
                        - (self.func_code.co_argcount - len(args)):])

        self._vm.loadCode(self.func_code, args, kw,
                          self.func_globals, self.func_dict)

    def init_locals(self, args, kw):
        argnames = self.code.co_varnames[:self.code.co_argcount]
        pos = len(argnames) - len(self.defargs)
        if verbose == 2:
            print 'init_locals'
            print '   argnames:', argnames
            print '   args, kw:', args, kw
            print '   defargs :', self.defargs, pos

        for k in kw:
            if k not in argnames:
                exit('%s() got an unexpected keyword argument %r' %
                     (self.name, k))
        res = {}
        for i, val in enumerate(self.defargs):
            var = argnames[i+pos]
            res[var] = val

        for i, val in enumerate(args):
            var = argnames[i]
            res[var] = val

        res.update(kw)
        if verbose == 2:
            print '   result  :', res
        assert len(res) == len(argnames)
        return res


class Class:

    def __init__(self, name, bases, methods):
        self._name = name
        self._bases = bases
        self._locals = methods

    def __call__(self, *args, **kw):
        return Object(self, self._name, self._bases, self._locals, args, kw)

    def __str__(self):
        return '<class %s at %s>' % (self._name, 
                                     hex(id(self))[2:].upper().zfill(8))

    def isparent(self, obj):
        if not isinstance(obj, Object):
            return 0
        if obj._class is self:
            return 1
        if self in obj._bases:
            return 1
        return 0


class Object:

    def __init__(self, _class, name, bases, methods, args, kw):
        self._class = _class
        self._name = name
        self._bases = bases
        self._locals = methods
        if methods.has_key('__init__'):
            methods['__init__'](self, *args, **kw)

    def __str__(self):
        return '<%s instance at %s>' % (self._name,
                                        hex(id(self))[2:].upper().zfill(8))


class Method:

    def __init__(self, object, _class, func):
        self.im_self = object
        self.im_class = _class
        self.im_func = func

    def __str__(self):
        if self.im_self:
            return '<bound method %s.%s of %s>' % (self.im_self._name,
                                                   self.im_func.func_name,
                                                   str(self.im_self))
        else:
            return '<unbound method %s.%s>' % (self.im_class._name,
                                               self.im_func.func_name)


class VirtualMachine:

    def __init__(self, opts):
        self.frames = [] # list of stack frames
        self.stack  = [] # stack
        self.returnValue = None
        self.f_globals = {}

        global suppress, verbose
        suppress = opts.suppress
        verbose  = opts.verbose

    def loadCode(self, code, args=[], kw={}, f_globals=None, f_locals=None):
        if f_globals:
            f_globals = f_globals
            if not f_locals:
                f_locals = f_globals
        elif self.frame():
            f_globals = self.frame().f_globals
            f_locals = {}
        else:
            f_globals = f_locals = globals()

        for i in xrange(code.co_argcount):
            name = code.co_varnames[i]
            if i < len(args):
                if kw.has_key(name):
                    raise TypeError("got multiple values for keyword "
                                    "argument '%s'" % name)
                else:
                    f_locals[name] = args[i]
            else:
                if kw.has_key(name):
                    locals[name] = kw[name]
                else:
                    raise TypeError("did not get value for argument "
                                    "'%s'" % name)

        if verbose == 2:
            print 'loadCode:', code.co_name
            print '    f_locals: %s' % f_locals

        self.frames.append(Frame(code, f_globals, f_locals, self))

    def getInst(self):
        """Get instruction and argument (if present) from top frame and
           return (i) opName (ii) was arg found (iii) arg"""
        frame = self.frame()
        byte = frame.f_code.co_code[frame.f_lasti]
        frame.f_lasti += 1

        opCode = ord(byte)
        opName = dis.opname[opCode]
        if verbose: print '%2s %-20s' % (len(self.frames),  opName),

        if opCode >= dis.HAVE_ARGUMENT:
            opArg = frame.f_code.co_code[frame.f_lasti:frame.f_lasti+2]
            frame.f_lasti += 2

            intArg = ord(opArg[0]) + 256 * ord(opArg[1])
            if verbose: print '%4s' % intArg,

            if opName.startswith('CALL_FUNCTION'):
                arg = map(ord, opArg)  #  (lenPosPar, lenKWPar)
                if verbose: print 'call_func',

            elif opCode in dis.hasconst:
                arg = frame.f_code.co_consts[intArg]
                if verbose: print 'hasconst',

            elif opCode in dis.hasfree:
                if intArg < len(frame.f_code.co_cellvars):
                    arg = frame.f_code.co_cellvars[intArg]
                else:
                    arg = frame.f_code.co_freevars[
                            intArg-len(frame.f_code.co_cellvars)]

            elif opCode in dis.hasname:
                arg = frame.f_code.co_names[intArg]
                if verbose: print 'hasname',

            elif opCode in dis.hasjrel:
                arg = frame.f_lasti + intArg
                if verbose: print 'hasjrel',

            elif opCode in dis.hasjabs:
                arg = intArg
                if verbose: print 'hasjabs',

            elif opCode in dis.haslocal:
                arg = frame.f_code.co_varnames[intArg]
                if verbose: print 'haslocal',

            else:
                arg = intArg
                if verbose: print 'else',

            if verbose: print arg
            return opName, True, arg

        else:                                      # opcode had no oparg
            if verbose: print
            return opName, False, None


    def run(self):
        while self.frames:
            # pre will go here
            opName, has_arg, arg = self.getInst()
            finished = 0

            if opName.startswith('UNARY_'):
                self.unaryOperator(opName[6:])

            elif opName.startswith('BINARY_'):
                self.binaryOperator(opName[7:])

            elif 'SLICE+' in opName:
                self.sliceOperator(opName)

            else:
                opFunc = getattr(self, 'op_' + opName, None)
                if not opFunc:
                    raise ValueError, "unknown opcode type: %s" % opName

                arguments = [arg] if has_arg else []
                finished = opFunc(*arguments)

            if finished:
                self.frames.pop()
                self.push(self.returnValue)

#            if opName == 'RETURN_VALUE':
#                self.frames.pop()
#                self.push(self.returnValue)

            if verbose == 2:
                print 'Stack:', self.stack
                frame = self.frame()
                if frame:
                    print 'Block:', frame.blockstack
                    print 'Cells:', frame._cells

        return self.returnValue


    def frame(self):
        if self.frames:
            return self.frames[-1]

    def top(self):
        return self.stack[-1]

    def pop(self, n=1):
        if n==1:
            return self.stack.pop()
        else:
            for i in xrange(n):
                self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def unaryOperator(self, op):
        u = self.pop()
        self.push(UNARY_OPERATORS[op](u))

    def binaryOperator(self, op):
        u = self.pop()
        v = self.pop()
        self.push(BINARY_OPERATORS[op](v, u))

    def sliceOperator(self, op):
        num = int(op[-1])
        assert 0 <= num < 4
        start = 0
        end = None # we'll None to mean end
        if num == 1:
            start = self.pop()
        elif num == 2:
            end = self.pop()
        elif num == 3:
            end = self.pop()
            start = self.pop()
        lst = self.pop()
        if end == None:
            end = len(lst)
        if op.startswith('STORE_SLICE+'):
            lst[start:end] = self.pop()
        elif op.startswith('DELETE_SLICE+'):
            del lst[start:end]
        elif op.startswith('SLICE+'):
            self.push(lst[start:end])
        else:
            raise op

    def op_POP_TOP(self):
        self.pop()

    def op_DUP_TOP(self):
        self.push(self.top())

    def op_ROT_TWO(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def op_ROT_THREE(self):
        self.stack[-1], self.stack[-2], self.stack[-3] = \
        self.stack[-2], self.stack[-3], self.stack[-1]

    def op_ROT_FOUR(self):
        self.stack[-1], self.stack[-2], self.stack[-3], self.stack[-4] = \
        self.stack[-2], self.stack[-3], self.stack[-4], self.stack[-1]

    def op_STORE_SUBSCR(self):
        w = self.stack[-1]
        v = self.stack[-2]
        u = self.stack[-3]
        v[w] = u
        self.pop(3)

    def op_DELETE_SUBSCR(self):
        w = self.stack[-1]
        v = self.stack[-2]
        del v[w]
        self.pop(2)

    def op_PRINT_ITEM(self):
        tmp = self.pop()
        if not suppress:
            print tmp,

    def op_PRINT_NEWLINE(self):
        if not suppress:
            print

    def op_BREAK_LOOP(self):
        block = self.frame().blockstack.pop()
        while block[0] != 'loop':
            block = self.frame().blockstack.pop()
        self.frame().f_lasti = block[1]

    def op_LOAD_LOCALS(self):
        self.push(self.frame().f_locals)

    def op_RETURN_VALUE(self):
        self.returnValue = self.pop()
        func = self.top()
        if isinstance(func, Object):
            self.frames.pop()
        else:
            return 1

    def op_POP_BLOCK(self):
        self.frame().blockstack.pop()

    def op_LIST_APPEND(self, n):
        w = self.pop()
        v = self.stack[-n].append(w)

    def op_UNPACK_SEQUENCE(self, count):
        items = list(self.pop())
        for item in items[::-1]:
            self.push(item)

    def op_DUP_TOPX(self, count):
        items = [self.pop() for i in xrange(count)]
        for item in items[::-1]:
            self.push(item)

    def op_LOAD_CONST(self, const):
        self.push(const)

    def op_LOAD_ATTR(self, attr):
        obj = self.pop()
        if isinstance(obj, (Object, Class)):
            val = obj._locals[attr]
        else:
            val = getattr(obj, attr)
        if isinstance(obj, Object) and isinstance(val, Function):
            val = Method(obj, obj._class, val)
        elif isinstance(obj, Class) and isinstance(val, Function):
            val = Method(None, obj, val)
        self.push(val)

    # ------------ scope -------------

    def op_LOAD_NAME(self, name):
        frame = self.frame()
        try:
            item = frame.f_locals[name]
        except KeyError:
            try:
                item = frame.f_globals[name]
            except KeyError:
                item = frame.f_builtins[name]
        self.push(item)

    def op_STORE_NAME(self, name):
        self.frame().f_locals[name] = self.pop()

    def op_DELETE_NAME(self, name):
        del self.frame().f_locals[name]

    def op_LOAD_FAST(self, name):
        self.push(self.frame().f_locals[name])

    def op_STORE_FAST(self, name):
        self.frame().f_locals[name] = self.pop()

    def op_DELETE_FAST(self, name):
        del self.frame().f_locals[name]

    def op_LOAD_GLOBAL(self, name):
        frame = self.frame()
        if name in frame.f_globals:
            self.push(frame.f_globals[name])
        elif name in frame.f_builtins:
            self.push(frame.f_builtins[name])

    def op_STORE_GLOBAL(self, name):
        self.frame().f_globals[name] = self.pop()

    def op_DELETE_GLOBAL(self, name):
        del self.frame().f_globals[name]

    def op_LOAD_DEREF(self, name):
        self.push(self.frame()._cells[name].get())

    def op_STORE_DEREF(self, name):
        self.frame().freevars[name] = self.pop()

    def op_LOAD_CLOSURE(self, name):
        self.push(self.frame()._cells[name])

    # ------------------------- import 

    def op_IMPORT_NAME(self, name):
        self.push(__import__(name))

    def op_IMPORT_FROM(self, name):
        mod = self.pop()
        self.push(mod)
        self.push(getattr(mod, name))

    # -------------------------

    def op_BUILD_TUPLE(self, count):
        lst = [self.pop() for i in xrange(count)]
        lst.reverse()
        self.push(tuple(lst))

    def op_BUILD_LIST(self, count):
        lst = [self.pop() for i in xrange(count)]
        lst.reverse()
        self.push(lst)

    def op_BUILD_MAP(self, size):
        self.push({})

    def op_STORE_MAP(self):
        w = self.pop()
        u = self.pop()
        self.top()[w] = u

    def op_BUILD_CLASS(self):
        methods = self.pop()
        bases = self.pop()
        name = self.pop()
        self.push(Class(name, bases, methods))

    def op_STORE_ATTR(self, name):
        obj = self.pop()
        setattr(obj, name, self.pop())

    def op_COMPARE_OP(self, opnum):
        u = self.pop()
        v = self.pop()
        self.push(COMPARE_OPERATORS[opnum](v, u))

    def op_POP_JUMP_IF_TRUE(self, jump):
        if self.pop():
            self.frame().f_lasti = jump

    def op_POP_JUMP_IF_FALSE(self, jump):
        if not self.pop():
            self.frame().f_lasti = jump

    def op_JUMP_FORWARD(self, jump):
        self.frame().f_lasti = jump

    def op_JUMP_ABSOLUTE(self, jump):
        self.frame().f_lasti = jump

    def op_SETUP_LOOP(self, dest):
        self.frame().blockstack.append(('loop', dest))

    def op_SETUP_EXCEPT(self, dest):
        self.frame().blockstack.append(('except', dest))

    def op_CALL_FUNCTION(self, (lenPos, lenKw)):
        kw = {}
        for i in xrange(lenKw):
            val = self.pop()
            key = self.pop()
            kw[key] = val

        args = [self.pop() for i in xrange(lenPos)]
        args.reverse()

        func = self.pop()
        frame = self.frame()
        if hasattr(func, 'im_func'): # method
            if func.im_self:
                args.insert(0, func.im_self)
            if not func.im_class.isparent(args[0]):
                raise TypeError('unbound method %s() must be called with %s '
                                'instance as first argument (got %s instead)'
                                % (func.im_func.func_name,
                                   func.im_class._name, type(args[0])))
            func = func.im_func
        if hasattr(func, 'func_code'):
            self.loadCode(func.func_code, args, kw)
            if func.func_code.co_flags & 32: #CO_GENERATOR:
                raise NotImplementedError("cannot do generators ATM")
                gen = Generator(self.frame(), self)
                self._frames.pop()._generator = gen
                self.push(gen)
        else:
            self.push(func(*args, **kw))

    def op_MAKE_FUNCTION(self, argc):
        defargs = [self.pop() for i in xrange(argc)]
        defargs.reverse()
        code = self.pop()
        self.push(Function(code, None, defargs, None, self))

    def op_MAKE_CLOSURE(self, argc):
        code = self.pop()
        defaults = []
        for i in xrange(argc):
            defaults.insert(0, self.pop())
        closure = []
        if code.co_freevars:
            for i in code.co_freevars:
                closure.insert(0, self.pop())
        self.push(Function(code, None, defaults, closure, self))

    def op_GET_ITER(self):
        self.push(iter(self.pop()))

    def op_FOR_ITER(self, jump):
        iterobj = self.top()
        try:
            v = iterobj.next()
            self.push(v)
        except StopIteration:
            self.pop()
            self.frame().f_lasti = jump


if __name__ == "__main__":
    pass
