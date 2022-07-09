import random
import pygame
import anims
import datastructs
import threading
import time
from pygame import mixer
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1000, 600
FONTSIZE = 12
SECONDFONTSIZE = 15
PLAYERLENGTH = FONTSIZE+3
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()
#---------------------------------------------Threads:
thread_list = []
def add_thread(thread):
    global thread_list
    thread_list.append(thread)
def end_threads():
    global thread_list
    pass

#FONT------------------------------------------
font = pygame.font.SysFont("Consolas", FONTSIZE)
second_font = pygame.font.SysFont("Consolas", SECONDFONTSIZE)
player_text = font.render('', True,"white")
dialogue_text = font.render('', True,"white")
player_color = (255,255,255)
#PLAYER RENDERING.
def render_multi_line(text, x, y, fsize):
    lines = text.splitlines()
    global player_text
    for i, l in enumerate(lines):
        #screen.blit(font.render(l, 0, "white"), (x, y + fsize * i))
        player_text = font.render(l, 0, player_color)
        screen.blit(player_text, (x, y + fsize * i))

####################################-------------
#-------------------TYPE WRITER-----------------#
# type writer is going to be using a dialogue queue
# methods that want stuff to be written on the screen
# add their texts to the type writing que.
#
###########################################---Thread based code here.
# current_dialogue = current_dialogue + text[current_dialougue_num]
#             dialogue_text = second_font.render(current_dialogue, 0, "yellow")

dialPos = (20, 500)


screen_typing_q = datastructs.queue()
dialogue_thread_working = False
dialogue_delay = 1.5  # secs
dialogue_char_delay = 0.05  # secs
def addDialogue(text):
    global dialogue_thread_working
    global screen_typing_q
    screen_typing_q.add_to_q(text)
    if dialogue_thread_working is True:
        return
    t = threading.Thread(target=typeWriteThreadManager)
    add_thread(t)
    dialogue_thread_working = True
    t.start()
def typeWriteThreadManager():
    print("entered manager dialogue")
    global dialogue_text
    global dialogue_delay
    global screen_typing_q
    global dialogue_thread_working
    popped_text = screen_typing_q.pop_from_q()
    while popped_text is not None:
        typeWrite(popped_text)
        time.sleep(dialogue_delay)
        popped_text = screen_typing_q.pop_from_q()
    dialogue_thread_working = False
    dialogue_text = second_font.render('', 0, "yellow")
def typeWrite(text):
    global dialogue_text
    global dialogue_char_delay
    for i in range(len(text)):
        dialogue_text = second_font.render(text[0:i+1], 0, "yellow")
        if text[i] != ' ':
            time.sleep(dialogue_char_delay)

    return

#----------------------------------------------
####################################################-------------
####################################################-------------
#-------------PLAYER------------------------#

normal_color = 'white'
crazyColor = False
player_pos_x = 200
player_pos_y = 200

#for collisions and more
real_player_pos_x = 200
real_player_pos_y = 200
#-----------------------
move_cooldown = 1
strech_cooldown = 1
color_cooldown = 8

#----Speed------
movement_speed = 5
strech_speed = 3
#-----------------
max_strech = PLAYERLENGTH * 3
def player_move(key):
    global player_pos_x
    global player_pos_y
    global real_player_pos_x
    global real_player_pos_y
    if pygame.time.get_ticks() % move_cooldown == 0:
        if key == pygame.K_RIGHT:
            player_pos_x += movement_speed
        if key == pygame.K_LEFT:
            player_pos_x -= movement_speed
        if key == pygame.K_UP:
            player_pos_y -= movement_speed
        if key == pygame.K_DOWN:
            player_pos_y += movement_speed
    real_player_pos_x = player_pos_x
    real_player_pos_y = player_pos_y

def playerStrech(key):
    global player_pos_y
    global PLAYERLENGTH
    global crazyColor
    if PLAYERLENGTH > max_strech:
        PLAYERLENGTH -= strech_speed
        player_pos_y += strech_speed*4
        return
    if PLAYERLENGTH < -max_strech:
        PLAYERLENGTH += strech_speed
        player_pos_y -= strech_speed*4
        return
    if abs(PLAYERLENGTH) > max_strech*0.75:
        crazyColor = True
    else:
        crazyColor = False
    if pygame.time.get_ticks() % strech_cooldown == 0:
        if key == pygame.K_w:
            player_pos_y -= strech_speed*4
            PLAYERLENGTH += strech_speed
        if key == pygame.K_s:
            player_pos_y += strech_speed*4
            PLAYERLENGTH -= strech_speed

############animation#######################################
#######################################---------------------
#######   PLAYER WALK ANIMATION   ##########-----------------

