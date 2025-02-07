import flet as ft

class DateRangePicker:
    def __init__(self, page):
        self.page = page
        self.start_date = None
        self.end_date = None

    def pick_date_range(self):
        def on_start_date_change(e):
            self.start_date = e.data
            if self.end_date and self.start_date > self.end_date:
                self.end_date = None
                end_date_picker.label = "Select End Date (Invalid Range)"
            else:
                end_date_picker.label = "Select End Date"
            self.page.update()

        def on_end_date_change(e):
            if self.start_date:
                if e.data < self.start_date: 
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text("End date cannot be earlier than start date."),
                        bgcolor=ft.colors.RED_500,
                    )
                    self.page.snack_bar.open = True
                else:
                    self.end_date = e.data 
            else:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Please select a start date first."),
                    bgcolor=ft.colors.RED_500,
                )
                self.page.snack_bar.open = True

            self.page.update()

        start_date_picker = ft.DatePicker(
            label="Select Start Date",
            on_change=on_start_date_change,
        )

        end_date_picker = ft.DatePicker(
            label="Select End Date",
            on_change=on_end_date_change,
        )

        self.page.add(
            ft.Column(
                [
                    ft.Text("Pick a date range:", size=16, weight=ft.FontWeight.BOLD),
                    start_date_picker,
                    end_date_picker,
                ],
                spacing=10,
            )
        )


