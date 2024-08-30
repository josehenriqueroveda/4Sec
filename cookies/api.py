from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class Cookie(BaseModel):
    name: str
    value: str


class CookiesRequest(BaseModel):
    cookies: list[Cookie]


@app.post("/api/cookies")
async def receive_cookies(cookies_request: CookiesRequest):
    cookies = cookies_request.cookies
    print(cookies)
    return {"status": "success", "data": cookies}
