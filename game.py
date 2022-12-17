import gamebox
import pygame
import math
import random
camera = gamebox.Camera(800,600)
screen = dict()
screen["settings"] = 0
screen["pause"] = 0
screen["play"] = 0
settings = dict()
settings["wasdMovement"] = True
settings["difficulty"] = "medium"
rectangle_image ="rectangle-modified.png"
line_image = "line-removebg-preview.png"
horizontal_image = "horizontal-removebg-preview.png"
circle_image = "circle-modified.png"
lines = dict()
lines["vertical"] = gamebox.from_image(50, 50, line_image)
lines["bottom"] = gamebox.from_image(50, 50, horizontal_image)
lines["top"] = gamebox.from_image(50, 50, horizontal_image)
ball = dict()
ball["ballImage"] = gamebox.from_image(50, 50, circle_image)
player = dict()
AI = dict()
player["playerImage"] = gamebox.from_image(50, 50, rectangle_image)
player["score"] = 0
player["scoreCount"] = 0
AI["AIImage"] = gamebox.from_image(50, 50, rectangle_image)
AI["score"] = 0
AI["scoreCount"] = 0
player["playerImage"].scale_by(.20)
AI["AIImage"].scale_by(.20)
ball["ballImage"].scale_by(.2)
lines["vertical"].scale_by(.82)
def settings_tick(settings):
    """The settings_tick function is a function that does all the drawing for the game's settings screen. It displays
    the settings and the back button. In addition, it sets the controls and the difficulty of the game"""
    camera.clear("black")
    camera.draw("SETTINGS", 100, "white", 400, 100)
    camera.draw("CONTROLS", 25, "white", 400, 200)
    camera.draw("PAUSING: SPACE BAR", 15, "white", 400, 225)
    camera.draw("QUTTING: ESCAPE", 15, "white", 400, 250)
    camera.draw("MOVEMENT:", 15, "white", 290, 275)
    # If the player decides to use WASD movements
    if(settings["wasdMovement"] == True):
        camera.draw("W AND S ", 15, "red", 375, 275)
        camera.draw("UP AND DOWN ARROWS", 15, "white", 500, 275)
    # If the player decides to use Up and Down Arrow Movements
    else:
        camera.draw("W AND S", 15, "white", 375, 275)
        camera.draw("UP AND DOWN ARROWS", 15, "red", 500, 275)
    camera.draw("DIFFICULTY", 25, "white", 400, 325)
    # If the difficulty is medium
    if(settings["difficulty"] == "medium"):
        camera.draw("EASY", 15, "white", 325, 350)
        camera.draw("MEDIUM", 15, "red", 400, 350)
        camera.draw("HARD", 15, "white", 475, 350)
    # If the difficulty is easy
    elif(settings["difficulty"] == "easy"):
        camera.draw("EASY", 15, "red", 325, 350)
        camera.draw("MEDIUM", 15, "white", 400, 350)
        camera.draw("HARD", 15, "white", 475, 350)
    # If the difficulty is hard
    else:
        camera.draw("EASY", 15, "white", 325, 350)
        camera.draw("MEDIUM", 15, "white", 400, 350)
        camera.draw("HARD", 15, "red", 475, 350)
    camera.draw("BACK", 50, "white", 400, 500)
    camera.display()
