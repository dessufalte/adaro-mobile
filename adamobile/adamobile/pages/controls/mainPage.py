import flet as ft
from datetime import datetime

class Widget(ft.Container):
    def __init__(self, content: ft.Control,page: ft.Page ,txt: str, rot:str, exp = True, wdth = 150):
        super().__init__()
        self.page = page
        self.expand = exp
        self.width = wdth
        self.bgcolor = 'grey200'
        self.height = 150
        self.rot = rot
        self.border_radius = 10
        self.content = ft.Column(
            [
                content,
                ft.Row(
                    [
                        ft.Text(txt, color='grey800', weight=ft.FontWeight.W_600),
                        ft.IconButton(ft.icons.ARROW_FORWARD, on_click=self.go_to)
                    ], alignment=ft.MainAxisAlignment.END
                )
            ], alignment=ft.MainAxisAlignment.END
        )
    def go_to(self, e):
        self.page.go(self.rot)
        

class MainPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.rand_img = ft.Image(
                        src=f"https://picsum.photos/800/200?1",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        expand=True,
                        width=800,
                        height=200,
                    )
        self.cover_button = ft.Column(
            [
                ft.Text(
                    value=str(datetime.utcnow().strftime("%H:%M")),
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                    size=40,
                    weight=ft.FontWeight.W_700
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.cover = ft.Stack(
            [
                    ft.Image(
                        src=f"/images/pit.jpeg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=400,
                    ),
                    self.cover_button
                    
                ], alignment= ft.alignment.center, expand=True, width=1000
        )

        self.main = ft.Column([
            self.cover,
            ft.Container(
                content=ft.Row(
                    [
                        Widget(ft.Image(
                        src=f"/images/tru.jpg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=200,
                    ), txt="Hauling Tracking", page=page, rot='/hts'),
                        Widget(ft.Image(
                        src=f"images/map.jpg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=200,
                    ), txt="Terminal Map", page=page, rot='/terminal'),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center, 
            ),
            ft.Container(
                content=ft.Row(
                    [
                        Widget(ft.Image(
                        src=f"images/dum.jpg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=200,
                    ), txt="Stockpile", page=page, rot='/stockpile'),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                alignment=ft.alignment.center, 
            ),
            ft.Container(
                content=ft.Row(
                    [
                        Widget(ft.Image(
                        src=f"images/kel.jpg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=200,
                    ), txt="Delay", page=page, rot='/delay'),
                        Widget(ft.Image(
                        src=f"images/mesh.jpeg",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=800,
                        height=200,
                    ), txt="Setting", exp=False, page=page, rot='/settings'),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                alignment=ft.alignment.center, 
            )                        
        ],scroll=ft.ScrollMode.ADAPTIVE)
        self.controls = [
            self.main
        ]