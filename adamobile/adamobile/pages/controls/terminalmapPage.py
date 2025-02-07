import flet as ft
from .diagram import conveyors, MapDiagram, ships, hoppers, stockpiles, ItemConvey, ways, get_random_way, get_way
import time
import random
import websockets, threading, asyncio, json
from .utils.fetch import get_data
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("ENDPOINT_WS")

class HistoryCells(ft.Column):
    def __init__(self):
        super().__init__()
        
        
        self.history = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Transaction History ", color='black', size=14, weight=ft.FontWeight.W_500),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ),
                    ft.Divider(height=1),
                ]
            ), bgcolor='white'
        )
        
        self.table = ft.DataTable(
                        [
                            ft.DataColumn(ft.Text("Product", color='grey600'), False),
                            ft.DataColumn(ft.Text("Hopper", color='grey600'), False),
                            ft.DataColumn(ft.Text("Destination", color='grey600'), False),
                            ft.DataColumn(ft.Text("Amount", color='grey600'), False),
                            ft.DataColumn(ft.Text("Timestamp", color='grey600'), False),

                        ],
                        []
                        ,expand=True, data_row_color= "teal300", column_spacing=5
                    )
        
        self.main = ft.Column([
            self.history,
            ft.Row(
                [
                    self.table
                ], scroll=ft.ScrollMode.ALWAYS    
            ),
                    
        ],scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        self.controls = [
            self.main
        ]
    


class TerminalMapPage(ft.Column):
    def __init__(self, hsm: ft.Column, page: ft.Page):
        super().__init__()
        self.page = page
        self.hsm = hsm
        self.borderRadTop = ft.BorderRadius(15,15,0,0)
        self.borderAll = ft.BorderRadius(15,15,15,15)
        self.border = ft.BorderSide(1,'grey')
        self.border_super = ft.Border(self.border, self.border, self.border, self.border)
        
        self.history = HistoryCells()
        
        self.canvas = MapDiagram(800, 400)
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas_container = ft.Container(self.canvas, alignment=ft.alignment.center, bgcolor='grey200')
        self.viewers = ft.InteractiveViewer(self.canvas_container, expand=True)
        # self.message_parse = None
        # self.thread_async = None
                                    
        
        self.loaded = False
        self.map_board = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Kelanis Map Diagram ", color='black', size= 20 , weight= ft.FontWeight.W_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ), 
                    ),
                    ft.Divider(height=1) ,
                    ft.Container(
                        ft.Column(
                            [
                                ft.Stack([
                                    self.viewers,
                                    ft.Container(
                                        ft.CupertinoSwitch(
                                            "lock",
                                            False,
                                            on_change=self.lock_map
                                        )
                                    ),
                                ]
                                ) ,
                            ]
                        ), padding= 10, expand=True
                    ),
                    self.history
                ]
            ),  bgcolor='white'
        )
        self.main = ft.Column([self.map_board])
        self.controls = [
            self.main
        ]
        self.expand = True
    
    def lock_map(self, e):
        is_locked = e.control.value
        self.viewers.pan_enabled = not is_locked
        self.viewers.scale_enabled = not is_locked
        self.update()
    def local_transfer(self, itemc: ItemConvey,):
        itemc.activate_way()
        h_name = itemc.get_hopper_name(ways)
        hoppers[h_name].activate()
        self.canvas.clean()
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas.update()
        time.sleep(1)
        hoppers[h_name].deactivate()
        itemc.deactivate_way()
        self.canvas.clean()
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas.update()
        
    def get_way(self, hopper, way):
        group_destinations = ways[f"H{hopper}"]
        destination = group_destinations[way]
        return destination, destination


    def local_item_test(self, hopper, the_ways, amount):
        for _ in range(1): 
            
            # destination, way = get_way(hopper, ways)
            destination, way = get_random_way(the_way=the_ways, the_hopper=hopper)
            item = ItemConvey(
                amount=amount,
                destination=destination,
                ways=way
            )
            self.local_transfer(itemc=item)
            time.sleep(0.1)
            
    async def api_data(self):
        api_data = await get_data(f"api/terminal/item/get_latest")
        print(f"Data API: {api_data}")
        
        if api_data['status']==200:
            self.history.table.rows.clear()
            for item in api_data['data']:
                amount = item['amount']
                hopper = item['hopper']
                ways = item['ways']
                tmpst = item['timestamp']
                product = item['product']
                
                data_row = ft.DataRow(
                    [
                        ft.DataCell(ft.Text(str(product))),
                        ft.DataCell(ft.Text(str(hopper))),
                        ft.DataCell(ft.Text(str(ways))),
                        ft.DataCell(ft.Text(str(amount))),
                        ft.DataCell(ft.Text(str(tmpst))),
                    ]
                )
                self.history.table.rows.append(data_row)
                self.history.update()
                
        self.update()
    

        
        
    # async def listen_to_server(self):
    #     while True:
    #         try:
    #             print("Attempting to connect to the WebSocket server...")
    #             async with websockets.connect(f"{BASE_URL}ws/endpoint") as websocket:
    #                 print(f"{BASE_URL}ws/itemkct")
    #                 is_connected = True
    #                 while True:
    #                     message = await websocket.recv()
    #                     if message:
    #                         message_parse = json.loads(message)
    #                         print(f"Received message: {message_parse}")

    #         except (websockets.ConnectionClosedError, websockets.InvalidURI, Exception) as e:
    #             is_connected = False
    #             print(f"Connection error: {e}. Retrying in 5 seconds...")
    #             time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

    #     # Jalankan WebSocket dalam thread terpisah
    # def start_websocket(self):
    #     asyncio.run(self.listen_to_server())
        
    def did_mount(self):
        # self.thread_async = threading.Thread(target=self.start_websocket, daemon=True)
        # self.thread_async.start()
        self.page.run_task(self.api_data)
        self.loaded = True
    
    def will_unmount(self):
        self.loaded = False