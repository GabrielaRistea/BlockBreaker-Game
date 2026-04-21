import pygame
import sys
import server
from settings import *
from ui import Button, draw_text
from game_objects import Paddle, Ball, create_blocks
from sound_manager import sounds
from leaderboard_manager import get_leaderboard, add_score

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Block Breaker")
clock = pygame.time.Clock()

state = "MENU"
current_theme = "DARK"
lives = 3
score = 0
level = 1
player_name = ""

btn_play = Button("START GAME", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50)
btn_settings = Button("SETTINGS", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 200, 50)
btn_theme = Button("CHANGE APPEARANCE", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 250, 50)
btn_back = Button("BACK", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 150, 50)
btn_pause = Button("PAUSE", SCREEN_WIDTH - 70, 20, 100, 30)
btn_resume = Button("RESUME", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 50)
btn_menu = Button("MAIN MENU", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, 200, 50)
btn_mute = Button("SOUND: ON", SCREEN_WIDTH - 200, 20, 130, 30)
btn_leaderboard = Button("LEADERBOARD", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140, 200, 50)
btn_back_leaderboard = Button("BACK", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 150, 50)

paddle = Paddle()
ball = Ball()
blocks = create_blocks(7, 10)

def main():
    global state, current_theme, blocks, lives, score, level
    server.start_server_thread()
    running = True

    while running:
        colors = THEMES[current_theme]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if btn_mute.is_clicked(event):
                sounds.toggle_mute()
                btn_mute.text = "SOUND: OFF" if sounds.muted else "SOUND: ON"

            elif state == "LEADERBOARD":
                if btn_back_leaderboard.is_clicked(event):
                    state = "MENU"

            elif state == "INPUT_NAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip() != "":
                            add_score(player_name, score)
                            state = "GAMEOVER"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 10:
                            player_name += event.unicode

            elif state == "SETTINGS":
                if btn_theme.is_clicked(event):
                    current_theme = "LIGHT" if current_theme == "DARK" else "DARK"
                if btn_back.is_clicked(event):
                    state = "MENU"

            elif state == "GAME":
                if btn_pause.is_clicked(event):
                    state = "PAUSE"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        state = "PAUSE"

            elif state == "PAUSE":
                if btn_resume.is_clicked(event):
                    state = "GAME"
                if btn_menu.is_clicked(event):
                    state = "MENU"

            if state == "MENU" or state == "GAMEOVER" or state == "VICTORY":
                if btn_play.is_clicked(event):
                    state = "GAME"
                    lives = 3
                    score = 0
                    level = 1
                    blocks = create_blocks(5, 3)
                    paddle.__init__()
                    ball.__init__()
                if btn_settings.is_clicked(event):
                    state = "SETTINGS"
                if btn_leaderboard.is_clicked(event):
                    state = "LEADERBOARD"

        screen.fill(colors["background"])

        if state == "MENU":
            draw_text(screen, "BLOCK BREAKER", 60, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50)
            btn_play.draw(screen, colors)
            btn_settings.draw(screen, colors)
            btn_leaderboard.draw(screen, colors)

        elif state == "GAMEOVER":
            draw_text(screen, "GAME OVER", 70, (220, 50, 50), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50)
            draw_text(screen, f"Final Score: {score}", 30, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 3 + 20)
            btn_play.draw(screen, colors)
            btn_settings.draw(screen, colors)
            btn_leaderboard.draw(screen, colors)

        elif state == "VICTORY":
            draw_text(screen, "YOU WIN!", 70, (50, 220, 50), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50)
            draw_text(screen, f"Final Score: {score}", 30, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 3 + 20)
            btn_play.draw(screen, colors)
            btn_settings.draw(screen, colors)

        elif state == "SETTINGS":
            draw_text(screen, "SETTINGS", 50, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text(screen, f"Current Theme: {current_theme}", 20, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 - 50)
            btn_theme.draw(screen, colors)
            btn_back.draw(screen, colors)

        elif state == "LEADERBOARD":
            draw_text(screen, "TOP SCORES", 50, colors["text_accent"], SCREEN_WIDTH // 2, 80)
            high_scores = get_leaderboard()
            if not high_scores:
                draw_text(screen, "NO SCORES YET", 30, colors["text_primary"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            else:
                for i, entry in enumerate(high_scores):
                    y_pos = 170 + (i * 45)
                    draw_text(screen, f"{i+1}. {entry['name']}: {entry['score']} PTS", 30, colors["text_primary"], SCREEN_WIDTH // 2, y_pos)
            btn_back_leaderboard.draw(screen, colors)

        elif state == "INPUT_NAME":
            draw_text(screen, "NEW HIGH SCORE!", 50, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text(screen, f"SCORE: {score}", 30, colors["text_primary"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, "ENTER YOUR NAME:", 20, colors["text_primary"], SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 2 + 20)
            draw_text(screen, player_name + "_", 40, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
            draw_text(screen, "PRESS ENTER TO SAVE", 15, colors["text_primary"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        elif state == "GAME":
            paddle.move(server.remote_command)
            was_active = ball.active
            ball.move(paddle, server.remote_action)
            if not was_active and ball.active:
                sounds.play_start()
                server.remote_action = False

            if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
                ball.dy *= -1
                sounds.play_hit_paddle()

            for block in blocks[:]:
                if ball.rect.colliderect(block.rect):
                    blocks.remove(block)
                    ball.dy *= -1
                    score += 10
                    sounds.play_hit_block()
                    break

            if len(blocks) == 0:
                sounds.play_level_up()
                level += 1
                blocks = create_blocks(7, 10)
                paddle.__init__()
                ball.__init__()

                speed_increase = level - 1
                ball.dx = 5 + speed_increase
                ball.dy = -(5 + speed_increase)

            if ball.rect.bottom >= SCREEN_HEIGHT:
                lives -= 1

                if lives > 0:
                    sounds.play_lose_life()
                    paddle.__init__()
                    ball.__init__()
                else:
                    sounds.play_game_over()
                    state = "INPUT_NAME"
                    player_name = ""
                    #add_score(player_name, score)
                    #state = "GAMEOVER"

            for block in blocks:
                block.draw(screen)

            paddle.draw(screen, colors["text_accent"])
            ball.draw(screen, colors["text_primary"])
            btn_mute.draw(screen, colors)
            draw_text(screen, f"LIVES: {lives}", 20, colors["text_primary"], 60, 20)
            draw_text(screen, f"SCORE: {score}", 20, colors["text_primary"], SCREEN_WIDTH // 2 - 50, 20)
            draw_text(screen, f"LEVEL: {level}", 20, colors["text_accent"], SCREEN_WIDTH // 2 + 80, 20)
            #draw_text(screen, "Press ESC for MENU", 16, colors["text_primary"], SCREEN_WIDTH - 100, 20)
            btn_pause.draw(screen, colors)

        elif state == "PAUSE":
            for block in blocks:
                block.draw(screen)
            paddle.draw(screen, colors["text_accent"])
            ball.draw(screen, colors["text_primary"])
            draw_text(screen, f"LIVES: {lives}", 20, colors["text_primary"], 60, 20)
            draw_text(screen, f"SCORE: {score}", 20, colors["text_primary"], SCREEN_WIDTH // 2, 20)

            draw_text(screen, "PAUSED", 60, colors["text_accent"], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 30)
            btn_resume.draw(screen, colors)
            btn_menu.draw(screen, colors)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()