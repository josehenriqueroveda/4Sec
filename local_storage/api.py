from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class LocalStorageItem(BaseModel):
    key: str
    value: str


@app.post("/api/localstorage")
async def receive_local_storage(local_storage_items: List[LocalStorageItem]):
    for item in local_storage_items:
        print(f"Key: {item.key}, Value: {item.value}")
    return {"status": "success", "data": local_storage_items}
