from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

shift = False
app = Ursina()


class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = FirstPersonController(**kwargs)
        super().__init__(parent=self.controller)

        self.stone = Entity(parent=self.controller.camera_pivot,
                            scale=0.1,
                            position=(0.7, -1,1,5),
                            rotation=Vec3(0, 170, 0),
                            model='stone',
                            visible=False)

        self.dirt = Entity(parent=self.controller.camera_pivot,
                           scale=0.1,
                           position=(0.7, -1, 1, 5),
                           rotation=Vec3(0, 170, 0),
                           model='dirt',
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


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
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
        voxel = Voxel(position=(x, 0, z))


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

    if key == 'left shift':  # shift controls
        shift = not shift
        if shift:
            player.speed = 2.5
        else:
            player.speed = 5


player = Player(position=(0, 10, 0))
app.run()
