from tkinter import *


from player import Ship
from game import Game

window = Tk()
window.geometry('1000x700')

game = Game(window)



# player = Ship(window)
# game.create_player(player)
# game.update_player()
player = Ship(window)

def start():
    UI_frame.destroy()
    game.create_asteroids()
    game.move_asteroids()
    game.create_player(player)
    game.update_player()
    window.mainloop()

def shoot(event):
    game.create_fire(player.phi)
    game.move_fire()


UI_frame = Frame(window, width=100, height=50)
UI_frame.pack(padx=100, pady=100)
Button(UI_frame, text='Start Game', command=start, bg='black', font=("Arial", 20, "bold")).pack()

window.bind("<space>", shoot)
window.mainloop()
