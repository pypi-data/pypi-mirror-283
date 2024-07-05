from dataclasses import dataclass

import pygame


@dataclass
class Button:
    rect: pygame.Rect
    image: pygame.Surface

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)
