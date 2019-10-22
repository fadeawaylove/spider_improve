__all__ = ['d02']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
var.get('console').callprop('log', Js('Hello World!'))


# Add lib to the module scope
d02 = var.to_python()