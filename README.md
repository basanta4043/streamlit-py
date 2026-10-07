# Streamlit Python Playground

A collection of Python-based applications and experiments built with **Streamlit**. This project brings together AI/LLM experiments, MQTT communication, utility tools, and interactive applications under a single Streamlit interface.

## 🚀 Features

The application provides several tools accessible from the sidebar.

### 🤖 AI Chatbot

A local AI chatbot powered by **Ollama** and **DeepSeek R1**.

- Uses `deepseek-r1:1.5b`
- Runs locally through Ollama
- Built with LangChain
- Maintains conversation history
- Stores chat history using SQLite
- Supports streaming responses
- Includes session-based conversations

### 📄 AI Cover Letter Generator

Generate a personalized cover letter from your resume and a job description.

The workflow:

1. Upload a `.pdf` or `.docx` resume.
2. Extract resume content.
3. Use an LLM to parse the resume into structured information.
4. Provide a target job description.
5. Generate a professional cover letter based on the candidate profile and job requirements.

The project supports LLM-based resume parsing and cover-letter generation using the Llama API.

### 📡 MQTT Client

An interactive MQTT publisher/subscriber interface.

Features include:

- Configure MQTT host and port
- Optional username/password authentication
- Subscribe to a receiver topic
- Publish messages to a sender topic
- Display received messages
- Start and stop the MQTT client
- JSON message support

This is useful for experimenting with IoT, messaging systems, payment-terminal integrations, and event-driven applications.

### 🔐 Password Encoder

A simple password hashing and verification utility.

- SHA-256 hashing
- Optional salt
- Password verification
- Streamlit-based interface

> **Note:** This component is intended for experimentation and learning. For production authentication systems, use a password-specific hashing algorithm such as Argon2id, bcrypt, or scrypt rather than plain SHA-256.

### 🎮 Tic-Tac-Toe

A browser-based Tic-Tac-Toe game implemented with Streamlit.

Features:

- Two-player X/O gameplay
- Turn management
- Winner detection
- Tie detection
- Game reset

---

## 🏗️ Project Structure

```text
streamlit-py/
│
├── app_image/
│   └── logo.png
│
├── coverletter/
│   ├── __init__.py
│   ├── constant.py
│   ├── cover_letter.py
│   ├── cover_letter_ui.py
│   └── file_loader.py
│
├── llm_instructions/
│   ├── cover_letter_api.json
│   └── resume_parser_api.json
│
├── .devcontainer/
│   └── devcontainer.json
│
├── deepseek_ollama.py
├── encoder.py
├── mqtt_publisher.py
├── tic_tac_toe.py
├── main.py
├── requirements.txt
└── chat_history.db
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web UI |
| LangChain | LLM orchestration |
| Ollama | Local LLM inference |
| DeepSeek R1 | Local AI chatbot |
| Llama API | Resume parsing and cover-letter generation |
| SQLite | Chat history persistence |
| MQTT / Paho MQTT | Messaging |
| PyPDF2 | PDF text extraction |
| python-docx | DOCX text extraction |

---

## ⚙️ Requirements

- Python 3.10+
- `pip`
- Ollama (required for the local chatbot)
- An Ollama model such as `deepseek-r1:1.5b`
- Llama API key for the cover-letter generator

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/basanta4043/streamlit-py.git
cd streamlit-py
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run main.py
```

The application will start a local web server and provide a URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## 🤖 Setting Up the Local AI Chatbot

The chatbot uses Ollama locally.

Install Ollama and download the required model:

```bash
ollama pull deepseek-r1:1.5b
```

Make sure Ollama is running:

```bash
ollama serve
```

The application expects the Ollama server at:

```text
http://localhost:11434
```

Once Ollama is running, select:

```text
Chat Bot
```

from the Streamlit sidebar.

---

## 📄 Using the Cover Letter Generator

Select:

```text
Cover Letter
```

from the sidebar.

You will need a Llama API key.

### Workflow

```text
Resume (.pdf/.docx)
        │
        ▼
Document Text Extraction
        │
        ▼
LLM Resume Parser
        │
        ▼
Structured Candidate Profile
        │
        +───────────────+
        │               │
        ▼               ▼
Job Description     Candidate Profile
        │               │
        +───────┬───────+
                ▼
        LLM Cover Letter
                │
                ▼
        Generated Letter
```

The resume parser extracts key information such as:

- First name
- Last name
- Location
- Work experience
- Education
- Skills

