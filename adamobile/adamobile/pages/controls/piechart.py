import flet as ft
import matplotlib.pyplot as plt
import math
from flet.matplotlib_chart import MatplotlibChart

def create_pie_chart(labels, values):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5)) 

    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Pie Chart")

    ax2.bar(labels, values, color="tab:blue")
    ax2.set_title("Bar Chart")
    ax2.set_ylabel("Values")
    ax2.set_xlabel("Labels")
    return MatplotlibChart(fig, expand=True)


class HorizontalChart(ft.Container):
    def __init__(self, left_axis_labels=None, visible = True):
        """
        :param data: List of float values for the chart bars.
        :param labels: List of labels corresponding to the bars.
        """
        super().__init__()
        self.data = []
        self.labels = []
        self.title = ""
        self.chart = None
        self.left_axis_labels = left_axis_labels or [str(value) for value in range(len(self.data))]
        self.visible = visible
        
    def setData(self, title,data: list, labels:list):
        self.labels = labels
        self.data = data
        self.title = title
        self.update()
        
    def setVisible(self, visible):
        self.visible = visible
        
        
    def build(self):
        def on_chart_event(e: ft.BarChartEvent):
            for group_index, group in enumerate(self.chart.bar_groups):
                for rod_index, rod in enumerate(group.bar_rods):
                    rod.hovered = e.group_index == group_index and e.rod_index == rod_index
            self.chart.update()

        bar_groups = [
            ft.BarChartGroup(
                x=index,
                bar_rods=[SampleRod(value)],
            )
            for index, value in enumerate(self.data)
        ]

        axis_labels = [
            ft.ChartAxisLabel(
                value=index, 
                label=ft.Text(label, size=10, offset=ft.Offset(0, 0.4), rotate=ft.Rotate(45), text_align= ft.TextAlign.START)
            ) for index, label in enumerate(self.labels)
        ]

        
        left_axis_labels = ft.ChartAxis(labels_size=40, title= ft.Text(self.title), title_size=40)
        
        
        
        self.chart = ft.BarChart(
            bar_groups=bar_groups,
            bottom_axis=ft.ChartAxis(labels=axis_labels),
            on_chart_event=on_chart_event,
            interactive=True,
            vertical_grid_lines= ft.ChartGridLines(None, ft.colors.GREY_100, 1, dash_pattern=[3, 3]),
            horizontal_grid_lines= ft.ChartGridLines(None, ft.colors.GREY, 1, dash_pattern=[3, 3]),
            tooltip_fit_inside_horizontally=True,
            tooltip_fit_inside_vertically=True,
            left_axis=left_axis_labels,
            expand=True,
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300)
        )
        self.content = ft.Column(
            [
              ft.Container( 
                    ft.Text(f"Delay Problem {self.title} : ", color= 'black', weight=ft.FontWeight.W_100),padding=10 ),
                    ft.Divider(height=1),  
                    ft.Container(
                        self.chart,
                        padding=20,
                        expand=True
                    ) ,
            ],
            expand=True,
        )

class SampleRod(ft.BarChartRod):
    def __init__(self, y: float, hovered: bool = False):
        super().__init__()
        self.hovered = hovered
        self.y = y
    def _before_build_command(self):
        self.to_y = self.y + 1 if self.hovered else self.y
        self.color = ft.colors.TEAL_500 if self.hovered else ft.colors.TEAL_100
        self.border_side = (
            ft.BorderSide(width=1, color=ft.colors.TEAL_400)
            if self.hovered
            else ft.BorderSide(width=0, color=ft.colors.WHITE)
        )
        super()._before_build_command()

    def _build(self):
        self.tooltip_style = ft.TextStyle(color='white', size=20)
        self.show_tooltip = False
        self.tooltip = str(self.y)
        self.width = 22
        self.color = ft.colors.WHITE
        self.bg_to_y = 20
        

# class ProgressBarWidget:
#     def __init__(self, stock, capacity, yst, tdy, title, visible=True):
#         self.stock = stock
#         self.capacity = capacity
#         self.yst = yst
#         self.tdy = tdy
#         self.title = title
#         self.progress = stock / capacity
#         self.percentage = f"{self.progress * 100:.1f}%" 
#         self.visible = visible

#         self.build()

