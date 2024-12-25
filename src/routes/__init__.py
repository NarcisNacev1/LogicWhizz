from .questions import questions_bp

def register_routes(app):
    app.register_blueprint(questions_bp, name='questions1', url_prefix='/questions')