The resulting candidate profile is then combined with the job description and current date to generate a customized cover letter.

---

## 📡 Using the MQTT Client

Select:

```text
MQTT Publisher
```

from the sidebar.

Configure:

```text
MQTT Host
MQTT Port
Username
Password
Sender Topic
Receiver Topic
```

Then start the MQTT client.

The application can:

- Subscribe to the receiver topic
- Publish messages to the sender topic
- Display incoming MQTT messages

The default MQTT port is:

```text
1883
```

For example:

```text
Sender:
terminal/txn/sgr-card/sale/request

Receiver:
terminal/txn/sgr-card/sale/response
```

---

## 🔐 Password Encoder

Select:

```text
Password Encoder
```

The utility provides two operations:

### Encode

```text
Plain Text
    ↓
SHA-256
    ↓
Optional Salt
    ↓
SHA-256
    ↓
Encoded Password
```

### Verify

The application generates the hash again and compares it with the provided encoded password.

> This is a learning/demo utility and should not be used as the password storage mechanism for a production authentication system.

---

## 🎮 Tic-Tac-Toe

Select:

```text
TIC TAC TOE
```

from the sidebar.

The game uses Streamlit session state to maintain:

- Board state
- Current player
- Winner
- Game-over state

Press **Reset Game** to start a new game.

---

## 🧩 Application Architecture

The project uses `main.py` as the main Streamlit entry point.

```text
                    ┌─────────────────────┐
                    │      main.py        │
                    │  Streamlit Router   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Password Encoder     MQTT Client      Tic-Tac-Toe
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
          AI Chatbot                  Cover Letter AI
                │                             │
             Ollama                    Llama API
                │                             │
          DeepSeek R1              Resume + Job Description
                │                             │
             SQLite                    Generated Letter
```

---

## 📁 Main Components

### `main.py`

Application entry point and sidebar navigation.

### `deepseek_ollama.py`

Implements the local AI chatbot using:

- Ollama
- DeepSeek R1
- LangChain
- SQLite chat history

### `encoder.py`

Contains password hashing and verification functionality.

### `mqtt_publisher.py`

Implements the MQTT client and Streamlit interface.

### `tic_tac_toe.py`

Contains the Tic-Tac-Toe game logic and UI.

### `coverletter/cover_letter.py`

Contains the core AI cover-letter generation logic.

### `coverletter/cover_letter_ui.py`

Provides the Streamlit UI for the cover-letter generator.

### `coverletter/file_loader.py`

Extracts text from:

- PDF documents
- DOCX documents

### `llm_instructions/`

Contains JSON-based prompts/instructions for:

- Resume parsing
- Cover-letter generation

---

## 🔒 Security Notes

This repository contains components that interact with external and local services.

For production usage:

- Do not commit API keys.
- Use environment variables or Streamlit secrets.
- Avoid storing sensitive resumes or personal information in Git.
- Use secure password hashing algorithms for authentication.
- Configure MQTT authentication and TLS when communicating over untrusted networks.
- Review local SQLite data before sharing or deploying the project publicly.

---

## 🛠️ Development

The repository also includes a Dev Container configuration:

```text
.devcontainer/devcontainer.json
```

This can be used to create a reproducible development environment with compatible tooling.

---

## 🎯 Purpose

This repository serves as a practical Python and Streamlit playground for experimenting with:

- Generative AI
- Local LLMs
- LangChain
- Document processing
- Resume parsing
- AI-assisted job applications
- MQTT communication
- Streamlit application development
- SQLite-backed chat history
- Interactive Python applications

It can also serve as a starting point for turning individual experiments into standalone production applications.

---

## 📌 Future Improvements

Potential improvements include:

- [ ] Move secrets/API keys to Streamlit Secrets
- [ ] Add Docker support
- [ ] Add automated tests
- [ ] Improve application configuration
- [ ] Add structured logging
- [ ] Improve MQTT connection lifecycle management
- [ ] Replace SHA-256 password hashing with Argon2/bcrypt
- [ ] Add persistent user authentication
- [ ] Improve chatbot configuration through the UI
- [ ] Add support for additional LLM providers
- [ ] Add resume/job-description matching
- [ ] Add downloadable generated cover letters
- [ ] Add CI/CD with GitHub Actions

---

## 👨‍💻 Author

**Basanta Regmi**

GitHub: [@basanta4043](https://github.com/basanta4043)

---

## 📜 License

This project is provided for learning, experimentation, and personal development. Add an explicit license to the repository if you intend to allow reuse or distribution.
