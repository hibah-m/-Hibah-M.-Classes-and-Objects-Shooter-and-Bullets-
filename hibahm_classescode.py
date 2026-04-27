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
        self.alive = True

        self.base_color = color
        self.colors = {3: color, 2: "yellow", 1: "red"}

        self.bullets = []

        self.st()

        screen.onkeypress(self.turn_left, left_key)
        screen.onkeypress(self.turn_right, right_key)
        screen.onkeypress(self.fire, fire_key)

    def fire(self):
        if self.alive:
            self.bullets.append(Bullet(self))

    def turn_left(self):
        if self.alive:
            self.left(10)

    def turn_right(self):
        if self.alive:
            self.right(10)

    def move(self):
        if self.alive == False:
            return

        self.forward(4)

        if self.xcor() > 230 or self.xcor() < -230:
            self.setheading(180 - self.heading())

        if self.ycor() > 230 or self.ycor() < -230:
            self.setheading(-self.heading())

    def take_damage(self):
        self.health -= 1

        if self.health > 0:
            self.color(self.colors[self.health])
        else:
            self.kill()

    def kill(self):
        self.health = 0
        self.alive = False
        self.hideturtle()


class Bullet(Turtle):
    def __init__(self, player):
        super().__init__()
        self.ht()
        self.speed(0)
        self.penup()
        self.shape("circle")

        self.player = player
        self.color(player.base_color)

        self.goto(player.xcor(), player.ycor())
        self.setheading(player.heading())
        self.forward(10)

        self.st()

    
    def die(self):
        self.hideturtle()

    def move(self):
        self.forward(10)

        
        if self.xcor() > 235 or self.xcor() < -235 or self.ycor() > 235 or self.ycor() < -235:
            self.die()
            return True

        return False




screen = Screen()
screen.bgcolor("black")
screen.setup(520, 520)
screen.listen()

playing_area()

p1 = Player(-100, 0, "purple", screen, "d", "a", "w")
p2 = Player(100, 0, "blue", screen, "Right", "Left", "Up")

players = [p1, p2]



while p1.alive and p2.alive:

    for player in players:
        player.move()

    for player in players:
        bullets_to_remove = []

        for bullet in player.bullets:
            bullet.move()

            hit_detected = False

            for other in players:
                if other != bullet.player and other.alive:
                    if bullet.distance(other) < 20:
                        other.take_damage()
                        bullet.die()
                        hit_detected = True

            out_of_bounds = (
                bullet.xcor() > 235 or bullet.xcor() < -235 or
                bullet.ycor() > 235 or bullet.ycor() < -235
            )

            if hit_detected or out_of_bounds:
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            if bullet in player.bullets:
                player.bullets.remove(bullet)

screen.exitonclick()