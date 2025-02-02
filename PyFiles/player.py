from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

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
