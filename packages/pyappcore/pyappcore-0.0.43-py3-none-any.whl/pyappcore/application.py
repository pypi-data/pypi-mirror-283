#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
import json
from .json_util import *
import logging
from logging import Logger
import subprocess
import traceback


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
EMPTY : str = ""
NONE : str = "NONE"
COMMA : str = ","
SLASH : str = "/"
BACKSLASH : str = "\\"
SEMICOLON : str = ";"
COLON : str = ":"
SPACE : str = " "
DEBUG : str = "DEBUG"
NODEBUG : str = "NODEBUG"

PYAPPCORE_SYMBOL_EXPRESS : str = "EXPRESS" # "PYAPPCORE_SYMBOL_EXPRESS"
PYAPPCORE_SYMBOL_SUBPROCESS : str = "SUBPROCESS" # "PYAPPCORE_SYMBOL_SUBPROCESS"
PYAPPCORE_SYMBOL_LOG : str = "LOG" # "PYAPPCORE_SYMBOL_LOG"
PYAPPCORE_SYMBOL_DEBUG : str = "DEBUG" # "PYAPPCORE_SYMBOL_DEBUG"
PYAPPCORE_SYMBOL_NODEBUG : str = "NODEBUG" # "PYAPPCORE_SYMBOL_NODEBUG"

CONFIGURATION_FILENAME : str = "configuration.json"
PYAPPCORE_LOG_LOGGERNAME : str = "pyappcore"
LOG_CRITICAL : int  = 50
LOG_ERROR : int = 40
LOG_EXCEPTION : int  = 40
LOG_WARNING : int  = 30
LOG_INFO : int = 20
LOG_DEBUG : int  = 10
LOG_NOTSET : int = 0