#     def build(self):
#         """Bangun elemen UI untuk widget progress bar."""
#         self.widget = ft.Column(
#             [
#                 ft.Text(self.title, size=10, color='grey700'),
#                 ft.Stack(
#                     [
#                         ft.Container(
#                             ft.ProgressBar(
#                                 value=self.progress,
#                                 bgcolor=ft.colors.GREY_100,
#                                 color=ft.colors.TEAL_500,
#                             ),
#                             height=20,
#                             expand=True,
#                         ),
#                         ft.Text(
#                             self.percentage,
#                             size=12,
#                             color='white',
#                             text_align=ft.TextAlign.CENTER,
#                             expand=True,
#                         ),
#                     ],
#                     width=float("inf"),  
#                     height=20,
#                     alignment=ft.alignment.center,
#                 ),
#                 # Informasi tambahan
#                 ft.Text(f"Stock: {self.stock} / Capacity: {self.capacity}", size=10, color='grey700'),
#                 ft.Text(f"Yesterday: {self.yst} / Today: {self.tdy}", size=10, color='grey700'),
#             ],
#             spacing=5,
#             expand=True,
#             visible=self.visible,  # Mengatur visibilitas
#         )

#     def set_stock(self, stock):
#         """Perbarui nilai stock dan progress bar."""
#         self.stock = stock
#         self.progress = self.stock / self.capacity
#         self.percentage = f"{self.progress * 100:.1f}%"
#         self.build()  # Bangun ulang elemen UI untuk mencerminkan perubahan

#     def set_visible(self, visible):
#         """Mengatur visibilitas widget."""
#         self.visible = visible
#         self.widget.visible = visible

#     def get_widget(self):
#         """Ambil elemen widget untuk digunakan di Flet."""
#         return self.widget
    
#     def set_value(self, stock, capacity):
#         """Perbarui nilai stock, capacity, dan progress bar."""
#         self.stock = stock
#         self.capacity = capacity
#         self.progress = self.stock / self.capacity if self.capacity > 0 else 0  # Hindari pembagian dengan 0
#         self.percentage = f"{self.progress * 100:.1f}%"
#         self.build()
        
class ProgressBarWidget(ft.Container):
    def __init__(self, stock, capacity, yst, tdy, title):
        """
        :param stock: Current stock value.
        :param capacity: Maximum capacity.
        :param yst: Stock value from yesterday.
        :param tdy: Stock value from today.
        :param title: Title for the progress bar widget.
        :param visible: Whether the widget is visible or not.
        """
        super().__init__()
        self.stock = stock
        self.capacity = capacity
        self.yst = yst
        self.tdy = tdy
        self.title = title
        self.progress = stock / capacity
        self.percentage = f"{self.progress * 100:.1f}%"
        self.visible = True

        # self.build()
    
    def build(self):
        """Build UI elements for the progress bar widget."""
        self.widget = ft.Column(
            [
                ft.Text(self.title, size=10, color='grey700'),
                ft.Stack(
                    [
                        ft.Container(
                            ft.ProgressBar(
                                value=self.progress,
                                bgcolor=ft.colors.GREY_300,
                                color=ft.colors.TEAL_500,
                            ),
                            height=20,
                            expand=True,
                        ),
                        ft.Text(
                            self.percentage,
                            size=12,
                            color='white',
                            text_align=ft.TextAlign.CENTER,
                            expand=True,
                        ),
                    ],
                    width=float("inf"),  
                    height=20,
                    alignment=ft.alignment.center,
                ),

                ft.Text(f"Stock: {self.stock} / Capacity: {self.capacity}", size=10, color='grey700'),
                ft.Text(f"Yesterday: {self.yst} / Today: {self.tdy}", size=10, color='grey700'),
            ],
            spacing=5,
            expand=True,
            visible=self.visible,  #
        )
        # Set content to the container
        self.content = ft.Column([self.widget], expand=True)
        return self
    def set_stock(self, stock):
        """Update stock and progress bar value."""
        self.stock = stock
        self.progress = self.stock / self.capacity
        self.percentage = f"{self.progress * 100:.1f}%"

    def set_visible(self, visible):
        """Set the visibility of the widget."""
        self.visible = visible
        self.build()
    # def get_widget(self):
    #     """Get the widget element for use in Flet."""
    #     return self.content
    def set_unexisted(self):
        self.percentage = "UNAVAILABLE DATA"
        self.build()

    def set_value(self, stock, capacity, yst, tdy):
        """Update stock, capacity, and progress bar."""
        self.stock = stock
        self.capacity = capacity
        self.yst = yst
        self.tdy = tdy
        self.progress = self.stock / self.capacity if self.capacity > 0 else 0  # Prevent division by zero
        self.percentage = f"{self.progress * 100:.1f}%"
        self.build()