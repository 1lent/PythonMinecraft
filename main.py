
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

shift = False
app = Ursina()
class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.hsv(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.red,
        )

for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x,0,z))


def input(key):
    global shift

    if held_keys['right mouse']:
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)

    if key == 'left mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)
    if held_keys['left mouse']:
        destroy(mouse.hovered_entity)

    if key == 'left shift': #shift controls
        shift = not shift
        if shift:
            player.speed = 2.5
        else:
            player.speed = 5



player = FirstPersonController()
app.run()
