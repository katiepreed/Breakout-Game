import pygame
import random
from pygame import mixer

# initialise Pygame
pygame.init()

screen_width = 650  # of screen
screen_height = 750  # of screen

# creating a screen
# pygame: to access the methods inside the pygame module
# display.set_mode() is a method
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

# creating a font
big_font = pygame.font.Font("arcade.ttf", 90)
small_font = pygame.font.Font("arcade.ttf", 40)

# loading an image
bg = pygame.image.load("images/Breakout_game_screenshot.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))


# a class for all the rectangles in the game
class Rectangle:
    def __init__(self, x, y, width, height, fill_colour, num_of_hits):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_colour = fill_colour
        self.num_of_hits = num_of_hits
        self.rect_info = pygame.Rect(self.x, self.y, self.width, self.height)

    # to draw the rectangle to the screen
    def draw(self):
        pygame.draw.rect(screen, self.fill_colour, self.rect_info)


def sound_effect(music):
    sound = mixer.Sound("sound/" + music)
    sound.play()


def draw_text(text, coord, font):
    # displaying text
    # this creates a new surface with text drawn already onto it
    # the True part is called aliasing, if true, the characters will have smooth edges
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, coord)


def end_of_game():
    # a button the player uses to restart the game
    button = Rectangle(230, 500, 200, 70, (255, 0, 0), 0)

    running = True
    while running:
        button.draw()
        draw_text("GAME  OVER", (120, 310), big_font)
        draw_text("Press   OK   to   continue", (120, 400), small_font)
        draw_text("OK", (button.x + 50, button.y - 10), big_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if the player clicks the button then the game will restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect_info.collidepoint(event.pos):
                    # reset the speed
                    available_num = [-0.9, 0.9]
                    v_x = random.choice(available_num)
                    v_y = 0.9
                    return v_x, v_y

        # updates the screen to show changes
        pygame.display.update()


def main():
    hit_orange = False
    hit_red = False
    hit_brick = False
    collision_4 = False
    collision_12 = False
    clicked = False
    halved = False
    points = 0
    lives = 5
    collisions = 0
    separation = 3
    speed_increase = 1.2
    paddle_width = 90

    # initial x and y coordinates of paddle
    paddle_x = 285
    paddle_y = 655

    # initial x and y coordinates of ball
    ball_x = paddle_x + (paddle_width // 2)  # 11 - 639 pixel
    ball_y = paddle_y - 5  # 291 - 349 pixel

    # initial components of velocity of ball
    # the ball can travel to the left or to the right
    available_num = [-0.9, 0.9]
    v_x = random.choice(available_num)
    v_y = 0.9

    # a list for all the bricks that are hit so that they can be recovered
    recovery_bricks = []
    # a list of all the bricks
    bricks = []
    # each item in the list is a colour for a row of bricks
    colours = [(163, 30, 10), (163, 30, 10), (194, 133, 10), (194, 133, 10), (10, 133, 51), (10, 133, 51),
               (194, 194, 41), (194, 194, 41), (255, 255, 255)]

    # generating each brick and adding it to the list
    brick_y = 140
    for i in range(9):
        for brick_x in range(10, 640, 45):
            if i == 8:
                bricks.append(Rectangle(brick_x + 2, brick_y, 40, 11, (colours[i]), 2))
            else:
                bricks.append(Rectangle(brick_x + 2, brick_y, 40, 11, (colours[i]), 1))
        brick_y += 14

    # white to green and then it breaks after two hits

    running = True
    while running:
        # to slow the game down
        pygame.time.delay(5)
        # background
        screen.blit(bg, (0, 0))

        # drawing the bricks
        for brick in bricks:
            brick.draw()

        # creating the paddle and the ball
        paddle = Rectangle(paddle_x, paddle_y, paddle_width, 15, (10, 133, 194), 0)
        ball = Rectangle(ball_x, ball_y, 10, 5, (255, 255, 255), 0)

        # drawing the paddle and the ball
        paddle.draw()
        ball.draw()

        # this if statement is used to make the points displayed have the extra 0s in front of it
        if len(str(points)) == 1:
            num = "00"
        elif len(str(points)) == 2:
            num = "0"
        else:
            num = ""

        # drawing the text to the screen
        draw_text(num + str(points), (80, 30), big_font)
        draw_text(str(lives), (490, 30), big_font)

        if not clicked:
            # movement of paddle
            # with a mouse
            # only the x-coordinate can change
            pos = pygame.mouse.get_pos()
            if 650 - (paddle_width - 10) >= (pos[0] - 20) >= 0:
                paddle_x = (pos[0] - 20)

            # initial x and y coordinates of ball
            ball_x = paddle_x + (paddle_width // 2)  # 11 - 639 pixel
            ball_y = paddle_y - 5  # 291 - 349 pixel
        else:
            # movement of paddle
            # with a mouse
            # only the x-coordinate can change
            pos = pygame.mouse.get_pos()
            if 650 - (paddle_width - 10) >= (pos[0] - 20) >= 0:
                paddle_x = (pos[0] - 20)

            # movement of ball
            ball_x += v_x
            ball_y += v_y

            # if ball hits the left wall
            if ball_x <= 10:
                # it reverses the direction
                v_x = - v_x
                # once the ball hits any other surface other than a brick the hit_brick variable will be set to false
                # if the hit_brick variable is false, the ball can collide with another brick.
                # this means that that the ball can only collide with one brick at a time.
                hit_brick = False
                sound_effect("beep.wav")

            # if ball hits the right wall
            elif ball_x >= 630:
                # it starts travelling from right to left
                v_x = - v_x
                hit_brick = False
                sound_effect("beep.wav")

            # if ball hits the ceiling
            elif ball_y <= 30:
                # reversing its direction
                v_y = - v_y
                # once the ball hits the ceiling the paddle will half in size only once
                if not halved:
                    paddle_width = paddle_width // 2
                    halved = True
                hit_brick = False
                sound_effect("beep.wav")

            # if ball hits the paddle
            elif paddle.rect_info.colliderect(ball.rect_info):
                # I need to separate the ball from the paddle by a few pixels once the ball and the paddle collide
                ball_y -= separation

                # the number of collisions with the paddle is incremented
                collisions += 1

                # if distance between corners of the paddle and ball is greater than 75% or less than 25% of paddle width
                # this if statement allows for different types of bouncing to occur
                if abs(ball_x - paddle_x) >= (paddle_width * 0.75) or abs(ball_x - paddle_x) <= (paddle_width * 0.25):
                    # the velocities can only increase (by bouncing off the paddle) up to the maximum value of 1.5
                    if abs(v_y) < 1.5 and abs(v_x) < 1.5:
                        # when hitting corners the ball becomes faster
                        # it also bounces backwards
                        v_y = round(- v_y * 1.03, 5)
                        v_x = round(- v_x * 1.03, 5)
                    else:
                        # reversing the direction of the ball
                        v_y = - v_y
                        v_x = - v_x
                else:
                    # when hitting the middle the ball becomes slower
                    # it also bounces to the opposite wall
                    v_y = round(- v_y * 0.97, 5)
                    v_x = round(v_x * 0.97, 5)

                hit_brick = False
                sound_effect("beep.wav")

            # if ball falls past the paddle
            elif ball_y >= 755:
                sound_effect("end.wav")
                # decrease the number of lives by 1
                lives -= 1
                # reset x and y coordinates of ball
                ball_x = paddle_x + (paddle_width // 2)  # 11 - 639 pixel
                ball_y = paddle_y - 5  # 291 - 349 pixel
                clicked = False
                # to give the player some time to recover
                pygame.time.wait(1700)

            for brick in bricks:
                # if brick collides with ball
                if brick.rect_info.colliderect(ball.rect_info) and not hit_brick:
                    # to separate the ball from the brick
                    if v_y < 0:
                        ball_y += separation
                    else:
                        ball_y -= separation

                    if abs(ball_x - brick.x) >= (brick.width * 0.75) or abs(ball_x - brick.x) <= (brick.width * 0.25):
                        # when hitting corners
                        if abs(v_y) < 1.5 and abs(v_x) < 1.5:
                            v_y = round(- v_y * 1.03, 5)
                            v_x = round(- v_x * 1.03, 5)
                        else:
                            v_y = - v_y
                            v_x = - v_x

                    else:
                        # when hitting the middle
                        v_y = round(- v_y * 0.97, 5)
                        v_x = round(v_x * 0.97, 5)

                    if brick.num_of_hits == 1:
                        bricks.remove(brick)
                    else:
                        brick.num_of_hits -= 1
                        brick.fill_colour = (0,255,0)

                    recovery_bricks.append(brick)

                    # each colour of brick has a different number of points assigned to it.
                    if brick.fill_colour == (163, 30, 10):
                        points += 7
                        # the ball will increase in speed when it comes in contact with the red brick only once
                        if not hit_red:
                            v_x = round(v_x*speed_increase, 5)
                            v_y = round(v_y*speed_increase, 5)
                            hit_red = True
                    elif brick.fill_colour == (194, 133, 10):
                        points += 5
                        # the ball will increase in speed when it comes in contact with the orange brick only once
                        if not hit_orange:
                            v_x = round(v_x * speed_increase, 5)
                            v_y = round(v_y * speed_increase, 5)
                            hit_orange = True
                    elif brick.fill_colour == (10, 133, 51):
                        points += 3
                    elif brick.fill_colour == (194, 194, 41):
                        points += 1

                    # so that it doesn't hit any other bricks
                    hit_brick = True
                    sound_effect("beep.wav")

            # the speed of the ball will increase once it has collided with the paddle 4 and 12 times
            # the collision_4 and collision_12 variables exist so that once the ball has left the paddle,
            # in the interval it takes for the next collision to occur, the ball will not keep speeding up
            if (collisions == 4 and not collision_4) or (collisions == 12 and not collision_12):
                v_x = round(v_x * speed_increase, 5)
                v_y = round(v_y * speed_increase, 5)

                if collisions == 4:
                    collision_4 = True
                elif collisions == 12:
                    collision_12 = True

            # once the player completes the game, the ball will stop moving and a message will be displayed
            if len(bricks) == 0:
                v_x = 0
                v_y = 0
                draw_text("END OF GAME", (90, 300), big_font)


            # once the player loses all their lives they will able to completely restart the game
            if lives == 0:
                # all the bricks that have been hit will be added to the original list again
                bricks = bricks + recovery_bricks
                recovery_bricks = []
                points = 0
                collisions = 0
                # end_of_game() is a function that displays a message to the player
                v_x, v_y = end_of_game()
                lives = 5
                paddle_width = 90

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        # updates the screen to show changes
        pygame.display.update()


main()
pygame.quit()
