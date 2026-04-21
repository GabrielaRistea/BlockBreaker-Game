import pygame


def draw_text(surface, text, font_size, color, x, y):
    font = pygame.font.SysFont("arial", font_size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text

    def draw(self, surface, colors):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, colors["text_accent"], self.rect, border_radius=12)
        else:
            pygame.draw.rect(surface, colors["text_primary"], self.rect, border_radius=12)

        draw_text(surface, self.text, 24, colors["background"], self.rect.centerx, self.rect.centery)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False