strToRenderWalk = anims.player_walk[0]
last_player_walk = 0
j = 0
def player_shoot_image():
    global strToRenderWalk
    strToRenderWalk = anims.player_hand_strech
def player_idle():
    global strToRenderWalk
    strToRenderWalk = anims.player_walk[0]
def player_walk_anim():
    global last_player_walk
    global j
    global strToRenderWalk
    # print(j)
    now = pygame.time.get_ticks()
    cooldown = 50
    if now - last_player_walk > cooldown:
        if j >= 5:
            j = 0
        j += 1
        strToRenderWalk = anims.player_walk[j]
        last_player_walk = now
def playerColor(spec):
    global player_color
    if pygame.time.get_ticks() % color_cooldown == 0:
        if spec is None:
            player_color = (random.randrange(50,250),random.randrange(50,250),random.randrange(50,250))
        else:
            player_color = spec

#####----------------ARROW------------
arrow = None
arrow_pos = [real_player_pos_x,real_player_pos_y]
can_throw_arrow = True
def throwArrow():
    global arrow_pos

    if can_throw_arrow:
        arrow_pos = [player_pos_x,player_pos_y]
        t = threading.Thread(target=arrow_throw)
        t.start()

def arrow_throw():
    global arrow_pos
    global arrow
    global can_throw_arrow
    can_throw_arrow = False
    t = threading.Thread(target=alter_arrow_pos)
    t.start()
    color = 0
    for i in range(20):
        color += 1
        h = 50+color*10 if 50+color*10 < 255 else 255
        h2 = 255-color*10 if 255-color*10 < 0 else 0
        arrow = font.render(anims.arrow_throw[i%4], 0, (0,h,h2))
        time.sleep(0.05)
    can_throw_arrow = True
    for i in range(len(anims.arrow_burned)):
        h = 50 + color * 10 if 50 + color * 10 < 255 else 255
        h2 = 255 - color * 10 if 255 - color * 10 < 0 else 0
        arrow = font.render(anims.arrow_burned[i % len(anims.arrow_burned)], 0, (0, h, h2))
        time.sleep(0.1)
        color-=1
    player_idle()
    return
def alter_arrow_pos():
    global can_throw_arrow
    while can_throw_arrow is False:
        arrow_pos[0] += 1
        time.sleep(0.001)
    return

############################################--------------------
######### KEYS #############################--------------------

def keysAction():
    pressed = pygame.key.get_pressed()
    ###PRESSED:
    ##MOVEMENT-------
    if pressed[pygame.K_RIGHT]:
        player_walk_anim()      # the movement animation
        player_move(pygame.K_RIGHT)     # the general movement method
    if pressed[pygame.K_LEFT]:
        player_walk_anim()
        player_move(pygame.K_LEFT)
    if pressed[pygame.K_UP]:
        player_walk_anim()
        player_move(pygame.K_UP)
    if pressed[pygame.K_DOWN]:
        player_walk_anim()
        player_move(pygame.K_DOWN)
    #STRECHING
    if pressed[pygame.K_w]:
        playerStrech(pygame.K_w)
    if pressed[pygame.K_s]:
        playerStrech(pygame.K_s)
    #-------------------------
    ##EVENTS:
    for event in pygame.event.get():
        #QUIT
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #KEY DOWN----------------------------
        if event.type == pygame.KEYDOWN:
            #Escape
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                addDialogue("hello i'm a robot")
                addDialogue("press Q to see me shooting lasers")
                addDialogue("...")
            # 2.shoot arrow
            if event.key == pygame.K_q:
                throwArrow()
                player_shoot_image()
            # ----MOVEMENT----
        #KEY UP---------------------------
        if event.type == pygame.KEYUP:
            #----MOVEMENT----
            #1.Right
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                player_idle()


#MUSIC-----------------------------------------

################################################---------------
###################################----------------------------

def printeverysec(text):
    for i in range(len(text)):
        print(text[i])
        time.sleep(4)

# x = threading.Thread(target=printeverysec, args=('hello worlddd',))
# x.start()

if __name__ == '__main__':
    while True:
        screen.fill((23, 28, 59))
        #things that update-------------------
        keysAction()
       # print(pygame.time.get_ticks())
        #player:---------------------------------
        if crazyColor:
            playerColor(None)
        else:
            playerColor(normal_color)
        render_multi_line(strToRenderWalk, player_pos_x, player_pos_y, PLAYERLENGTH)
        # dialogueTypewrite("Hello every one, my name is robot man 2")
        #----------------------------------------
        # pygame.display.flip()
        #DIALOGUE:------
        screen.blit(dialogue_text, dialPos)
        if arrow is not None:
            screen.blit(arrow, (arrow_pos[0], arrow_pos[1]))
        # print(screen_typing_q.size)
        #---------------
        pygame.display.update()
        clock.tick(60)
