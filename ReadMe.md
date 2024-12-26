# UACS AI-Powered Teaching Assistant for Data Science

This API provides an AI-powered teaching assistant for the "Introduction to Data Science" course at UACS. It leverages OpenAI's advanced language models to answer student questions based on course materials and provides real-time interaction and comprehensive logging. 

**Note:** To use this API, you must create a `data` directory in the main project directory. Inside the `data` directory, create a `materials` folder. Place any relevant course materials (e.g., PDFs, lecture notes, assignments) within the `materials` folder. 

## Features

- **Ask Questions:** Students can submit questions to the assistant and receive relevant and informative responses.
- **Real-Time Interaction:** The assistant streams responses, providing updates as they are generated for a more engaging user experience.
- **Logging:** All interactions, including questions, responses, and any relevant system information, are logged for auditing and debugging purposes.
- **Environment Management:** Utilizes the `.env` file for secure and flexible configuration of sensitive information like API keys and database credentials.
- **File Management:** Course materials are processed to create a vector store, enabling efficient retrieval and analysis of information related to student queries.
- **Database Integration:** **Questions and answers are stored in a PostgreSQL database** for persistent storage and future analysis.

## Installation

### Prerequisites

- Python 3.10+
- Flask
- PostgreSQL
- OpenAI Python library
- dotenv library for environment variable management

### Steps

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>

    Set Up Virtual Environment:
    Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:
Bash

pip install -r requirements.txt

Set Up Environment Variables:
Create a .env 1  file with the following keys:  
 1. github.com

MIT
github.com
Code snippet

OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_connection_string 
FLASK_ENV=development

Set Up Database:

    Configure the database connection string in the .env file.
    Run migrations if applicable.

Place Course Materials:

    Create a data directory in the main project directory.
    Create a materials folder inside the data directory.
    Place your course materials (e.g., PDFs, lecture notes, assignments) within the materials folder.

Run the Flask Application:
Bash

    flask run

Endpoints
Base URL

http://127.0.0.1:5000
/questions/ask (POST)
Description

Submit a question to the assistant.
Request Body
JSON

{
  "question": "What is data science?"
}

Response

    200 OK
    JSON

{
  "question": "What is data science?",
  "answer": "Data science is the field of study that combines domain expertise..."
}

400 Bad Request
JSON

{
  "error": "Question is required"
}

500 Internal Server Error
JSON

    {
      "error": "Error during streaming: <error-message>"
    }

Logging

All interactions with the assistant are logged in the logs/assistant_responses.log file for audit, debugging, and analysis.
File Management

    Course materials are placed in the data/materials/ directory.
    The system automatically processes these materials to create a vector store for efficient question answering.

Clean-Up Process

Unused resources (e.g., assistant, threads, vector store, and files) are cleaned up automatically after each interaction.
Swagger Documentation

Swagger is used to document the API endpoints. Ensure the URL paths in Swagger include any prefixes added during route registration, e.g., /questions/ask.
Troubleshooting

    404 Error in Swagger:
        Verify that the URL path includes the correct prefix.
        Check the Swagger configuration for proper endpoint definitions.

    500 Internal Server Error:
        Check the logs in logs/assistant_responses.log.
        Ensure that all required environment variables are set correctly.

    Database Errors:
        Ensure the database connection string in .env is correct.
        Verify database migrations and schema are up-to-date.

Contributing

    Fork the repository and create a new branch for your feature/bugfix.
    Submit a pull request with a clear description of changes.
