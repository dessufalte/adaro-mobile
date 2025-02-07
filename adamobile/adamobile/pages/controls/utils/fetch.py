import flet as ft
import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("ENDPOINT")
print(BASE_URL)

async def get_data(route: str, token: str = None):
    url = f"{BASE_URL}{route}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, follow_redirects=True)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code} dan {url}"}
