import flet as ft
from pages import homescreen, logscreen
import websockets
import asyncio
import json
from functools import partial
import threading
import time
from pages.controls.utils.fetch import get_data 
from dotenv import load_dotenv
import os


load_dotenv()

BASE_URL = os.getenv("ENDPOINT_WS")
DARK_MODE = ['']
LIGHT_MODE = ['']
TOKEN = ""

def main(page: ft.Page):

    page.window.width = 375
    page.window.height = 667
    page.window.max_width = 375
    page.window.max_height = 667
    page.window.min_height = 667
    page.window.min_width = 375
    page.title = "Adamobile"
    page.theme_mode = ft.ThemeMode.LIGHT
    is_connected = False
    
    page.client_storage.set('color_scheme', DARK_MODE)
    TOKEN = page.client_storage.get('token')

    logn_screen = logscreen.LoginPage(page)
    home_screen = homescreen.HomeScreen(page)
    home_screen.news_page.this = home_screen.switcher
    
    
    page.views.append(home_screen.get_view())
    
    
    page.update()
    

    def change_route(e):
        page.views.clear()
        if page.route == "/":
            home_screen.switcher.content = home_screen.mainpage
            page.views.append(home_screen.get_view())
        elif page.route == "/hts":
            home_screen.switcher.content = home_screen.hts_page
            page.views.append(home_screen.get_view())
        elif page.route == "/news":
            home_screen.switcher.content = home_screen.news_page
            page.views.append(home_screen.get_view())
        elif page.route == "/terminal":
            home_screen.switcher.content = home_screen.terminal_page
            page.views.append(home_screen.get_view())
        elif page.route == "/emergency":
            home_screen.switcher.content = home_screen.emergency_page
            page.views.append(home_screen.get_view())
        elif page.route == "/stockpile":
            home_screen.switcher.content = home_screen.stock_page
            page.views.append(home_screen.get_view())
        elif page.route == "/settings":
            home_screen.switcher.content = home_screen.settings_page
            page.views.append(home_screen.get_view())
        elif page.route == "/delay":
            home_screen.switcher.content = home_screen.delay_page
            page.views.append(home_screen.get_view())
        elif page.route == "/login":
            page.views.append(logn_screen)
        page.update()
    page.on_route_change = change_route
    

    message_parse = None
    print(page.route)
    def close_banner(e):
        page.close(banner)

    def going_to_emergency(e, message_parse_text):
        print(f"TEST: {message_parse_text}")
        if message_parse_text:
            home_screen.emergency_page.recieve_information(message_parse_text)
            page.go("/emergency")
            home_screen.emergency_page.build()
            page.close(banner)
            page.update()
    action_button_style = ft.ButtonStyle(color=ft.colors.WHITE)

    banner = ft.Banner(
        bgcolor=ft.colors.RED_300,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.WHITE, size=40),
        content=ft.Text(
            value="Oops, there were some errors while trying to delete the file. What would you like me to do?",
            color=ft.colors.WHITE,
        ),
        actions=[
            ft.TextButton(
                text="Show",
                style=action_button_style,
                on_click=lambda e: going_to_emergency(e, message_parse),
            ),
            ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
            ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
        ],
        force_actions_below=False,
    )

    # async def listen_to_server():
    #     nonlocal message_parse
    #     async with websockets.connect("ws://127.0.0.1:8000/ws/hazard") as websocket:
    #         while True:
    #             message = await websocket.recv()
    #             if message:
    #                 message_parse = json.loads(message)
    #                 print(message_parse)
    #                 banner.content = ft.Text(value=str(message_parse), color=ft.colors.BLACK)
    #                 page.open(banner)
    #                 page.update()

    # # Jalankan fungsi listen_to_server
    # asyncio.run(listen_to_server())

    async def listen_to_server():
            nonlocal message_parse
            while True:
                try:
                    print("Attempting to connect to the WebSocket server...")
                    async with websockets.connect(f"{BASE_URL}ws/endpoint") as websocket:
                        print("Connected to the WebSocket server.")
                        is_connected = True
                        while True:
                            message = await websocket.recv()
                            if message:
                                # print(f"Received message: {message}")
                                message_parse = json.loads(message)
                                # print(f"Received message: {message_parse}")
                                if 'latitude' in message_parse and 'longitude' in message_parse:
                                    print('lat dan long')
                                    banner.content = ft.Container(
                                        ft.Column([
                                            ft.Text(
                                                value=f"Emergency point detected!", color=ft.colors.WHITE
                                            ),
                                            ft.Container(
                                                ft.Text(f"Terdapat: {message_parse["reason"]}", color='white'),
                                                bgcolor='red300'
                                            )
                                        ])
                                    )
                                    page.open(banner)
                                    page.update()
                                if 'hopper' in message_parse:
                                    print('hopper masuk')
                                    if home_screen.terminal_page.loaded:
                                        home_screen.terminal_page.local_item_test(amount=message_parse["amount"],hopper=message_parse["hopper"],the_ways=message_parse["ways"])
                                        # local_item_test(
                                        #     amount=message_parse["amount"],
                                        #     destination=message_parse["destination"],
                                        #     hopper=message_parse["hopper"],
                                        #     way=message_parse["ways"]
                                        # )

                                
                except (websockets.ConnectionClosedError, websockets.InvalidURI, Exception) as e:
                    is_connected = False
                    print(f"Connection error: {e}. Retrying in 5 seconds...")
                    time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

        # Jalankan WebSocket dalam thread terpisah
    def start_websocket():
        asyncio.run(listen_to_server())

    
    websocket_thread = threading.Thread(target=start_websocket, daemon=True)
    websocket_thread.start()

ft.app(target=main, view=ft.AppView.FLET_APP, assets_dir="assets", host="0.0.0.0")
