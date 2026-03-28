import pygame
import sys
from settings import *
from ui import Button, draw_text

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Block Breaker")
clock = pygame.time.Clock()

state = "MENU"
current_theme = "DARK"

btn_play = Button("START GAME", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50)
btn_settings = Button("SETTINGS", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 200, 50)
btn_theme = Button("CHANGE APPEARANCE", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250, 50)
btn_back = Button("BACK", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 150, 50)


def main():
    global state, current_theme
    running = True

    while running:
        colors = THEMES[current_theme]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "MENU":
                if btn_play.is_clicked(event):
                    state = "GAME"
                if btn_settings.is_clicked(event):
                    state = "SETTINGS"

            elif state == "SETTINGS":
                if btn_theme.is_clicked(event):
                    current_theme = "LIGHT" if current_theme == "DARK" else "DARK"
                if btn_back.is_clicked(event):
                    state = "MENU"

            elif state == "GAME":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "MENU"

        screen.fill(colors["background"])

        if state == "MENU":
            draw_text(screen, "BLOCK BREAKER", 60, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50)
            btn_play.draw(screen, colors)
            btn_settings.draw(screen, colors)

        elif state == "SETTINGS":
            draw_text(screen, "SETTINGS", 50, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text(screen, f"Current Theme: {current_theme}", 20, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 - 50)
            btn_theme.draw(screen, colors)
            btn_back.draw(screen, colors)

        elif state == "GAME":
            draw_text(screen, "Game...", 40, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 3)
            draw_text(screen, "(Press ESC for the Menu)", 20, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()