import flet as ft
import flet.map as mp


# class MapComponent(mp.Map):
#     def __init__(self, initial_center, hazard, initial_zoom=4.2):
#         self.hazard = hazard
        
#         # Definisikan layers terlebih dahulu
#         layers = [
#             mp.TileLayer(
#                 url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
#                 on_image_error=lambda e: print("Tile Error"),
#             ),
#             mp.MarkerLayer(
#                 markers=[
#                     mp.Marker(
#                         coordinates=self.hazard,
#                         content=ft.Icon(ft.icons.WARNING),
#                     )
#                 ],
#             ),
#         ]

#         # Panggil constructor dari kelas induk dengan layers
#         super().__init__(
#             layers=layers,
#             initial_center=initial_center,
#             initial_zoom=initial_zoom,
#             expand=True,
#             interaction_configuration=mp.MapInteractionConfiguration(
#                 flags=mp.MapInteractiveFlag.ALL
#             ),
#             on_init=lambda e: print("Initialized Map"),
#         )

# class HazardLocation:
#     def __init__(self, latitude: float, longitude: float, hazard_type: str):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.hazard_type = hazard_type
#         self.marker = None
    
#     def create_marker(self):
#         """Create a marker for the hazard location."""
#         color = self._get_hazard_color()
#         self.marker = mp.Marker(
#             content=ft.Icon(ft.icons.LOCATION_ON, color=color),
#             coordinates=mp.MapLatitudeLongitude(self.latitude, self.longitude),
#         )
#         return self.marker
#     def init_point(self):
#         return mp.MapLatitudeLongitude(self.latitude, self.longitude)

#     def _get_hazard_color(self):
#         """Return color based on hazard type."""
#         if self.hazard_type == "fire":
#             return ft.colors.RED
#         elif self.hazard_type == "flood":
#             return ft.colors.BLUE
#         elif self.hazard_type == "earthquake":
#             return ft.colors.ORANGE
#         return ft.colors.GRAY
