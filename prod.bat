@echo off
REM 프로덕션 모드 실행 스크립트 (Windows)
REM 프론트엔드 빌드 후 Flask에서 통합 서빙

echo ========================================
echo 프로덕션 모드 빌드 및 실행
echo ========================================
echo.

echo [1/2] React 앱 빌드 중...
cd client
call npm run build
if %ERRORLEVEL% neq 0 (
    echo.
    echo 빌드 실패! npm install을 먼저 실행하세요.
    pause
    exit /b 1
)
cd ..

echo.
echo [2/2] Flask 서버 시작 중... (포트 5050)
echo.
echo ========================================
echo 프로덕션 모드 실행 완료!
echo ========================================
echo.
echo - 웹 접속: http://localhost:5050
echo - 외부 접속: http://<YOUR_IP>:5050
echo - API 문서: http://localhost:5050/docs
echo.
echo Caddy 리버스 프록시 사용 시:
echo   caddy run
echo   접속: https://localhost
echo ========================================
echo.

python run.py
