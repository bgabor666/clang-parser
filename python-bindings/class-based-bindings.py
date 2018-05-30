#!/usr/bin/env python

from __future__ import print_function

import pprint
import sys
import clang.cindex


class Decl:
    def __init__(self, cursor):
        self._cursor = cursor

    @property
    def name(self):
        return self._cursor.spelling


class CFunctionDecl(Decl):
    def __init__(self, cursor):
        Decl.__init__(self, cursor)
        self._params = []

        function_children = list(cursor.get_children())
        for child in function_children:
            if child.kind == clang.cindex.CursorKind.PARM_DECL:
                self._params.append(CFunctionParameterDecl(child))

    @property
    def canonical_return_type(self):
        return self._cursor.type.get_result().get_canonical().spelling

    @property
    def params(self):
        return self._params

class CFunctionParameterDecl(Decl):
    def __init__(self, cursor):
        Decl.__init__(self, cursor)

    @property
    def canonical_type(self):
        return self._cursor.type.get_canonical().spelling


funcs = []

def parm_visitor(cursor):
  if cursor.kind == clang.cindex.CursorKind.PARM_DECL:
    #print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname), end='')
    print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.spelling), end='')

def enum_constant_visitor(cursor):
  if cursor.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
    #print('{} {}'.format(cursor.type.get_canonical().spelling, cursor.displayname), end='')
    print('{}'.format(cursor.displayname), end='')

def visitor(cursor):
  if (cursor.location.file != None and
      cursor.location.file.name == sys.argv[1] and
      cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL):
    print('//{} {}'.format(cursor.type.get_result().spelling, cursor.canonical.displayname))

    funcs.append(CFunctionDecl(cursor))

    for arg in cursor.get_arguments():
      print('Function argument: {}', arg.kind)

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

for func in funcs:
    print('{} {}'.format(func.canonical_return_type, func.name))
    for param in func.params:
        print('>>> {} {}'.format(param.canonical_type, param.name))
