from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # 환경 변수로 포트 설정 (기본값: 80)
    # 개발 시: PORT=5050 python run.py
    # 프로덕션: sudo python run.py (포트 80)
    port = int(os.getenv('PORT', 5050))

    # 포트 80은 Linux에서 sudo 권한 필요
    if port == 80:
        print("⚠️  포트 80 사용: Linux/Mac에서는 'sudo python run.py' 실행 필요")

    app.run(host='0.0.0.0', port=port, debug=True)
