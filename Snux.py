#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snux.py
#  
#  Copyright 2023 Ilija Culap <ilija.culap14@gmail.com>
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
WINDOW_H = 900
WINDOW_W = 1200

### Keys ###
KEY_UP = "<Up>"
KEY_DOWN = "<Down>"
KEY_RIGHT = "<Right>"
KEY_LEFT = "<Left>"

### Colors ###
BG_COLOR = "black"
TEXT_COLOR = "white"
SNAKE_COLOR = "#9191F8"
FOOD_COLOR = "green"
FRAME_COLOR = "white"
MENU_TEXT_COLOR = "white"
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
		self.GameFrame = tk.Canvas(self, height=WINDOW_H, width=WINDOW_W, bg=BG_COLOR)
		
		# Background image
		self.backgroundImage = tk.PhotoImage(file = "./data/bg.png")
		self.backgroundImageOnCanvas = self.GameFrame.create_image(0, 0, image=self.backgroundImage, anchor=tk.NW)
		
		# GameFrame lines (4 of them)
		li = [50, 50, WINDOW_W - 49, 50, 
			  WINDOW_W - 49, 50, WINDOW_W - 49, WINDOW_H - 48, 
			  50, WINDOW_H - 49, WINDOW_W - 49, WINDOW_H - 49, 
			  50, 50, 50, WINDOW_H - 49]
		
		x = 0
		for i in range(4):	
			self.frame_line = self.GameFrame.create_line(li[x], li[x + 1], li[x + 2], li[x + 3], width=1, fill=FRAME_COLOR)
			x += 4			
		
		# Version in bottom right corner
		self.v_text = self.GameFrame.create_text(WINDOW_W - 50, WINDOW_H - 25, anchor=tk.E, justify=tk.RIGHT, text=LABEL_VERSION + GAME_VERSION , font=('Calibri', '11'), fill=TEXT_COLOR)
		self.GameFrame.pack()

	def welcome_menu(self):
		
		# Hide logo for now
		#self.LogoImage = tk.PhotoImage(file = "./data/ph/logo.gif")
		#self.LogoImage = self.LogoImage.subsample(2, 2)
		#self.GameName = self.GameFrame.create_image(WINDOW_W/2, WINDOW_H*0.2, image=self.LogoImage, tags="wmitemTag")
		
		self.newGameButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.3, text=LABEL_NEW_GAME, font=('Calibri', '30', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.tutorialButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.4, text=LABEL_TUTORIAL, font=('Calibri', '30', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.aboutButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.5, text=LABEL_ABOUT, font=('Calibri', '30', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		self.quitButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.6, text=LABEL_QUIT, font=('Calibri', '30', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="wmitemTag")
		
		self.GameFrame.tag_bind(self.newGameButton, "<Button-1>", self.goto_PlayGame)
		self.GameFrame.tag_bind(self.aboutButton, "<Button-1>", self.goto_About)
		self.GameFrame.tag_bind(self.tutorialButton, "<Button-1>", self.goto_Tutorial)
		self.GameFrame.tag_bind(self.quitButton, "<Button-1>", self.quit_game)
		
	def goto_Tutorial(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
		self.tutorial_text = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.50, text=TEXT_1_TUTORIAL, font=('Calibri', '20'), fill=TEXT_COLOR, width=WINDOW_W-120, tags="tutorialItems")
		self.back_Button = self.GameFrame.create_text(50, 25, text=LABEL_BACK, font=('Calibri', '20', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="tutorialItems", anchor=tk.W, justify=tk.RIGHT)
		self.GameFrame.tag_bind(self.back_Button, "<Button-1>", self.goto_MainMenu)		

	def goto_About(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
		
		# Hide image for now
		#self.LogoImage = tk.PhotoImage(file = "./data/ph/logo.gif")
		#self.LogoImage = self.LogoImage.subsample(3, 3)
		#self.GameName = self.GameFrame.create_image(150, 70, image=self.LogoImage, tags="aboutItems")
		
		self.t1 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.40, text="Name des Spiels: " + GAME_NAME, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t2 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.45, text="Spiel Version: " + GAME_VERSION, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t3 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.50, text="Lizenz: " + GAME_LICENCE, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t4 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.55, text="Author: " + AUTHOR, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t5 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.60, text="Email: " + AUTHOR_EMAIL, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		
		self.back_Button = self.GameFrame.create_text(50, 25, text=LABEL_BACK, font=('Calibri', '20', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="aboutItems", anchor=tk.W, justify=tk.RIGHT)
		self.GameFrame.tag_bind(self.back_Button, "<Button-1>", self.goto_MainMenu)

	def game_over(self): #### Need work
		
		# Remove everything from the screen
		self.GameFrame.delete("gameItems")
		
		# Text
		self.game_over_text = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.3, text=LABEL_GAME_OVER, font=('Calibri', '30', "bold"), fill=GAME_OVER_LABEL_COLOR, tags="goScreenItem")
		self.newGameButton_1 = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.45, text=LABEL_NEW_GAME, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.welcomeMenuButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.5, text=LABEL_MAIN_MENU, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.quitButton_1 = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.55, text=LABEL_QUIT, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		
		# Bind buttons
		self.GameFrame.tag_bind(self.newGameButton_1, "<Button-1>", self.goto_PlayGame)
		self.GameFrame.tag_bind(self.welcomeMenuButton, "<Button-1>", self.goto_MainMenu)
		self.GameFrame.tag_bind(self.quitButton_1, "<Button-1>", self.quit_game)

		
	def game_win(self):
		self.GameFrame.delete("gameItems")
		self.game_win_text = self.GameFrame.create_text(150, 150, text=LABEL_GAME_WIN, font=('Calibri', '14', "bold"), fill=GAME_WIN_LABEL_COLOR, tags="goScreenItem")
		self.newGameButton_1 = self.GameFrame.create_text(150, 190, text=LABEL_NEW_GAME, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.welcomeMenuButton = self.GameFrame.create_text(150, 210, text=LABEL_MAIN_MENU, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.quitButton_1 = self.GameFrame.create_text(150, 230, text=LABEL_QUIT, font=('Calibri', '9', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.GameFrame.tag_bind(self.newGameButton_1, "<Button-1>", self.goto_PlayGame)
		self.GameFrame.tag_bind(self.welcomeMenuButton, "<Button-1>", self.goto_MainMenu)
		self.GameFrame.tag_bind(self.quitButton_1, "<Button-1>", self.quit_game)
		self.GameFrame.itemconfigure(self.score_text, font=('Calibri', '11'), anchor=tk.CENTER, justify=tk.CENTER, tags="goScreenItem")
		self.GameFrame.move(self.score_text, 130, 90)
		
	def goto_MainMenu(self, GameFrame):
		self.GameFrame.delete("goScreenItem")
		self.GameFrame.delete("aboutItems")
		self.GameFrame.delete("aboutItems")
		self.GameFrame.delete("tutorialItems")
		self.welcome_menu()
		
	def goto_PlayGame(self, GameFrame):
		self.GameFrame.delete("goScreenItem")
		self.GameFrame.delete("aboutItems")
		self.GameFrame.delete("aboutItems")
		self.GameFrame.delete("tutorialItems")
		self.GameFrame.delete("wmitemTag")
		self.play_game()
	
	def play_game(self):
		
		# Calculate game grid
		gameGridWidth = round((WINDOW_W - 142)/40)
		gameGridHeight = round((WINDOW_H - 142)/40)
		
		# Set grid origins
		gridOriginX = WINDOW_W / 2 - (gameGridWidth * 20)
		gridOriginY = WINDOW_H / 2 - (gameGridHeight * 20)

		# Snake index
		snake_index = [10, 11, 9, 11, 8, 11, 7, 11, 6, 11, 5, 11]
		
		# Food index
		food_index = [17, 12]
		
		# Some vars for game
		snake_tail = 5
		snake_points = 0
		snake_level = 1
		self.dir_x = 40
		self.dir_y = 0
		moves = 0
		food_eaten = 0
		
		def create_head():
			# Snake Head, new
			# Snake width is 24px
			self.snake_head_object = self.GameFrame.create_oval(gridOriginX + (snake_index[0]*40) - 32, 
																	 gridOriginY + (snake_index[1]*40) - 32, 
																	 gridOriginX + (snake_index[0]*40) - 8, 
																	 gridOriginY + (snake_index[1]*40) - 8, 
																	 fill="white", tags=("gameItems"))
																	 
		def create_tail():
			self.GameFrame.delete("tailItems")
			t = 1
			for i in range(snake_tail):
				self.snake_tail_object = self.GameFrame.create_oval(gridOriginX + (snake_index[t+1]*40) - 32, 
																	gridOriginY + (snake_index[t+2]*40) - 32, 
																	gridOriginX + (snake_index[t+1]*40) - 8, 
																	gridOriginY + (snake_index[t+2]*40) - 8, 
																	fill="yellow", tags=("tailItems", "gameItems"))
																	 
				t += 2
				
		def create_food():
			
			# Put some random number in food index, need work
			food_index.insert(0, randint(1, gameGridHeight))
			food_index.insert(0, randint(1, gameGridWidth))
			
			# Draw food
			self.food_object = self.GameFrame.create_oval(gridOriginX + (food_index[0]*40) - 32, 
																	 gridOriginY + (food_index[1]*40) - 32, 
																	 gridOriginX + (food_index[0]*40) - 8, 
																	 gridOriginY + (food_index[1]*40) - 8,
																		fill="blue", tags=("foodItem", "gameItems"))
				

		def food_energy():
			pass
		
		def define_level(x):
			if x < 15:
				snake_level = 1
			else:
				snake_level = str(round((x + 5) / 10)).replace(".0", "")
			return snake_level

		def update_index():
			
			# Get the position where the snake head is	
			xField = (self.GameFrame.coords(self.snake_head_object)[0] - 38) / 40
			yField = (self.GameFrame.coords(self.snake_head_object)[1] - 38) / 40
			
			# Put those field in snake_index
			snake_index.insert(0, round(yField))
			snake_index.insert(0, round(xField))
		
		def arrow_key_up(event):
			unbind_keys()
			if (self.dir_x == 40 and self.dir_y == 0) or (self.dir_x == -40 and self.dir_y == 0):
				self.dir_x = 0
				self.dir_y = -40
				
		def arrow_key_down(event):
			unbind_keys()
			if (self.dir_x == 40 and self.dir_y == 0) or (self.dir_x == -40 and self.dir_y == 0):
				self.dir_x = 0
				self.dir_y = 40
				
		def arrow_key_left(event):
			unbind_keys()
			if (self.dir_x == 0 and self.dir_y == -40) or (self.dir_x == 0 and self.dir_y == 40):
				self.dir_x = -40
				self.dir_y = 0
				
		def arrow_key_right(event):
			unbind_keys()
			if (self.dir_x == 0 and self.dir_y == -40) or (self.dir_x == 0 and self.dir_y == 40):
				self.dir_x = 40
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

		self.score_text = self.GameFrame.create_text(50, 25, anchor=tk.W, justify=tk.CENTER, text=LABEL_SCORE + str(snake_points).replace(".0",""), font=('Calibri', '15', 'bold'), fill=TEXT_COLOR)
		self.level_text = self.GameFrame.create_text(WINDOW_W/2, 25, anchor=tk.CENTER, justify=tk.CENTER, text=str(define_level(snake_tail)), font=('Calibri', '15', "bold"), fill=TEXT_COLOR, tags="gameItems")	
		create_food()
		create_head()
		
		while True:
			
			self.GameFrame.focus_set()	
			bind_keys()			
			
			# Show tail, wait, move head and remove tail
			create_tail()
			root.update()
			self.GameFrame.move(self.snake_head_object, self.dir_x, self.dir_y)
			create_tail()

			# Define Game Over >>>> need work
			if snake_index[0] == 0 or snake_index[0] > gameGridWidth or snake_index[1] == 0 or snake_index[1] > gameGridHeight:
				self.game_over()
				break
			
			self.GameFrame.after(75)
			bind_keys()	

			# If the food is eaten
			if snake_index[0] == food_index[0] and snake_index[1] == food_index[1]:
				self.GameFrame.delete("foodItem")
				snake_points += 1
				snake_tail += 1
				food_eaten += 1
				create_food()
				
			update_index()
			bind_keys()
	
	def quit_game(self, root):
		self.quit()	
			
if __name__ == '__main__':
	root = tk.Tk()
	root.geometry(str(WINDOW_W) + "x" + str(WINDOW_H))
	root.resizable(width=False, height=False)
	app = Application(root)
	app.master.title(GAME_NAME)
	root.mainloop()
