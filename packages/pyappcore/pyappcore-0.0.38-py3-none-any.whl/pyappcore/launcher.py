#------------------------------------------------------------------------
# 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
import debugpy # type: ignore
import importlib
import os
import sys
from .application import Application
from .str_util import *
from .log_util import *


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
FROZEN : str = "frozen"
MAIN : str = "__main__"
SEMICOLON : str = ";"
SYMBOL_SUBPROCESS : str = "SUBPROCESS"
SYMBOL_LOG : str = "LOG"
SYMBOL_DEBUG : str = "DEBUG"
SYMBOL_NODEBUG : str = "NODEBUG"
DEPENDENCIESINBUILDMODULENAME : str = "__pyappcore_dependencies_in_build__"
SYMBOLSINBUILDMODULENAME : str = "__pyappcore_symbols_in_build__"


#------------------------------------------------------------------------
# 빌드.
#------------------------------------------------------------------------
def IsBuild() -> bool:
	# 실행 환경 체크.
	try:
		return builtins.getattr(sys, FROZEN, False)
	except Exception as exception:
		return False


#------------------------------------------------------------------------
# 시작.
# - Symbols는 바이너리상태에서는 
#------------------------------------------------------------------------
def Launching(moduleName : str, functionName : str) -> int:
	builtins.print("pyappcore.launcher.Launch()")

	# 빌드인 경우 경로.
	isBuild : bool = IsBuild()
	if isBuild:
		# 실행파일에서 생성되는 임시 루트 경로.
		# 리소스를 위한 캐시폴더로 실제 실행파일의 위치가 아님.
		cachePath : str = sys._MEIPASS
		rootPath : str = os.path.dirname(sys.executable)
		sourceDirPath : str = os.path.join(cachePath, "src")
		resPath : str = os.path.join(cachePath, "res")
	# 빌드가 아닌 경우 경로.
	else:
		# 현재 프로젝트를 기준으로 한 경로.
		sourceDirPath : str = os.path.dirname(os.path.abspath(sys.modules[MAIN].__file__))
		rootPath : str = os.path.dirname(sourceDirPath)
		resPath : str = os.path.join(rootPath, "res")

	# 프로젝트 값 설정.
	Application._Application__SetBuild(isBuild)
	Application._Application__SetRootPath(rootPath)
	Application._Application__SetResPath(resPath)
	Application._Application__SetSymbols("")

	# 프로젝트 값 출력.
	builtins.print(f"Application.IsBuild(): {Application.IsBuild()}")  
	builtins.print(f"Application.GetRootPath(): {Application.GetRootPath()}")
	builtins.print(f"Application.GetResPath(): {Application.GetResPath()}")

	# 시도.
	try:
		# 실행파일 빌드.
		if Application.IsBuild():
			print("__build__")

			# 실행된 파일 이름 설정.
			executeFileName = sys.argv[0]
			Application._Application__SetExecuteFileName(executeFileName)
			sys.argv = sys.argv[1:]

			# 심볼 설정.
			if SYMBOLSINBUILDMODULENAME in sys.modules:
				builtins.print("__pycore_symbols_in_build__")
				module = sys.modules[SYMBOLSINBUILDMODULENAME]
				symbols = module.SYMBOLS
				symbolsString : str = SEMICOLON.join(symbols)
				Application._Application__SetSymbols(symbolsString)

			# 디버그 모드 설정.
			# 빌드 시 DEBUG 심볼이 있던 없던 무조건 False.
			Application._Application__SetDebug(False)
			builtins.print(f"Application.IsDebug() : {Application.IsDebug()}")

		# 빌드 외.
		else:
			print("__nobuild__")

			# PYCHARM.
			# MANUAL.
			# 둘은 일단 상황 제외.

			# VSCODE.
			# run.bat을 통한 실행일 경우 최대 9개의 미사용 인수가 넘어오므로.
			# 빈 문자열들은 안쓰는 값으로 간주하고 제거.
			sys.argv = sys.argv[3:]
			sys.argv = [argument for argument in sys.argv if argument]

			# 실행된 파이썬 스크립트 파일 설정.
			executeFileName = sys.argv[0]
			Application._Application__SetExecuteFileName(executeFileName)
			sys.argv = sys.argv[1:]

			# 심볼 설정.
			symbolsString = sys.argv[0]
			Application._Application__SetSymbols(symbolsString)
			sys.argv = sys.argv[1:]

			# 디버그 모드 설정.
			useDebug : bool = Application.HasSymbol(SYMBOL_DEBUG)
			Application._Application__SetDebug(useDebug)
			builtins.print(f"Application.IsDebug() : {Application.IsDebug()}")

			# 디버그 모드 일 경우 원격 디버거 실행.
			# 콘솔에 출력되는 해당 문자열을 감지해서 디버그 대기와 시작을 판단하므로 수정금지.
			if Application.IsDebug():
				builtins.print("pyappcore.launcher.debugpy.start()")
				remotePort : int = 4885 # vscodeSettings["launcher"]["debug"]["remotePort"]
				debugpy.listen(("localhost", remotePort))
				builtins.print("pyappcore.launcher.debugpy.wait()")
				debugpy.wait_for_client()
				builtins.print("pyappcore.launcher.debugpy.started()")

		# 공통.
		# 인자 재조립 처리.
		# VSCODE 상황일때의 인자 목록은 문자열 리스트가 아닌 콤마로 합쳐진 형태로 넘어올 수 있음.
		# 어찌 되었건 쉼표 또한 구분자로 인정하고 공통 처리.
		if not Application.IsBuild() and sys.argv:
			sys.argv = CreateStringListFromSeperatedStringLists(sys.argv)	

		# 인자 출력.
		if sys.argv:
			builtins.print("sys.argv")
			index = 0
			for arg in sys.argv:
				builtins.print(f" - [{index}] {arg}")
				index += 1

		# 로그 설정.
		# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
		useLog : bool = Application.HasSymbol(SYMBOL_LOG)
		if useLog:
			builtins.print("__log__")
			InitializeLOGSystem()

	# 예외.
	except Exception as exception:
		builtins.print(exception)
		return 1
		
	# 시작.
	try:
		builtins.print("__running__")
		module = importlib.import_module(moduleName)
		function = builtins.getattr(module, functionName)
		exitCode : int = function(sys.argv)
		return exitCode
	# 예외.
	except Exception as exception:
		useLog : bool = Application.HasSymbol(SYMBOL_LOG)
		if useLog:
			Application.LogException(exception)
		else:
			builtins.print(exception)
		return 1


# #------------------------------------------------------------------------
# # 파일 진입점.
# #------------------------------------------------------------------------
# if __name__ == "__main__":
# 	exitCode = Launching()
# 	sys.exit(exitCode)