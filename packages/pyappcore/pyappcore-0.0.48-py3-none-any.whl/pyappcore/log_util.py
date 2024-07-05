#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
from logging import Logger, Handler, StreamHandler, FileHandler, Formatter, LogRecord, NOTSET, DEBUG, INFO, WARN, WARNING, ERROR, CRITICAL, FATAL
import os
from .application import Application, PYAPPCORE_SYMBOL_EXPRESS
from .ansicode import *
from .str_util import GetTimestampString


#------------------------------------------------------------------------
# 화면 출력 핸들러.
#------------------------------------------------------------------------
class PrintHandler(Handler):
	def emit(self, record : LogRecord):
		message = self.format(record)
		if record.levelno == FATAL or record.levelno == CRITICAL: Print(f"<bg_red><white><b>{message}</b></white></bg_red>")
		elif record.levelno == ERROR: Print(f"<red>{message}</red>")
		elif record.levelno == WARN or record.levelno == WARNING: Print(f"<yellow>{message}</yellow>")
		elif record.levelno == INFO: Print(f"{message}")
		elif record.levelno == DEBUG: Print(f"<magenta>{message}</magenta>")


#------------------------------------------------------------------------
# 화면 출력.
#------------------------------------------------------------------------
def InitializeLOGSystem():
	timestamp = GetTimestampString("", "", "", False)
	useLogFile : bool = False
	logLevel : int = NOTSET
	logFilePath : str = str()

	# EXE 파일 실행.
	if Application.IsBuild():
		useLogFile = False
		logLevel = WARNING
	# VSCode에서 디버깅 실행.
	elif Application.IsDebug():
		useLogFile = True
		logLevel = DEBUG
		logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-debug-{timestamp}.log")
	# Blender.exe로 소스코드 실행.
	elif Application.HasSymbol(PYAPPCORE_SYMBOL_EXPRESS):
		useLogFile = True
		logLevel = INFO
		logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-express-{timestamp}.log")
	# VSCode에서 디버깅 없이 실행.
	else:
		useLogFile = True
		logLevel = INFO
		logFilePath = Application.GetRootPathWithRelativePath(f"logs/pyappcore-nodebug-{timestamp}.log")

	# 설정.
	applicationLogger : Logger = Application.GetLogger()
	applicationLogger.setLevel(logLevel)
	# formatter : Formatter = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
	formatter : Formatter = Formatter("[%(asctime)s][%(levelname)s] %(message)s")
	printHandler : PrintHandler = PrintHandler()
	printHandler.setLevel(logLevel)
	printHandler.setFormatter(formatter)
	applicationLogger.addHandler(printHandler)

	# 로그파일 설정.
	if useLogFile:
		logDirPath = Application.GetRootPathWithRelativePath("logs")
		if not os.path.exists(logDirPath):
			os.makedirs(logDirPath)
		fileHandler : StreamHandler = FileHandler(logFilePath)
		fileHandler.setLevel(logLevel)
		fileHandler.setFormatter(formatter)
		applicationLogger.addHandler(fileHandler)