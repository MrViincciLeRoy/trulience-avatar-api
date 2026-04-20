from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.sessions import session_store
from app.llm import get_reply

app = FastAPI()


class TrulienceRequest(BaseModel):
    action: str
    sessionId: str
    userId: Optional[str] = None
    message: Optional[str] = None
    authToken: Optional[str] = None
    callbackUrl: Optional[str] = None


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/trulience")
async def trulience(body: TrulienceRequest):
    match body.action:
        case "LOGIN":
            session_store.create(body.sessionId, {
                "userId": body.userId,
                "authToken": body.authToken,
                "callbackUrl": body.callbackUrl,
            })
            return {
                "sessionId": body.sessionId,
                "status": "OK",
                "statusMessage": "Hello! How can I help you today?"
            }

        case "CHAT":
            if not session_store.exists(body.sessionId):
                raise HTTPException(status_code=400, detail="Session not found")
            reply = await get_reply(body.message or "", body.sessionId)
            return {
                "sessionId": body.sessionId,
                "reply": reply,
                "status": "OK",
                "statusMessage": "Reply Sent"
            }

        case "LOGOUT":
            session_store.delete(body.sessionId)
            return {
                "sessionId": body.sessionId,
                "status": "OK",
                "statusMessage": "Goodbye!"
            }

        case _:
            raise HTTPException(status_code=400, detail="Unknown action")