def hitting_ball(player, ball, AI, settings):
    """The hitting_ball function is a function that allows the ball to bounce once it hits the player or the AI."""
    # If the ball touches the right side of the player, use a physics formula to determine the velocity in the
    # x-direction and the velocity in the y-direction towards the AI.
    if(player["playerImage"].right_touches(ball["ballImage"])):
        intersection = player["playerImage"].center[1] - ball["ballImage"].y
        intersection = intersection / (player["playerImage"].height / 2)
        bounceAngle = intersection * (math.pi/ 3)
        if (settings["difficulty"] == "easy"):
            ball["ballImage"].speedx = 16 * math.cos(bounceAngle)
            ball["ballImage"].speedy = 16 * math.sin(bounceAngle)
        elif (settings["difficulty"] == "medium"):
            ball["ballImage"].speedx = 18 * math.cos(bounceAngle)
            ball["ballImage"].speedy = 18 * math.sin(bounceAngle)
        else:
            ball["ballImage"].speedx = 20 * math.cos(bounceAngle)
            ball["ballImage"].speedy = 20 * math.sin(bounceAngle)
    # If the ball touches the left side of the AI, use a physics formula to determine the velocity in the x-direction
    # and the velocity in the y-direction towards the player.
    elif (AI["AIImage"].left_touches(ball["ballImage"])):
        intersection = AI["AIImage"].center[1] - ball["ballImage"].y
        intersection = intersection / (AI["AIImage"].height / 2)
        bounceAngle = intersection * (math.pi / 3)
        if(settings["difficulty"] == "easy"):
            ball["ballImage"].speedx = -16 * math.cos(bounceAngle)
            ball["ballImage"].speedy = -16 * math.sin(bounceAngle)
        elif(settings["difficulty"] == "medium"):
            ball["ballImage"].speedx = -18 * math.cos(bounceAngle)
            ball["ballImage"].speedy = -18 * math.sin(bounceAngle)
        else:
            ball["ballImage"].speedx = -20 * math.cos(bounceAngle)
            ball["ballImage"].speedy = -20 * math.sin(bounceAngle)
def moving_player(player, keys, settings):
    """The moving_player function is a function that creates the movements for the player during the game"""
    # If the player is at the bottom of the screen, do not allow them to go down anymore. Only allow them to go up.
    if (player["playerImage"].bottom >= 590.0):
        # If the player decides to play with the keys W and S.
        if(settings["wasdMovement"] == True):
            if pygame.K_w in keys:
                player["playerImage"].speedy = -10
            if pygame.K_s in keys:
                player["playerImage"].speedy = 0
        # If the player decides to play with the keys Up-Arrow and Down-Arrow.
        else:
            if pygame.K_UP in keys:
                player["playerImage"].speedy = -10
            if pygame.K_DOWN in keys:
                player["playerImage"].speedy = 0
    # If the player is at the top of the screen, do not allow them to go up anymore. Only allow them to go down.
    elif (player["playerImage"].top <= 9.0):
        # If the player decides to play with the keys W and S.
        if(settings["wasdMovement"] == True):
            if pygame.K_w in keys:
                player["playerImage"].speedy = 0
            if pygame.K_s in keys:
                player["playerImage"].speedy = 10
        # If the player decides to play with the keys Up-Arrow and Down-Arrow.
        else:
            if pygame.K_UP in keys:
                player["playerImage"].speedy = 0
            if pygame.K_DOWN in keys:
                player["playerImage"].speedy = 10
    # If the player is in neither of these positions, allow them to move normally.
    else:
        # If the player decides to play with the keys W and S.
        if(settings["wasdMovement"] == True):
            if pygame.K_w in keys:
                player["playerImage"].speedy = -10
            if pygame.K_s in keys:
                player["playerImage"].speedy = 10
        # If the player decides to play with the keys Up-Arrow and Down-Arrow.
        else:
            if pygame.K_UP in keys:
                player["playerImage"].speedy = -10
            if pygame.K_DOWN in keys:
                player["playerImage"].speedy = 10
def moving_AI(AI, ball, settings):
    """The moving_AI function is a function that creates the movements of the AI during the game."""
    # If the ball is below the bottom part of the AI, move it down
    if (ball["ballImage"].y > AI["AIImage"].bottom):
        if(settings["difficulty"] == "easy"):
            AI["AIImage"].speedy = 8
        elif(settings["difficulty"] == "medium"):
            AI["AIImage"].speedy = 10
        else:
            AI["AIImage"].speedy = 12
    # If the ball is above the top part of the AI, move it up
    elif (ball["ballImage"].y < AI["AIImage"].top):
        if (settings["difficulty"] == "easy"):
            AI["AIImage"].speedy = -8
        elif (settings["difficulty"] == "medium"):
            AI["AIImage"].speedy = -10
        else:
            AI["AIImage"].speedy = -12
    # If the y-position of the ball is near the position of the center part of the AI, stop moving it.
    elif (abs(ball["ballImage"].y - AI["AIImage"].center[1]) <= 10):
        AI["AIImage"].speedy = 0
