from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .config.config import Config
from flask_swagger_ui import get_swaggerui_blueprint
from .routes import register_routes
from .routes.questions import questions_bp
from .models import Question
from flasgger import Swagger  # Import Flasgger for automatic Swagger documentation

def create_app():
    app = Flask(__name__)
    SWAGGER_URL = '/swagger'  # Swagger UI endpoint
    API_URL = '/static/swagger.json'  # Location of the Swagger JSON file

    # Initialize Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "UACS GPT"
        }
    )

    # Set the JWT secret key and load other configurations
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config.from_object(Config)

    # Initialize database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Register blueprints
    app.register_blueprint(questions_bp, url_prefix='/questions')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Initialize Flasgger for automatic OpenAPI (Swagger) generation
    swagger = Swagger(app)

    # Register other routes and configurations
    register_routes(app)

    return app
