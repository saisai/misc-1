import sys
from xml.etree import ElementTree

XMLindentation = 2 * " "

def indent(elem, level=0):
    "Adds whitespace to the tree, so that it results in a prettyprinted tree."
    i = "\n" + level * XMLindentation
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + XMLindentation
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + XMLindentation
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


tree = ElementTree.ElementTree(None, sys.argv[1])
indent(tree.getroot())
tree.write(sys.stdout)
sys.stdout.write('\n')
