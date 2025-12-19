from flask import Flask, redirect, jsonify, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
import os

# Swagger 설정
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "static_url_path": "/flasgger_static",
}

def create_app():
    # 정적 파일 경로 설정 (빌드된 React 앱)
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'dist')

    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    # CORS 허용
    CORS(app)

    # Swagger 적용
    Swagger(app, config=swagger_config, template_file=None)

    # 백그라운드 스케줄러 시작
    from app.scheduler import start_scheduler
    start_scheduler()

    # 조이스틱 리스너 시작
    from app.services.joystick_service import start_joystick_listener
    start_joystick_listener()

    # -------- Swagger 문서 --------
    @app.route("/docs")
    def docs():
        return redirect("/apidocs/")

    # -------- 정적 파일 서빙 (프로덕션 모드) --------
    @app.route("/")
    def serve_react_app():
        """
        프로덕션 모드: 빌드된 React 앱의 index.html 제공
        개발 모드: React Dev Server(포트 3000)를 별도로 실행하세요
        """
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            # 빌드 파일이 없는 경우 (개발 모드)
            return jsonify({
                "message": "API 서버가 정상 동작 중입니다.",
                "mode": "development",
                "frontend": "React Dev Server를 별도로 실행하세요 (포트 3000)",
                "build": "프로덕션 빌드: cd client && npm run build"
            })

    @app.route("/<path:path>")
    def serve_static_files(path):
        """
        SPA 라우팅 지원: 모든 경로를 index.html로 리다이렉트
        단, /api, /docs, /apidocs 등은 제외
        """
        if path.startswith(('api/', 'docs', 'apidocs', 'apispec.json', 'flasgger_static')):
            # API 라우트는 그대로 처리
            return app.send_static_file(path) if os.path.exists(os.path.join(app.static_folder, path)) else ("Not Found", 404)

        # 정적 파일이 존재하면 반환
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)

        # 그 외의 경로는 React Router에게 처리하도록 index.html 반환
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({"error": "Frontend not built"}), 404

    # -------- 블루프린트 등록 --------
    from app.routes.weather_routes import weather_bp
    from app.routes.device_routes import device_bp
    from app.routes.gpt_fashion_routes import gpt_fashion_bp
    from app.routes.settings_routes import settings_bp
    from app.routes.cities_routes import cities_bp
    from app.routes.tts_routes import tts_bp
    from app.routes.gpt_environment_routes import gpt_environment_bp # 임포트 확인
    from app.routes.demo_routes import demo_bp # 데모 라우트 추가

    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(device_bp, url_prefix="/api/device")
    app.register_blueprint(gpt_fashion_bp, url_prefix="/api/gpt")
    app.register_blueprint(gpt_environment_bp, url_prefix="/api/gpt") 
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(cities_bp, url_prefix="/api/cities")
    app.register_blueprint(tts_bp, url_prefix="/api/tts")
    app.register_blueprint(demo_bp, url_prefix="/api/demo") # 데모 블루프린트 등록

    return app