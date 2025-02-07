import flet as ft
from dotenv import load_dotenv
import os
import httpx
import asyncio
load_dotenv()

BASE_URL = os.getenv("ENDPOINT_WS")


class LoginPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        

        self.username_field = ft.TextField(label="Username", autofocus=True)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)
        

        self.error_text = ft.Text(value="", color="red")
        

        self.login_button = ft.ElevatedButton(text="Login", on_click=self.act_log)
        

        self.main = ft.Column(
            [
                ft.Stack(
                    [
                        ft.Column(
                            [
                                ft.Text("Login", size=30, weight="bold"),
                                self.username_field,
                                self.password_field,
                                self.error_text,
                                self.login_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        )
                    ],
                    width=page.width,
                    height=page.height,
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE
        )
        
        self.controls = [self.main]

    
    def act_log(self, e):
        self.page.run_task(self.login)
    
    async def login(self):
        username = self.username_field.value
        password = self.password_field.value
        
        async def authenticate():
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BASE_URL}login",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    if token:
                        await self.page.client_storage.set_async("token", token)
                        self.error_text.value = "Login successful!"
                        self.error_text.color = "green"
                        print(token)
                        self.page.go("/")
                    else:
                        self.error_text.value = "Failed to retrieve token"
                        self.error_text.color = "red"
                else:
                    self.error_text.value = "Invalid username or password"
                    self.error_text.color = "red"
                
                self.page.update()
        
        asyncio.create_task(authenticate())