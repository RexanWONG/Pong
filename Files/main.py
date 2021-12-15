import pygame, random, os
pygame.font.init()
pygame.mixer.init()
# Display dimensions
width = 800
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')
#Load button images
play_img = pygame.image.load(os.path.join('Buttons','play.png')).convert_alpha()
#ingpongback = pygame.image.load(os.path.join('Pics', 'Table.png'))
exit_img = pygame.image.load(os.path.join('Buttons','Exit.png')).convert_alpha()
class Button():
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self,screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1  and self.clicked == False: #when clicked
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


#Button instances
play_button = Button(100, 200, play_img)
exit_button = Button(600, 200, exit_img)


win = pygame.display.set_mode((width, height))
# left player = rectangle on left
# right player - rectangle on right
left_player = pygame.Rect(0, height / 2 - 35, 20, 70)
right_player = pygame.Rect(780, height / 2 - 35, 20, 70)
ball = pygame.Rect(width / 2 - 8, height / 2 - 8, 16, 16)
background = pygame.Rect(0, 0, 800, 500)
pingpongback = pygame.image.load(os.path.join('Pics', 'Table.png'))
pingpongback = pygame.transform.scale(pingpongback, (width, height))
pygame.mixer.init()
Windows = pygame.mixer.Sound(os.path.join('Audio', 'Windows (1).mp3'))
Music = pygame.mixer.music.load(os.path.join('Track', 'Beat.mp3'))
pygame.mixer.music.play(-1)
scorefont = pygame.font.SysFont('impact', 100)
# Color List:
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 200)
black = (0, 0, 0)
orange = (255, 165, 0)
# Movement 'global variables'
fps = 50
player_speed = 8
x = (-7, 7)
y = (-7, 7)
score_win = 11


# define what keys to use
def handle_movement(keys):
    if keys[pygame.K_q] and left_player.y > 0:
        left_player.y -= player_speed
    if keys[pygame.K_a] and left_player.y + 70 < height:
        left_player.y += player_speed
    if keys[pygame.K_p] and right_player.y > 0:
        right_player.y -= player_speed
    if keys[pygame.K_l] and right_player.y + 70 < height:
        right_player.y += player_speed

    # blit == draw


def draw_winner(winner):
    if winner == 'left':
        wtext = scorefont.render('Left Player wins!', 1, red)
    else:
        wtext = scorefont.render('Right Player wins!', 1, red)
    win.blit(wtext, (width / 2 - wtext.get_width() / 2, height / 2 - wtext.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


def draw_window(lscore, rscore):
    pygame.draw.rect(win, black, background)
    win.blit(pingpongback, (0, 0))
    ltext = scorefont.render('' + str(lscore), 1, red)
    rtext = scorefont.render('' + str(rscore), 1, red)
    title = scorefont.render('Epic Ping Pong Battle', 1, red)
    win.blit(ltext, (250, 40))
    win.blit(rtext, (550, 40))
    pygame.draw.rect(win, red, left_player)
    pygame.draw.rect(win, red, right_player)
    pygame.draw.rect(win, orange, ball)
    pygame.display.update()


# Ball Speed
def ball_movement(x_vel, y_vel, keys, lscore, rscore):
    if x_vel == 0:
        pygame.time.delay(1500)
        x_vel = x[random.randint(0, 1)]
        y_vel = y[random.randint(0, 1)]
    if ball.y < 0:
        y_vel = y_vel * -1
    if ball.y > height - 16:
        y_vel = y_vel * -1
    if ball.x < 0 or ball.x > width - 16:
        if ball.x < 0:
            rscore += 1
        else:
            lscore += 1
        x_vel = 0
        y_vel = 0
        ball.x = (width / 2 - 8)
        ball.y = (height / 2 - 8)
    if left_player.colliderect(ball):
        x_vel = (x_vel * -1) + 1.5
        if keys[pygame.K_q]:
            y_vel += -3
        if keys[pygame.K_a]:
            y_vel += 3
    if right_player.colliderect(ball):
        if keys[pygame.K_p]:
            y_vel += -3
        if keys[pygame.K_l]:
            y_vel += 3
        x_vel = (x_vel * -1) - 1.5
    return (x_vel, y_vel, lscore, rscore)


# Main Function - Fps  (Game loop)
def main():
    x_vel = 0
    y_vel = 0
    lscore = 0
    rscore = 0
    game_ended = False
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(fps)

        if play_button.draw(screen):
            print ('Play')
            run = True
        if exit_button.draw(screen):
            run = False
            print ('Exit')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        keys = pygame.key.get_pressed()
        if lscore == score_win:
            draw_winner('left')
            if not game_ended:
                Windows.play()
                print('SFX played')
                game_ended = True
            continue
        if rscore == score_win:
            draw_winner('right')
            if not game_ended:
                Windows.play()
                print('SFX played')
                game_ended = True
            continue
        handle_movement(keys)
        x_vel, y_vel, lscore, rscore = ball_movement(x_vel, y_vel, keys, lscore, rscore)
        ball.x += x_vel
        ball.y += y_vel

        draw_window(lscore, rscore)


if __name__ == "__main__":
    main()

# return - stops entire function
# break - stops the enclosing loop
# continue - skips rest of code and goes into next time the loop runs


