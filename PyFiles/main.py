from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import time

shift = False
lastPlacedBlock: int = 0

app = Ursina()

class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = FirstPersonController(**kwargs)
        super().__init__(parent=self.controller)

        self.stone = Entity(parent=self.controller.camera_pivot,
                            scale=0.5,
                            position=(1, -0.75, 1.2),
                            rotation=Vec3(0, 170, 0),
                            model='stone',
                            texture='stone.jpg',
                            visible=False)

        self.wood = Entity(parent=self.controller.camera_pivot,
                            scale=0.5,
                            position=(1, -0.75, 1.2),
                            rotation=Vec3(0, 170, 0),
                            model='cube',
                            texture='texture-of-wood-photo.jpg',
                            visible=False)

        self.dirt = Entity(parent=self.controller.camera_pivot,
                           scale=0.25,
                           position=(1, -0.5, 1.2),
                           rotation=Vec3(0, 170, 0),
                           model='dirt',
                           texture='dirt_texture.jpg',
                        #    color = rgb(128, 128, 0),
                           visible=False)

        self.inventory = [self.stone, self.dirt]
        self.current_inventory = 0
        self.switch_inventory()

    def switch_inventory(self):
        for i, v in enumerate(self.inventory):
            if i == self.current_inventory:
                v.visible = True
            else:
                v.visible = False

    def input(self, key):
        try:
            self.current_inventory = int(key) - 1
            self.switch_inventory()
        except ValueError:
            pass

        if key == 'scroll up':
            self.current_inventory = (self.current_inventory + 1) % len(self.inventory)
            self.switch_inventory()
        if key == 'scroll down':
            self.current_inventory = (self.current_inventory - 1) % len(self.inventory)
            self.switch_inventory()

    def update(self):
        self.controller.camera_pivot.y = 2 - held_keys['left control']


def place_block(position = [0, 0, 0], texture = 'cube_white'):
    global lastPlacedBlock
    current_time = time.time()
    if (current_time - lastPlacedBlock < 0.1):
        pass
    else:
      Voxel(position, texture)
      lastPlacedBlock = current_time

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='white_cube'):
        super().__init__(parent=scene,
                         position=position,
                         model='cube',
                         origin_y=.5,
                         texture=texture,
                         color=color.hsv(0, 0, random.uniform(.9, 1.0)),
                         highlight_color=color.red,
                         )


for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x, 0, z))

class Voxel(Button):
    def __init__(self, position=(0, 1, 0), texture='white_cube'):
        super().__init__(parent=scene,
                         position=position,
                         model='cube',
                         origin_y=.5,
                         texture='texture-of-wood-photo.jpg',
                         color=color.hsv(0, 0, random.uniform(.9, 1.0)),
                         highlight_color=color.red,
                         )


for z in range(1):
    for x in range(1):
        voxel = Voxel(position=(x, 1, z))


def input(key):
    global shift

    if held_keys['right mouse']:
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            # Voxel(position=hit_info.entity.position + hit_info.normal)
            place_block(position=hit_info.entity.position + hit_info.normal, texture = player.inventory[player.current_inventory].texture)
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            place_block(position=hit_info.entity.position + hit_info.normal, texture = player.inventory[player.current_inventory].texture)
            # Voxel(position=hit_info.entity.position + hit_info.normal, texture = player.inventory[player.current_inventory].texture)
            # Assign the texture of held item to Voxel

    if key == 'left mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)
    if held_keys['left mouse']:
        destroy(mouse.hovered_entity)
        if mouse.hovered_entity and texture is 'texture-of-wood-photo.jpg':
            self.inventory.append(self.wood)


    if key == 'left shift':  # shift controls
        shift = not shift
        if shift:
            player.speed = 2.5
        else:
            player.speed = 5


player = Player(position=(0, 10, 0))
app.run()
