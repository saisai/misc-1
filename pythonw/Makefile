pythonw: pythonw.c
	$(CC) $(LDFLAGS) -DPYTHONFRAMEWORK='"$(PYTHONFRAMEWORK)"' -o $@ $(srcdir)/Tools/pythonw.c -I.. -I$(srcdir)/../Include ../$(PYTHONFRAMEWORK).framework/Versions/$(VERSION)/$(PYTHONFRAMEWORK)
