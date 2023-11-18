import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Screen")

# Font untuk teks
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def game_loop(difficulty):
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        draw_text(f"Game in {difficulty} Mode", font, WHITE, screen, 280, 100)
        draw_text("Press ESC to go back to Home Screen", font, WHITE, screen, 200, 200)
        draw_text("Back", font, WHITE, screen, 700, 0)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse is clicked in a specific area
                if 690 < mouse_x < 780 and -10 < mouse_y < 20:
                    game_running = False

# Home Screen Loop
while True:
    screen.fill(BLACK)

    # Teks di home screen
    draw_text("Welcome to the Game!", font, WHITE, screen, 250, 100)
    draw_text("Play Game", font, WHITE, screen, 330, 200)
    draw_text("Quit", font, WHITE, screen, 370, 250)
    # draw_text("Easy", font, WHITE, screen, 370, 300)
    # draw_text("Hard", font, WHITE, screen, 370, 350)

    # Memperbarui tampilan
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Cek apakah mouse berada di area Easy
            if 370 < mouse_x < 470 and 190 < mouse_y < 230:
                print("Play")
                game_loop("Play")
            elif 330 < mouse_x < 500 and 240 < mouse_y < 260:
                pygame.quit()  # Fix the typo here
                sys.exit()

            # Cek apakah mouse berada di area Hard
            # elif 370 < mouse_x < 470 and 350 < mouse_y < 380:
            #     print("Hard Mode Selected")
            #     game_loop("Hard")
