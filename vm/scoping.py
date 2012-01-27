def outer():
    a = 1
    # creating a lexically nested function bar
    def inner():
        # a is visible from outer's locals
        return a
    b = 2 # b is here for an example later on
    return inner

# inner_nonlexical will be called from within
#  outer_nonlexical but it is not lexically nested
def inner_nonlexical():
    return a # a is not visible

def outer_nonlexical():
    a = 1
    inner = inner_nonlexical
    b = 2 # b is here for an example later on
    return inner_nonlexical

print outer()()
