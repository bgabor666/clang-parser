#!/usr/bin/env python

from __future__ import print_function

import pprint
import sys
import clang.cindex

def parm_visitor(cursor):
  if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
    #print('>>> Found %s type %s [line=%s, col=%s]' % (
            #cursor.displayname, cursor.type.get_canonical().spelling, cursor.location.line, cursor.location.column))
    print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname), end='')

def visitor(cursor):

  if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
    print('//{} {}'.format(cursor.type.get_result().spelling, cursor.canonical.displayname))
    #print '//{} {}'.format(cursor.type.get_result().spelling, cursor.spelling)

    print('Built-in displayname: {} {}'.format(cursor.type.get_result().get_canonical().spelling, cursor.canonical.displayname))

    print('Generated: {} {}('.format(cursor.type.get_result().get_canonical().spelling, cursor.spelling), end='')

    function_children = list(cursor.get_children())
    number_of_children = len(function_children)
    for index in range(number_of_children):
      if function_children[index].kind == clang.cindex.CursorKind.PARM_DECL:
        parm_visitor(function_children[index])
        if index < number_of_children - 1:
          print(', ', end='')

    print(')')

  children = list(cursor.get_children())
  for child in children:
    visitor(child)

index = clang.cindex.Index.create()
# Parse as C++
tu = index.parse(sys.argv[1], args=['-x', 'c++'])

diagnostics = list(tu.diagnostics)
if len(diagnostics) > 0:
    print('There were parse errors')
    pprint.pprint(diagnostics)
else:
    visitor(tu.cursor)
