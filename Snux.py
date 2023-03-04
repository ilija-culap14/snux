#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snux 1.0.py
#  
#  Copyright 2017 Ilija Culap <ilija.culap14@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License v3 for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

try:
	# Python2
	import Tkinter as tk
except ImportError:
	# Python3
	import tkinter as tk

from random import randint

### Game relevant ###
GAME_NAME = "Snux"
GAME_VERSION = "2.0"
GAME_LICENCE = "GPLv3"
AUTHOR = "Ilija Culap"
AUTHOR_EMAIL = "ilija.culap14@gmail.com"

### Keys ###
KEY_UP = "<Up>"
KEY_DOWN = "<Down>"
KEY_RIGHT = "<Right>"
KEY_LEFT = "<Left>"

### Colors ###
BG_COLOR = "black"
TEXT_COLOR = "yellow"
SNAKE_COLOR = "#9191F8"
FOOD_COLOR = "green"
FRAME_COLOR = "yellow"
MENU_TEXT_COLOR = "yellow"
MENU_TEXT_COLOR_OVER = "#1B94C6"
GAME_OVER_LABEL_COLOR = "yellow"
GAME_WIN_LABEL_COLOR = "yellow"

### Translation ###
LABEL_NEW_GAME = "Neues Spiel"
LABEL_ABOUT = "Über"
LABEL_TUTORIAL = "Tutorial"
LABEL_QUIT = "Beenden"
LABEL_MAIN_MENU = "Hauptmenü"
LABEL_GAME_OVER = "GAME OVER"
LABEL_GAME_WIN = "GEWONNEN"
LABEL_BACK = "Zurück"
LABEL_SCORE = "Punkte: "
LABEL_LEVEL = "Level: "
LABEL_VERSION = "Version: "
TEXT_1_TUTORIAL = "Bei diesem Spiel müsst ihr schnell sein. Ihr seid die Schlange im Spielfeld. Diese Schlange könnt ihr mit den Pfeiltasten steuern: rechts, links, oben und unten. \n\nIhr dürft nie den Rand des Spielfeldes berühren. Kommt ihr an den Rand, ist das Spiel sofort vorbei. \n\nZiel ist es die Punkte im Spielfeld aufzusammeln. Durch die Punkte wird die Schlange nach und nach länger und schneller.\n\n\nViel Spaß"

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.create_gameframe()
		self.welcome_menu()
		
	def create_gameframe(self):
		self.GameFrame = tk.Canvas(self, height=300, width=300, bg=BG_COLOR)
		li = [20, 20, 282, 20, 281, 20, 281, 282, 20, 281, 282, 281, 20, 20, 20, 282]
		x = 0
		for i in range(4):	
			self.frame_line = self.GameFrame.create_line(li[x], li[x + 1], li[x + 2], li[x + 3], width=1, fill=FRAME_COLOR)
			x += 4			
		self.v_text = self.GameFrame.create_text(280, 290, anchor=tk.E, justify=tk.RIGHT, text=LABEL_VERSION + GAME_VERSION , font=('Calibri', '7', "bold"), fill=TEXT_COLOR)
		self.GameFrame.pack()

	def welcome_menu(self):
		self.LogoImage = tk.PhotoImage(file = "./data/ph/logo.gif")
		self.LogoImage = self.LogoImage.subsample(2, 2)
		self.GameName = self.GameFrame.create_image(150, 70, image=self.LogoImage, tags="wmitemTag")
		self.newGameButton = self.GameFrame.create_text(150, 130, text=LABEL_NEW_GAME, font=('Calibri', '13', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.tutorialButton = self.GameFrame.create_text(150, 160, text=LABEL_TUTORIAL, font=('Calibri', '13', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.aboutButton = self.GameFrame.create_text(150, 190, text=LABEL_ABOUT, font=('Calibri', '13', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.quitButton = self.GameFrame.create_text(150, 220, text=LABEL_QUIT, font=('Calibri', '13', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.GameFrame.tag_bind(self.newGameButton, "<Button-1>", self.menu_option_new_game_clicked)
		self.GameFrame.tag_bind(self.aboutButton, "<Button-1>", self.menu_option_about_clicked)
		self.GameFrame.tag_bind(self.tutorialButton, "<Button-1>", self.menu_option_tutorial_clicked)
		self.GameFrame.tag_bind(self.quitButton, "<Button-1>", self.quit_game)

	def menu_option_new_game_clicked(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
		self.play_game()
		
	def menu_option_tutorial_clicked(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
		self.tutorial_text = self.GameFrame.create_text(150, 120, text=TEXT_1_TUTORIAL, font=('Calibri', '7'), fill=TEXT_COLOR, width="230", tags="tutorialItems")
		self.zuruck_tutorial_Button = self.GameFrame.create_text(260, 265, text=LABEL_BACK, font=('Calibri', '10', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="tutorialItems", anchor=tk.SE, justify=tk.RIGHT)
		self.GameFrame.tag_bind(self.zuruck_tutorial_Button, "<Button-1>", self.zuruck_tutorial_button_clicked)		

	def menu_option_about_clicked(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
		self.LogoImage = tk.PhotoImage(file = "./data/ph/logo.gif")
		self.LogoImage = self.LogoImage.subsample(3, 3)
		self.GameName = self.GameFrame.create_image(150, 70, image=self.LogoImage, tags="aboutItems")
		pad = 80
		self.t1 = self.GameFrame.create_text(30, pad + 40, text="Name des Spiels: " + GAME_NAME, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t2 = self.GameFrame.create_text(30, pad + 55, text="Spiel Version: " + GAME_VERSION, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t3 = self.GameFrame.create_text(30, pad + 70, text="Lizenz: " + GAME_LICENCE, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t4 = self.GameFrame.create_text(30, pad + 85, text="Author: " + AUTHOR, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t5 = self.GameFrame.create_text(30, pad + 100, text="Email: " + AUTHOR_EMAIL, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t6 = self.GameFrame.create_text(30, pad + 115, text="Logo Design: " + AUTHOR_LOGO, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t7 = self.GameFrame.create_text(30, pad + 130, text="Email: " + AUTHOR_LOGO_EMAIL, font=('Calibri', '7'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.zuruck_about_Button = self.GameFrame.create_text(260, 265, text=LABEL_BACK, font=('Calibri', '10', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="aboutItems", anchor=tk.SE, justify=tk.RIGHT)
		self.GameFrame.tag_bind(self.zuruck_about_Button, "<Button-1>", self.zuruck_about_button_clicked)
		
	def zuruck_tutorial_button_clicked(self, GameFrame):
		self.GameFrame.delete("tutorialItems")
		self.welcome_menu()
		
	def zuruck_about_button_clicked(self, GameFrame):
		self.GameFrame.delete("aboutItems")
		self.welcome_menu()

	def game_over(self):
		self.GameFrame.delete("gameItems")
		self.game_over_text = self.GameFrame.create_text(150, 150, text=LABEL_GAME_OVER, font=('Calibri', '14', "bold"), fill=GAME_OVER_LABEL_COLOR, tags="goScreenItem")
		self.newGameButton_1 = self.GameFrame.create_text(150, 190, text=LABEL_NEW_GAME, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.welcomeMenuButton = self.GameFrame.create_text(150, 210, text=LABEL_MAIN_MENU, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.quitButton_1 = self.GameFrame.create_text(150, 230, text=LABEL_QUIT, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.GameFrame.tag_bind(self.newGameButton_1, "<Button-1>", self.ng_a_go)
		self.GameFrame.tag_bind(self.welcomeMenuButton, "<Button-1>", self.wm_a_go)
		self.GameFrame.tag_bind(self.quitButton_1, "<Button-1>", self.quit_game)
		self.GameFrame.itemconfigure(self.score_text, font=('Calibri', '11'), anchor=tk.CENTER, justify=tk.CENTER, tags="goScreenItem")
		self.GameFrame.move(self.score_text, 130, 90)
		
	def game_win(self):
		self.GameFrame.delete("gameItems")
		self.game_win_text = self.GameFrame.create_text(150, 150, text=LABEL_GAME_WIN, font=('Calibri', '14', "bold"), fill=GAME_WIN_LABEL_COLOR, tags="goScreenItem")
		self.newGameButton_1 = self.GameFrame.create_text(150, 190, text=LABEL_NEW_GAME, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.welcomeMenuButton = self.GameFrame.create_text(150, 210, text=LABEL_MAIN_MENU, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.quitButton_1 = self.GameFrame.create_text(150, 230, text=LABEL_QUIT, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.GameFrame.tag_bind(self.newGameButton_1, "<Button-1>", self.ng_a_go)
		self.GameFrame.tag_bind(self.welcomeMenuButton, "<Button-1>", self.wm_a_go)
		self.GameFrame.tag_bind(self.quitButton_1, "<Button-1>", self.quit_game)
		self.GameFrame.itemconfigure(self.score_text, font=('Calibri', '11'), anchor=tk.CENTER, justify=tk.CENTER, tags="goScreenItem")
		self.GameFrame.move(self.score_text, 130, 90)

	def ng_a_go(self, GameFrame): # New game after game over
		self.GameFrame.delete("goScreenItem")
		self.play_game()
		
	def wm_a_go(self, GameFrame): # Welcome menu after game over
		self.GameFrame.delete("goScreenItem")
		self.welcome_menu()
	
	def play_game(self):	
				
		### Create some variables ###
		snake_index = ["1515", "1415", "1315", "1215", "1115", "1015"] 		# Start position
		snake_tail = 5
		snake_points = 0
		snake_level = 1
		self.dir_x = 5
		self.dir_y = 0
		self.food_np = [0,0]
		self.food_op = [15, 15]
		moves = 0
		food_eaten = 0
		
		def create_head():
			x = (int(snake_index[0][:2]) * 5) + 15
			y = (int(snake_index[0][-2:]) * 5) + 15
			self.snake_head_object = self.GameFrame.create_line(x + 1, y + 3, x + 6, y + 3, width=5, fill=SNAKE_COLOR, tags="gameItems")			

		def create_tail():
			t = 1
			for i in range(snake_tail):
				x = (int(snake_index[t][:2]) * 5) + 15
				y = (int(snake_index[t][-2:]) * 5) + 15
				self.snake_tail_object = self.GameFrame.create_line(x + 1, y + 3, x + 6, y + 3, fill=SNAKE_COLOR, width=5, tags=("tailItems", "gameItems"))
				t += 1
				
		def create_food():
			x = (randint(1, 52) * 5) + 15
			y = (randint(1, 52) * 5) + 15
			self.food_np[0] = (x - 15) / 5
			self.food_np[1] = (y - 15) / 5
			if len(str(x)) == 1:
				x = "0" + str(x)
			if len(str(y)) == 1:
				y = "0" + str(y)
			xy = str(x) + str(y)
			while xy in snake_index:
				x = randint(1, 52)
				y = randint(1, 52)
				if len(str(x)) == 1:
					x = "0" + str(x)
				if len(str(y)) == 1:
					y = "0" + str(y)
				xy = str(x) + str(y)		
			self.food_object = self.GameFrame.create_line(x + 1, y + 3, x + 6, y + 3, width=5, fill=FOOD_COLOR, tags=("foodItem", "gameItems"))
		
		def delete_food():
			self.GameFrame.delete("foodItem")
		
		def food_energy():
			x = ((int(str(self.GameFrame.coords(self.food_object)[0]).replace(".0","")) - 1) / 5) - 3
			y = ((int(str(self.GameFrame.coords(self.food_object)[1]).replace(".0","")) - 3) / 5) - 3
			if (x in range(1,3) and y in range(1,3)) or (x in range(51,53) and y in range(51,53)) or (x in range(51,53) and y in range(1,3)) or (x in range(1,3) and y in range(51,53)):
				m = 5
			elif (x in range(3,19) and y in range(3,51)) or (x in range(35,51) and y in range(3,51)) or (x in range(19,35) and y in range(3,19)) or (x in range(19,35) and y in range(35,51)):
				m = 3
			elif x in range(19,35) and y in range(19,35):
				m = 2
			else:
				m = 4
			return m
		
		def define_level(x):
			if x < 15:
				snake_level = 1
			else:
				snake_level = str(round((x + 5) / 10)).replace(".0", "")
			return snake_level

		def define_speed(x):
			speed = 90 - (x / 2)
			return int(speed)

		def min_distance(x1, y1, x2, y2):
			distance = abs(x1 - x2) + abs(y1 - y2)
			return distance

		def update_index():
			x = str((int(str(self.GameFrame.coords(self.snake_head_object)[0] - 1).replace(".0","")) - 15) / 5).replace(".0","")
			y = str((int(str(self.GameFrame.coords(self.snake_head_object)[1] - 3).replace(".0","")) - 15) / 5).replace(".0","")
			if len(str(x)) == 1:
				x = "0" + str(x)
			if len(str(y)) == 1:
				y = "0" + str(y)
			z = str(x) + str(y)
			snake_index.insert(0, z)
			if snake_tail == len(snake_index) - 1:
				pass
			else:
				snake_index.pop(snake_tail + 1)
			
		def get_x_head():
			x = str(self.GameFrame.coords(self.snake_head_object)[0]).replace(".0","")
			if len(str(x)) == 1:
				x = "0" + str(x)
			return x
		
		def get_y_head():
			y = str(self.GameFrame.coords(self.snake_head_object)[1]).replace(".0","")
			if len(str(y)) == 1:
				y = "0" + str(y)
			return y
		
		def arrow_key_up(event):
			unbind_keys()
			if (self.dir_x == 5 and self.dir_y == 0) or (self.dir_x == -5 and self.dir_y == 0):
				self.dir_x = 0
				self.dir_y = -5
				
		def arrow_key_down(event):
			unbind_keys()
			if (self.dir_x == 5 and self.dir_y == 0) or (self.dir_x == -5 and self.dir_y == 0):
				self.dir_x = 0
				self.dir_y = 5
				
		def arrow_key_left(event):
			unbind_keys()
			if (self.dir_x == 0 and self.dir_y == -5) or (self.dir_x == 0 and self.dir_y == 5):
				self.dir_x = -5
				self.dir_y = 0
				
		def arrow_key_right(event):
			unbind_keys()
			if (self.dir_x == 0 and self.dir_y == -5) or (self.dir_x == 0 and self.dir_y == 5):
				self.dir_x = 5
				self.dir_y = 0
		
		def bind_keys():
			self.GameFrame.bind(KEY_UP, arrow_key_up)
			self.GameFrame.bind(KEY_DOWN, arrow_key_down)
			self.GameFrame.bind(KEY_LEFT, arrow_key_left)
			self.GameFrame.bind(KEY_RIGHT, arrow_key_right)
		
		def unbind_keys():
			self.GameFrame.unbind(KEY_UP)
			self.GameFrame.unbind(KEY_DOWN)
			self.GameFrame.unbind(KEY_LEFT)
			self.GameFrame.unbind(KEY_RIGHT)

		self.score_text = self.GameFrame.create_text(20, 9, anchor=tk.W, justify=tk.LEFT, text=LABEL_SCORE + str(snake_points), font=('Calibri', '7', "bold"), fill=TEXT_COLOR)
		self.level_text = self.GameFrame.create_text(280, 9, anchor=tk.E, justify=tk.RIGHT, text=LABEL_LEVEL + str(define_level(snake_tail)), font=('Calibri', '7', "bold"), fill=TEXT_COLOR, tags="gameItems")	
		create_food()
		create_head()

		while True:
			
			self.GameFrame.focus_set()				
			
			# Show tail, wait, move head and remove tail
			create_tail()
			root.update()
			self.GameFrame.move(self.snake_head_object, self.dir_x, self.dir_y)
			self.GameFrame.after(define_speed(food_eaten))
			moves += 1			
			bind_keys()
			
			# Define Game Over		
			if int(get_x_head()) > 280 or int(get_y_head()) > 280 or int(get_y_head()) < 20 or int(get_x_head()) < 20 or snake_index.count(snake_index[0]) == 2:
				self.game_over()
				break
			
			# If the food is eaten
			if self.GameFrame.coords(self.snake_head_object)[:2] == self.GameFrame.coords(self.food_object)[:2]:
				distance = min_distance(self.food_op[0], self.food_op[1], self.food_np[0], self.food_np[1])
				self.food_op[0] = self.food_np[0]
				self.food_op[1] = self.food_np[1]
				if moves < (distance + 30):
					food_bonus = 30 - (moves - distance)
					moves = 0
				else:
					food_bonus = 0
					moves = 0
				snake_points = snake_points + ((snake_level + 5) * food_energy()) + food_bonus
				snake_tail += 1
				self.GameFrame.itemconfigure(self.score_text, text="Punkte: " + str(snake_points))
				self.GameFrame.itemconfigure(self.level_text, text="Level: " + str(define_level(snake_tail)))			
				food_eaten += 1
				if food_eaten == 130:
					self.game_win()
					break
				delete_food()
				create_food()

			self.GameFrame.delete("tailItems")	
			update_index()
	
	def quit_game(self, root):
		self.quit()	
			
if __name__ == '__main__':
	root = tk.Tk()
	root.geometry("300x300")
	root.resizable(width=False, height=False)
	app = Application(root)
	app.master.title(GAME_NAME)
	root.mainloop()
