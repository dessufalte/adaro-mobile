import flet as ft 
from .controls import *
import socket, httpx
class HomeScreen(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
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
        
        self.side_bar = ft.NavigationDrawer(
            on_change= self.on_nav_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Home",
                    icon=ft.icons.HOUSE_OUTLINED,
                    selected_icon=ft.icons.HOUSE,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.FIRE_TRUCK_OUTLINED,
                    label="Hauling Tracking ",
                    selected_icon=ft.icons.FIRE_TRUCK,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.MAP_OUTLINED,
                    label="Terminal Map",
                    selected_icon=ft.icons.MAP,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.STORAGE_OUTLINED,
                    label="Stock Pile Information",
                    selected_icon=ft.icons.STORAGE,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.TIMELAPSE_OUTLINED,
                    label="Delay Chart Problem",
                    selected_icon=ft.icons.TIMELAPSE,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.NEWSPAPER_OUTLINED,
                    label="News",
                    selected_icon=ft.icons.NEWSPAPER,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    label="Settings",
                    selected_icon=ft.icons.SETTINGS,
                ),
            ],
            
            
        )
        self.pop_up_menu = ft.IconButton(
            ft.icons.MENU, on_click=lambda e: self.page.open(self.side_bar)
        )
        
        self.danger = ft.IconButton(
            ft.icons.SOS_ROUNDED, icon_color='red500',
            on_click=self.on_sos
        )
        self.data = ""
        self.log_row = ft.Row(
            [
                self.pop_up_menu,
                self.danger
            ]
        )
        self.adalogo = ft.Image("images/logo1.png", height=50)
        self.header = ft.Row(
            [
                self.log_row,
                self.adalogo,
            ],
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= ft.VerticalAlignment.CENTER,
            
        )
        self.error_text = ft.Text("", color="red")
        self.input_field = ft.CupertinoTextField("Type 'SOS'", autofocus=True)
        self.input_reason = ft.CupertinoTextField("Type reasons of emergency...", autofocus=True)
        self.emergency_reason = "SOS"
        self.latitude = None
        self.longitude = None
        
        self.dialog = ft.CupertinoAlertDialog(
            modal=True,
            title=ft.Text("Emergency Confirmation"),
            content=ft.Column(
                [
                    self.input_field,
                    self.error_text
                ]
            ),
            actions=[
                ft.CupertinoDialogAction(
                    "Submit",
                    is_destructive_action=True,
                    on_click=self.submit_sos
                ),
                ft.CupertinoDialogAction(
                    "Cancel",
                    is_destructive_action=True,
                    on_click=self.close_sos_dialog
                )
            ]
        )
        
        self.reason = ft.CupertinoAlertDialog(
            modal=True,
            title=ft.Text("Emergency Confirmation"),
            content=ft.Column(
                [
                    self.input_reason,
                    ft.Text("This message will announce on public server."),
                    self.error_text
                ]
            ),
            actions=[
                ft.CupertinoDialogAction(
                    "Next",
                    is_destructive_action=True,
                    on_click=self.collect_reasons
                ),
                ft.CupertinoDialogAction(
                    "Cancel",
                    is_destructive_action=True,
                    on_click=self.close_sos_reason
                )
            ]
        )
        
        self.mainpage = mainPage.MainPage(page=page)
        self.kct_page = kctPage.KCTPage()
        self.hts_page = htsPage.HTSPage(page=page)
        self.delay_page = delaychartPage.DelayChartPage()
        self.stock_page = stockpilePage.StockpilePage(page=page)
        self.terminal_page = terminalmapPage.TerminalMapPage(page=page, hsm=self)
        self.emergency_page = emergencyPage.Emergency()
        self.settings_page = settingsPage.SettingsPage(page=page)
        self.news_page = newsPage.NewsPage(page=page)
        
        self.switcher = ft.AnimatedSwitcher(
            self.mainpage , transition=ft.AnimatedSwitcherTransition.FADE, duration=500, reverse_duration=100, switch_in_curve=ft.AnimationCurve.EASE_IN, switch_out_curve=ft.AnimationCurve.EASE_OUT,
        )

        self.main_col = ft.Column([self.switcher], scroll=ft.ScrollMode.AUTO, expand=True)
        self.geolocator = ft.Geolocator(
            location_settings=ft.GeolocatorSettings(
                accuracy=ft.GeolocatorPositionAccuracy.HIGH
            ),
            on_position_change=self.handle_position_change,
            on_error=lambda e: print(f"Geolocator Error: {e.data}"),
        )
        

        self.safe_area = ft.SafeArea(
            ft.Column(
                [
                    self.header,
                    self.main_col
                ]
            ), expand=True
        )
        
        self.view = ft.View(
            "/",
            [   
                self.safe_area,
                
            ]  ,bgcolor= 'white', drawer=self.side_bar
        )
        self.page.overlay.append(self.geolocator)
        self.page.update()
    def get_view(self):
        self.page.update()
        return self.view
   
    def on_nav_change(self, e):
        print("test")
        if e.control.selected_index == 0:  
            self.page.go("/")
            self.page.close(self.side_bar)
        elif e.control.selected_index == 1:
            self.page.go("/hts")
            self.page.close(self.side_bar)
        elif e.control.selected_index == 2:
            self.page.go("/terminal")
            self.page.close(self.side_bar)
        elif e.control.selected_index == 3:
            self.page.go("/stockpile")
            self.page.close(self.side_bar)
        elif e.control.selected_index == 4:
            self.page.go("/delay")
            self.page.close(self.side_bar)
        elif e.control.selected_index == 5:
            self.page.go("/news")
            self.page.close(self.side_bar)      
        elif e.control.selected_index == 6:
            self.page.go("/settings")
            self.page.close(self.side_bar)           
        self.page.update()
        
    def on_sos(self, e):
        # print("test")
        
        self.page.open(self.reason)
        self.page.update()

    def close_sos_dialog(self, e):
        self.page.close(self.dialog)
        self.page.update()            
    
    def close_sos_reason(self, e):
        self.page.close(self.reason)
        self.page.update()      
    
    def submit_sos(self, e):
        if self.input_field.value.strip().lower() == "sos":
            self.page.snack_bar = ft.SnackBar(ft.Text("SOS Confirmed! Emergency activated!"))
            self.error_text.value = ""
            self.page.close(self.dialog)
            self.page.snack_bar.open = True
            self.page.launch_url('tel: 08001237911')
            try:
                response = httpx.get("https://api.ipify.org?format=json")
                public_ip = response.json().get("ip")
                
            except Exception as ex:
                print(f"Error mendapatkan IP publik: {ex}")
                
            data = {
                "latitude": self.latitude,
                "longitude": self.longitude,  
                "ip_address": public_ip, 
                "reason": self.emergency_reason,
            }
            try:
                response = httpx.post("http://localhost:8000/api/hazard/emergency", json=data)
                if response.status_code == 200:
                    print("SOS berhasil dikirim!")
            except Exception as ex:
                print(ex)
        else:
            self.error_text.value = "Incorrect input. Please type 'SOS'."
            self.page.snack_bar = ft.SnackBar(ft.Text("SOS Failed to Confirm"))
            self.page.snack_bar.open = True
        self.page.update()
            
    def collect_reasons(self, e):
        if self.input_reason.value:
            self.emergency_reason = self.input_reason.value
            self.error_text.value = ""
            self.page.open(self.dialog)
            self.page.close(self.reason)
            self.page.update()
        else:
            self.error_text.value = "Invalid reason"
            self.page.update()
            
    def handle_position_change(self, e):
        # print(f"Change{e.latitude}, {e.longitude}")
        self.latitude = e.latitude
        self.longitude = e.longitude
        if self.emergency_page.loaded :
            self.emergency_page.update_user_location(e.latitude, e.longitude)
            self.page.update()


        # geolocator.request_permission_async()
        
    
    # async def listen_to_server(self):
    #     try:
    #         async with websockets.connect("ws://127.0.0.1:8000/ws/hazard") as websocket:
    #             while True:
    #                 print("Listening for WebSocket messages...")
    #                 message = await websocket.recv()
    #                 if message:
    #                     print(f"Message received: {message}")
    #                     # Perbarui konten sesuai kebutuhan
    #                     self.switcher.content = self.emergency_page
    #                     self.page.update()
    #     except Exception as e:
    #         print(f"WebSocket error: {e}")
