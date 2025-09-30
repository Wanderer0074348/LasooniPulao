import datetime
import uuid

from openai import AsyncOpenAI
from sqlalchemy import desc, insert, select, update

from src.app.config import settings
from src.database.db import database
from src.models.models import ChatMessageDB, ChatSessionDB

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def get_history(session_id: str, window: int = 10) -> list:
    query = (
        select(ChatMessageDB)
        .where(ChatMessageDB.session_id == session_id)
        .order_by(desc(ChatMessageDB.timestamp))
        .limit(window)
    )

    results = await database.fetch_all(query=query)

    history = [
        {"role": row["role"], "content": row["content"]} for row in reversed(results)
    ]

    return history


async def get_llm_response(message: str, session_id: str) -> str:
    await save_messages(session_id, "user", message)

    history = await get_history(session_id=session_id, window=10)

    messages = [
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": message},
    ]
    messages.extend(history)

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

    await update_session_metadata(session_id=session_id)


async def create_new_session_id():
    session_id = str(uuid.uuid4())

    query = insert(ChatSessionDB).values(session_id=session_id)

    await database.execute(query)

    return session_id


async def update_session_metadata(session_id: str):
    query = (
        update(ChatSessionDB)
        .where(ChatSessionDB.session_id == session_id)
        .values(
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            message_count=ChatSessionDB.message_count + 1,
        )
    )

    await database.execute(query)
