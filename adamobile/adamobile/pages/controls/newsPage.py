import flet as ft
import datetime
from .utils.fetch import get_data

class EmergencyTile(ft.ExpansionTile):
    def __init__(
        self,
        latitude,
        longitude,
        reason,
        ip_address,
        data_times,
        initially_expanded: bool = False,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.RED_300,
        **kwargs
    ):

        super().__init__(
            title=ft.Text(f"{reason}", weight=ft.FontWeight.BOLD),
            subtitle=ft.Text(data_times),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=initially_expanded,
            collapsed_text_color=collapsed_text_color,
            text_color=text_color,
            **kwargs
        )

        self.trailing = ft.Icon(ft.icons.WARNING, color='white')
        self.date = data_times
        self.collapsed_bgcolor = 'red300'
        self.bgcolor = 'white'
        self.icon_color = 'red300'
        self.reason = reason
        self.latitude = latitude
        self.longitude = longitude
        self.ip_address = ip_address
        self.data_times = data_times
        
        self.collapsed_icon_color = 'white'
        
    def build(self):
        self.controls = [
            ft.Column(
                [
                    ft.Text(f"Latitude : {self.latitude}", color='black', text_align=ft.TextAlign.LEFT),
                    ft.Text(f"Longitude : {self.longitude}", color='black'),
                    ft.Text(f"Reason : {self.reason}", color='black'),
                    ft.Text(f"Time : {self.data_times}", color='black'),
                ]
            )
        ]
        
class CardNews(ft.Container):
    def __init__(self,title ,time , text):
        super().__init__()
        self.bgcolor = 'grey200'
        self.expand = True
        self.border_radius = 10
        self.border = ft.border.all(1, 'grey300')
        self.padding = 10
        self.title = title
        self.time = time
        self.text = text
        self.content = (
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(self.title, color='black', size=20, weight= ft.FontWeight.BOLD),
                            ft.Text(self.text, color='grey600', max_lines=2, width=340, overflow=ft.TextOverflow.FADE),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(self.time, color='grey500'),
                                            ft.Icon(ft.icons.PUNCH_CLOCK, size=14, color='grey500'),
                                        ], alignment=ft.MainAxisAlignment.START
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("Selengkapnya ", color='grey500'),
                                            ft.IconButton(ft.icons.ARROW_FORWARD_IOS, icon_color='grey500', icon_size=14)
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                            )
                        ]
                    )
                ]
            )
        )
    
        
class NewsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.hazard_data: list[EmergencyTile] = []
        
        self.news_board = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  News & Information ", color='black', size=20, weight=ft.FontWeight.W_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ),
                    ft.Divider(height=1),
                ]
            ), bgcolor='white'
        )
        self.col_haz = ft.Column()
        self.main = ft.Column([
            self.news_board,   
            ft.Column(
                [
                    ft.Stack(
                        [
                            
                            ft.Image(
                                src=f"images/adr.jpg",
                                fit=ft.ImageFit.COVER,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                                expand=True,
                                width=800,
                                height=200,
                            ),
                            ft.Row(
                                [
                                    ft.Text('Berita', color='white', size=20, text_align=ft.TextAlign.CENTER),
                                    ft.IconButton(ft.icons.ARROW_FORWARD, icon_color='white',icon_size=20)
                                ], bottom=10, left=10
                            )
                        ]
                    ),
                    ft.Column(
                        [
                            CardNews(text="lorem ipsum lorem ipsum lorem  ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem", title='Berita 1', time='06:50'),
                            CardNews(text="lorem ipsum lorem ipsum lorem  ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem", title='Berita 2', time='06:50'),
                            CardNews(text="lorem ipsum lorem ipsum lorem  ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem", title='Berita 3', time='06:50'),
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Text("Hazard Info", color='red500', weight=ft.FontWeight.W_500, size=20),
                            ft.Divider(height=1, color='red500'),
                        ]
                    ),
                    self.col_haz,
                    ft.Row(
                        [
                            ft.CupertinoFilledButton("Hazard Map", icon=ft.icons.WARNING, expand=True, on_click=self.to_map)      
                        ]
                    )
                    
                ]
            ),
              
        ],scroll=ft.ScrollMode.ADAPTIVE)
        self.controls = [
            self.main
        ]

    def to_map(self, e):
        self.page.go('/emergency')
        
    def did_mount(self):
        self.col_haz.controls.clear()
        self.hazard_data.clear()
        self.page.run_task(self.api_data)
    
    async def api_data(self):
        api_data = await get_data("api/hazard/emergency/latest")
        print(f"Data API: {api_data}")
        if api_data:
            for item in api_data:
                longt = item['longitude']
                latitude = item['latitude']
                ipaddr = item['ip_address']
                reason = item['reason']
                tmstmp = item['timestamp']
                self.col_haz.controls.append(EmergencyTile(latitude, longt, reason, ipaddr, tmstmp))
                
        self.col_haz.update()
        self.update()