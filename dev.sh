#!/bin/bash
# 개발 모드 실행 스크립트 (Linux/Mac/라즈베리파이)
# React Dev Server(포트 3000) + Flask API(포트 5050)

echo "========================================"
echo "개발 모드 시작"
echo "========================================"
echo ""

# Flask API 서버 백그라운드 실행
echo "[1/2] Flask API 서버 시작 중... (포트 5050)"
python3 run.py &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

# React Dev Server 실행
echo ""
echo "[2/2] React Dev Server 시작 중... (포트 3000)"
cd client
npm run dev &
REACT_PID=$!

echo ""
echo "========================================"
echo "개발 환경 실행 완료!"
echo "========================================"
echo ""
echo "- React Dev Server: http://localhost:3000"
echo "- Flask API Server: http://localhost:5050"
echo "- API 문서: http://localhost:5050/docs"
echo ""
echo "종료하려면 Ctrl+C를 누르세요"
echo "========================================"

# Ctrl+C로 종료 시 모든 프로세스 종료
trap "echo '종료 중...'; kill $FLASK_PID $REACT_PID 2>/dev/null; exit" INT TERM

# 대기
wait
