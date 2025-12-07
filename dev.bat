@echo off
REM 개발 모드 실행 스크립트 (Windows)
REM React Dev Server(포트 3000) + Flask API(포트 5050)

echo ========================================
echo 개발 모드 시작
echo ========================================
echo.
echo [1/2] Flask API 서버 시작 중... (포트 5050)
start "Flask API Server" cmd /k "python run.py"

echo.
echo [2/2] React Dev Server 시작 중... (포트 3000)
cd client
start "React Dev Server" cmd /k "npm run dev"

echo.
echo ========================================
echo 개발 환경 실행 완료!
echo ========================================
echo.
echo - React Dev Server: http://localhost:3000
echo - Flask API Server: http://localhost:5050
echo - API 문서: http://localhost:5050/docs
echo.
echo 종료하려면 각 창에서 Ctrl+C를 누르세요
echo ========================================