def play_tick(keys, player, AI, ball, lines, settings):
    """The play_tick function is a function that does all the drawing to play the game and creates the mechanics for
    the game."""
    # If the ball hits the bottom of the screen, bounce back in the opposite y-direction
    if (ball["ballImage"].bottom >= 590.0):
        ball["ballImage"].speedy = -ball["ballImage"].speedy
    # If the ball hits the top of the screen, bounce back in the opposite y-direction
    elif(ball["ballImage"].top <= 9.0):
        ball["ballImage"].speedy = -ball["ballImage"].speedy
    # Mechanics to get the player and the AI to hit the ball
    hitting_ball(player, ball, AI, settings)
    player["playerImage"].speedx = 0
    player["playerImage"].speedy = 0
    camera.clear("black")
    # Mechanics to get the player to move
    moving_player(player, keys, settings)
    initialSpeed = [-7, 7]
    # Randomize the direction of the initial speed of the ball
    speed = initialSpeed[random.randint(0, 1)]
    # If the ball is past the left side of the screen, add the AI score by one
    if(ball["ballImage"].x < 0):
        if(AI["scoreCount"] == 0):
            AI["score"] += 1
            AI["scoreCount"] += 1
        # Wait a little before the ball returns to its starting position
        if(ball["ballImage"].x < -125):
            # If the ball is initially going towards the player, randomize the y-direction of the ball
            if (speed == -7):
                ball["ballImage"].speedx = speed
                ball["ballImage"].speedy = random.randint(speed, 0)
            # If the ball is initially going towards the AI, randomize the y-direction of the ball
            elif (speed == 7):
                ball["ballImage"].speedx = speed
                ball["ballImage"].speedy = random.randint(0, speed)
            # Randomize the starting position of the ball
            ball["ballImage"].center = [400, random.randint(200, 400)]
            AI["scoreCount"] = 0
    # If the ball is past the right side of the screen, add the player score by one
    if(ball["ballImage"].x > 800.0):
        if(player["scoreCount"] == 0):
            player["score"] += 1
            player["scoreCount"] += 1
        # Wait a little before the ball returns to its starting position
        if(ball["ballImage"].x > 950):
            # If the ball is initially going towards the player, randomize the y-direction of the ball
            if (speed == -7):
                ball["ballImage"].speedx = speed
                ball["ballImage"].speedy = random.randint(speed, 0)
            # If the ball is initially going towards the AI, randomize the y-direction of the ball
            elif (speed == 7):
                ball["ballImage"].speedx = speed
                ball["ballImage"].speedy = random.randint(0, speed)
            # Randomize the starting position of the ball
            ball["ballImage"].center = [400, random.randint(200, 400)]
            player["scoreCount"] = 0
    # Mechanics to get the AI to move
    moving_AI(AI, ball, settings)
    AI["AIImage"].move_speed()
    ball["ballImage"].move_speed()
    player["playerImage"].move_speed()
    # Drawing all the objects needed for the game
    camera.draw(AI["AIImage"])
    camera.draw(ball["ballImage"])
    camera.draw(lines["vertical"])
    camera.draw(lines["top"])
    camera.draw(lines["bottom"])
    camera.draw(str(player["score"]), 50, "white", 150, 50)
    camera.draw(str(AI["score"]), 50, "white", 650, 50)
    camera.draw(player["playerImage"])
    camera.display()

def starting_tick():
    """The starting_tick function is a function that does all the drawing for the game's starting screen. It displays
    the title of the game, the game's author, the play button, and the settings button."""
    camera.clear("black")
    camera.draw("PONG", 100, "white", 400, 100)
    camera.draw("PLAY", 50, "white", 160, 340)
    camera.draw("SETTINGS", 50, "white", 600, 340)
    camera.draw("Made by Connor Goodall", 15, "red", 400, 450)
    camera.draw("Created with the help of Professor Luther Tychonievich", 15, "white", 400, 500)
    camera.display()
