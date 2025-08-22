import pygame
class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, image, difficulty):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        if difficulty == "E":
            self.speed = 2
        elif difficulty == "M":
            self.speed = 4
        elif difficulty == "H":
            self.speed = 6
        else:
            self.speed = 4
