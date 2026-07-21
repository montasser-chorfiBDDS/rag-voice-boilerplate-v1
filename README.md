# RAG Voice Boilerplate

A production-ready Python boilerplate for building RAG (Retrieval Augmented Generation) applications with voice processing capabilities.

## 🚀 Features

- **📚 RAG Engine Integration** - Built with LangChain and OpenAI
- **🎤 Voice Processing Pipeline** - Speech-to-text and text-to-speech
- **🗄️ Vector Store Support** - FAISS for efficient similarity search
- **🐋 Docker Containerization** - Ready for deployment
- **🧪 Testing Infrastructure** - Pytest setup included
- **🔧 Modular Architecture** - Easy to extend and customize

## 📁 Project Structure

```
rag-voice-boilerplate/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag_engine.py
│   │   ├── voice_processor.py
│   │   └── document_processor.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── db.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   └── __init__.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🛠️ Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rag-voice-boilerplate.git
cd rag-voice-boilerplate
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
DEBUG=true
```

5. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

### Docker

1. Build and run with Docker Compose:
```bash
cd docker
docker-compose up -d
```

2. The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Query Endpoints

- `POST /api/v1/query` - Query with text
- `POST /api/v1/query/voice` - Query with voice

### Document Endpoints

- `POST /api/v1/documents/upload` - Upload a document
- `POST /api/v1/documents/text` - Add text document
- `GET /api/v1/documents` - List all documents

### Conversation Endpoints

- `GET /api/v1/conversations` - List recent conversations

## 🔧 Configuration

All configuration is in `config.py`. You can customize:

- **OpenAI Settings**: Model, API key
- **Vector Store**: Embedding model, storage path
- **Voice Processing**: Whisper model, TTS engine
- **Chunking**: Size and overlap

## 🧪 Testing

```bash
pytest tests/
```

## 📝 Example Usage

### Add a Document

```python
import requests

# Upload PDF
files = {"file": open("document.pdf", "rb")}
response = requests.post("http://localhost:8000/api/v1/documents/upload", files=files)
print(response.json())
```

### Query the RAG Engine

```python
import requests

# Text query
response = requests.post(
    "http://localhost:8000/api/v1/query",
    params={"question": "What is the document about?"}
)
print(response.json())
```

### Voice Query

```python
import requests

# Voice query
files = {"audio": open("recording.wav", "rb")}
response = requests.post("http://localhost:8000/api/v1/query/voice", files=files)
with open("response.wav", "wb") as f:
    f.write(response.content)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Montasse Chorfi** - Data Scientist & Big Data Specialist

- GitHub: [montasser-chorfiBDDS](https://github.com/montasser-chorfiBDDS)
- Email: montasserchorfi26@gmail.com
