import datetime
import uuid

from openai import AsyncOpenAI
from sqlalchemy import insert

from src.app.config import settings
from src.database.db import database
from src.models.models import ChatMessageDB

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def get_llm_response(message: str) -> str:
    session_id = str(uuid.uuid4())
    await save_messages(session_id, "user", message)

    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": message},
    ]

    completion = await client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )

    answer = completion.choices[0].message.content

    await save_messages(session_id, "assistant", answer)

    return answer


async def save_messages(session_id: str, role: str, content: str):
    query = insert(ChatMessageDB).values(
        session_id=session_id,
        role=role,
        content=content,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    await database.execute(query)