#------------------------------------------------------------------------
# 애플리케이션.
#------------------------------------------------------------------------
class Application:
	__ExecuteFileName : str = str()
	__IsBuild : bool = False
	__IsDebug : bool = False
	__RootPath : str = str()
	__ResPath : str = str()
	__Symbols : set[str] = set()

	#------------------------------------------------------------------------
	# 실제 로그 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def __Log(message : str, level : int) -> None:
		if not Application.HasSymbol(PYAPPCORE_SYMBOL_LOG):
			return
		
		logger = Application.GetLogger()
		if level == LOG_NOTSET: # logging.NOTSET:
			return
		elif level == LOG_DEBUG: # logging.DEBUG:
			logger.debug(message)
		elif level == LOG_INFO: # logging.INFO:
			logger.info(message)
		elif level == LOG_WARNING: # logging.WARN or logging.WARNING:
			logger.warning(message)
		elif level == LOG_ERROR: # logging.ERROR:
			logger.error(message)
		elif level == LOG_CRITICAL: # logging.FATAL or logging.CRITICAL:
			logger.critical(message)

	#------------------------------------------------------------------------
	# 로그 디버그 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogDebug(message : str) -> None:
		Application._Application__Log(message, LOG_DEBUG)

	#------------------------------------------------------------------------
	# 로그 인포 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def Log(message : str) -> None:
		Application._Application__Log(message, LOG_INFO)

	#------------------------------------------------------------------------
	# 로그 인포 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogInfo(message : str) -> None:
		Application._Application__Log(message, LOG_INFO)

	#------------------------------------------------------------------------
	# 로그 워닝 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogWarning(message : str) -> None:
		Application._Application__Log(message, LOG_WARNING)

	#------------------------------------------------------------------------
	# 로그 에러 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogError(message : str) -> None:
		Application._Application__Log(message, LOG_ERROR)

	#------------------------------------------------------------------------
	# 로그 익셉션 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogException(exception : Exception, useTraceback : bool = False) -> None:
		Application._Application__Log(exception, LOG_EXCEPTION)
		if useTraceback:
			traceback.print_exc()
	
	#------------------------------------------------------------------------
	# 로그 크리티컬 출력.
	#------------------------------------------------------------------------
	@staticmethod
	def LogCritical(message : str) -> None:
		Application._Application__Log(message, LOG_CRITICAL)
	
	# ----------------------------------------------------------------------------------
	# 메인 프로세스에서 서브 프로세스 실행.
	# - 예를 들어 블렌더 : {pythonInterpreterPath} "--background" "--python" launcher.py {symbols} {argument1} {argument2} ...
	# - 블렌더 기준의 options : "--background" "--python" ...
	# - 블렌더 기준의 arguments : {argument1} {argument2} ...
	# ----------------------------------------------------------------------------------
	@staticmethod
	def RunSubprocess(pythonInterpreterPath : str, options : str, symbols : str, arguments : list[str]) -> subprocess.CompletedProcess:
		command = list()
		command.append(pythonInterpreterPath)
		
		newOptions = set()
		newOptions.add(options.split(SEMICOLON))
		command.append(SEMICOLON.join(newSymbols))

		command.append(Application.GetRootPathWithRelativePath("/launcher/launcher.py"))

		newSymbols = set()
		newSymbols.add(PYAPPCORE_SYMBOL_SUBPROCESS)
		newSymbols.update(symbols.split(SEMICOLON))
		command.append(SEMICOLON.join(newSymbols))
		
		if arguments:
			for argument in arguments:
				command.append(argument)
		return subprocess.run(command, check = True)

 	#------------------------------------------------------------------------
	# 실행 된 파일 이름.
	#------------------------------------------------------------------------
	@staticmethod
	def __SetExecuteFileName(executeFileName : str) -> None:
		Application._Application__ExecuteFileName = executeFileName

 	#------------------------------------------------------------------------
	# 빌드 여부 설정.
	#------------------------------------------------------------------------
	@staticmethod
	def __SetBuild(isBuild : bool) -> None:
		Application._Application__IsBuild = isBuild

	#------------------------------------------------------------------------
	# 디버그 모드 여부 설정.
	#------------------------------------------------------------------------
	@staticmethod
	def __SetDebug(isDebug : bool) -> None:
		Application._Application__IsDebug = isDebug

	#------------------------------------------------------------------------
	# 루트 경로 설정.
	#------------------------------------------------------------------------
	@staticmethod
	def __SetRootPath(rootPath : str) -> None:
		Application._Application__RootPath = rootPath.replace(BACKSLASH, SLASH)

	#------------------------------------------------------------------------
	# 리소스 경로 설정.
	#------------------------------------------------------------------------
	@staticmethod
	def __SetResPath(resPath : str) -> None:
		Application._Application__ResPath = resPath.replace(BACKSLASH, SLASH)

	#------------------------------------------------------------------------
	# 기존 심볼을 모두 지우고 새로운 심볼 목록 설정 (구분자 : ;).
	#------------------------------------------------------------------------
	@staticmethod
	def __SetSymbols(symbolsString : str) -> None:	
		# 입력받은 텍스트 정리.
		symbolsString = symbolsString.upper()

		# 중복을 허용하지 않는 선에서 처리.
		symbols : list[str] = symbolsString.split(SEMICOLON) if SEMICOLON in symbolsString else [symbolsString]

		# 객체 생성 및 심볼 설정.
		Application._Application__Symbols = set()
		if symbols: Application._Application__Symbols.update(symbols)

		# NONE, EMPTY, SPACE는 없는 것과 마찬가지이므로 목록에서 제거.
		Application._Application__Symbols.discard(NONE)
		Application._Application__Symbols.discard(EMPTY)
		Application._Application__Symbols.discard(SPACE)

	#------------------------------------------------------------------------
	# 빌드된 상태인지 여부.
	#------------------------------------------------------------------------
	@staticmethod
	def IsBuild() -> bool:
		return Application._Application__IsBuild

	#------------------------------------------------------------------------
	# 디버깅 상태인지 여부.
	#------------------------------------------------------------------------
	@staticmethod
	def IsDebug() -> bool:
		return Application._Application__IsDebug

	#------------------------------------------------------------------------
	# 실행된 파일 이름 반환.
	#------------------------------------------------------------------------
	def GetExecuteFileName() -> str:
		return Application._Application__ExecuteFileName

	#------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로 / 실행파일이 존재하는 경로.
	#------------------------------------------------------------------------
	@staticmethod
	def GetRootPath() -> str:
		return Application._Application__RootPath

	#------------------------------------------------------------------------
	# 리소스 경로 / 실행 파일 실행시 임시 리소스 폴더 경로.
	#------------------------------------------------------------------------
	@staticmethod
	def GetResPath() -> str:
		return Application._Application__ResPath

	#------------------------------------------------------------------------
	# 현재 앱에 해당 심볼이 등록 되어있는지 여부.
	#------------------------------------------------------------------------
	@staticmethod
	def HasSymbol(symbolString : str) -> bool:
		symbols = Application._Application__Symbols
		if not symbols:
			return False
		if not symbolString in symbols:
			return False
		return True

	#------------------------------------------------------------------------
	# 현재 앱에 입력되어있는 심볼 목록.
	#------------------------------------------------------------------------
	@staticmethod
	def GetSymbols() -> list[str]:
		return list(Application._Application__Symbols)

	#------------------------------------------------------------------------
	# 애플리케이션이 존재하는 경로에 상대경로를 입력하여 절대경로를 획득.
	#------------------------------------------------------------------------
	@staticmethod
	def GetRootPathWithRelativePath(relativePath : str) -> str:
		rootPath = Application.GetRootPath()
		if not relativePath:
			return rootPath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{rootPath}/{relativePath}"
		return absolutePath

	#------------------------------------------------------------------------
	# 리소스가 존재하는 경로에 상대경로를 입력하여 절대경로를 획득.
	#------------------------------------------------------------------------
	@staticmethod
	def GetResPathWithRelativePath(relativePath : str) -> str:
		resPath = Application.GetResPath()
		if not relativePath:
			return resPath
		relativePath = relativePath.replace(BACKSLASH, SLASH)
		absolutePath = f"{resPath}/{relativePath}"
		return absolutePath

	#------------------------------------------------------------------------
	# 로거 반환.
	#------------------------------------------------------------------------
	@staticmethod
	def GetLogger() -> Logger:
		return logging.getLogger(PYAPPCORE_LOG_LOGGERNAME)

	#------------------------------------------------------------------------
	# 설정값 반환 : "{workspace}/res/configuration.json" 필요, 만약 파일이 없으면 None 반환.
	#------------------------------------------------------------------------
	@staticmethod
	def GetConfiguration(propertyName : str = EMPTY) -> Union[dict, None]:
		try:
			configFilePath = Application.GetResPathWithRelativePath(CONFIGURATION_FILENAME)
			with open(configFilePath, "r") as file:
				jsonText = RemoveAllCommentsInString(file.read())
				jsonData = json.loads(jsonText)
				if propertyName:
					return jsonData[propertyName]
				else:
					return jsonData     
		except Exception as exception:
			Application.LogException(exception)
			return None