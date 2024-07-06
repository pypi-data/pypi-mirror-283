#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
import builtins
import os
import sys
import traceback


#------------------------------------------------------------------------
# 익셉션.
#------------------------------------------------------------------------
def RaiseException(exception : Exception):
	traceback.print_exc()
	tb = exception.__traceback__
	while tb:
		filename = tb.tb_frame.f_code.co_filename
		lineno = tb.tb_lineno
		funcname = tb.tb_frame.f_code.co_name
		result = traceback.format_exc()
		result = result.strip()
		line = result.splitlines()[-1]
		builtins.print(f"Exception in {filename}, line {lineno}, in {funcname}")
		builtins.print(f"\t{line}")
		tb = tb.tb_next
	sys.exit(1)