############################################################
# Project 4 - KIRBY PONG
############################################################
# Name:   Dave Alger
# Date:   15 OCT 2014
# Follow: https://twitter.com/DaveAlger
############################################################

import simplegui
import random
import math

############################################################
# 1. Initialize global variables
############################################################
W = 600
H = 400

MSG = ""
T = 0
T2 = 0
TXT = [
"#FFECFF",
"#F9ECFF",
"#FFDAFF",
"#F3DAFF",
"#FFC8FF",
"#EDC8FF",
"#FFBDFF",
"#EABDFF",
"#FFB6FF",
"#E7B6FF",
"#EEAAEE",
"#D8AAEE",
"#CD92CD",
"#BA92CD",
"#8B638B",
"#7E638B"
]

turbo_score = 0
turbo_high = 0

NEW_TURBO_RECORD = "NEW TURBO RECORD"
TURBO_MODE = "TURBO  MODE"

GAME_OVER = False
POINTS_TO_WIN = 10

kirby_dance = [
". . . . . . . (>'-')> . . . . . .",
". . . . . . . <('-'<) . . . . . .",
". . . . . . .^(' - ')^. . . . . ."
]

controls = {
    "p1_up": simplegui.KEY_MAP["w"],
    "p1_down": simplegui.KEY_MAP["s"],
    "p2_up": simplegui.KEY_MAP["up"],
    "p2_down": simplegui.KEY_MAP["down"]
}

ball = {}

pad1 = {}

pad2 = {}

############################################################
# 2. Define helper functions
############################################################
def new_game():
    global stage,ball,pad1,pad2,MSG,T,turbo_high,turbo_score, GAME_OVER
    stage = {
        "width": W,
        "height": H,
        "pad_width": 20,
        "pad_height": 100,
        "fire_mode": False,
        "kirby_mode": False,
        "bg_music_on": True
    }
    
    ball = {
        "position": [stage["width"]/2,stage["height"]/2],
        "radius": 15,
        "color": "lightred",
        "vector": [0, 0],
        "step": 1,
        "max_step": 20,
        "direction": 1,
        "show_trail": False,
        "history": [[0,0],[0,0],[0,0],[0,0],[0,0]]
    }
    
    pad1 = {
        "position": [0,stage["height"]/2-stage["pad_height"]/2],
        "key": -1,
        "vector": [0, 0],
        "step": 1,
        "hit": 0,
        "score": 0,
        "color": "#3388ff"
    }
    
    pad2 = {
        "position": [stage["width"],stage["height"]/2-stage["pad_height"]/2],
        "key": -1,
        "vector": [0, 0],
        "step": 1,
        "hit": 0,
        "score": 0,
        "color": "#ff4422"
    }
    timer_bg_music.stop()
    timer_bg_music.start()
    turbo_score = 0
    bg_music_loop()
    GAME_OVER = False
    spawn_ball()
    
def spawn_ball():
    global turbo_score
    turbo_score = 0
    ball["position"] = [stage["width"]/2,stage["height"]/2]
    update_vector(0)
    ball["show_trail"] = False
    stage["fire_mode"] = False
    stage["kirby_mode"] = False
    
def pad_hit(y, p_t):
    f = ball["radius"] * 0.666
    p_t = p_t - f
    p_h = stage["pad_height"] + 2 * f
    
    if y >= p_t and y <= p_t + p_h * 0.333:
        return 1
    elif y >= p_t + p_h * 0.333 and y <= p_t + p_h * 0.666:
        return 2
    elif y >= p_t + p_h * 0.666 and y <= p_t + p_h:
        return 3
    else:
        return 0
    
def init_trail():
    global MSG
    stage["fire_mode"] = True
    stage["kirby_mode"] = True
    ball["history"][4] = [ball["position"][0],ball["position"][1]]
    ball["history"][3] = [ball["position"][0],ball["position"][1]]
    ball["history"][2] = [ball["position"][0],ball["position"][1]]
    ball["history"][1] = [ball["position"][0],ball["position"][1]]
    ball["history"][0] = [ball["position"][0],ball["position"][1]]
    MSG = TURBO_MODE
    timer_txt.start()
        
