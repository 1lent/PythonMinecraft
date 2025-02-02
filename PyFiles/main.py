from ursina import *
from player import Player
from ursina.prefabs.first_person_controller import FirstPersonController


import time


lastPlacedBlock: int = 0
shift = False
pause = False

app = Ursina()



def place_block(position=[0, 0, 0], texture='cube_white'):
    global lastPlacedBlock
    current_time = time.time()
    if (current_time - lastPlacedBlock < 0.1):
        pass
    else:
        Voxel(position, texture)
        lastPlacedBlock = current_time


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='cube_white'):
        super().__init__(parent=scene,
                         position=position,
                         model='cube',
                         origin_y=.5,
                         texture=texture,
                         color=color.hsv(0, 0, random.uniform(.9, 1.0)),
                         highlight_color=color.red,
                         )

for z in range(1):
    for x in range(1):
        voxel_1 = Voxel(position=(3,1,4), texture='texture-of-wood-photo')
        voxel_2 = Voxel(position=(3, 2, 4), texture='texture-of-wood-photo')

for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x, 0, z))


def input(key):
    global shift
    global pause

    if held_keys['right mouse']:
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            # Voxel(position=hit_info.entity.position + hit_info.normal)
            place_block(position=hit_info.entity.position + hit_info.normal,
                        texture=player.inventory[player.current_inventory].texture)
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            place_block(position=hit_info.entity.position + hit_info.normal,
                        texture=player.inventory[player.current_inventory].texture)

            # Voxel(position=hit_info.entity.position + hit_info.normal, texture = player.inventory[player.current_inventory].texture)
            # Assign the texture of held item to Voxel

    if key == 'left mouse down':
        if mouse.hovered_entity.texture.name == "texture-of-wood-photo.jpg":
            player.inventory.append(player.wood)
        destroy(mouse.hovered_entity)

    if held_keys['left mouse']:
        if mouse.hovered_entity.texture.name == "texture-of-wood-photo.jpg":
            print("hi")
            player.inventory.append(player.wood)
        destroy(mouse.hovered_entity)



    if key == 'left shift':  # shift controls
        shift = not shift
        if shift:
            player.speed = 2.5
        else:
            player.speed = 5

    if key == 'escape':
        application.paused = not application.paused


player = Player(position=(0, 10, 0))
app.run()
