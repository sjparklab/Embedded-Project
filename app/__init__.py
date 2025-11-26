from flask import Flask, redirect, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
import os

# Swagger 설정
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "static_url_path": "/flasgger_static"
}

def create_app():
    app = Flask(__name__)

    CORS(app)
    Swagger(app, config=swagger_config, template_file=None)  

    # 루트('/') 요청 → index.html 반환
    @app.route("/")
    def index_page():
        return send_from_directory(os.getcwd(), "index.html")

    # /docs 는 Swagger UI 리다이렉트
    @app.route("/docs")
    def docs():
        return redirect("/apidocs/")

    # 블루프린트 등록
    from app.routes.weather_routes import weather_bp
    from app.routes.device_routes import device_bp
    from app.routes.gpt_routes import gpt_bp

    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(device_bp, url_prefix="/api/device")
    app.register_blueprint(gpt_bp, url_prefix="/api/gpt")

    return app
