# ----------------------------------------------------------------------------------
# 참조 모듈 목록.
# ----------------------------------------------------------------------------------
from __future__ import annotations
import builtins
import os
import shutil
import sys


# #------------------------------------------------------------------------
# # 현재 위치를 기준으로 폴더 생성.
# #------------------------------------------------------------------------
# DIRECTORIES = set()
# DIRECTORIES.add(".vscode")
# DIRECTORIES.add("build")
# DIRECTORIES.add("hints")
# DIRECTORIES.add("libs")
# DIRECTORIES.add("res")
# DIRECTORIES.add("src")
# DIRECTORIES.add("tests")
# DIRECTORIES.add("tools")
# DIRECTORIES.add("workspace")


#------------------------------------------------------------------------
# 현재 위치를 기준으로 폴더 생성.
#------------------------------------------------------------------------
def CreateDirectory(path : str) -> bool:
	if not os.path.isdir(path): 
		os.makedirs(path)
		return True
	else:
		return False


#------------------------------------------------------------------------
# 파일 생성.
#------------------------------------------------------------------------
def CreateFile(path : str, fileName : str, content : str = "") -> bool:
	gitkeepFilePath = f"{path}/{fileName}"
	if not os.path.isfile(gitkeepFilePath):
		with builtins.open(gitkeepFilePath, "w", encoding = "utf-8") as file:
			file.write(content)
		return True
	return False


# #------------------------------------------------------------------------
# # 현재 위치를 기준으로 루트 폴더 생성.
# #------------------------------------------------------------------------
# def CreateRootDirectory(projectName : str) -> str:
# 	basePath = os.getcwd()
# 	basePathName : str = os.path.dirname(basePath)

# 	if basePathName == projectName:
# 		rootPath = f"{basePath}"	
# 		rootPath = rootPath.replace("\\", "/")
# 	else:
# 		rootPath = f"{basePath}/{projectName}"
# 		rootPath = rootPath.replace("\\", "/")

# 	if not os.path.isdir(rootPath): 
# 		os.makedirs(rootPath)
# 		return rootPath
# 	else:
# 		return None


# #------------------------------------------------------------------------
# # 파일 진입점.
# #------------------------------------------------------------------------
# if __name__ == "__main__":

# 	# 인자가 있을 때.
# 	# [0] 실행 스크립트 경로
# 	# [1] 프로젝트 이름
# 	if len(sys.argv) >= 2:
# 		executeFilePath = sys.argv[0]
# 		sys.argv = sys.argv[1:]
# 		projectName = sys.argv[0]
# 		sys.argv = sys.argv[1:]
# 		builtins.print(f"projectName: {projectName}")
# 	else:
# 		builtins.print("not found projectName arguments.")
# 		sys.exit(1)

# 	# 현재 위치를 기준으로 프로젝트 루트 폴더가 없으면 생성.
# 	rootPath = CreateRootDirectory(projectName)
# 	if not rootPath:
# 		builtins.print(f"is exists path: '{rootPath}'")
# 		sys.exit(1)

# 	# 폴더 및 파일 생성.
# 	for directory in DIRECTORIES:
# 		path : str = f"{rootPath}/{directory}"
# 		if CreateDirectory(path):
# 			CreateFile(path, ".gitkeep")

# 	# 루트폴더 기준 파일 생성.
# 	CreateFile(path, ".env")
# 	CloneFile(f"{path}/requirements.txt", "{path}/requirements.txt")
# 	CreateFile(path, "run-exe")
# 	CreateFile(path, "run-tests")

# 	# Visual Studio Code 폴더에 파일 추가.
# 	vscodePath = f"{rootPath}/.vscode"
# 	CreateFile(path, "launch.json")
# 	CreateFile(path, "settings.json")
# 	CreateFile(path, "tasks.json")
	
# 	# 리소스 폴더에 파일 추가.
# 	resPath = f"{rootPath}/res"
# 	CreateFile(path, "configuration.json")
# 	CreateFile(path, "main.py")

# 	# 소스 폴더에 파일 추가.
# 	srcPath = f"{rootPath}/src"
# 	CreateFile(srcPath, "__init__.py")
# 	CloneFile("", srcPath)
# 	CreateFile(srcPath, "main.py")

# 	# 테스트 폴더에 파일 추가.
# 	testsPath = f"{rootPath}/tests"
# 	CreateFile(testsPath, "__init__.py")
# 	CreateFile(testsPath, "__main__.py")	
# 	CreateFile(testsPath, "test_main.py")

#------------------------------------------------------------------------
# 시작점.
#------------------------------------------------------------------------
def main():
	builtins.print("makeproject")
	projectName = sys.argv[1]
	makeFilePath = os.path.abspath(__file__)
	toolsPath = os.path.dirname(makeFilePath).replace("\\", "/")
	rootPath = os.path.dirname(toolsPath).replace("\\", "/")
	sourcePath = os.path.join(rootPath, "res", "PythonProjectTemplate")

	workPath = os.getcwd()
	if workPath.endswith(projectName):
		destinationPath = workPath
	else:
		destinationPath = f"{workPath}/{projectName}"

	if not os.path.isdir(destinationPath):
		CreateDirectory(destinationPath)

	shutil.copytree(sourcePath, destinationPath)


#------------------------------------------------------------------------
# 파일 진입점.
#------------------------------------------------------------------------
if __name__ == "__main__":
	main()