from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any
import time
import uuid
import uvicorn
import logging

from langchain_ollama import ChatOllama
import ollama
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


#bacause the app is running inside docker (macos)
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434",
)

# Create ollama client with custom host
ollama_client = ollama.Client(host=OLLAMA_URL)



class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[dict[str, Any]]
    temperature: float | None = 0
    stream: bool = False

app = FastAPI()

@app.get("/v1/models")
async def list_models(request: Request):
    logger.info(f"GET /v1/models - Client: {request.client.host if request.client else 'unknown'}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = ollama_client.list()
    logger.info(f"Returning {len(response['models'])} models")

    return {
        "object": "list",
        "data": [
            {
                "id": model["model"],
                "object": "model",
                "created": int(time.time()),
                "owned_by": "ollama",
            }
            for model in response["models"]
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, http_request: Request):
    logger.info(f"POST /v1/chat/completions - Client: {http_request.client.host if http_request.client else 'unknown'}")
    logger.info(f"Model: {request.model}, Temperature: {request.temperature}, Messages: {len(request.messages)}")

    llm = ChatOllama(
        model="gemma4:e4b",
        temperature=request.temperature or 0,
        base_url=OLLAMA_URL,
    )

    messages = []

    for message in request.messages:
        role = message["role"]
        content = message["content"]

        if role == "system":
            messages.append(("system", content))
        elif role == "user":
            messages.append(("human", content))
        elif role == "assistant":
            messages.append(("ai", content))

    ai_msg = llm.invoke(messages)
    
    logger.info(f"Response generated: {len(ai_msg.content)} characters")

    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": ai_msg.content,
                },
                "finish_reason": "stop",
            }
        ],
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )