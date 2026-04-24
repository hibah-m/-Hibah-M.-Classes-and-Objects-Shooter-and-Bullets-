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
    def __init__(self, x, y, color, screen, right_key, left_key):
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
        screen.onkeypress(self.fire, "space")

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
    def __init__(self, x, y, heading):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("yellow")
        self.goto(x, y)
        self.setheading(heading)
        self.alive = True

    def move(self):
        if self.alive:
            self.forward(10)

            if self.xcor() > 235 or self.xcor() < -235 or self.ycor() > 235 or self.ycor() < -235:
                self.die()

    def die(self):
        self.alive = False
        self.hideturtle()


def check_hit(shooter, target, bullet):
    bx = bullet.xcor()
    by = bullet.ycor()
    tx = target.xcor()
    ty = target.ycor()

    if -15 < bx - tx < 15 and -15 < by - ty < 15:
        target.health -= 1
        bullet.die()

        if target.health <= 0:
            target.kill()


screen = Screen()
screen.bgcolor("black")
screen.setup(520, 520)
screen.listen()

playing_area()

p1 = Player(-100, 0, "red", screen, "d", "a")
p2 = Player(100, 0, "blue", screen, "Right", "Left")

while p1.alive and p2.alive:
    p1.move()
    p2.move()

    new_bullets = []
    for b in p1.bullets:
        b.move()
        check_hit(p1, p2, b)
        if b.alive:
            new_bullets.append(b)
    p1.bullets = new_bullets

    new_bullets = []
    for b in p2.bullets:
        b.move()
        check_hit(p2, p1, b)
        if b.alive:
            new_bullets.append(b)
    p2.bullets = new_bullets

screen.exitonclick()
