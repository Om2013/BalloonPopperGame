import pygame

class Dart(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(screen_width//2, screen_height-120))
        self.is_shot = False
        self.speed = 15

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10

        if self.is_shot:
            self.rect.y -= self.speed  
            if self.rect.bottom < 0:
                self.is_shot = False
                self.rect.y = 480 
