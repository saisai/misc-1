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

class Frame:
    def __init__(self, f_code, f_locals, vm):
        self.f_code = f_code
        self.f_locals = f_locals
        self.f_globals = vm.f_globals
        self.f_builtins = globals()['__builtins__']

        self.f_lasti = 0
        self.blockstack = []

        if verbose == 2:
            print self
            print '    f_locals: %s' % f_locals

    def __str__(self):
        return '<frame at 0x%s>' % hex(id(self))[2:]


class Function:
    def __init__(self, code, defargs, vm):
        self.code = code
        self.name = code.co_name
        self.defargs = defargs

        if verbose == 2:
            print self
            print '    defargs: %s' % defargs

    def __str__(self):
        return '<function %s at 0x%s>' % (self.code.co_name, hex(id(self))[2:])

    def init_locals(self, args, kw):
        argnames = self.code.co_varnames[:self.code.co_argcount]
        pos = len(argnames)-len(self.defargs)
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


class VirtualMachine:
    def __init__(self, opts):
        self._frames = [] # list of stack frames
        self._stack  = [] # stack
        self.returnValue = None
        self.f_globals = {}

        global suppress, verbose
        suppress = opts.suppress
        verbose  = opts.verbose

    def loadCode(self, code, f_locals={}):
        if verbose == 2:
            print 'loadCode:', code.co_name
            print '    f_locals: %s' % f_locals

        self._frames.append(Frame(code, f_locals, self))

    def getInst(self):
        """Get instruction and argument (if present) from top frame and
           return (i) opName (ii) was arg found (iii) arg"""
        frame = self.frame()
        byte = frame.f_code.co_code[frame.f_lasti]
        frame.f_lasti += 1

        opCode = ord(byte)
        opName = dis.opname[opCode]
        if verbose: print '%2s %-20s' % (len(self._frames),  opName),

        if opCode >= dis.HAVE_ARGUMENT:
            opArg = frame.f_code.co_code[frame.f_lasti:frame.f_lasti+2]
            frame.f_lasti += 2

            intArg = ord(opArg[0]) + 256*ord(opArg[1])
            if verbose: print '%4s' % intArg,

            if opName.startswith('CALL_FUNCTION'):
                arg = map(ord, opArg)  #  (lenPosPar, lenKWPar)
                if verbose: print 'call_func',

            elif opCode in dis.hasconst:
                arg = frame.f_code.co_consts[intArg]
                if verbose: print 'hasconst',

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
        while self._frames:
            # pre will go here
            opName, has_arg, arg = self.getInst()

            if opName.startswith('UNARY_'):
                self.unaryOperator(opName)

            elif opName.startswith('BINARY_'):
                self.binaryOperator(opName)

            elif opName.count('SLICE+'):
                self.sliceOperator(opName)

            else:
                opFunc = getattr(self, 'op_' + opName, None)
                if not opFunc:
                    raise ValueError, "unknown opcode type: %s" % opName

                if has_arg:
                    opFunc(arg)
                else:
                    opFunc()

            if opName == 'RETURN_VALUE':
                self._frames.pop()
                self.push(self.returnValue)

            if verbose == 2:
                print 'Stack:', self._stack
                if self.frame():
                    print 'Block:', self.frame().blockstack

        return self.returnValue


    def frame(self):
        return self._frames and self._frames[-1] or None

    def pop(self, n=1):
        if n==1:
            return self._stack.pop()
        else:
            for i in xrange(n):
                self._stack.pop()

    def push(self, item):
        self._stack.append(item)

    def unaryOperator(self, op):
        op = op[6:]
        u = self.pop()
        self.push(UNARY_OPERATORS[op](u))

    def binaryOperator(self, op):
        op = op[7:]
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
        self.push(self._stack[-1])

    def op_ROT_TWO(self):
        self._stack[-1], self._stack[-2] = self._stack[-2], self._stack[-1]

    def op_ROT_THREE(self):
        self._stack[-1], self._stack[-2], self._stack[-3] = \
        self._stack[-2], self._stack[-3], self._stack[-1]

    def op_ROT_FOUR(self):
        self._stack[-1], self._stack[-2], self._stack[-3], self._stack[-4] = \
        self._stack[-2], self._stack[-3], self._stack[-4], self._stack[-1]

    def op_STORE_SUBSCR(self):
        w = self._stack[-1]
        v = self._stack[-2]
        u = self._stack[-3]
        v[w] = u
        self.pop(3)

    def op_DELETE_SUBSCR(self):
        w = self._stack[-1]
        v = self._stack[-2]
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

    def op_POP_BLOCK(self):
        self.frame().blockstack.pop()

    def op_LIST_APPEND(self):
        w = self.pop()
        v = self.pop()
        v.append(w)

    def op_STORE_NAME(self, name):
        item = self.pop()
        self.frame().f_locals[name] = item
        self.frame().f_globals[name] = item

    def op_STORE_GLOBAL(self, name):
        self.frame().f_globals[name] = self.pop()

    def op_DELETE_NAME(self, name):
        del self.frame().f_locals[name]

    def op_DELETE_GLOBAL(self, name):
        del self.frame().f_globals[name]

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

    def op_LOAD_NAME(self, name):
        frame = self.frame()
        if name in frame.f_locals:
            item = frame.f_locals[name]

        elif name in frame.f_globals:
            item = frame.f_globals[name]

        elif name in frame.f_builtins:
            item = frame.f_builtins[name]

        self.push(item)

    def op_BUILD_TUPLE(self, count):
        lst = [self.pop() for i in xrange(count)]
        lst.reverse()
        self.push(tuple(lst))

    def op_BUILD_LIST(self, count):
        lst = [self.pop() for i in xrange(count)]
        lst.reverse()
        self.push(lst)

    def op_BUILD_MAP(self, zero):
        assert zero == 0
        self.push({})

    def op_COMPARE_OP(self, opnum):
        u = self.pop()
        v = self.pop()
        self.push(COMPARE_OPERATORS[opnum](v, u))

    def op_JUMP_IF_TRUE(self, jump):
        if self._stack[-1]:
            self.frame().f_lasti = jump

    def op_JUMP_IF_FALSE(self, jump):
        if not self._stack[-1]:
            self.frame().f_lasti = jump

    def op_JUMP_FORWARD(self, jump):
        self.frame().f_lasti = jump

    def op_JUMP_ABSOLUTE(self, jump):
        self.frame().f_lasti = jump

    def op_LOAD_GLOBAL(self, name):
        f = self.frame()
        if name in f.f_globals:
            self.push(f.f_globals[name])

        elif name in f.f_builtins:
            self.push(f.f_builtins[name])

    def op_SETUP_LOOP(self, dest):
        self.frame().blockstack.append(('loop', dest))

    def op_LOAD_FAST(self, name):
        self.push(self.frame().f_locals[name])

    def op_STORE_FAST(self, name):
        self.frame().f_locals[name] = self.pop()

    def op_LOAD_DEREF(self, name):
        self.push(self.frame()._cells[name].get())

    def op_CALL_FUNCTION(self, (lenPosPar, lenKWPar)):
        kw = {}
        for i in xrange(lenKWPar):
            val = self.pop()
            key = self.pop()
            kw[key] = val

        args = [self.pop() for i in xrange(lenPosPar)]
        args.reverse()

        func = self.pop()

        if isinstance(func, Function):
            self.loadCode(func.code, func.init_locals(args, kw))
        else:
            self.push(func(*args, **kw))

    def op_MAKE_FUNCTION(self, argc):
        code = self.pop()
        defargs = [self.pop() for i in xrange(argc)]
        defargs.reverse()
        self.push(Function(code, defargs, self))

    def op_GET_ITER(self):
        self.push(iter(self.pop()))

    def op_FOR_ITER(self, jump):
        iterobj = self._stack[-1]
        try:
            v = iterobj.next()
            self.push(v)
        except StopIteration:
            self.pop()
            self.frame().f_lasti = jump


if __name__ == "__main__":
    pass
