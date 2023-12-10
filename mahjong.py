import pygame
from pygame.locals import *
import sys
from board import Board  # Replace 'board' with the actual name of your module
from pygame import time as pygame_time
import pygame.mixer
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

SCREEN_WIDTH = 980
SCREEN_HEIGHT = 650

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Mahjong")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load background image
background = pygame.image.load('./res/background.jpg')

# Define your fonts
title_font = pygame.font.Font("./font/Sergio_Trendy.ttf", 40)
sub_title_font = pygame.font.Font("./font/Montserrat-SemiBold.ttf", 35)
title = pygame.font.Font("./font/Sergio_Trendy.ttf", 40)
sub_title = pygame.font.Font("./font/Montserrat-SemiBold.ttf", 35)
font = pygame.font.Font("./font/Montserrat-Regular.ttf", 20)
fontjam = pygame.font.Font("./font/Montserrat-SemiBold.ttf", 20)
fontisi = pygame.font.Font("./font/Montserrat-SemiBold.ttf", 18)
fontcr = pygame.font.Font("./font/Montserrat-SemiBold.ttf", 16)
fontisicr = pygame.font.Font("./font/Montserrat-Regular.ttf", 16)

click_sound = pygame.mixer.Sound("./sound/mouse-click.mp3")
game_over = pygame.mixer.Sound("./sound/game-over.wav")
good_job= pygame.mixer.Sound("./sound/good-job.wav")
pygame.mixer.music.load('./sound/backsound.mp3')
pygame.mixer.music.set_volume(0.5)

glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_text(text, font, color, x, y, alpha=1.0):
    text_surface = font.render(text, True, color)
    text_surface.set_colorkey((255, 255, 255))
    text_surface.set_alpha(int(alpha * 255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    pygame.Surface.blit(background, text_surface, text_rect)

def draw_text2(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_text_with_background(text, font, text_color, background_color, x, y, width, height, padding=5):
    text_surface = font.render(text, True, text_color)
    background_rect = pygame.Rect(x - padding, y - padding, width + 2 * padding, height + 2 * padding)

    # Draw white background
    pygame.draw.rect(background, background_color, background_rect)

    text_rect = text_surface.get_rect()
    text_rect.center = background_rect.center

    # Draw text
    pygame.Surface.blit(background, text_surface, text_rect)

def run_mahjong_game():
    SCREEN_SIZE = 980, 650

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Mahjong')

    background = pygame.image.load('./res/background.jpg')
    gameover = pygame.image.load('./res/gameover.png')
    success = pygame.image.load('./res/success.png')
    replay = pygame.image.load('./res/kayu.png')  # 133, 30
    random = pygame.image.load('./res/kayu.png')
    undo = pygame.image.load('./res/undo.png')  # 60, 60
    home = pygame.image.load('./res/home.png')  # 60, 60
    jam= pygame.image.load('./res/jam.png')  # 60, 60

    REPLAY = [133, 30]
    REPLAY_POS = [770, 568]

    UNDO = [60,60]
    UNDO_POS = [915, 38]

    RANDOM = [133, 30]
    RANDOM_POS = [600, 568]

    HOME = [60,60]
    HOME_POS = [915, 118]

    JAM = [233, 30]
    JAM_POS = [50, SCREEN_HEIGHT - 86]

    start_time = pygame.time.get_ticks()  # Record the start time in milliseconds
    game_continue = True

    pygame.mixer.music.play(-1)

    while game_continue:
        board = Board()
        status = 0
        restart = False

        while True:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate elapsed time in seconds

            screen.fill(0)
            screen.blit(background, (0, 0))
            screen.blit(replay, (REPLAY_POS[0], REPLAY_POS[1]))
            screen.blit(undo, (UNDO_POS[0], UNDO_POS[1]))
            screen.blit(home, (HOME_POS[0], HOME_POS[1]))
            screen.blit(random, (RANDOM_POS[0], RANDOM_POS[1]))
            screen.blit(jam, (JAM_POS[0], JAM_POS[1]))

            draw_text2("Mulai Ulang", fontisi, BLACK, screen, 785, 573)
            draw_text2("Acak", fontisi, BLACK, screen, 647, 573)

            # Draw the timer in the bottom left corner
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate elapsed time in seconds

            # Calculate hours, minutes, and seconds
            hours = elapsed_time // 3600
            minutes = (elapsed_time % 3600) // 60
            seconds = elapsed_time % 60

            # Format the time as "00:00:00"
            timer_text = f"Waktu: {hours:02d}:{minutes:02d}:{seconds:02d}"
            if elapsed_time > 540:
                timer_color = RED if elapsed_time % 2 == 0 else BLACK
            else:
                timer_color = BLACK
            draw_text2(timer_text, fontjam, timer_color, screen, 70, SCREEN_HEIGHT - 80)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()  # mouse pos

                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index == 0: 
                                click_sound.play() # left
                                if position[0] >= REPLAY_POS[0] and position[0] <= REPLAY_POS[0] + REPLAY[0] and \
                                        position[1] >= REPLAY_POS[1] and position[1] <= REPLAY_POS[1] + REPLAY[1]:
                                    restart = True
                                    pygame.mixer.music.rewind()
                                    break
                                if position[0] >= UNDO_POS[0] and position[0] <= UNDO_POS[0] + UNDO[0] and \
                                        position[1] >= UNDO_POS[1] and position[1] <= UNDO_POS[1] + UNDO[1]:
                                    board.undo()
                                    break
                                if position[0] >= HOME_POS[0] and position[0] <= HOME_POS[0] + HOME[0] and \
                                        position[1] >= HOME_POS[1] and position[1] <= HOME_POS[1] + HOME[1]:
                                    status = -1  
                                    break
                                if position[0] >= RANDOM_POS[0] and position[0] <= RANDOM_POS[0] + RANDOM[0] and \
                                        position[1] >= RANDOM_POS[1] and position[1] <= RANDOM_POS[1] + RANDOM[1]:
                                    board.shuffle_tiles()
                                    break
                                status = board.choose(position)
                            elif index == 2:  # right
                                status = board.pop(position)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = True
                        pygame.mixer.music.rewind()
                    elif event.key == pygame.K_u:
                        board.undo()
                    elif event.key == pygame.K_h:
                        status = -1
                    elif event.key == pygame.K_s:
                        board.shuffle_tiles()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            if restart:
                status = 0
                break

            board.display(screen)
            if status != 0:
                break

            elif elapsed_time >= 600:
                status = -1
                break

            pygame.display.update()


        if restart:
            continue
        pygame.mixer.music.stop()

        if status == 1:
            screen.blit(success, ((SCREEN_WIDTH - success.get_width()) // 2, (SCREEN_HEIGHT - success.get_height()) // 2))
            pygame.display.update()
            good_job.play()
            game_continue = False
            pygame.time.delay(2000)  # Delay for 2000 milliseconds (2 seconds) to display the success screen
            return main()

        if status == -1 or elapsed_time >= 600:
            screen.blit(gameover, ((SCREEN_WIDTH - gameover.get_width()) // 2, (SCREEN_HEIGHT - gameover.get_height()) // 2))
            pygame.display.update()
            game_over.play()
            game_continue = False
            pygame.time.delay(2000)  # Delay for 2000 milliseconds (2 seconds) to display the game over screen
            return main()  # Return to home screen

        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    click_sound.play()
                    if position[0] >= REPLAY_POS[0] and position[0] <= REPLAY_POS[0] + REPLAY[0] and \
                            position[1] >= REPLAY_POS[1] and position[1] <= REPLAY_POS[1] + REPLAY[1]:
                        flag = False
                        game_continue = True
                        break
                    if position[0] >= HOME_POS[0] and position[0] <= HOME_POS[0] + HOME[0] and \
                            position[1] >= HOME_POS[1] and position[1] <= HOME_POS[1] + HOME[1]:
                        status = -1 
                        break

def draw_rect2(screen, color, rect_dimensions, border_radius=0):
    x, y, width, height = rect_dimensions
    
    pygame.draw.polygon(screen, color, [
        (x + border_radius, y),
        (x + width - border_radius, y),
        (x + width, y + border_radius),
        (x + width, y + height - border_radius),
        (x + width - border_radius, y + height),
        (x + border_radius, y + height),
        (x, y + height - border_radius),
        (x, y + border_radius)
    ])
    
    if border_radius > 0:
        pygame.draw.circle(screen, color, (x + border_radius, y + border_radius), border_radius)
        pygame.draw.circle(screen, color, (x + width - border_radius, y + border_radius), border_radius)
        pygame.draw.circle(screen, color, (x + width - border_radius, y + height - border_radius), border_radius)
        pygame.draw.circle(screen, color, (x + border_radius, y + height - border_radius), border_radius)

def show_instructions():
    SCREEN_SIZE = 980, 650

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Mahjong')

    show_instructions = True

    home2 = pygame.image.load('./res/home.png')  # 60, 60
    # papan = pygame.image.load('./res/papan_instruksi.png')  # 60, 60
    selanjutnya= pygame.image.load('./res/kayu.png')

    HOME2 = [60, 60]
    HOME2_POS = [915, 38]

    # PAPAN = [335, 186]
    # PAPAN_POS = [35, 115]

    SELANJUTNYA = [133, 30]
    SELANJUTNYA_POS = [770, 548]

    while show_instructions:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_sound.play()
                # Check if the mouse is clicked in a specific area to exit
                if 690 < mouse_x < 780 and -10 < mouse_y < 20:
                    show_instructions = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if position[0] >= HOME2_POS[0] and position[0] <= HOME2_POS[0] + HOME2[0] and \
                        position[1] >= HOME2_POS[1] and position[1] <= HOME2_POS[1] + HOME2[1]:
                            return main()
                            break
                    if position[0] >= SELANJUTNYA_POS[0] and position[0] <= SELANJUTNYA_POS[0] + SELANJUTNYA[0] and \
                                        position[1] >= SELANJUTNYA_POS[1] and position[1] <= SELANJUTNYA_POS[1] + SELANJUTNYA[1]:
                                    show_instructions2()
                                    break

        screen.fill(0)
        screen.blit(background, (0, 0))
        screen.blit(home2, (HOME2_POS[0], HOME2_POS[1]))
        # screen.blit(papan, (PAPAN_POS[0], PAPAN_POS[1]))
        # pygame.draw.rect(screen, (248, 249, 223), (70, 120, 860, 490), border_radius=20)
        draw_rect2(screen, (172,180,156), (55, 120, 860, 510), border_radius=20)
        draw_rect2(screen, (248, 249, 223), (65, 120, 860, 490), border_radius=20)
        screen.blit(selanjutnya, (SELANJUTNYA_POS[0], SELANJUTNYA_POS[1]))

        draw_text2("Instruksi", title, BLACK, screen, 380, 40)
        draw_text2("Cara Bermain", fontjam, BLACK, screen, 400, 160)
        draw_text2("Selanjutnya", fontisi, BLACK, screen, 785, 553)

        # Teks untuk instruksi cara bermain
        instructions_text = [
            "1. Untuk memulai permainan, klik tombol 'Mulai' pada menu utama.",
            "Selanjutnya pengguna akan diarahkan ke dalam permainan mahjong.",
            "2. Pada permainan ini, klik dua tile yang sama dengan urutan dari atas.",
            "Jika tidak ada tile yang sama, gunakan tombol 'Acak' untuk",
            "mengganti susunan tile. Jika tile sama, jumlah tiles pada layar akan berkurang.",
            "Jika tiles sudah habis maka game berhasil dimainkan (Menang).",
            "3. Permainan memiliki batasan waktu 10 menit. Jika waktu habis sebelum",
            "menyelesaikan permainan, maka permainan dianggap kalah (Game Over).",
            "Waktu permainan terlihat di pojok kiri bawah.",
            "4. Untuk memahami permainan secara detail, dapat dilihat pada instruksi",
            "di menu utama."
        ]

        # Draw the instruction text
        y_offset = 210
        for instruction_line in instructions_text:
            draw_text2(instruction_line, font, BLACK, screen, 110, y_offset)
            y_offset += 30

        pygame.display.flip()

    # Ensure that the event queue is empty before exiting the function
    pygame.event.clear()
def show_instructions2():
    SCREEN_SIZE = 980, 650

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Mahjong')

    show_instructions2= True

    home3 = pygame.image.load('./res/home.png')  # 60, 60
    # papan = pygame.image.load('./res/papan_instruksi.png')  # 60, 60
    sebelumnya= pygame.image.load('./res/kayu.png')

    HOME3 = [60, 60]
    HOME3_POS = [915, 38]

    # PAPAN = [335, 186]
    # PAPAN_POS = [35, 115]

    SEBELUMNYA = [133, 30]
    SEBELUMNYA_POS = [110, 548]

    while show_instructions2:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_sound.play()
                # Check if the mouse is clicked in a specific area to exit
                # if 690 < mouse_x < 780 and -10 < mouse_y < 20:
                #     show_instructions = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if position[0] >= HOME3_POS[0] and position[0] <= HOME3_POS[0] + HOME3[0] and \
                        position[1] >= HOME3_POS[1] and position[1] <= HOME3_POS[1] + HOME3[1]:
                            return main()
                            break
                    if position[0] >= SEBELUMNYA_POS[0] and position[0] <= SEBELUMNYA_POS[0] + SEBELUMNYA[0] and \
                        position[1] >= SEBELUMNYA_POS[1] and position[1] <= SEBELUMNYA_POS[1] + SEBELUMNYA[1]:
                            show_instructions()
                            break

        screen.fill(0)
        screen.blit(background, (0, 0))
        screen.blit(home3, (HOME3_POS[0], HOME3_POS[1]))
        # screen.blit(papan, (PAPAN_POS[0], PAPAN_POS[1]))
        draw_rect2(screen, (172,180,156), (55, 120, 860, 510), border_radius=20)
        draw_rect2(screen, (248, 249, 223), (65, 120, 860, 490), border_radius=20)
        screen.blit(sebelumnya, (SEBELUMNYA_POS[0], SEBELUMNYA_POS[1]))

        draw_text2("Instruksi", title, BLACK, screen, 380, 40)
        draw_text2("Informasi Tombol", fontjam, BLACK, screen, 400, 160)
        draw_text2("Sebelumnya", fontisi, BLACK, screen, 120, 553)

        # Teks untuk instruksi cara bermain
        instructions_text = [
            "Mulai: Memulai permainan. Tekan M, Enter, atau Space Bar pada keyboard.",
            "Instruksi: Melihat instruksi permainan. Tekan I pada keyboard.",
            "Mulai Ulang: Mereset atau memulai ulang permainan. Tekan R pada keyboard.",
            "Acak: Mengganti susunan tile secara acak. Tekan S pada keyboard.",
            "Undo: Kembali ke langkah sebelumnya. Gunakan tombol Undo atau tekan ",
            "              U pada keyboard.",
            "Home: Kembali ke menu utama. Gunakan tombol dengan ikon Home atau",
            "              tekan H pada keyboard.",
            "Keluar: Keluar dari permainan. Klik tombol keluar atau tekan ESC pada keyboard.",
        ]

        # Draw the instruction text
        y_offset = 210
        for instruction_line in instructions_text:
            draw_text2(instruction_line, font, BLACK, screen, 110, y_offset)
            y_offset += 30

        draw_text2("Copy Right ©️ - TI 2022 A", fontcr, BLACK, screen, 390, 495)
        draw_text2("Adelia Miftakul J, Anissa Alifia P, Adinda Salsa L", fontisicr, BLACK, screen, 320, 515)

        pygame.display.flip()

    # Ensure that the event queue is empty before exiting the function
    pygame.event.clear()


def main():
    clock = pygame.time.Clock()

    # Animation variables
    translation_y = -100 # Initial position above the screen
    alpha = 0.0

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, background.get_width(), background.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(background, "RGBA", 1))
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(SCREEN_WIDTH, 0)
        glTexCoord2f(1, 1)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
        glTexCoord2f(0, 1)
        glVertex2f(0, SCREEN_HEIGHT)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        # Update and draw the welcome text
        if translation_y < 0:
            translation_y += 20  # Adjust the speed of translation
        else:
            alpha += 0.01

        draw_text("Selamat Datang di Game Mahjong", title_font, (0, 0, 0), 180, 130 + translation_y, alpha=alpha)

        # Draw rectangles with white background behind the text
        draw_text_with_background("Mulai", sub_title_font, (0, 0, 0), (255, 255, 255), 460, 260, 170, 50)
        draw_text_with_background("Instruksi", sub_title_font, (0, 0, 0), (255, 255, 255), 460, 375, 170, 50)
        draw_text_with_background("Keluar", sub_title_font, (0, 0, 0), (255, 255, 255), 460, 485, 170, 50)

        # Draw static text
        draw_text("Copy Right ©️ - TI 2022 A", fontcr, (0, 0, 0), 420, 650)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_sound.play()
                if 429 < mouse_x < 600 and 239 < mouse_y < 296:
                    run_mahjong_game()
                if 429 < mouse_x < 600 and 348 < mouse_y < 403:
                    show_instructions()
                if 429 < mouse_x < 600 and 453 < mouse_y < 507:
                    pygame.quit()
                    quit()
                if event.button == 1:  # Check for left mouse button click
                    print(f"Mouse Clicked at Coordinates: {event.pos}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_m or event.key == pygame.K_SPACE:  # Enter key
                    print("Play")
                    return True
                elif event.key == pygame.K_i:  # 'i' key
                    print("Instruction")
                    show_instructions()
                elif event.key == pygame.K_ESCAPE:  # Escape key
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    game_continue = True
    
    while game_continue:
        mode = main()

        if mode:
            run_mahjong_game()
            # Handle anything you need after the Mahjong game loop here

        # Reset the game_continue flag
        game_continue = True