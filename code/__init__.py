# Re-export stdlib 'code' attributes to prevent shadowing when
# project root is in sys.path (e.g. werkzeug.debug.console needs
# code.InteractiveInterpreter).
import importlib.util
import os
import sys
import sysconfig

_stdlib_dir = sysconfig.get_path("stdlib")
_stdlib_code_path = os.path.join(_stdlib_dir, "code.py")

# Directly load the stdlib code.py to avoid recursive self-import.
spec = importlib.util.spec_from_file_location("_stdlib_code", _stdlib_code_path)
_stdlib_code = importlib.util.module_from_spec(spec)
sys.modules["_stdlib_code"] = _stdlib_code
spec.loader.exec_module(_stdlib_code)

for _attr in dir(_stdlib_code):
    if not _attr.startswith("_"):
        globals()[_attr] = getattr(_stdlib_code, _attr)

del importlib, os, sys, sysconfig, _stdlib_dir, _stdlib_code_path, spec, _stdlib_code, _attr
