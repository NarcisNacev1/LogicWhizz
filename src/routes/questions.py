from flasgger import swag_from
from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override
# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define the EventHandler class for assistant events
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        # We can add custom logic here if needed
        pass

    @override
    def on_text_delta(self, delta, snapshot):
        if hasattr(delta, "value"):
            self.stream.append(delta.value)  # Append the response value to the list
        return ""

    def on_tool_call_created(self, tool_call):
        pass

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# Function to clean up resources
def clean_up(assistant_id, thread_id, vector_store_id, file_ids):
    """Delete the assistant, thread, vector store, and uploaded files."""
    client.beta.assistants.delete(assistant_id)
    client.beta.threads.delete(thread_id)
    client.beta.vector_stores.delete(vector_store_id)
    [client.files.delete(file_id) for file_id in file_ids]

FILES_DIR = "./data/Materials/"
file_ids = []

# Upload files and create a vector store
for file in sorted(os.listdir(FILES_DIR)):
    with open(FILES_DIR + file, "rb") as file_obj:
        _file = client.files.create(file=file_obj, purpose="assistants")
    file_ids.append(_file.id)
    print(f"Uploaded file: {_file.id} - {file}")

vector_store = client.beta.vector_stores.create(
    name="Introduction to Data Science Lecture Presentations.",
    file_ids=file_ids
)
print(f"Created vector store: {vector_store.id} - {vector_store.name}")

# Create an assistant
instructions = (
    "You are a teaching assistant for Computer Science at the University of American College Skopje."
    "Focus on questions that are related to computer science and data science."
    " If you do not know the answer to a question, state that you do not know, rather than guessing."
    " Do not provide full answers to problem sets, as this would violate academic honesty."
    " You can refer to the uploaded course materials for any course-related queries."
)

assistant = client.beta.assistants.create(
    instructions=instructions,
    name="UACS GPT",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}} ,
    model="gpt-4o-mini",  # Correct model name
)
print(f"Created assistant: {assistant.id} - {assistant.name}")

questions_bp = Blueprint("questions", __name__)


# POST request handler for questions
@questions_bp.route("/ask", methods=["POST"])
@swag_from({
    'summary': 'Ask a question to the assistant',
    'parameters': [
        {
            'name': 'question',
            'in': 'body',
            'type': 'string',
            'description': 'The question to ask the assistant',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'The assistant\'s answer to the question',
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {'type': 'string'},
                    'answer': {'type': 'string'}
                }
            }
        },
        '400': {'description': 'Missing question'},
        '500': {'description': 'Internal server error'}
    }
})
def ask_question():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Create a new thread for interaction
    thread = client.beta.threads.create()
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=question
    )

    assistant_response = ""  # Variable to store the assistant's response

    event_handler = EventHandler()
    event_handler.stream = []  # List to collect stream responses

    # Stream the response from the assistant
    try:
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=event_handler
        ) as stream:
            # Capture the assistant's response during the streaming process
            for delta in stream:
                if hasattr(delta, "value"):
                    event_handler.stream.append(delta.value)  # Append the response value

        assistant_response = ''.join(event_handler.stream)  # Combine all streamed responses
        stream.until_done()  # Ensure the stream completes
        print("\nStreaming completed.")
    except Exception as e:
        return jsonify({"error": f"Error during streaming: {e}"}), 500

    # Example response structure with the model's answer stored in the variable
    response = {"question": question, "answer": assistant_response}

    # Clean up after interaction
    clean_up(assistant.id, thread.id, vector_store.id, file_ids)

    return jsonify(response)

# Route to test the service
@questions_bp.route("/", methods=["GET"])
def get_questions():
    return jsonify({"message": "Send a POST request with a question."})
