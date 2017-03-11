def foo(force, dry, changes):
    if dry or not (force or changes):
        return "skiping"
    return "repacking..."


for force in 0, 1:
    for dry in 0, 1:
        for changes in 0, 1:
            print 'force: %s   dry: %s   changes: %s     %s' % (
                force, dry, changes, foo(force, dry, changes))
