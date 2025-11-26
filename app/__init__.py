from flask import Flask, redirect
from flask_cors import CORS
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # CORS
    CORS(app)

    # Swagger 등록
    Swagger(app)

    # 기본 라우트 → Swagger UI로 리다이렉트
    @app.route("/docs")
    def docs():
        return redirect("/apidocs")

    # 블루프린트 등록
    from app.routes.weather_routes import weather_bp
    from app.routes.device_routes import device_bp
    from app.routes.gpt_routes import gpt_bp   

    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(device_bp, url_prefix="/api/device")
    app.register_blueprint(gpt_bp, url_prefix="/api/gpt")

    return app
