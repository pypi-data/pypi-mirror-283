#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
import warnings
import importlib
import inspect


#------------------------------------------------------------------------
# 워닝 존재 여부.
#------------------------------------------------------------------------
def CheckWarningForMmoduleName(moduleName : str) -> bool:
    with warnings.catch_warnings(record = True) as caughtWarnings:
        warnings.simplefilter("always")
        try:
            importlib.import_module(moduleName)
        except ImportError:
            return False
        if caughtWarnings:
            for caughtWarning in caughtWarnings:
                continue
            return True
        return False
    

#------------------------------------------------------------------------
# 패키지 이름 반환.
#------------------------------------------------------------------------
def GetParentPackage(moduleName: str) -> str:
    try:
        module = importlib.import_module(moduleName)
        moduleFile = inspect.getfile(module)
        moduleSpec = importlib.util.find_spec(moduleName)
        
        if moduleSpec and moduleSpec.submodule_search_locations:
            packageName = moduleSpec.name
            return packageName
        else:
            parts = moduleName.split(".")
            if len(parts) > 1:
                return ".".join(parts[:-1])
    except Exception as e:
        print(f"Error finding parent package for '{moduleName}': {e}")
    return str()