def end_tick(player, AI, lines):
    """The end_tick function is the function that does all the drawing for the winner of the game. It ends the game
    if the player or AI has a score of 5."""
    # If the player has a score of 5 points, the player wins and the AI loses
    if(player["score"] >= 5):
        camera.draw("YOU WIN", 25, "white", 160, 300)
        camera.draw("AI LOSES", 25, "white", 600, 300)
    # If the AI has a score of 5 points, the AI wins and the player loses
    elif(AI["score"] >= 5):
        camera.draw("YOU LOSE", 25, "white", 160, 300)
        camera.draw("AI WINS", 25, "white", 600, 300)
    # Draw all the objects needed for the game
    camera.draw(player["playerImage"])
    camera.draw(AI["AIImage"])
    camera.draw(str(player["score"]), 50, "white", 150, 50)
    camera.draw(str(AI["score"]), 50, "white", 650, 50)
    camera.draw(lines["top"])
    camera.draw(lines["bottom"])
    camera.draw(lines["vertical"])
    camera.draw("RESTART", 35, "white", 400, 400)
    camera.draw("MAIN MENU", 35, "white", 400, 500)
    camera.display()
def reset(player, AI, ball, lines):
    """The reset function is a function that resets the game to its initial state if the player decides to restart
    or go back to the main menu while playing or after playing the game."""
    # Set all the objects in the game back to the initial positions
    player["playerImage"].center = [50, 300]
    AI["AIImage"].center = [750, 300]
    lines["vertical"].center = [400, 300]
    lines["top"].center = [400, -6.99]
    lines["bottom"].center = [400, 590]
    initialSpeed = [-7, 7]
    # Randomize the direction of the initial speed of the ball
    speed = initialSpeed[random.randint(0, 1)]
    # If the ball is initially going towards the player, randomize the y-direction of the ball
    if(speed == -7):
        ball["ballImage"].speedx = speed
        ball["ballImage"].speedy = random.randint(speed, 0)
    # If the ball is initially going towards the AI, randomize the y-direction of the ball
    elif(speed == 7):
        ball["ballImage"].speedx = speed
        ball["ballImage"].speedy = random.randint(0, speed)
    # Randomize the starting position of the ball
    ball["ballImage"].center = [400, random.randint(200, 400)]
    # Set the player and AI scores back to 0
    player["score"] = 0
    player["scoreCount"] = 0
    AI["score"] = 0
    AI["scoreCount"] = 0
def pause_tick(player, AI, ball, lines):
    """The pause_tick function is a function that does all the drawing when the game is paused. It draws all the
    objects needed for the game."""
    # Draw all the objects needed for the game
    camera.draw(player["playerImage"])
    camera.draw(AI["AIImage"])
    camera.draw(str(player["score"]), 50, "white", 150, 50)
    camera.draw(str(AI["score"]), 50, "white", 650, 50)
    camera.draw(ball["ballImage"])
    camera.draw(lines["vertical"])
    camera.draw(lines["top"])
    camera.draw(lines["bottom"])
    camera.draw("PAUSE", 50, "white", 400, 300)
    camera.draw("BACK", 35, "white", 400, 400)
    camera.draw("MAIN MENU", 35, "white", 400, 500)
    camera.display()
