from flask import Blueprint

def register_routes(app):
    app.register_blueprint(questions_bp, url_prefix='/questions')
