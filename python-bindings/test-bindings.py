#!/usr/bin/env python

from __future__ import print_function

import pprint
import sys
import clang.cindex

def parm_visitor(cursor):
  if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
    print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname), end='')

def enum_constant_visitor(cursor):
  if cursor.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
    #print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname), end='')
    print('{}'.format(cursor.displayname), end='')

def visitor(cursor):
  if (cursor.location.file != None and
      cursor.location.file.name == sys.argv[1] and
      cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL):
    print('//{} {}'.format(cursor.type.get_result().spelling, cursor.canonical.displayname))

    print('Built-in displayname: {} {}'.format(cursor.type.get_result().get_canonical().spelling, cursor.canonical.displayname))
    #print('Built-in displayname: {} {}'.format(cursor.type.get_result().get_canonical().kind, cursor.canonical.kind))

    print('Generated: {} {}('.format(cursor.type.get_result().get_canonical().spelling, cursor.spelling), end='')

    function_children = list(cursor.get_children())
    number_of_children = len(function_children)
    for index in range(number_of_children):
      if function_children[index].kind == clang.cindex.CursorKind.PARM_DECL:
        parm_visitor(function_children[index])
        if index < number_of_children - 1:
          print(', ', end='')

    print(');')

  elif (cursor.location.file != None and
        cursor.location.file.name == sys.argv[1] and
        cursor.kind == clang.cindex.CursorKind.ENUM_DECL):
    print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname))

    enum_children = list(cursor.get_children())
    number_of_children = len(enum_children)
    for index in range(number_of_children):
      if enum_children[index].kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
        enum_constant_visitor(enum_children[index])
        if index < number_of_children - 1:
          print(', ', end='')

    print('')

  if cursor.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
    print('Direct processing: {}'.format(cursor.displayname))

  children = list(cursor.get_children())
  for child in children:
    visitor(child)


clang.cindex.Config.set_library_file('libclang-5.0.so.1')
index = clang.cindex.Index.create()
# Parse as C++
#tu = index.parse(sys.argv[1], args=['-x', 'c++'])

# Parse as C
tu = index.parse(sys.argv[1], args=['-x', 'c', '-I/usr/include/clang/5.0/include/'])

diagnostics = list(tu.diagnostics)
if len(diagnostics) > 0:
    print('There were parse errors')
    pprint.pprint(diagnostics)
else:
    visitor(tu.cursor)
