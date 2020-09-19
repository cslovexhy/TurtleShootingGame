import turtle, math

phi = 180 * (3 - math.sqrt(5))
t = turtle.Pen()
t.speed(0)
num = 200
for x in reversed(range(0, num)):
    t.fillcolor((1, 1-(x+1)/num, 0))
    t.begin_fill()
    t.circle(5 + x, None, 7)
    # for tmp in range(0, 4):
    #     t.forward(5 + x)
    #     t.right(90)
    t.end_fill()
    t.right(phi+.8)

turtle.mainloop()