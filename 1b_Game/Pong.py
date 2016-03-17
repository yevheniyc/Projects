"""
    Pong.py - Yevheniy Chuba - Spring 2014
    Implementation of classic arcade game Pong. Enjoy: http://www.codeskulptor.org/#user30_SsWb6yzDfo7EUyz.py
    
    Although we used class-specific CodeSculptor for graphics, most of the methods
    and the rest of the concepts are similar if not the same in other Python librararies, 
    such as Pygame.
    Learned to:
        - interact with keyboard inputs
        - draw frames and objects on canvas
        - implement velocity, direction, angles
"""

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]

paddle2_vel = [0,0]
paddle1_vel = [0,0]
glob_paddle_vel = 3
ball_vel = [2,-1]

paddle1_pos = [PAD_WIDTH/2,160]
paddle2_pos = [WIDTH-PAD_WIDTH/2, 160]


score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, paddle2_vel, paddle1_vel, paddle1_pos, paddle2_pos # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    paddle2_vel = [0,0]
    paddle1_vel = [0,0]
    paddle1_pos = [PAD_WIDTH/2,160]
    paddle2_pos = [WIDTH-PAD_WIDTH/2, 160]
    
    # check if going to the right is true - is yes: through the ball to the left
    if RIGHT: 
        ball_vel = [2,-1]
    else: 
        ball_vel = [-2,-1]


# define event handlers
def new_game():
    # when clicking "Restart" button, reinitiate the game 
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel  # these are numbers
    global score1, score2  # these are ints
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    paddle1_pos = [PAD_WIDTH/2,160]
    paddle2_pos = [WIDTH-PAD_WIDTH/2, 160]
    score1 = 0
    score2 = 0
    ball_vel = [2,-1]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, RIGHT, BALL_RADIUS
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    #####################################################################################
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] = paddle1_pos[1] + paddle1_vel[1]
    paddle2_pos[1] = paddle2_pos[1] + paddle2_vel[1]
    
    # make sure the paddles do not move beyond vertical limits
    if paddle1_pos[1] <= 0 or paddle1_pos[1] >= HEIGHT-PAD_HEIGHT: 
        paddle1_vel[1] = 0
    
    if paddle2_pos[1] <= 0 or paddle2_pos[1] >= HEIGHT-PAD_HEIGHT: 
        paddle2_vel[1] = 0
    ##################################################################################### 
        
    # check if the ball is touching the upper/bottom bounderies - reflect
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT -1 - BALL_RADIUS):
       ball_vel[1] = - ball_vel[1]
        
    
    ################################################ 
    # Check if the ball hits a left/right paddle and reflect
    # Make sure to account for PAD_WIDTH from both directions, if the ball is in the gutter
    if (ball_pos[0]+20) >= (WIDTH-PAD_WIDTH) and ball_pos[1] >=paddle2_pos[1] and ball_pos[1] <= (paddle2_pos[1]+78):
        ball_vel[0] = - ball_vel[0]*1.2
    elif ball_pos[0] <= BALL_RADIUS+8 and ball_pos[1] >=paddle1_pos[1] and ball_pos[1] <= (paddle1_pos[1]+78):
        ball_vel[0] = - ball_vel[0]*1.2
    elif ball_pos[0] < (BALL_RADIUS+5) or ball_pos[0] > (WIDTH - BALL_RADIUS-5): 
        if ball_pos[0] > 300: 
            score1 += 1
            RIGHT = False
        else: 
            score2 +=1
            RIGHT = True
        ball_vel[0] = 0
        ball_vel[1] = 0
        spawn_ball(RIGHT) 
    
    ################################################
   
    
    # draw paddles
    canvas.draw_line (paddle1_pos, [paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line (paddle2_pos, [paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_text (str(score1), [100, 50], 40, 'White')
    canvas.draw_text (str(score2), [500, 50], 40, 'White')
    # draw scores


# keyup and down handlers will keep a record of what is going on with the paddles
def keydown(key):
    # the paddle will move in constant velocity
    global paddle1_vel, paddle2_vel, glob_paddle_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += glob_paddle_vel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= glob_paddle_vel
    elif key==simplegui.KEY_MAP["s"]: 
        paddle1_vel[1] += glob_paddle_vel
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= glob_paddle_vel
   
def keyup(key):
    # the paddle will stop its motion
    global paddle1_vel, paddle2_vel, glob_paddle_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]: 
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button1 = frame.add_button('Restart', new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
frame.start()
