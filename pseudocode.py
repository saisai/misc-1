raise ImportError("module is just pseudocode")

import sys
def __import__(name, globals, locals, fromlist, level):
    """Pseudocode to explain how importing works.

    Caveats:
        + Classic relative import semantics are not covered.
        + Assume all code runs with the import lock held.
        + Some structure (e.g., using importers for built-in and frozen
          modules) is purely conceptual and not used in the C
          implementation of import.

    """
    path = globals.get('__path__')
    # If a relative import, figure out absolute name of requested module.
    if level != 0:
        # Adjust relative import based on whether caller is a package and
        # the specified level in the call.
        # Also make sure import does not go beyond top-level.
        name = resolve_name(name, globals['__name__'], path, level)
    # Import each parent in the name, starting at the top.
    # Assume each_parent iterates through each parent of the module request,
    # starting at the top-level parent.
    # Since loaders are required to set the module in sys.modules, a successful
    # import should be followed by 'continue' to let the next module be
    # imported.
    for name in each_parent(name):
        # If the module is already cached in sys.modules then move along.
        if name in sys.modules:
            continue
        # Try to find a __path__ attribute on the (possibly non-existent)
        # parent.
        immediate_parent = name.rsplit('.', 1)[0]
        try:
            path = sys.modules[immediate_parent].__path__
        except (KeyError, AttributeError):
            path = None
        # Search sys.meta_path.
        for meta_importer in sys.meta_path:
            loader = meta_importer.find_module(name, path)
            if loader:
                loader.load_module(name)
                continue
        # Check built-in and frozen modules.
        else:
            for module_finder in (builtin_importer, frozen_importer):
                loader = module_finder(name, path)
                if loader:
                    loader.load_module(name)
                    continue
        # With sys.meta_path, built-ins, and frozen modules checked, now look
        # at sys.path or parent.__path__.
        search_path = path if path else sys.path
        for path_entry in search_path
            # Look for a cached importer.
            if path_entry in sys.path_importer_cache:
                importer = sys.path_importer_cache[path_entry]
                # Found an importer.
                if importer:
                    loader = importer.find_module(name)
                    # If the import can handle the module, load it.  Otherwise
                    # fall through to the default import.
                    if loader:
                        loader.load_module(name)
                        continue
            # A pre-existing importer was not found; try to make one.
            else:
                for importer_factory in sys.path_hooks:
                    try:
                        # If an importer is found, cache it and try to use it.
                        # If it can't be used, then fall through to the default
                        # import.
                        importer = importer_factory(path_entry)
                        sys.path_importer_cache[path_entry] = importer
                        loader = importer.find_module(name)
                        if loader:
                            loader.load_module(name)
                    except ImportError:
                        continue
                else:
                    # No importer could be created, so set to None in
                    # sys.path_import_cache to skip trying to make one in the
                    # future, then fall through to the default import.
                    sys.path_importer_cache[path_entry] = None
            # As no importer was found for the sys.path entry, use the default
            # importer for extension modules, Python bytecode, and Python
            # source modules.
            loader = find_extension_module(name, path_entry)
            if loader:
                loader.load_module(name)
                continue
            loader = find_py_pyc_module(name, path_entry)
            if loader:
                loader.load_module(name)
                continue
        # All available places to look for a module have been exhausted; raise
        # an ImportError.
        raise ImportError
    # With the module now imported and store in sys.modules, figure out exactly
    # what module to return based on fromlist and how the module name was
    # specified.
    if not fromlist:
        # The fromlist is empty, so return the top-most parent module.
        # Whether the import was relative or absolute must be considered.
        if level:
            return top_relative_name(name, level)
        else:
            return sys.modules[name.split('.', 1)[0]]
    else:
        # As fromlist is not empty, return the module specified by the import.
        # Must also handle possible imports of modules if the module imported
        # was a package and thus names in the fromlist are modules within the
        # package and not object within a module.
        module = sys.modules[name]
        # If not a module, then can just return the module as the names
        # specified in fromlist are supposed to be attributes on the module.
        if not hasattr(module, '__path__'):
            return module
        # The imported module was a package, which means everything in the
        # fromlist are supposed to be modules within the package.  That means
        # that an *attempt* must be made to try to import every name in
        # fromlist.
        if '*' in fromlist and hasattr(module, '__all__'):
            fromlist = list(fromlist).extend(module.__all__)
        for item in fromlist:
            if item == '*':
                continue
            if not hasattr(module, item):
                try:
                    __import__('.'.join([name, item]), module.__dict__, level=0)
                except ImportError:
                    pass
        return module


from imp import get_suffixes, C_EXTENSION
def find_extension_module(name, path_entry):
    """Try to locate a C extension module for the requested module."""
    # Get the immediate name of the module being searched for as the extension
    # module's file name will be based on it.
    immediate_name = name.rsplit('.', 1)[-1]
    # Check every possible C extension suffix with the immediate module name
    # (typically two; '.so' and 'module.so').
    for suffix in (suffix[0] for suffix in get_suffixes()
            if suffix[2] == C_EXTENSION):
        file_path = os.path.join(path_entry, immediate_name + suffix)
        if os.path.isfile(file_path):  # I/O
            return extension_loader(name, file_path)
    else:
        return None


from imp import PY_SOURCE, PY_COMPILED
def find_py_pyc_module(name, path_entry):
    """Try to locate a Python source code or bytecode module for the requested
    module."""
    # Get the immediate name of the module being imported as the Python file's
    # name will be based on it.
    immediate_name = name.rsplit('.', 1)[-1]
    # Check every valid Python code suffix for possible files (typically two;
    # '.py' and either '.pyc' or '.pyo').
    for suffix in (suffix[0] for suffix in get_suffixes()
            if suffix[2] in (PY_SOURCE, PY_COMPILED)):
        # See if the module is actually a package.
        pkg_init_path = os.path.join(path_entry, immediate_name,
                                        '__init__' + suffix)
        if os.path.isfile(pkg_init_path):  # I/O
            return py_loader(name, pkg_init_path, is_pkg=True)
        # If module is not a package, see if it is a file by itself.
        file_path = os.path.join(path_entry, immediate_name + suffix)
        if os.path.isfile(file_path):  # I/O
            return py_loader(name, file_path, is_pkg=False)


def py_loader(name, file_path, is_pkg):
    pass
