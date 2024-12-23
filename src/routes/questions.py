from flask import Blueprint, request, jsonify

questions_bp = Blueprint("questions", __name__)

@questions_bp.route("/", methods=["GET"])
def get_questions():
    return jsonify({"message": "Get all questions"})

@questions_bp.route("/", methods=["POST"])
def post_question():
    data = request.json
    return jsonify({"message": "Question received", "data": data})
