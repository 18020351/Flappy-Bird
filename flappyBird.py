import pygame
import time
import os
from random import randint


pygame.init()

# set tỷ lệ dài và rộng của màn hình
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Flappy Bird D.NV')

clock = pygame.time.Clock()

# create background cho game
background_img = pygame.image.load('flappy bird/images/background.png')

# set kích thước image background cho đúng tỷ lệ màn hình
background_img = pygame.transform.scale(background_img, (400, 600))

# khởi tạo tọa độ cho con chim
x_bird = 50
y_bird = 350

# khởi tạo tọa độ X cho ống tre
tube1_x = 400
tube2_x = 600
tube3_x = 800
tube_y = 0
# Note: Tọa độ Y của ống luôn luôn bằng 0

# khởi tạo kích thước dài rộng cho ống tre
# Note: chiều rộng = const, chiều dài = random
tube_width = 50
tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)

# khơi tạo ống tre
tube_img = pygame.image.load('flappy bird/images/tube.png')
tube_op_img = pygame.image.load('flappy bird/images/tube_op.png')

# khoảng cách giữa 2 ống tre đối diện
d_2tube = 150

# vận tốc rơi ban đầu
bird_drop_velocity = 0

# trọng lực = 0.5
gravity = 0.5

# vận tốc di chuyển của màn hình (vận tốc của các ống di chuyển trong màn hình)
tube_velocity = 2

# điểm
score = 0
# Tạo font ghi điểm ra màn hình
font_score = pygame.font.SysFont('san', 30)

# Tạo font game over
font_gameOver = pygame.font.SysFont('san', 40)

# hàm vẽ con chim


bird_images = [pygame.image.load('flappy bird/images/bluebird' + str(i)+ '.png') for i in range(1,4)]

# bird_img1 = pygame.image.load(
#     'flappy bird/images/bluebird-midflap.png')
bird_img1 = pygame.transform.scale(bird_images[0], (35, 35))
bird_img2 = pygame.transform.scale(bird_images[1], (35, 35))
bird_img3 = pygame.transform.scale(bird_images[2], (35, 35))

# Biến kiểm tra xem con chim pass qua ống hay chưa
tube1_pass = False
tube2_pass = False
tube3_pass = False


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# biến kiểm tra dừng
pausing = False

# âm thanh
# sound = pygame.mixer.Sound('flappy bird/no6.wav')
sound_hit = pygame.mixer.Sound('flappy bird/sound/hit.wav')
sound_wing = pygame.mixer.Sound('flappy bird/sound/wing.wav')
sound_point = pygame.mixer.Sound('flappy bird/sound/point.wav')
sound_die = pygame.mixer.Sound('flappy bird/sound/die.wav')
sound_swoosh = pygame.mixer.Sound('flappy bird/sound/swoosh.wav')

# Khởi tạo và set tỷ lệ ảnh cát
sand_img = pygame.image.load('flappy bird/images/sand.png')
sand_img = pygame.transform.scale(sand_img, (400, 30))

running = True
while running:
    # pygame.mixer.Sound.play(sound)

    # nháy 60 lần / 1 giây
    clock.tick(60)

    # set màu nền
    screen.fill(WHITE)

    # vẽ background vào khung hình game
    screen.blit(background_img, (0, 0))

    # set kích thước của ống sao cho phù hợp với khung màn hình game
    tube1_img = pygame.transform.scale(tube_img, (tube_width, tube1_height))
    tube2_img = pygame.transform.scale(tube_img, (tube_width, tube2_height))
    tube3_img = pygame.transform.scale(tube_img, (tube_width, tube3_height))

    # vẽ ống tre
    tube1 = screen.blit(tube1_img, (tube1_x, tube_y))
    tube2 = screen.blit(tube2_img, (tube2_x, tube_y))
    tube3 = screen.blit(tube3_img, (tube3_x, tube_y))

    # set tỷ lệ các ống phía đối diện cho khớp với khung hình
    tube1_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-tube1_height-d_2tube))
    tube2_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-tube2_height-d_2tube))
    tube3_op_img = pygame.transform.scale(
        tube_op_img, (tube_width, 600-tube3_height-d_2tube))

    # vẽ ống đối diện
    tube1_op = screen.blit(tube1_op_img, (tube1_x, tube1_height+d_2tube))
    tube2_op = screen.blit(tube2_op_img, (tube2_x, tube2_height+d_2tube))
    tube3_op = screen.blit(tube3_op_img, (tube3_x, tube3_height+d_2tube))

    # ống di chuyển sang trái màn hình
    tube1_x -= tube_velocity
    tube2_x -= tube_velocity
    tube3_x -= tube_velocity

    # khởi tạo ống mới khi chạy hết màn hình ban đầu.
    if tube1_x < -tube_width:
        tube1_x = 550
        tube1_height = randint(100, 400)
        tube1_pass = False
    if tube2_x < -tube_width:
        tube2_x = 550
        tube2_height = randint(100, 400)
        tube2_pass = False
    if tube3_x < -tube_width:
        tube3_x = 550
        tube3_height = randint(100, 400)
        tube3_pass = False

    # Vẽ cát
    sand = screen.blit(sand_img, (0, 570))

    # vẽ con chim vào game
    
    bird = screen.blit(bird_img1, (x_bird, y_bird))
    

    # chim rơi
    y_bird += bird_drop_velocity
    bird_drop_velocity += gravity

    # hiển thị điểm ra màn hình
    score_txt = font_score.render("Score: " + str(score), True, RED)
    screen.blit(score_txt, (5, 5))

    # check nếu chim pass qua ống sẽ cộng điểm
    if (tube1_x + tube_width <= x_bird) and (tube1_pass == False):
        pygame.mixer.Sound.play(sound_point)
        score += 1
        tube1_pass = True

    if (tube2_x + tube_width <= x_bird) and (tube2_pass == False):
        score += 1
        pygame.mixer.Sound.play(sound_point)
        tube2_pass = True
    if (tube3_x + tube_width <= x_bird) and (tube3_pass == False):
        score += 1
        pygame.mixer.Sound.play(sound_point)
        tube3_pass = True

    # kiểm tra va chạm
    list_tube = [tube1, tube2, tube3, tube1_op, tube2_op, tube3_op, sand]
    for tube in list_tube:
        if bird.colliderect(tube):
            if pausing == False:
                sound_hit.play()
                sound_die.play()
           # pygame.mixer.pause()

            tube_velocity = 0
            bird_drop_velocity = 0
            font_gameOver_txt = font_gameOver.render(
                'Game Over, Score: ' + str(score), True, BLUE)
            screen.blit(font_gameOver_txt, (75, 260))
            space_txt = font_score.render(
                'Press Space to replay game!', True, RED)
            screen.blit(space_txt, (70, 290))
            pausing = True

    # kiểm tra các sự kiện trong game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound_wing.play()
                bird_drop_velocity = 0
                bird_drop_velocity -= 6
                if pausing:
                   # pygame.mixer.unpause()
                    x_bird = 50
                    y_bird = 350
                    tube1_x = 400
                    tube2_x = 600
                    tube3_x = 800
                    tube_y = 0
                    tube_velocity = 2
                    score = 0
                    pausing = False

    pygame.display.flip()
pygame.quit()
