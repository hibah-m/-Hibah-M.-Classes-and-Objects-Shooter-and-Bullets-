from turtle import *
import random

def generate_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def playing_area():
    pen = Turtle()
    pen.ht()
    pen.speed(0)
    pen.color('teal')
    pen.penup()
    pen.goto(-240, 240)
    pen.pendown()
    pen.begin_fill()
    pen.goto(240, 240)
    pen.goto(240, -240)
    pen.goto(-240, -240)
    pen.goto(-240, 240)
    pen.end_fill()

class Player(Turtle):
    def __init__(self, x, y, color, screen, right_key, left_key, fire_key):
        super().__init__()
        self.ht()
        self.speed(0)
        self.color(color)
        self.penup()
        self.goto(x, y)
        self.setheading(90)
        self.shape("turtle")

        self.health = 3
        self.bullets = []
        self.alive = True

        self.st()

        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkeypress(self.fire, fire_key)

    def fire(self):
        if self.alive:
            self.bullets.append(Bullet(self.xcor(), self.ycor(), self.heading()))

    def turn_left(self):
        self.left(10)

    def turn_right(self):
        self.right(10)

    def move(self):
        self.forward(4)

        if self.xcor() > 230 or self.xcor() < -230:
            self.setheading(180 - self.heading())

        if self.ycor() > 230 or self.ycor() < -230:
            self.setheading(-self.heading())

    def kill(self):
        self.alive = False
        self.hideturtle()


class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.speed(0)
        self.penup()
        self.shape("circle")
        self.color(player.color)
        self.goto(player.xcor(), player.ycor())
        self.setheading(player.heading())
        self.forward(10)
        self.player = player
        self.st()

    def move(self):
        if self.player.fire_key:
            self.forward(10)
            if self.xcor() > 235 or self.xcor() < -235 or self.ycor() > 235 or self.ycor() < -235:
                self.die()

    def die(self):

        self.hideturtle()




screen = Screen()
screen.bgcolor("black")
screen.setup(520, 520)
screen.listen()

playing_area()

p1 = Player(-100, 0, "purple", screen, "d", "a","w")
p2 = Player(100, 0, "blue", screen, "Right", "Left","Up")

while p1.alive and p2.alive:
    p1.move()
    p2.move()

    new_bullets = []
    for b in p1.bullets:
        b.move()
        

screen.exitonclick()
