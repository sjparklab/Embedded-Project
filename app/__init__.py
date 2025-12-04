from flask import Flask, redirect, jsonify
from flask_cors import CORS
from flasgger import Swagger

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
    app = Flask(__name__)

    # CORS 허용
    CORS(app)

    # Swagger 적용
    Swagger(app, config=swagger_config, template_file=None)

    # 백그라운드 스케줄러 시작
    from app.scheduler import start_scheduler
    start_scheduler()

    # -------- 루트('/') --------
    @app.route("/")
    def root():
        return jsonify({"message": "API 서버가 정상 동작 중입니다."})

    # -------- Swagger 문서 --------
    @app.route("/docs")
    def docs():
        return redirect("/apidocs/")

    # -------- 블루프린트 등록 --------
    from app.routes.weather_routes import weather_bp
    from app.routes.device_routes import device_bp
    from app.routes.gpt_fashion_routes import gpt_fashion_bp
    from app.routes.settings_routes import settings_bp
    from app.routes.cities_routes import cities_bp

    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(device_bp, url_prefix="/api/device")
    app.register_blueprint(gpt_fashion_bp, url_prefix="/api/gpt")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(cities_bp, url_prefix="/api/cities")

    return app
