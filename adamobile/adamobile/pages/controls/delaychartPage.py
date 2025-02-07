import flet as ft
from .piechart import HorizontalChart
from .diagram import MapDiagram, conveyors, ships, stockpiles, hoppers
import copy
from .utils.fetch import get_data
import datetime


def get_delay_union(data):
    temp_union = {}

    for category in data.values():
        for label, freq, lost in zip(category["labels"], category["frequency"], category["losttime"]):
            if label not in temp_union:
                temp_union[label] = {"frequency": freq, "losttime": lost}
            else:
                temp_union[label]["frequency"] += freq
                temp_union[label]["losttime"] += lost

    union_data = {
        "frequency": [value["frequency"] for value in temp_union.values()],
        "losttime": [value["losttime"] for value in temp_union.values()],
        "labels": list(temp_union.keys())
    }

    return union_data


hoppers_delay = copy.deepcopy(hoppers)

class DelayChartPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.borderRadTop = ft.BorderRadius(15,15,0,0)
        self.borderAll = ft.BorderRadius(15,15,15,15)
        self.border = ft.BorderSide(1,'grey')
        self.border_super = ft.Border(self.border, self.border, self.border, self.border)
        
        self.delay_data = {}
        self.delay_union = {}
        
        self.map_viewer = MapDiagram(300, 200)
        self.map_viewer.create_map(conveyors, hoppers_delay, stockpiles, ships)
        
        self.from_date_viewer = ft.TextField(disabled=True, expand=True)
        self.to_date_viewer = ft.TextField(disabled=True, expand=True)
        
        self.from_date = datetime.datetime.utcnow()
        self.to_date = None
        
        self.date_picker_start = ft.DatePicker(
            open=True,
            on_change=self.confirm_start_date,
            
        )
        self.date_picker_end = ft.DatePicker(
            open=True,
            on_change=self.confirm_end_date
        )
        
        self.list_hoppers = [ft.dropdown.Option("ALL")] + [ft.dropdown.Option(key) for key in hoppers_delay.keys()]
        self.dropdown_lines = ft.Dropdown(
            options= self.list_hoppers,
            value="ALL",
            on_change=self.drop_down
        )
        
        self.chart_data = {
            "L1": HorizontalChart(),
            "L2": HorizontalChart(visible=False),
        }
        
        self.delay_chart = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text("  Delay Chart Problem ", color='black', size= 20 , weight= ft.FontWeight.W_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ), 
                    ),
                    ft.Divider(height=1) ,
                    ft.Container(
                        ft.Column(
                            [
                                ft.Container(
                                    ft.Row(
                                        [
                                            ft.Text("Test", font_family='consolas', color='black')
                                        ]    
                                    ),
                                    bgcolor='grey200', padding=10
                                )
                            ]
                        ), padding= 10
                    ),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("From : "),
                                        self.from_date_viewer,
                                        ft.Text("To : "),
                                        self.to_date_viewer,
                                        ft.IconButton(ft.icons.DATE_RANGE, on_click=self.get_date_time)
                                    ]
                                ),
                            ]
                        )
                    ),
                    ft.Divider(height=1) ,
                    ft.Container(
                        self.map_viewer, padding= 10, expand=True
                    ),
                    self.dropdown_lines,
                    ft.Row(
                        [
                            ft.SegmentedButton(
                                    allow_multiple_selection=True,
                                    allow_empty_selection=False,
                                    selected={"L1"},
                                    segments=[
                                        ft.Segment(
                                            "L1",
                                            label=ft.Text("Sum of LostTime", size=10)
                                        ),
                                        ft.Segment(
                                            "L2",
                                            label=ft.Text("Count of Frequency", size=10)
                                        ),
                                    ],
                                    style= ft.ButtonStyle(color={
                                        ft.ControlState.HOVERED: ft.colors.WHITE,
                                        ft.ControlState.FOCUSED: ft.colors.BLUE,
                                        ft.ControlState.DEFAULT: ft.colors.BLACK,
                                        ft.ControlState.SELECTED: 'teal500',
                                    }) ,  expand=True, width=1000, on_change= self.update_chart
                                ) ,
                        ]
                    ),
                    self.chart_data["L1"],
                    self.chart_data["L2"],
                    
                ]
            ),  bgcolor='white'
        )
        self.main = ft.Column([self.delay_chart])
        
        self.expand = True
    

    def get_date_time(self, e):
        self.page.open(self.date_picker_start)
        
    def confirm_start_date(self, e):
        if self.date_picker_start.value:
            self.from_date = self.date_picker_start.value
            self.from_date_viewer.value = self.from_date
            self.update()
            self.page.close(self.date_picker_start)
            self.page.open(self.date_picker_end)
    
    def confirm_end_date(self, e):
        if self.date_picker_end.value:
            self.to_date = self.date_picker_end.value
            self.to_date_viewer.value = self.to_date
            self.page.close(self.date_picker_end)
            self.page.run_task(self.api_data)
            self.dropdown_lines.value = "ALL"
            for conveyor in hoppers_delay.values():
                conveyor.highlight()
            self.chart_data["L1"].setData(f"Sum of Lost Time", self.delay_union["losttime"], self.delay_union["labels"])
            self.chart_data["L2"].setData(f"Count of Frequency", self.delay_union["frequency"], self.delay_union["labels"])
            self.chart_data["L1"].build()
            self.chart_data["L2"].build() 
            self.map_viewer.clean()
            self.map_viewer.create_map(conveyors, hoppers_delay, stockpiles, ships)
            self.update()

    def drop_down(self, e):
        # self.page.run_task(self.api_data)
        if e.control.value == "ALL":
            for conveyor in hoppers_delay.values():
                conveyor.highlight()
            self.chart_data["L1"].setData(f"Sum of Lost Time", self.delay_union["losttime"], self.delay_union["labels"])
            self.chart_data["L2"].setData(f"Count of Frequency", self.delay_union["frequency"], self.delay_union["labels"])
            
        else:
            hoppers_delay[e.control.value].highlight()
            for key, hopper in hoppers_delay.items():
                if key != e.control.value:
                    hopper.deactivate()
            if e.control.value in self.delay_data:
                print(self.delay_data["H1"])
                self.chart_data["L1"].setData(f"Sum of Lost Time ({e.control.value})", self.delay_data[e.control.value]["losttime"], self.delay_data[e.control.value]["labels"])
                self.chart_data["L2"].setData(f"Count of Frequency ({e.control.value})", self.delay_data[e.control.value]["frequency"], self.delay_data[e.control.value]["labels"])
            else:
                self.chart_data["L1"].setData(f"Sum of Lost Time ({e.control.value})", [], [])
                self.chart_data["L2"].setData(f"Count of Frequency ({e.control.value})", [], [])
        self.chart_data["L1"].build()
        self.chart_data["L2"].build()
        
        self.map_viewer.clean()
        self.map_viewer.create_map(conveyors, hoppers_delay, stockpiles, ships)
        self.update()

    
    def update_chart(self, e):
        selected = e.control.selected
        for key, chart,  in self.chart_data.items():
            if key in selected:
                chart.setVisible(True)
            else:
                chart.setVisible(False)
        self.update()
    
    def build(self):
        self.controls = [
            self.main
        ]
        return self.main

    def did_mount(self):
        self.page.run_task(self.api_data)
    
    async def api_data(self):
        token = await self.page.client_storage.get_async("token")
        
        if self.to_date:
            api_response = await get_data(f"api/hopper/delay/get/grouped?start_date={self.from_date.date()}&end_date={self.to_date.date()}", token if token else None)
        else:
            api_response = await get_data(f"api/hopper/delay/get/grouped?start_date={self.from_date.date()}", token if token else None)
        # print(f"Data API: {api_response}")
        self.delay_data.clear()
        if api_response.get('status') == 200:
            api_data = api_response.get('data')
            if api_data:
                for hopper, data in api_data.items():
                    # print(f"{hopper}:")
                    # print(f"  Frequency: {data['frequency']}")
                    # print(f"  Losttime: {data['losttime']}")
                    # print(f"  Labels: {data['labels']}")
                    if hopper not in self.delay_data:
                        self.delay_data[hopper] = {
                            "frequency": data['frequency'],
                            "losttime": data['losttime'],
                            "labels": data['labels']
                        }

            print(f"Updated Delay Data: {self.delay_data}")
            self.delay_union = get_delay_union(self.delay_data)
            self.update()

        else:
            print("Error: Data API tidak ditemukan atau status bukan 200.")
