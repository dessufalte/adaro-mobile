import flet as ft
from .piechart import create_pie_chart, ProgressBarWidget, HorizontalChart
from .utils.fetch import get_data
import datetime



class StockpilePage(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.borderRadTop = ft.BorderRadius(15,15,0,0)
        self.borderAll = ft.BorderRadius(15,15,15,15)
        self.border = ft.BorderSide(1,'grey')
        self.border_super = ft.Border(self.border, self.border, self.border, self.border)
        
        self.exist = False
        
        
       
        self.date = datetime.datetime.utcnow().date()
        self.date_viewer = ft.TextField(self.date, disabled=True, expand=True)
        self.date_picker = ft.DatePicker(
            open=True,
            on_change=self.confirm_date,
            
        )


        self.stockpileloads_L1 = {
            "L1": ProgressBarWidget(0,1, '0T', '0T', 'L1:'),
            "L2": ProgressBarWidget(0,1, '0T', '0T', 'L2:'),
            "L3": ProgressBarWidget(0,1, '0T', '0T', 'L3:')
        }
        
        self.stockpileloads_L2 = {
            "L16": ProgressBarWidget(0,1, '0T', '0T', 'L16:'),
            "L17": ProgressBarWidget(0,1, '0T', '0T', 'L17:'),
            "L18": ProgressBarWidget(0,1, '0T', '0T', 'L18:'),
            "L8/L9": ProgressBarWidget(0,1, '0T', '0T', 'L8/L9:'),
            "L21": ProgressBarWidget(0,1, '0T', '0T', 'L21:'),
        }
        
        self.search_form = ft.Container(
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text("Date : "),
                                                    self.date_viewer,
                                                    ft.IconButton(ft.icons.DATE_RANGE, on_click=self.get_date_time)
                                                ]
                                            ),
                                        ]
                                    )
                                )
        self.stockpile =  ft.Column(
                            [
                                ft.Container(
                                    ft.Row([ ft.Text("K1", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
                                    ,padding=5 , bgcolor='teal500'),
                                
                                ft.SegmentedButton(
                                    allow_multiple_selection=True,
                                    allow_empty_selection=False,
                                    selected={"L1"},
                                    segments=[
                                        ft.Segment(
                                            "L1",
                                            label=ft.Text("L1", size=10)
                                        ),
                                        ft.Segment(
                                            "L2",
                                            label=ft.Text("L2", size=10)
                                        ),
                                        ft.Segment(
                                            "L3",
                                            label=ft.Text("L3", size=10)
                                        ),
                                    ],
                                    style= ft.ButtonStyle(color={
                                        ft.ControlState.HOVERED: ft.colors.WHITE,
                                        ft.ControlState.FOCUSED: ft.colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.colors.BLACK,
                                        ft.ControlState.SELECTED: 'teal500',
                                    }) ,  expand=True, width=1000, on_change= self.update_k1load
                                ) ,
                                *[pb for pb in self.stockpileloads_L1.values()],
                                ft.Divider(1,1) , 
                                ft.Container(
                                    ft.Row([ ft.Text("K2", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
                                    ,padding=5 , bgcolor='teal500'),
                                ft.SegmentedButton(
                                    allow_multiple_selection=True,
                                    allow_empty_selection=False,
                                    selected={"L16"},
                                    segments=[
                                        ft.Segment(
                                            "L16",
                                            label=ft.Text("L16", size=10)
                                        ),
                                        ft.Segment(
                                            "L17",
                                            label=ft.Text("L17", size=10)
                                        ),
                                        ft.Segment(
                                            "L18",
                                            label=ft.Text("L18", size=10)
                                        ),
                                        ft.Segment(
                                            "L8/L9",
                                            label=ft.Text("L8/L9", size=10)
                                        ),
                                        ft.Segment(
                                            "L21",
                                            label=ft.Text("L21", size=10)
                                        ),
                                    ],
                                    style= ft.ButtonStyle(color={
                                        ft.ControlState.HOVERED: ft.colors.WHITE,
                                        ft.ControlState.FOCUSED: ft.colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.colors.BLACK,
                                        ft.ControlState.SELECTED: 'teal500',
                                    }) ,  expand=True, width=1000, on_change=self.update_k2load
                                ) ,
                                *[pb for pb in self.stockpileloads_L2.values()],
                            ]
                        )
                  
        self.stockpile_board = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Stockpile Information ", color='black', size= 20 , weight= ft.FontWeight.W_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ), 
                    ),
                    ft.Divider(height=1) ,
                    self.search_form,
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(
                                    ft.Row(
                                        [
                                            ft.Text("Data stockpile berikut diambil pada bulan desember 2024", font_family='consolas', color='black')
                                        ]    
                                    ),
                                    bgcolor='grey200', padding=10
                                ),
                                self.stockpile
                                
                            ]
                        ), padding= 10
                    )
                  
                ]
            ),  bgcolor='white'
        )
        self.main = ft.Column([self.stockpile_board])
        self.expand = True
        self.controls = [
            self.main
        ]

    def did_mount(self):
        self.page.run_task(self.api_data)

    
    
    def update_k1load(self, e):
        selected = e.control.selected
        for key, stockpile,  in self.stockpileloads_L1.items():
            if key in selected:
                stockpile.set_visible(True)
            else:
                stockpile.set_visible(False)
        self.update()
        
    def update_k2load(self, e):
        selected = e.control.selected
        for key, stockpile,  in self.stockpileloads_L2.items():
            if key in selected:
                stockpile.set_visible(True)
            else:
                stockpile.set_visible(False)
        self.update()

    async def api_data(self):
            api_data = await get_data(f"api/stockpile/get/?selected_date={self.date}")
            print(f"Data API: {api_data}")
            if api_data:
                self.exist = True
                for item in api_data:
                    stockpile_name = item['stockpile_name']
                    stock = item['stock']
                    capacity = item['capacity']
                    tdy = item['stock']
                    yst = item['stock_old']
                    
                    if stockpile_name in self.stockpileloads_L1:
                        self.stockpileloads_L1[stockpile_name].set_value(stock, capacity, yst, tdy)

                    elif stockpile_name in self.stockpileloads_L2:
                        self.stockpileloads_L2[stockpile_name].set_value(stock, capacity, yst, tdy)
            else:
                self.exist = False
                
                for stockpile in self.stockpileloads_L1.values():
                    stockpile.set_value(0, 1, 0, 0)
                    stockpile.set_unexisted()
                for stockpile in self.stockpileloads_L2.values():
                    stockpile.set_value(0, 1, 0, 0)
                    stockpile.set_unexisted()
            
            
                
            self.update()

    def get_date_time(self, e):
        self.page.open(self.date_picker)
        
    def confirm_date(self, e):
        if self.date_picker.value:
            self.date = self.date_picker.value
            self.date_viewer.value = self.date
            self.page.run_task(self.api_data)
            self.update()
            self.page.close(self.date_picker)
