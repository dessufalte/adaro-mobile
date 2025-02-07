import flet as ft
import flet.canvas as cv
import time
import random

class Conveyor:
    def __init__(self, start, end, name, status=False, invert=False):
        self.start = start
        self.end = end
        self.status = status
        self.name = name
        self.next_conveyors = []
        self.previous_conveyor = None 
        self.inverted = invert
        self.status_color = {
            0: ft.colors.GREY,
            1: ft.colors.GREEN,
            2: ft.colors.RED,
            3: ft.colors.YELLOW
        }
    def add_next_conveyor(self, conveyor):
        self.next_conveyors.append(conveyor)
        conveyor.previous_conveyor = self 

    def activate(self):
        self.status = 1

    def deactivate(self):
        self.status = 0

    def toggle(self):
        self.status = not self.status

    def highlight(self):
        self.status = 3
    
    def problems(self):
        self.status = 2

    
    def blink_status(self):
        if self.previous_conveyor:
            self.previous_conveyor.toggle()
    def transfer_mat(self, amount, destination=None):
        if not self.next_conveyors:
            print(f"{self.name}: Material has reached the destination.")
            return
        for conveyor in self.next_conveyors:
            if destination and destination == conveyor.name:
                print(f"{self.name}: Transferring {amount} material to {conveyor.name}.")
                conveyor.receive_material(amount, destination)
                return

       
        for conveyor in self.next_conveyors:
            conveyor.receive_material(amount, destination)

    def receive_material(self, amount, destination=None):
        
        self.activate()
        print(f"{self.name}: Receiving {amount} material.")
        self.transfer_mat(amount, destination)

    def before_conveyor(self):
        if self.previous_conveyor:
            print(f"{self.name}: Receiving material from {self.previous_conveyor.name}.")
            
            self.receive_material(1)  
        else:
            print(f"{self.name}: No previous conveyor.")
            
    def draw(self):
        mid_x = (self.start[0] + self.end[0]) / 2
        mid_y = (self.start[1] + self.end[1]) / 2

        if self.inverted:
            temp = self.start
            self.start = self.end
            self.end = temp

        return [
            cv.Path(
                [
                    cv.Path.MoveTo(*self.start),
                    cv.Path.LineTo(*self.end),
                ],
                paint=ft.Paint(
                    color= self.status_color.get(self.status, ft.colors.GREY) ,
                    stroke_width=(
                        0.5 if self.status == 0 
                        else 1 if self.status == 1
                        else 1.5  
                    ),
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
            cv.Text(
                mid_x,
                mid_y,
                self.name,
                ft.TextStyle(size=4, color=ft.colors.BLACK),
            ),
        ]

class Hopper:
    def __init__(self,  capacity, size, position , name, connected_conveyor=None , status=0):
        self.status = status
        self.name = name
        self.capacity = capacity
        self.current_load = 0
        self.connected_conveyor = connected_conveyor
        self.position = position
        self.size = size
        self.status_color = {
            0: ft.colors.GREY,
            1: ft.colors.GREEN,
            2: ft.colors.RED,
            3: ft.colors.YELLOW
        }
    def load_mat(self, amount):
        if self.current_load + amount <= self.capacity:
            self.current_load += amount
            print(f"{amount} units loaded into the hopper. Current load: {self.current_load}")
        else:
            print("Hopper is full! Cannot load more material.")
    
    def activate(self):
        self.status = 1

    def deactivate(self):
        self.status = 0

    def highlight(self):
        self.status = 3
    
    def problem(self):
        self.status = 2
    
    def toggle(self):
        self.status = not self.status
         
    def draw(self):
        x, y = self.position
        if self.connected_conveyor:
            x, y = self.connected_conveyor.start
            x+= 2
        width, height = self.size
        return [
            cv.Rect(
                x=x,
                y=y,
                width=width,
                height=height,
                paint=ft.Paint(
                    color=self.status_color.get(self.status, ft.colors.GREY) ,
                    style=ft.PaintingStyle.FILL,
                ),border_radius=3
            ),
            cv.Text(
                x + width / 2 - 10,
                y + height / 2 - 10,
                f"{self.current_load}/{self.capacity}",
                ft.TextStyle(size=4, color=ft.colors.BLACK),
            ),
            cv.Text(
                x + width / 2 + 5,
                y + height / 2 - 4,
                f"{self.name}",
                ft.TextStyle(size=4, color=ft.colors.BLACK),
            ),
        ]

class Stockpile:
    def __init__(self, name, capacity, size, connected_conveyor=None):
        self.name = name
        self.connected_convey = connected_conveyor
        self.capacity = capacity
        self.size = size
        self.current_load = 0
    def draw(self):
        if self.connected_convey:
            x, y = self.connected_convey.end
        radius_x, radius_y = self.size
        fill_color = ft.colors.with_opacity(0.5, ft.colors.GREY) if self.current_load < self.capacity else ft.colors.RED
        return[
            cv.Circle(
                x=x,
                y=y,
                radius=radius_x,
                paint=ft.Paint(
                    color=fill_color,
                    style=ft.PaintingStyle.FILL,
                ),
            ),
            cv.Text(
                x - 10,
                y,
                f"{self.current_load}/{self.capacity}",
                ft.TextStyle(size=4, color=ft.colors.BLACK),
            ),
        ]

class Ship:
    def __init__(self, capacity, position, size, name):
        self.capacity = capacity
        self.current_load = 0
        self.position = position 
        self.size = size
        self.name = name

    def draw(self):
        x, y = self.position
        width, height = self.size
        fill_color = ft.colors.TEAL_400

        return [
            cv.Rect(
                x=x,
                y=y,
                width=width,
                height=height,
                paint=ft.Paint(
                    color=fill_color,
                    style=ft.PaintingStyle.FILL,
                ),
            ),
            cv.Text(
                x + width / 2 ,
                y + height / 2,
                self.name,
                ft.TextStyle(size=4, color=ft.colors.WHITE),
            ),
        ]
class ItemConvey:
    def __init__(self, amount, destination, ways: list[Conveyor]):
        self.amount = amount
        self.destination = destination
        self.ways = ways
    def activate_way(self):
        for way in self.ways:
            way.activate()
    def get_hopper_name(self, ways_group):
        for hopper_name, destinations in ways_group.items():
            for destination, conveyors in destinations.items():
                if self.ways == conveyors and self.destination == destination:
                    return hopper_name
        return None           
               
    def deactivate_way(self):
        for way in self.ways:
            way.deactivate()
    def deactivate_way(self):
        for way in self.ways:
            way.deactivate()
           

class MapDiagram(cv.Canvas):
    def __init__(self, canvas_width, canvas_height):
        super().__init__(width=canvas_width, height=canvas_height)
    
    def add_hoppers(self, hoppers):
        """Add hoppers to the canvas."""
        for hopper in hoppers.values():
            for shape in hopper.draw():
                self.shapes.append(shape)
        
    def add_stockpiles(self, stockpiles):
        """Add stockpiles to the canvas."""
        for stockpile in stockpiles.values():
            for shape in stockpile.draw():
                self.shapes.append(shape)

    def add_conveyors(self, conveyors):
        """Add conveyors to the canvas."""
        for conveyor in conveyors.values():
            for shape in conveyor.draw():
                self.shapes.append(shape)

    def add_ships(self, ships):
        """Add ships to the canvas."""
        for ship in ships.values():
            for shape in ship.draw():
                self.shapes.append(shape)
                
    def create_map(self, conveyors, hoppers, stockpiles, ships):
        """Create and populate the map with all elements."""
        self.add_hoppers(hoppers)
        self.add_stockpiles(stockpiles)
        self.add_conveyors(conveyors)
        self.add_ships(ships)
        


conveyors = {
    "S5": Conveyor((275, 50), (265, 30), "S5"),
    "S6": Conveyor((265, 30), (220, 40), "S6"),
    "S8": Conveyor((255, 60), (220, 30), "S8"),
    "S9": Conveyor((220, 40), (200, 40), "S9"),
    "S7": Conveyor((220, 30), (100, 30), "S7"),
    "S10": Conveyor((200, 40), (180, 15), "S10"),
    "L20": Conveyor((180, 15), (40, 15), "L20"),
    "L17": Conveyor((150, 15), (150, 25), "L17"),
    "L18": Conveyor((120, 15), (120, 25), "L18"),
    "L19": Conveyor((90, 15), (90, 25), "L19"),
    "S11": Conveyor((275, 85), (250, 80), "S11"),
    "S12": Conveyor((250, 80), (210, 78), "S12"),
    "L13": Conveyor((210, 78), (100, 78), "L13"),
    "S14": Conveyor((240, 70), (230, 90), "S14"),
    "S15": Conveyor((230, 90), (210, 88), "S15"),
    "L15": Conveyor((210, 88), (90, 88), "L15"),
    "S17": Conveyor((275, 110), (230, 100), "S17"),
    "S18": Conveyor((230, 100), (210, 97), "S18"),
    "S19": Conveyor((210, 97), (150, 97), "S19"),
    "S2": Conveyor((225, 115), (225, 130), "S2"),
    "S4": Conveyor((225, 130), (200, 125), "S4"),
    "S21": Conveyor((200, 125), (150, 125), "S21"),
    "L25": Conveyor((150, 125), (90, 125), "L25"),
    "S22": Conveyor((150, 125), (150, 145), "S22"),
    "S1": Conveyor((225, 165), (225, 180), "S1"),
    "L10": Conveyor((225, 165), (215, 152), "L10"),
    "L12": Conveyor((215, 152), (200, 145), "L12"),
    "L30": Conveyor((200, 145), (40, 145), "L30"),
    "S3": Conveyor((225, 165), (90, 165), "S3"),
    "L1": Conveyor((200, 145), (200, 155), "L1"),
    "L2": Conveyor((140, 145), (140, 155), "L2"),
    "L3": Conveyor((100, 145), (100, 155), "L3"),
    "L6": Conveyor((100, 135), (40, 135), "L6"),
    "L26": Conveyor((90, 125), (40, 125), "L26"),
    "L5": Conveyor((100, 135), (100, 70), "L5"),
    "L28": Conveyor((100, 45), (80, 35), "L28"),
    "L9": Conveyor((80, 35), (40, 35), "L9"),
    "L9#2": Conveyor((80, 35), (100, 55), "L9"),
    "L24": Conveyor((90, 88), (90, 125), "L24"),
    "L27": Conveyor((90, 88), (90, 60), "L27"),
    "L28": Conveyor((90, 60), (75, 45), "L28"),
    "L29": Conveyor((75, 45), (40, 45), "L29"),
    "S23": Conveyor((150, 145), (180, 160), "S23"),
    "L22": Conveyor((90, 70), (180, 70), "L22"),
    "L23": Conveyor((150, 97), (90, 97), "L23"),
    "S20": Conveyor((150, 97), (150, 50), "S20"),
    "L7": Conveyor((100, 70), (100, 55), "L7"),
    "L16": Conveyor((180, 70), (180, 60), "L16"),
    "L21": Conveyor((120, 70), (120, 60), "L21"),
    "L8": Conveyor((100, 30), (85, 40), "L8"),
    "S16": Conveyor((200, 88), (200, 60), "S16"),
    "S13": Conveyor((100, 55), (115, 45), "S13"),
    "L4": Conveyor((100, 145), (40, 145), "L4"),
}

hoppers = {
    "H3": Hopper(2980, (10, 10), (275, 50), "Hopper 3",connected_conveyor=conveyors["S5"] ),
    "H4": Hopper(2980, (10, 10), (255, 60), "Hopper 4",connected_conveyor=conveyors["S8"] ),
    "H6": Hopper(2980, (10, 10), (255, 60), "Hopper 6",connected_conveyor=conveyors["S14"] ),
    "H5": Hopper(2980, (10, 10), (255, 60), "Hopper 5",connected_conveyor=conveyors["S11"] ),
    "H7": Hopper(2980, (10, 10), (255, 60), "Hopper 7",connected_conveyor=conveyors["S17"] ),
    "H2": Hopper(2980, (10, 10), (255, 60), "Hopper 2",connected_conveyor=conveyors["S2"] ),
    "H1": Hopper(2980, (10, 10), (255, 60), "Hopper 1",connected_conveyor=conveyors["S1"] ),
}

stockpiles = {
    "S1": Stockpile("S16", 3000, (8, 5), conveyors["S16"]),
    "S2": Stockpile("S20", 3000, (8, 5), conveyors["S20"]),
    "S3": Stockpile("S13", 3000, (8, 5), conveyors["S13"]),
    "S4": Stockpile("S23", 3000, (8, 5), conveyors["S23"]),
}

ships = {
    "K1": Ship(10000, (20, 10), (20,40), "K3"),
    "K2": Ship(10000, (20, 110), (20,40), "K1"),
}


ways = {
    "H1": { 
        "S3": [conveyors["S1"], conveyors["S3"]],
        "L4": [conveyors["S1"], conveyors["L10"], conveyors["L12"], conveyors["L30"], conveyors["L4"]],
    },
    "H2": {
        "L4": [conveyors["S2"], conveyors["S4"], conveyors["S21"], conveyors["S22"], conveyors["L30"], conveyors["L4"]],
        "L26": [conveyors["S2"], conveyors["S4"], conveyors["S21"], conveyors["L25"], conveyors["L26"]],
        "S23": [conveyors["S2"], conveyors["S4"], conveyors["S21"], conveyors["S22"], conveyors["S23"]],
    },
    "H3": {
        "L20": [conveyors["S5"], conveyors["S6"], conveyors["S8"], conveyors["S9"], conveyors["S10"], conveyors["L20"]],
        "S7": [conveyors["S5"], conveyors["S6"], conveyors["S8"], conveyors["S7"]],
    },
    "H4": {
        "L20": [conveyors["S8"], conveyors["S9"], conveyors["S10"], conveyors["L20"]],
        "S7": [conveyors["S8"], conveyors["S7"]],
    },
    "H5": {
        "S13": [conveyors["S11"], conveyors["S12"], conveyors["L13"], conveyors["S13"]],
        "L6": [conveyors["S11"], conveyors["S12"], conveyors["L13"], conveyors["L5"], conveyors["L6"]],
        "L9": [conveyors["S11"], conveyors["S12"], conveyors["L13"], conveyors["L7"], conveyors["L8"], conveyors["L9"]],
        "S13": [conveyors["S11"], conveyors["S12"], conveyors["L13"], conveyors["L7"], conveyors["S13"]],
    },
    "H6": {
        "L6": [conveyors["S14"], conveyors["S15"], conveyors["L15"], conveyors["L5"], conveyors["L6"]],
        "L26": [conveyors["S14"], conveyors["S15"], conveyors["L15"], conveyors["L24"], conveyors["L26"]],
        "L9": [conveyors["S14"], conveyors["L7"], conveyors["L8"], conveyors["L9"]],
        "S16": [conveyors["S14"], conveyors["S12"], conveyors["L13"], conveyors["S16"]],
    },
    "H7": {
        "L6": [conveyors["S17"], conveyors["S18"], conveyors["S19"], conveyors["L23"], conveyors["L5"], conveyors["L6"]],
        "L26": [conveyors["S17"], conveyors["S18"], conveyors["S19"], conveyors["L23"], conveyors["L24"], conveyors["L26"]],
        "L9": [conveyors["S17"], conveyors["S18"], conveyors["S19"], conveyors["L23"], conveyors["L7"], conveyors["L8"], conveyors["L9"]],
        "L29": [conveyors["S17"], conveyors["S18"], conveyors["S19"], conveyors["L23"], conveyors["L27"], conveyors["L28"], conveyors["L29"]],
        "S20": [conveyors["S17"], conveyors["S18"], conveyors["S19"], conveyors["S20"]],
    }
}

        
def transfer_item(canvas: MapDiagram, itemc: ItemConvey,):
        itemc.activate_way()
        h_name = itemc.get_hopper_name(ways)
        hoppers[h_name].activate()
        canvas.update()
        time.sleep(2)
        hoppers[h_name].deactivate()
        itemc.deactivate_way()
        canvas.update()
        
        
def get_way(hopper, way):
    try:
        return way, list(ways[f"H{hopper}"].values())[way]
    except KeyError:
        raise ValueError(f"Tidak ditemukan way '{way}' untuk hopper 'H{hopper}'")
    
    
def get_random_way(the_way, the_hopper):
        random_group = random.choice(list(ways.keys()))
        group_destinations = ways[the_hopper]
        random_destination = random.choice(list(group_destinations.keys()))
        return random_destination, group_destinations[the_way]

def transfer_item_test(MD: MapDiagram):
        for _ in range(1): 
            
            destination, way = get_random_way() 
            item = ItemConvey(
                amount=random.randint(1, 20),
                destination=destination,
                ways=way 
            )
            
            transfer_item(MD, item)
            time.sleep(0.1)
        
       