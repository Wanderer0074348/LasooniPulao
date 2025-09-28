# FastAPI LLM Chatbot Setup

## Install uv Package Manager

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Or with wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Setup Project

1. Clone the project and navigate to directory
2. Create `.env` file with your OpenAI API key and DATABASE_URL
3. Install dependencies using uv (automatically reads pyproject.toml and uv.lock):
   ```bash
   uv sync
   ```

## Run the Application
```bash
uv run uvicorn app:app --reload
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`.
