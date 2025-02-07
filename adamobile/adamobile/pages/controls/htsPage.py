import flet as ft
from .utils.fetch import get_data
import json

class TruckTile(ft.ExpansionTile):
    def __init__(
        self,
        truck_id: str,
        truck_name: str,
        data_times: dict = None,
        material: str = "",
        weight: float = 0,
        initially_expanded: bool = False,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.TEAL_300,
        **kwargs
    ):
        data_times = data_times or {}

        

        super().__init__(
            title=ft.Text(truck_id, weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(truck_name),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=initially_expanded,
            collapsed_text_color=collapsed_text_color,
            text_color=text_color,
            **kwargs
        )
        self.columns = [ft.DataColumn(ft.Text(jadwal, color=self.text_color)) for jadwal in data_times.keys()]

        self.rows = [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(value, color=self.text_color)) for value in data_times.values()]
            )
        ]

        self.trailing = ft.Icon(ft.icons.FIRE_TRUCK, color='white')

        self.collapsed_bgcolor = 'teal300'
        self.bgcolor = 'white'
        self.icon_color = 'teal300'
        
        
        self.truck_id = truck_id
        self.truck_name = truck_name
        self.material = material
        self.data_times = data_times
        self.weight = weight
        
        self.collapsed_icon_color = 'white'
    def build(self):
        self.controls = [
            ft.Column(
                [
                    ft.Text(f"Material: {self.material}", color='black'),
                    ft.Text(f"Weight: {self.weight} kg", color='black'),
                    ft.Row(
                        [
                        ft.DataTable(columns=self.columns, rows=self.rows,expand=True, column_spacing=10),
                    ], scroll= ft.ScrollMode.ALWAYS, width=400
                        ),
                ], scroll=ft.ScrollMode.ALWAYS
            )
        ]
        
jadwal_truck =  {"Jadwal 1": "07:00", "Jadwal 2": "09:00", "Jadwal 3": "09:00", "Jadwal 4": "09:00"}       

class HTSPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.current_page = 1
        self.limit = 10  
        self.total_pages = 1
        self.search_query = ""

        self.all_truck_tiles = []
        self.trucktiles = ft.Column()

        self.search_form = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(expand=True, color='black', hint_text='Search...', on_change=self.search_truck),
                        ]
                    )
                ]
            ), padding=10
        )

        self.pagination_text = ft.Text(f"Page {self.current_page} of {self.total_pages}", color='black')


        self.pagination = ft.Container(
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.prev_page),
                    self.pagination_text,  
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD, on_click=self.next_page),
                ], alignment=ft.MainAxisAlignment.CENTER
            ), padding=3
        )
        
        self.hauling_board = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Hauling Board ", color='black', size=20, weight=ft.FontWeight.W_100),
                                ft.IconButton(ft.icons.REFRESH, on_click=self.refresh)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ),
                    ft.Divider(height=1),
                    self.search_form,
                    self.trucktiles
                ]
            ), bgcolor='white'
        )
        
        self.main = ft.Column([self.hauling_board, self.pagination])
        self.controls = [self.main]
        self.expand = True

    def search_truck(self, e):
        # query = e.control.value.lower()
        # filtered = [tile for tile in self.all_truck_tiles if query in tile.truck_id.lower()]
        # self.trucktiles.clean()
        # self.trucktiles.controls = filtered
        # self.trucktiles.update()
        self.search_query = e.control.value.lower()
        self.current_page = 1
        self.page.run_task(self.api_data)

    def build(self):
        self.trucktiles.controls = self.all_truck_tiles

    def did_mount(self):
        self.page.run_task(self.api_data)
        
    async def api_data(self):
        token = await self.page.client_storage.get_async("token")
        api_response = await get_data(f"api/truck/?page={self.current_page}&limit={self.limit}&search={self.search_query}", token if token else None)
        print(f"Data API: {api_response}")
        self.all_truck_tiles.clear()
        
        if api_response.get('status') == 200:
            api_data = api_response.get('data', [])
            self.total_pages = api_response.get('total_pages', 1)
            self.update_pagination()
            for item in api_data:
                truck_id = item.get('truck_id')
                material = item.get('material')
                rom = item.get('rom')
                weight_net = item.get('weight_net')
                checkin = item.get('checkin')
                km_67 = item.get('km_67')
                km_36 = item.get('km_36')
                wb_35 = item.get('wb_35')
                km_29 = item.get('km_29')
                wb_28 = item.get('wb_28')
                km_02 = item.get('km_02')
                km_00 = item.get('km_00')
                closing = item.get('closing')

                truck_tile = TruckTile(
                    truck_name=rom,
                    material=material,
                    weight=weight_net,
                    truck_id=truck_id,
                    data_times={
                        "Check-in": checkin,
                        "KM67": km_67,
                        "KM36": km_36,
                        "WB35": wb_35,
                        "KM29": km_29,
                        "WB28": wb_28,
                        "KM02": km_02,
                        "KM00": km_00,
                        "Closing": closing,
                    }
                )
                self.all_truck_tiles.append(truck_tile)
            self.build()
            self.update()
            self.page.update()
        else:
            snackbar = ft.SnackBar(
                content=ft.Text("Pengguna Tidak Valid"),
                action="OK",
                bgcolor=ft.colors.RED
            )
            self.page.overlay.append(snackbar)
            self.page.update()
            print("Error: Data API tidak ditemukan atau status bukan 200.")
    
    def prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.page.run_task(self.api_data)
            self.update_pagination()

    def next_page(self, e):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.page.run_task(self.api_data)
            self.update_pagination()

    def update_pagination(self):
        self.pagination_text.value = f"Page {self.current_page} of {self.total_pages}"
        self.pagination_text.update()  
        self.pagination.update()
        
    def refresh(self, e):
        self.page.run_task(self.api_data)