def check_paddle():
    ball["vector"][0] += 1
    
    if ball["vector"][0] > 12:
        ball["vector"][0] = 12
    
    if not(ball["show_trail"]) and ball["vector"][0] > 6:
        init_trail()
        ball["show_trail"] = True
    
    if ball["direction"] == -1:
        pad2["hit"] = pad_hit(ball["position"][1],pad2["position"][1])
        
        if pad2["hit"] != 0:
            update_vector(pad2["hit"])
            snd_ping()
        else:
            update_score(1)
    else:
        pad1["hit"] = pad_hit(ball["position"][1],pad1["position"][1])
        
        if pad1["hit"] != 0:
            update_vector(pad1["hit"])
            snd_pong()
        else:
            update_score(2)

def check_ball():
    if (ball["position"][1] <= ball["radius"]) or (ball["position"][1] >= stage["height"] - ball["radius"]):
        ball["vector"][1] = -ball["vector"][1]
        snd_wall()
    
    if (ball["position"][0] <= ball["radius"] + stage["pad_width"]/2) or (ball["position"][0] >= stage["width"] - ball["radius"] - stage["pad_width"]/2):
        ball["direction"] *= -1
        check_paddle()

def update_ball():
    ball["position"][0] += ball["vector"][0] * ball["direction"]
    ball["position"][1] += ball["vector"][1]
    check_ball()

def update_score(player):
    global turbo_high, turbo_score, MSG, GAME_OVER
    snd_miss()
    
    if stage["kirby_mode"] and turbo_score > turbo_high:
        turbo_high = turbo_score
        turbo_score = 0
        MSG = NEW_TURBO_RECORD
        snd_cheer()
        timer_txt.start()
        lbl_high.set_text("TURBO RECORD: "+str(turbo_high))
    
    if player == 1:
        pad1["score"] += 1
    elif player == 2:
        pad2["score"] += 1
        
    if pad1["score"] >= POINTS_TO_WIN or pad2["score"] >= POINTS_TO_WIN:
        stage["kirby_mode"] = False
        stage["fire_mode"] = False
        GAME_OVER = True
        snd_cheer()
    else:
        spawn_ball()
    
def draw_pad(canvas,position,velocity,color):
    if (stage["fire_mode"]):
        color = "#cc66cc"
    position[1] += velocity[1]
    if position[1] < 0:
       position[1] = 0
    elif position[1] > stage["height"]-stage["pad_height"]:
       position[1] = stage["height"]-stage["pad_height"]
    canvas.draw_line(position,[position[0],position[1]+stage["pad_height"]],stage["pad_width"],color)

def update_vector(kind):
    if (kind == 0):
        ball["vector"] = [2, -random.randrange(1,4)]
    elif (kind == 1):
        if (ball["vector"][1] >= -3):
            ball["vector"][1] -= random.randrange(0,2)
        else:
            ball["vector"][1] += random.randrange(0,2)
    elif (kind == 2):
        if (random.random() >= 0.1):
            ball["vector"][1] += random.randrange(0,2)
    elif (kind == 3):
        if (ball["vector"][1] <= 3):
            ball["vector"][1] += random.randrange(0,2)
        else:
            ball["vector"][1] -= random.randrange(0,2)
    if ball["vector"][1] == 0:
        if (random.random() >= 0.5):
            ball["vector"][1] = 1
        else:
            ball["vector"][1] = -1
            
def draw_ball(canvas):
    if (ball["show_trail"]):
        canvas.draw_circle(ball["history"][4], ball["radius"]-6, 1, "#ccaacc", "#110011")
        canvas.draw_circle(ball["history"][3], ball["radius"]-3, 1, "#ccaacc", "#330033")
        canvas.draw_circle(ball["history"][2], ball["radius"], 1, "#ccaacc", "#663366")
        canvas.draw_circle(ball["history"][1], ball["radius"]+5, 1, "#ffccff", "#996699")
        canvas.draw_circle(ball["history"][0], ball["radius"]+10, 1, "#ffccff", "#cc88cc")
    else:
        canvas.draw_circle(ball["position"], ball["radius"], 1, "#ffffff", "#eeeeee")
    
    if True: #stage["kirby_mode"]:
        center_source = [30,30]
        width_height_source = [60,60]
        center_dest = ball["position"]
        width_height_dest = [60,60]
        
        rotation = ball["position"][0] / 15
        
        canvas.draw_image(kirby, center_source, width_height_source, center_dest, width_height_dest, rotation)

def draw_dotted_line(canvas):
    x = 0
    while x < stage["height"]:
        if (stage["fire_mode"]):
            canvas.draw_line([stage["width"] / 2, x],[stage["width"] / 2, x + 5], 3, "#cc99cc")
        else:
            canvas.draw_line([stage["width"] / 2, x],[stage["width"] / 2, x + 5], 3, "#cccccc")
        x += 10

