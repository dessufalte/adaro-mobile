import flet as ft
import flet.map as map
import asyncio
from .utils.fetch import get_data

# class Emergency(ft.Column):
#     def __init__(self):
#         super().__init__()
#         self.init_coor = None
#         self.loaded = False
#         self.hazard_id = 0
#         self.latitude = 0
#         self.longitude = 0
#         self.ip_address = ""
#         self.reason = ""
#         self.timestamp = ""
#         self.message = ""
#         self.map = map.Map(
#             layers=[
#                 map.TileLayer(
#                     url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
#                 )
#             ],
#         )
#         self.found_container = ft.Column()

#     def recieve_information(self, message):
#         self.message = message
#         self.hazard_id = message.get('id')
#         self.latitude = float(message.get('latitude', 0)) 
#         self.longitude = float(message.get('longitude', 0))
#         self.ip_address = message.get('ip_address')
#         self.reason = message.get('reason')
#         self.timestamp = message.get('timestamp')
#         self._set_new_loc(self.latitude, self.longitude)
#         self.loc_layer = None
#     def _set_new_loc(self, latitude, longitude):
#         self.init_coor = map.MapLatitudeLongitude(latitude, longitude)
#         self.loc_layer = map.MarkerLayer(
#             [
#                 map.Marker(
#                     ft.Icon(ft.icons.WARNING, color='red500'),
#                     coordinates = self.init_coor
#                 )
#             ]
#         )
#         self.map.initial_center = self.init_coor
#         self.map.layers.append(self.loc_layer)
#         self.found_container.controls.append(
#             ft.Text(self.message, color='white')
#         )
#         self.loaded = True
#     async def move_to_loc(self):
#         if hasattr(self, "init_coor") and isinstance(self.init_coor, map.MapLatitudeLongitude):
#             self.map.move_to(
#                 destination=self.init_coor
#             )
#             print(f"Moved to location: {self.init_coor.latitude}, {self.init_coor.longitude}")
#             # self.build()
#         else:
#             print("Error: init_coor is not set or invalid.")
#     def build(self):
#         self.container_map = ft.Container(
#             self.map,
#             bgcolor='GREY',
#             width=1000,
#             height=400
#         )
#         self.controls = [
#             ft.Container(
#                 ft.Column(
#                     [
#                         self.container_map,
#                         self.found_container,
#                         ft.ElevatedButton("Test", on_click=self.move_to_loc)
#                     ]
#                 )    
#                 ,bgcolor='red300'
#             ),
            
#         ]
#     def did_mount(self):
#         self.page.run_task(self.move_to_loc)
#         print("test")
        
class Emergency(ft.Column):
    def __init__(self):
        super().__init__()
        self.init_coor = None
        self.loaded = False
        self.hazard_id = 0
        self.latitude = 0
        self.longitude = 0
        self.ip_address = ""
        self.reason = ""
        self.timestamp = ""
        self.message = ""
        self.map = map.Map(
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                )
            ],
        )
        self.tile_layer = map.TileLayer(
            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        )
        self.found_container = ft.Column()
        self.coordinates_text = ft.Text()
        self.position = map.MarkerLayer([])
        self.hazard_marker = map.MarkerLayer([])
    def recieve_information(self, message):
        self.message = message
        self.hazard_id = message.get("id")
        self.latitude = float(message.get("latitude", 0))
        self.longitude = float(message.get("longitude", 0))
        self.ip_address = message.get("ip_address")
        self.reason = message.get("reason")
        self.timestamp = message.get("timestamp")
        self.init_coor = map.MapLatitudeLongitude(self.latitude, self.longitude)
        self.loc_layer = None
        new_hazard = map.Marker(
                        ft.Icon(ft.icons.WARNING, color='red500'),
                        coordinates=self.init_coor,
                    )
        self.hazard_marker.markers.append(new_hazard)
        self._set_new_loc()
    
    def extract_info(self, latitude, longitude, reason):
        self.init_coor = map.MapLatitudeLongitude(latitude, longitude)    
        self.reason = reason
        new_hazard = map.Marker(
                        ft.Icon(ft.icons.WARNING, color='red500'),
                        coordinates=self.init_coor,
                    )
        self.hazard_marker.markers.append(new_hazard)
        self._set_new_loc()
        
    def update_user_location(self, latitude, longitude):
        self.position.markers.clear()
        self.latitude = latitude
        self.longitude = longitude
        # print(f"loc: {self.latitude}, {self.longitude}")
        self.init_coor = map.MapLatitudeLongitude(self.latitude, self.longitude)
        new_position = map.Marker(
            ft.Icon(ft.icons.LOCATION_ON, color='blue500'),
            coordinates= self.init_coor
        )
        self.position.markers.append(new_position)
        self.coordinates_text.value = f"Lat: {self.latitude}, Long: {self.longitude}"
        self.coordinates_text.update()
        if self.loaded:
            self.coordinates_text.update()
        self._set_new_loc()

    def _set_new_loc(self):
        self.map.layers.clear()
        self.map.layers.append(self.tile_layer)
        # print(f"Position: {self.position.coordinates.latitude}, {self.position.coordinates.longitude}")
        # print(f"Position: {self.hazard_marker}")
        if self.hazard_marker:
            self.map.layers.append(self.hazard_marker)
        if self.position:
            self.map.layers.append(self.position)             
        
        # new_marker_layer = map.MarkerLayer(
        #     [
        #         map.Marker(
        #             ft.Icon(icon, color=color),
        #             coordinates=self.init_coor,
        #         )
        #     ]
        # )
        # self.marker_layer.append(new_marker_layer)
        self.map.configuration = map.MapConfiguration(
            initial_center=self.init_coor
        )
        self.found_container.controls.clear()
        
        # self.map.layers.append(marker_layer)
        for hazard in self.hazard_marker.markers:
            self.found_container.controls.append(
                ft.Row(
                    [
                        ft.Icon(ft.icons.WARNING),
                        ft.Text(f"Hazard: {self.reason} ({hazard.coordinates.latitude}, {hazard.coordinates.longitude})", color="white")
                    ]
                )
                
            )
        # elif icon == ft.icons.LOCATION_ON:
        #     self.found_container.controls.append(
        #         ft.Text(f"User Location: ({latitude}, {longitude})", color="blue")
        #     )
        # self.loaded = True
        

    # async def move_to_loc(self):
    #     if hasattr(self, "init_coor") and isinstance(self.init_coor, map.MapLatitudeLongitude):
    #         self.map.move_to(destination=self.init_coor)
    #         print(f"Moved to location: {self.init_coor.latitude}, {self.init_coor.longitude}")
    #     else:
    #         print("Error: init_coor is not set or invalid.")

    def build(self):
        self.container_map = ft.Container(
            self.map,
            bgcolor="GREY",
            width=1000,
            height=400,
        )
        self.controls = [
            ft.Container(
                ft.Column(
                    [
                        self.container_map,
                        self.found_container,
                        self.coordinates_text
                        # ft.ElevatedButton("Test"),
                    ]
                ),
                bgcolor="red300",
            ),
        ]

    async def api_data(self):
        api_data = await get_data("api/hazard/emergency/latest")
        self.hazard_marker.markers.clear()
        if api_data:
            for item in api_data:
                longt = item['longitude']
                latitude = item['latitude']
                ipaddr = item['ip_address']
                reason = item['reason']
                tmstmp = item['timestamp']
                self.extract_info(latitude, longt, reason)
    
    def did_mount(self):
        self.loaded = True
        self.page.run_task(self.api_data)
        
    def will_unmount(self):
        self.loaded = False
        