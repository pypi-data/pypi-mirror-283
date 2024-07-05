# pyappcore
## 개요
- 파이썬 기반의 앱을 구현할 때 사용할 수 있는 프레임워크 패키지 입니다.

## pyappcore 패키지 스펙
- Python 3.12.4를 사용했습니다. (전체설치)
- 외부 라이브러리는 프로젝트 개발시 setuptools, wheel, twine, debugpy 패키지 등을 사용했습니다.
- 그 외는 기본 내장 라이브러리만을 사용 했습니다.
- 패키지 작업 환경이 Windows OS 및 Visual Sutido Code 여서 그 외의 환경에서는 관련 이슈가 있을 수 있습니다.
- 일단 3.9 이상이면 무리없이 동작하리라 생각합니다.
- 사용하려면 일단 .venv 설정을 해주어야 하는데 Visual Studio Code의 경우 Control + Shift + P를 눌러 파있썬 인터프리터 환경 선택을 누르면 됩니다.

## 프로젝트 가상환경 생성 방법
1. VSCode에서 Control + Shift + P 를 눌러 Python: 환경 만들기 실행
2. Venv 선택
3. 인터프리터는 Python 3.12.4 64-bit 선택
4. 설치할 종속성 선택

## 프로젝트 배치파일 목록
- run-venv.bat : 가상환경 설치 (제작중단).
- run-activate.bat : 가상환경 활성화.
- run-deactivate.bat : 가상환경 비활성화.
- run-test.bat : 유닛테스트.
- run-pip.bat : 패키지 최신 업데이트.
- run-clean.bat : 기존 빌드파일 제거.
- run-build.bat : wheel 빌드.
- run-distribution.bat : PyPi 배포.

## 개발방법
1. run-activate 로 가상환경을 활성화 합니다.
2. 기능 개발.
3. run-distribution 으로 패키지를 릴리즈 합니다.

## 설치방법
1. pip install pyappcore
2. 

## 사용방법
1. 매 빌드될 때 마다 __prebuild__.py를 실행합니다.
2. 실제 IDE 와 연결될 메인 함수는 __launcher__.py 입니다.

## 조건


## 실행시 자동으로 생성되는 파일
- __pyappcore_dependencies_in_build__
- __pyappcore_symbols_in_build__
