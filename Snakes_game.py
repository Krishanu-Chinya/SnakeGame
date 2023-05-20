import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# defining colors with RGB values
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 175, 0)
yellow = (208, 146, 1)

# creating window
screen_width = 1000
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Backgroun Image
bgimg = pygame.image.load("field.png")
bgimg = pygame.transform.scale(bgimg, [screen_width, screen_height]).convert_alpha()

wlcm_img = pygame.image.load("snk_bg.jpg")
wlcm_img = pygame.transform.scale(wlcm_img, [screen_width, screen_height]).convert_alpha()

gmOvr_img = pygame.image.load("game_ovr.png")
gmOvr_img = pygame.transform.scale(gmOvr_img, [screen_width, screen_height]).convert_alpha()

pastry = pygame.image.load("pastry.png")
pastry = pygame.transform.scale(pastry, [40, 40])

snk = pygame.image.load("snk.png")
snk = pygame.transform.scale(snk, [30, 30])

profile_pic = pygame.image.load("profile_pic.png")
profile_pic = pygame.transform.scale(profile_pic, [200,200])

# setting title
pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)

with open("highscore.txt", "r") as f:
    highscore = f.read()


def score_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        if [x, y] == snake_list[-1]:
            gameWindow.blit(snk, (x, y))
        else:
            # pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
            pygame.draw.circle(gameWindow, color, (x + 15, y + 15), 15)


def welcome_screen():
    exit_game = False
    # add music here
    while not exit_game:
        gameWindow.fill((230, 210, 240))
        gameWindow.blit(wlcm_img, (0, 0))
        score_screen("W E L C O M E   T O   S N A K E S", black, 200, 150)
        score_screen("Press SPACE to play", black, 310, 300)

        #applying my details
        gameWindow.blit(profile_pic, (5, 350))
        score_screen("Developed by - Krishanu Cinya", black, 20, 550)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("background.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    gameLoop()

        pygame.display.update()
        clock.tick(60)


# Creating game loop
def gameLoop():
    # game specific variables
    game_over = False
    exit_game = False

    snake_x = 45
    snake_y = 55
    snake_size = 30
    fps = 60
    velocity_x = 0
    velocity_y = 0

    snake_list = []
    snake_length = 1

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    score = 0
    init_velocity = 2
    count = 0

    # checking if highscore file exist or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(gmOvr_img, (0, 0))
            score_screen("Snake is Dead!!! Press ENTER to play again.", white, 100, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0


                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # cheatcode
                    # if event.key==pygame.K_KP0:
                    # score+=10

            snake_x += velocity_x
            snake_y += velocity_y



            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                eat_sound = pygame.mixer.Sound("Tasty.mp3")
                eat_sound.play()
                score += 10
                snake_length += 5
                #increasing snake speed gradually
                count += 1
                if count == 15:
                    init_velocity += 1
                    count = 0

                # print("Score = " , score)
                # score_screen(("Score : " + str(score)), red, 5, 5)
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                if score == int(highscore):
                    dance_sound = pygame.mixer.Sound("highscr_music.mp3")
                    dance_sound.play()

                if score > int(highscore):
                    highscore = score

            gameWindow.fill(green)
            gameWindow.blit(bgimg, (0, 0))
            score_screen("Score : " + str(score) + "  Highscore: " + str(highscore), red, 5, 5)
            # pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            gameWindow.blit(pastry, (food_x, food_y))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                pygame.mixer.music.load("squidGame.mp3")
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load("squidGame.mp3")
                pygame.mixer.music.play()
                game_over = True

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, yellow, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome_screen()
