import flet as ft

class SettingsPage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.setting_board = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Settings ", color='black', size=20, weight=ft.FontWeight.W_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ),
                    ft.Divider(height=1),
                ]
            ), bgcolor='white'
        )
        self.main = ft.Column([
            self.setting_board,
            ft.Column(
                [
                    ft.Container(
                        ft.Column(
                        [
                            ft.ListTile(title=ft.Text("Appearance", weight=ft.FontWeight.W_500, color='black')),
                            ft.ListTile(
                                title=ft.Text("Dark mode", color='black'),
                                trailing=ft.Switch(inactive_thumb_color='white', inactive_track_color='grey300', active_color='teal400'),
                            ),
                            ft.ListTile(
                                title=ft.Text("Language ", color='black'),
                                trailing=ft.SegmentedButton(
                                    allow_multiple_selection=False,
                                    allow_empty_selection=False,
                                    selected={"EN"},
                                    segments=[
                                        ft.Segment(
                                            "EN",
                                            label=ft.Text("EN", size=10)
                                        ),
                                        ft.Segment(
                                            "ID",
                                            label=ft.Text("ID", size=10)
                                        ),
                                    ] ,  expand=True,
                                    style= ft.ButtonStyle(color={
                                        ft.ControlState.HOVERED: ft.colors.GREY_300,
                                        ft.ControlState.FOCUSED: ft.colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.colors.GREY_500,
                                        ft.ControlState.SELECTED: 'white',
                                    }, bgcolor={
                                        ft.ControlState.HOVERED: ft.colors.WHITE,
                                        ft.ControlState.FOCUSED: ft.colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.colors.WHITE,
                                        ft.ControlState.SELECTED: 'teal500',
                                    }
                                    )
                                ) ,
                            ),
                            
                        ],
                    spacing=0,
                ),
                    ),
                    ft.ListTile(title=ft.Text("Data", weight=ft.FontWeight.W_500, color='black')),
                    ft.ListTile(
                        title=ft.Text("Export Data", color='black'),
                        trailing=ft.IconButton(ft.icons.SAVE_ALT, icon_color='teal500')
                    ),
                    ft.ListTile(title=ft.Text("User", weight=ft.FontWeight.W_500, color='black')),
                    ft.ListTile(
                        title=ft.Text("Log out", color='black'),
                        trailing=ft.IconButton(ft.icons.LOGOUT, icon_color='teal500', on_click=self.logout)
                    ),
                ]
            )        
        ],scroll=ft.ScrollMode.ADAPTIVE)
        self.controls = [
            self.main
        ]

    def logout(self, e):
        self.page.client_storage.clear()
        self.page.go('/login')