# UACS ASSISTENT GPT

This API allows users to interact with an OpenAI-powered teaching assistant for a course called "Introduction to Data Science." The assistant can answer course-related questions based on uploaded materials and logs all interactions for auditing purposes.

---

## Features

- **Ask Questions:** Users can post a question to the assistant and receive a response.
- **Real-Time Interaction:** The assistant streams responses, providing updates as they are generated.
- **Logging:** All assistant responses and deltas are logged to a file.
- **Environment Management:** Uses `.env` for secure configuration.
- **File Management:** Uploaded files are processed to create a vector store for course-related queries.
- **Database Integration:** Questions and answers are saved in a database for persistent storage.

---

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
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file with the following keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=your_database_connection_string
   FLASK_ENV=development
   ```

5. **Set Up Database:**
   - Configure the database connection string in the `.env` file.
   - Run migrations if applicable.

6. **Run the Flask Application:**
   ```bash
   flask run
   ```

---

## Endpoints

### Base URL
`http://127.0.0.1:5000`

### `/questions/ask` (POST)
#### Description
Submit a question to the assistant.

#### Request Body
```json
{
  "question": "What is data science?"
}
```

#### Response
- **200 OK**
  ```json
  {
    "question": "What is data science?",
    "answer": "Data science is the field of study that combines domain expertise..."
  }
  ```
- **400 Bad Request**
  ```json
  {
    "error": "Question is required"
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "error": "Error during streaming: <error-message>"
  }
  ```

---

## Logging
All responses from the assistant are logged in the `logs/assistant_responses.log` file for audit and debugging purposes.

---

## File Management
- Files for course materials should be placed in the `data/Intro_to_DS/` directory.
- Each file is uploaded to the OpenAI API and used to create a vector store.

---

## Clean-Up Process
Unused resources (e.g., assistant, threads, vector store, and files) are cleaned up automatically after each interaction.

---

## Swagger Documentation
Swagger is used to document the API endpoints. Ensure the URL paths in Swagger include any prefixes added during route registration, e.g., `/questions/ask`.

---

## Troubleshooting

1. **404 Error in Swagger:**
   - Verify that the URL path includes the correct prefix.
   - Check the Swagger configuration for proper endpoint definitions.

2. **500 Internal Server Error:**
   - Check the logs in `logs/assistant_responses.log`.
   - Ensure that all required environment variables are set correctly.

3. **Database Errors:**
   - Ensure the database connection string in `.env` is correct.
   - Verify database migrations and schema are up-to-date.

---

## Contributing
- Fork the repository and create a new branch for your feature/bugfix.
- Submit a pull request with a clear description of changes.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

