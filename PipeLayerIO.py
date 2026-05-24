import turtle
import time
import random

delay = 0.1

#screen set up
window = turtle.Screen()
window.title("PipeLayer.io")
window.bgcolor("#009dc4")
window.setup(width=600, height=600)
window.tracer(0)

#! snakehead
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("#D98B09")
head.penup()
head.goto(0,0)
head.direction = "stop"

#food
apple = turtle.Turtle()
apple.speed(0)
apple.shape("circle")
apple.color("green")
apple.penup()
apple.goto(0,100)

t = turtle.Turtle()
t.hideturtle() # Hide the turtle icon
t.penup()
t.goto(-299, -299)
t.write(0, align="left", font=("Arial", 16, "bold"))
t.penup()

high_score_text = turtle.Turtle()
high_score_text.hideturtle() # Hide the turtle icon
high_score_text.penup()
high_score_text.goto(100, -290)
high_score_text.write("high score: 0", align="left", font=("Arial", 16, "bold"))
high_score_text.penup()

#body
segments = []
pipe_layed = []
high_score = 0

#functions
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

def go_up():
    head.direction = "up"
def go_down():
    head.direction = "down"
def go_left():
    head.direction = "left"
def go_right():
    head.direction = "right"

def add_to_pipe():
    for i in segments:
        #if head.xcor() == i.xcor() or head.ycor() == i.ycor():
        pipe_layed.append(i)
    segments.clear()
    
#keyboard bindings
window.listen()
window.onkeypress(go_up, "w")
window.onkeypress(go_down, "s")
window.onkeypress(go_left, "a")
window.onkeypress(go_right, "d")
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")
window.onkeypress(add_to_pipe, "space")

#! main game loop
while True:
    window.update()
    t.clear()
    t.write(len(pipe_layed), align="left", font=("Arial", 16, "bold"))
    t.penup()

    high_score_text.clear()
    high_score_text.write(f"high score: {high_score}", align="left", font=("Arial", 16, "bold"))
    high_score_text.penup()

    #check head and wall
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction  = "stop"
        add_to_pipe()
        
    #drops off the segments of brick
    if len(segments) > 5:
        add_to_pipe()
    
    #check for brick collision
    for pipe in pipe_layed:
        if head.xcor() >= pipe.xcor() and head.xcor() <= pipe.xcor() + 10:
            if head.ycor() >= pipe.ycor() and head.ycor() <= pipe.ycor() + 10:
                time.sleep(1)
                head.goto(0,0)
                for pipe2 in pipe_layed:
                    pipe2.goto(1000,1000)
                if len(pipe_layed) > high_score:
                    high_score = len(pipe_layed)
                pipe_layed.clear()
                break
        
    if head.distance(apple) < 20:
        #move food
        x = random.randint(-290,290)
        y = random.randint(-290,290)
        valid_placement = False
        if len(pipe_layed) > 0:
            while valid_placement == False:
                for i in pipe_layed:
                    if x >= pipe.xcor() and x <= pipe.xcor() + 10:
                        if y >= pipe.ycor() and y <= pipe.ycor() + 10:
                            x = random.randint(-290,290)
                            y = random.randint(-290,290)
                            valid_placement = False
                            break
                    valid_placement = True   
        apple.goto(x,y) 

        #add segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()

        segments.append(new_segment)

    #move end segments first in reverse order
    for index in range(len(segments)-1,0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
    #move segment 0 to head
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
    time.sleep(delay)
    move()

window.mainloop()
