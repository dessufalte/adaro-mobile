import flet as ft
from .utils import fetch
from .datepicker import DateRangePicker
from .piechart import create_pie_chart, ProgressBarWidget, HorizontalChart
import asyncio
import datetime
from .diagram import conveyors, MapDiagram, ships, hoppers, stockpiles, transfer_item_test, ItemConvey, ways, get_random_way
import time
import random

class KCTPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.data
        self.data_api = ft.Text("Kosong")
        self.shadowdef = ft.BoxShadow(0.1, 1.4, 'grey')
        self.borderRadTop = ft.BorderRadius(15,15,0,0)
        self.borderAll = ft.BorderRadius(15,15,15,15)
        self.api_button = ft.ElevatedButton("Test API",on_click= lambda e: self.get_api())
        self.border = ft.BorderSide(1,'grey')
        self.border_super = ft.Border(self.border, self.border, self.border, self.border)
        
        
        self.canvas = MapDiagram(800, 200)
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas_container = ft.Container(self.canvas, alignment=ft.alignment.center, expand=True)
        
        self.start_date = None
        self.end_date = None
        
        self.delay_data = ["Test1", "Test2"]
        self.delay_val = [1,2]
        
        self.data_num = [5, 6.5, 5, 7.5, 3, 8, 6, 4, 4, 3]
        self.labels = ["StandBy", "Changing Barge", "Metal Detector", "Waiting Coal", "Changing Barge", "Metal Detector", "Waiting Coal", "Changing Barge", "Metal Detector", "Waiting Coal"]
        
        self.horizontal_chart = HorizontalChart()
        self.horizontal_chart2 = HorizontalChart()
        
        # self.stockpileloads_L1 = {
        #     "L1": ProgressBarWidget(200,1000, '17T', '20T', 'L1:'),
        #     "L2": ProgressBarWidget(570,1000, '17T', '20T', 'L2:', False),
        #     "L3": ProgressBarWidget(570,1000, '17T', '20T', 'L3:', False)
        # }
        
        # self.stockpileloads_L2 = {
        #     "L16": ProgressBarWidget(200,1000, '17T', '20T', 'L16:'),
        #     "L17": ProgressBarWidget(570,1000, '17T', '20T', 'L17:', False),
        #     "L18": ProgressBarWidget(570,1000, '17T', '20T', 'L18:', False),
        #     "L8/L9": ProgressBarWidget(570,1000, '17T', '20T', 'L8/L9:', False),
        #     "L21": ProgressBarWidget(570,1000, '17T', '20T', 'L21:', False),
        # }
        self.hopper =  ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("Hopper Status", color='white')
                            ]
                        ),bgcolor='teal500', padding=10, border_radius=self.borderRadTop
                        ),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Stack([
                                    ft.InteractiveViewer(self.canvas_container, expand=True),
                                    ft.ElevatedButton("Test", on_click=lambda e: self.update_map(e))
                                ]
                                ) ,
                                
                            ]
                        ), padding=10
                    ),
                ]
            ), bgcolor='white', border_radius=self.borderAll, border=ft.border.all(1,'teal500')
        )
        self.Indicator =  ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("Data Export"),
                            ]
                        ), padding=10
                    ),
                ]
            ), bgcolor='white', border_radius=self.borderAll, border=ft.border.all(1,'teal500')
        )
        # self.stockpile =  ft.Container(
        #     ft.Column(
        #         [
        #             ft.Container(
        #                 ft.Row(
        #                     [
        #                         ft.Text("  Stockpile Information", color='white'),
        #                         ft.IconButton(ft.icons.CALENDAR_MONTH, icon_color='white',splash_color='teal100', scale=0.8)
                                
        #                     ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        #                 ),bgcolor='teal500', padding=5, border_radius=self.borderRadTop
        #                 ),
        #             ft.Container(
        #                 ft.Column(
        #                     [
        #                         ft.Container(
        #                             ft.Row([ ft.Text("K1", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
        #                             ,padding=5 , bgcolor='teal500'),
                                
        #                         ft.SegmentedButton(
        #                             allow_multiple_selection=True,
        #                             allow_empty_selection=False,
        #                             selected={"L1"},
        #                             segments=[
        #                                 ft.Segment(
        #                                     "L1",
        #                                     label=ft.Text("L1", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L2",
        #                                     label=ft.Text("L2", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L3",
        #                                     label=ft.Text("L3", size=10)
        #                                 ),
        #                             ],
        #                             style= ft.ButtonStyle(color={
        #                                 ft.ControlState.HOVERED: ft.colors.WHITE,
        #                                 ft.ControlState.FOCUSED: ft.colors.BLUE,
        #                                 ft.ControlState.DEFAULT: ft.colors.BLACK,
        #                                 ft.ControlState.SELECTED: 'teal500',
        #                             }) ,  expand=True, width=1000, on_change= self.update_k1load
        #                         ) ,
        #                         *[pb.get_widget() for pb in self.stockpileloads_L1.values()],
        #                         ft.Divider(1,1) , 
        #                         ft.Container(
        #                             ft.Row([ ft.Text("K2", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
        #                             ,padding=5 , bgcolor='teal500'),
        #                         ft.SegmentedButton(
        #                             allow_multiple_selection=True,
        #                             allow_empty_selection=False,
        #                             selected={"L16"},
        #                             segments=[
        #                                 ft.Segment(
        #                                     "L16",
        #                                     label=ft.Text("L16", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L17",
        #                                     label=ft.Text("L17", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L18",
        #                                     label=ft.Text("L18", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L8/L9",
        #                                     label=ft.Text("L8/L9", size=10)
        #                                 ),
        #                                 ft.Segment(
        #                                     "L21",
        #                                     label=ft.Text("L21", size=10)
        #                                 ),
        #                             ],
        #                             style= ft.ButtonStyle(color={
        #                                 ft.ControlState.HOVERED: ft.colors.WHITE,
        #                                 ft.ControlState.FOCUSED: ft.colors.BLUE,
        #                                 ft.ControlState.DEFAULT: ft.colors.BLACK,
        #                                 ft.ControlState.SELECTED: 'teal500',
        #                             }) ,  expand=True, width=1000, on_change=self.update_k2load
        #                         ) ,
        #                         *[pb.get_widget() for pb in self.stockpileloads_L2.values()],
        #                     ]
        #                 ), padding=10
        #             ),
        #         ]
        #     ), bgcolor='white', border_radius=self.borderAll, border=ft.border.all(1,'teal500')
        # )
        self.delay_chart = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Delay Chart Problems", color='white'),
                                ft.IconButton(ft.icons.CALENDAR_MONTH, icon_color='white',splash_color='teal100', scale=0.8,on_click= lambda e: self.date_picker.pick_date_range)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ), bgcolor='teal500', padding=5, border_radius=self.borderRadTop
                    ),
                    ft.Container(
                        ft.Column(
                            [
                               ft.Container(
                                    ft.Row([ ft.Text("Delay Problem", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
                                    ,padding=5 , bgcolor='teal500'),
                               self.horizontal_chart,
                               ft.Container(
                                    ft.Row([ ft.Text("Delay Problem", size=10, color='white', weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)], alignment=ft.alignment.center)
                                    ,padding=5 , bgcolor='teal500'),
                               self.horizontal_chart2
                            ]
                        ), padding= 10
                    ),
                    
                ]
            ),  bgcolor='white', border_radius=self.borderAll, border=ft.border.all(1,'teal500')
        )
      
        self.main = ft.Column([self.hopper, self.delay_chart , self.Indicator],scroll=ft.ScrollMode.ADAPTIVE)
        self.controls = [
            self.main
        ]
    def build(self):
        return self.main
    
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
        
    def update_map(self, e):
        self.local_item_test()
    
    def local_transfer(self, itemc: ItemConvey,):
        itemc.activate_way()
        h_name = itemc.get_hopper_name(ways)
        hoppers[h_name].activate()
        self.canvas.clean()
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas.update()
        time.sleep(2)
        hoppers[h_name].deactivate()
        itemc.deactivate_way()
        self.canvas.clean()
        self.canvas.create_map(conveyors, hoppers, stockpiles, ships)
        self.canvas.update()
        
    def local_item_test(self):
        for _ in range(1):  # Misalnya kita ingin mengirim 5 item
            
            destination, way = get_random_way()  # Dapatkan 
            item = ItemConvey(
                amount=random.randint(1, 20),
                destination=destination,
                ways=way 
            )
            self.local_transfer(itemc=item)
            time.sleep(0.1)
        
    
    def get_api(self):
        fetch.test_dotenv()
        self.data = asyncio.run(fetch.get_data())
        self.data_api.value = self.data["message"]
        self.data_api.update()
        self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Berhasil mengambil data"),
                    open=True,
                )
        self.update()
    
