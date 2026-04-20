import os
from groq import AsyncGroq
from app.sessions import session_store

def _client():
    return AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = os.environ.get(
    "AVATAR_SYSTEM_PROMPT",
    "You are a helpful and friendly avatar assistant. Keep responses concise and conversational."
)


async def get_reply(message: str, session_id: str) -> str:
    session = session_store.get(session_id)
    history = session.get("history", []) if session else []

    history.append({"role": "user", "content": message})

    response = await _client().chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "llama3-8b-8192"),
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
        max_tokens=300,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    session_store.update_history(session_id, history)

    return reply