def draw_turbo_score(canvas):
    global turbo_score

    if stage["kirby_mode"]:
        m = 17
        if turbo_score > 9:
            m = 32
        else:
            m = 17
        c = "#442244"
        c2 = "#442244"
        if T2 > 0:
            c = TXT[T2]
            c2 = "#442244"
        else:
            c = "#442244"
            c2 = "#ffccff"
        canvas.draw_circle([stage["width"]/2,stage["height"]/2], 50, 4, "#ffccff", c)
        canvas.draw_text(str(turbo_score), [stage["width"]/2 - m,stage["height"]/2 + 20], 60, c2, "monospace")

def draw_msg(canvas):
    if stage["kirby_mode"]:
        canvas.draw_text(MSG, [stage["width"]*0.25, stage["height"] * 0.3], 40, TXT[T], "sans-serif")
    elif MSG == NEW_TURBO_RECORD:
        canvas.draw_text(MSG, [90, stage["height"] * 0.5], 40, TXT[T], "sans-serif")

def draw_scores(canvas):
    if (stage["fire_mode"]):
        canvas.draw_text(str(pad1["score"]), [stage["width"]*0.25, 60], 50, "#cc66cc", "sans-serif")
        canvas.draw_text(str(pad2["score"]), [stage["width"]*0.75, 60], 50, "#cc66cc", "sans-serif")
    else:
        canvas.draw_text(str(pad1["score"]), [stage["width"]*0.25, 60], 50, pad1["color"], "sans-serif")
        canvas.draw_text(str(pad2["score"]), [stage["width"]*0.75, 60], 50, pad2["color"], "sans-serif")

def snd_ping():
    global turbo_score
    if stage["kirby_mode"]:
        sound_bump.rewind()
        sound_bump.play()
        turbo_score += 1
        timer_turbo_hit.start()
    else:
        sound_ping.rewind()
        sound_ping.play()

def snd_pong():
    global turbo_score
    if stage["kirby_mode"]:
        sound_bump.rewind()
        sound_bump.play()
        turbo_score += 1
        timer_turbo_hit.start()
    else:
        sound_pong.rewind()
        sound_pong.play()
        
def snd_wall():
    if stage["kirby_mode"]:
        sound_wall.rewind()
        sound_wall.play()
    else:
        sound_wall.rewind()
        sound_wall.play()

def snd_miss():
    sound_miss.rewind()
    sound_miss.play()
    
def snd_cheer():
    sound_cheer.rewind()
    sound_cheer.play()
    
    
############################################################
# 3. Define classes
############################################################


############################################################
# 4. Define event handlers
############################################################
def draw(c):
    if stage["kirby_mode"]:
        c.draw_image(bg_pink, [stage["width"]/2,stage["height"]/2], [stage["width"],stage["height"]], [stage["width"]/2,stage["height"]/2], [stage["width"],stage["height"]], 0)
    else:
        c.draw_image(bg_green, [stage["width"]/2,stage["height"]/2], [stage["width"],stage["height"]], [stage["width"]/2,stage["height"]/2], [stage["width"],stage["height"]], 0)
    
    draw_dotted_line(c)
    draw_scores(c)
    
    if not(GAME_OVER):
        draw_pad(c,pad1["position"],pad1["vector"],pad1["color"])
        draw_pad(c,pad2["position"],pad2["vector"],pad2["color"])
        draw_turbo_score(c)
        draw_ball(c)
    
        update_ball()
    
        if MSG != "":
            draw_msg(c)
    else:
        if pad1["score"] >= POINTS_TO_WIN:
            c.draw_text("Blue Wins!", (190, 200), 50, pad1["color"], "sans-serif")
        else:
            c.draw_text("Red Wins!", (200, 200), 50, pad2["color"], "sans-serif")
   
def tick():
    if stage["kirby_mode"]:
        lbl_kirby.set_text(kirby_dance[2])
    else:
        if ball["direction"] == 1:
            lbl_kirby.set_text(kirby_dance[0])
        else:
            lbl_kirby.set_text(kirby_dance[1])
    
    ball["history"][4] = ball["history"][3]
    ball["history"][3] = ball["history"][2]
    ball["history"][2] = ball["history"][1]
    ball["history"][1] = ball["history"][0]
    ball["history"][0] = [ball["position"][0],ball["position"][1]]
    
    if not(pad1["key"] == -1):
        pad1["step"] += 1
        if pad1["step"] > ball["max_step"]:
            pad1["step"] = ball["max_step"]
        keydown(pad1["key"])
        
    if not(pad2["key"] == -1):
        pad2["step"] += 1
        if pad2["step"] > ball["max_step"]:
            pad2["step"] = ball["max_step"]
        keydown(pad2["key"])

