import flet as ft 
from .controls import *

class KC_Terminal:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                thickness=2,radius=10
            )
        )
        self.cover_button = ft.Column(
            [
                ft.Text("Test", color="white", text_align=ft.TextAlign.CENTER),
                # ft.OutlinedButton(
                #     "Login",
                #     ft.icons.LOGIN,
                    
                # )
            ], alignment=ft.MainAxisAlignment.CENTER
        )
        self.cover = ft.Stack(
            [
                    ft.Image(
                        src=f"https://picsum.photos/400/400?1",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        expand=True,
                        width=1000
                    ),
                    self.cover_button
                    
                ], alignment= ft.alignment.center, expand=True, width=1000
        )
        self.pop_up_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(icon=ft.icons.BUSINESS_CENTER, text="Kelanis Coal Terminal"),
                ft.PopupMenuItem(icon=ft.icons.FIRE_TRUCK, text="Hauling Tracking System"),
            ], on_select= lambda e: self.on_nav_change(e)
        )
        self.data = ""
        self.navigationbar =  ft.NavigationBar(bgcolor="white",indicator_color="teal200", shadow_color='white',overlay_color='teal300',surface_tint_color='white',
                    destinations=[
                        ft.NavigationBarDestination("AMIVEN", ft.Icon("EXPLORE",color='teal200'),selected_icon=ft.Icon("EXPLORE",color='white')),
                        ft.NavigationBarDestination("HTS", ft.Icon("EXPLORE",color='teal200'),selected_icon=ft.Icon("EXPLORE",color='white')),
                        ft.NavigationBarDestination("KCT", ft.Icon("EXPLORE",color='teal200'),selected_icon=ft.Icon("EXPLORE",color='white')),
                    ],on_change=self.on_nav_change, visible=False
                )
        
        self.adalogo = ft.Image("images/logo1.png", height=50)
        self.header = ft.Row(
            [
                self.adalogo,
                self.pop_up_menu
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= ft.VerticalAlignment.CENTER
        )
        
        self.mainpage = mainPage.MainPage()
        self.kct_page = kctPage.KCTPage()
        self.hts_page = htsPage.HTSPage()
        
        self.switcher = ft.AnimatedSwitcher(
            self.mainpage, transition=ft.AnimatedSwitcherTransition.SCALE, duration=500, reverse_duration=100, switch_in_curve=ft.AnimationCurve.BOUNCE_OUT, switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )

        self.view = ft.View(
            "/kct",
            [   
                self.header,
                self.cover,
                self.switcher
                
            ] , bottom_appbar=self.navigationbar  ,bgcolor= 'white',scroll=ft.ScrollMode.ADAPTIVE
        )
        
    def get_view(self):
        self.page.update()
        return self.view
    
    
   
    def on_nav_change(self, e):
        if e.control.selected_index == 0:
            self.switcher.content = self.mainpage
        elif e.control.selected_index == 1:
            self.switcher.content = self.hts_page
        elif e.control.selected_index == 2:
            self.switcher.content = self.kct_page
        self.page.update()