def tick(keys):
    """The tick function is the function that sets the entire game, including the starting screen, the controls screen,
    the two-player mode, and the single-player mode. It determines which portion of the game is being used by seeing
    which key the player pressed (if they pressed any at all)."""
    global screen
    global player
    global lines
    global AI
    global ball
    global settings
    # If the mouse is on the word settings and is left-clicked, go to the settings screen and stay there
    if((pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 449 and pygame.mouse.get_pos()[0] <= 743) and
            (pygame.mouse.get_pos()[1] >= 313 and pygame.mouse.get_pos()[1] <= 353)) or screen["settings"] > 0):
        settings_tick(settings)
        screen["settings"] += 1
        # If the mouse is on the words W and S and is left-clicked, set the up button to W and the down button to S
        if(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 340 and pygame.mouse.get_pos()[0] <= 400) and
            (pygame.mouse.get_pos()[1] >= 265 and pygame.mouse.get_pos()[1] <= 280)):
            settings["wasdMovement"] = True
        # If the mouse is on the words up and down arrows and is left-clicked, set the up button to the up-arrow and
        # the down button to the down-arrow
        elif(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 410 and pygame.mouse.get_pos()[0] <= 585)
             and (pygame.mouse.get_pos()[1] >= 265 and pygame.mouse.get_pos()[1] <= 280)):
            settings["wasdMovement"] = False
        # If the mouse is on the word easy and is left-clicked, set the difficulty of the game to easy
        if(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[0] <= 340) and
            (pygame.mouse.get_pos()[1] >= 340 and pygame.mouse.get_pos()[1] <= 355)):
            settings["difficulty"] = "easy"
        # If the mouse is on the word medium and is left-clicked, set the difficulty of the game to medium
        elif(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 365 and pygame.mouse.get_pos()[0] <= 430) and
            (pygame.mouse.get_pos()[1] >= 340 and pygame.mouse.get_pos()[1] <= 355)):
            settings["difficulty"] = "medium"
        # If the mouse is on the word hard and is left-clicked, set the difficulty of the game to hard
        elif(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 450 and pygame.mouse.get_pos()[0] <= 495) and
            (pygame.mouse.get_pos()[1] >= 340 and pygame.mouse.get_pos()[1] <= 355)):
            settings["difficulty"] = "hard"
        # If the mouse is on the word back and is left-clicked, go back to the main screen and stay there
        if(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 320 and pygame.mouse.get_pos()[0] <= 470) and
            (pygame.mouse.get_pos()[1] >= 470 and pygame.mouse.get_pos()[1] <= 510)):
            screen["settings"] = 0
            starting_tick()
    # If the mouse is on the word back and is left-clicked, go to the game screen and stay there until the AI or player
    # scores 5 points
    elif((pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 80 and pygame.mouse.get_pos()[0] <= 230) and
          (pygame.mouse.get_pos()[1] >= 310 and pygame.mouse.get_pos()[1] <= 350)) or (screen["play"] > 0 and
        player["score"] < 5 and AI["score"] < 5 and pygame.K_SPACE not in keys)):
        play_tick(keys, player, AI, ball, lines, settings)
        screen["play"] += 1
    # If the player presses the space bar button during the game, pause the game
    elif((screen["play"] > 0 and player["score"] < 5 and AI["score"] < 5 and pygame.K_SPACE in keys) or
         (screen["pause"] > 0)):
        pause_tick(player, AI, ball, lines)
        screen["play"] = 0
        screen["pause"] += 1
        # If the mouse is on the words main menu and is left-clicked, go back to the starting screen of the game
        if(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 285 and pygame.mouse.get_pos()[0] <= 500) and
                (pygame.mouse.get_pos()[1] >= 480 and pygame.mouse.get_pos()[1] <= 510)):
            screen["pause"] = 0
            reset(player, AI, ball, lines)
        # If the mouse is on the word back and is left-clicked, go back to the game
        elif(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 345 and pygame.mouse.get_pos()[0] <= 450) and
                (pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 410)):
            screen["pause"] = 0
            screen["play"] += 1
    # If the player or AI has a score above 5 points, show them the winner of the game
    elif(player["score"] >= 5 or AI["score"] >= 5):
        end_tick(player, AI, lines)
        # If the mouse is on the word restart and is left-clicked, restart the game for the player
        if(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[0] <= 480) and
                (pygame.mouse.get_pos()[1] >= 380 and pygame.mouse.get_pos()[1] <= 410)):
            reset(player, AI, ball, lines)
        # If the mouse is on the word main menu and is left-clicked, go back to the start screen
        elif(pygame.mouse.get_pressed()[0] and (pygame.mouse.get_pos()[0] >= 285 and pygame.mouse.get_pos()[0] <= 500) and
                (pygame.mouse.get_pos()[1] >= 480 and pygame.mouse.get_pos()[1] <= 510)):
            screen["play"] = 0
            reset(player, AI, ball, lines)
    else:
        starting_tick()
reset(player, AI, ball, lines)
gamebox.timer_loop(30, tick)