def keydown(key):
    if key == controls["p2_up"]:
        pad2["vector"][1] = -pad2["step"]
        pad2["key"] = key
    elif key == controls["p2_down"]:
        pad2["vector"][1] = pad2["step"]
        pad2["key"] = key
    elif key == controls["p1_up"]:
        pad1["vector"][1] = -pad1["step"]
        pad1["key"] = key
    elif key == controls["p1_down"]:
        pad1["vector"][1] = pad1["step"]
        pad1["key"] = key


def turbo_hit_loop():
    global T2
    T2 += 1
    if T2 >= len(TXT):
        timer_turbo_hit.stop()
        T2 = 0
        
def text_loop():
    global T, MSG
    T += 1
    if T >= len(TXT):
        timer_txt.stop()
        T = 0
        MSG = ""
        
def bg_music_loop():
    bg_music.rewind()
    bg_music.play()
    
def keyup(key):
    if key == controls["p2_up"] or key == controls["p2_down"]:
        pad2["step"] = 1
        pad2["vector"][1] = 0
        pad2["key"] = -1
    elif key == controls["p1_up"] or key == controls["p1_down"]:
        pad1["step"] = 1
        pad1["vector"][1] = 0
        pad1["key"] = -1

def on_music():
    if stage["bg_music_on"]:
        stage["bg_music_on"] = False
        bg_music.set_volume(0.0)
        btn_music.set_text("Turn Music ON")
    else:
        stage["bg_music_on"] = True
        bg_music.set_volume(0.7)
        btn_music.set_text("Turn Music OFF")

def on_reset():
    global turbo_high
    turbo_high = 0     
    lbl_high.set_text("^^^^^^^^^^^^^^^^^^^")
    new_game()

def on_new():
    new_game()
    
############################################################
# 5. Create frame
############################################################
frame = simplegui.create_frame("Kirby Pong", W, H, 150)
kirby = simplegui.load_image("http://davealger.com/python/img/kirby.png")
bg_green = simplegui.load_image("http://davealger.com/python/img/green.jpg")
bg_pink = simplegui.load_image("http://davealger.com/python/img/pink.jpg")

############################################################
# 6. Register event handlers
############################################################
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

lbl_kirby = frame.add_label(kirby_dance[0])
frame.add_label(" ")
lbl_high = frame.add_label("^^^^^^^^^^^^^^^^^^^")
frame.add_label(" ")
btn_reset = frame.add_button("Reset", on_reset, 146)
btn_new = frame.add_button("New Game", on_new, 146)
btn_music = frame.add_button("Turn Music OFF", on_music, 146)
frame.add_label("___________________")
frame.add_label(" ")
frame.add_label("Instructions: ")
frame.add_label("Blue player use the 'w' and 's' keys.")
frame.add_label(" ")
frame.add_label("Red player use the up and down arrow keys.")
frame.add_label(" ")
frame.add_label("First one to 10 wins the game!")
frame.add_label("___________________")
timer = simplegui.create_timer(50, tick)
timer_txt = simplegui.create_timer(150, text_loop)
timer_turbo_hit = simplegui.create_timer(20, turbo_hit_loop)
timer_bg_music = simplegui.create_timer(54000, bg_music_loop)

bg_music = simplegui.load_sound("http://pygame.org/music/zanthor-grass.mp3")
bg_music.set_volume(0.7)

sound_bump = simplegui.load_sound("http://mariomedia.net/music/Nintendo%20Gamecube/Luigi's%20Mansion/013%20-%20Kazumi%20Totaka%3B%20Shinobu%20Tanaka%20-%20End%20of%20Training.mp3")
sound_wall = simplegui.load_sound("http://davealger.com/apps/jthump/instruments/drums/41.ogg")
sound_ping = simplegui.load_sound("http://davealger.com/apps/jthump/instruments/drums/42.ogg")
sound_pong = simplegui.load_sound("http://davealger.com/apps/jthump/instruments/drums/43.ogg")
sound_miss = simplegui.load_sound("http://davealger.com/apps/jthump/instruments/drums/46.ogg")
sound_cheer = simplegui.load_sound("http://davealger.com/python/snd/kid_cheer.ogg")

############################################################
# 7. Start frame and timers
############################################################
frame.start()
timer.start()
new_game()
