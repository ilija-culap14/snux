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
from PIL import Image as pilimage
from PIL import ImageDraw as pildraw
from PIL import ImageFont as pilfont
from PIL import ImageTk

### Game relevant ###
GAME_NAME = "Snux"
GAME_VERSION = "2.0"
GAME_LICENCE = "GPLv3"
AUTHOR = "Ilija Culap"
AUTHOR_EMAIL = "ilija.culap14@gmail.com"
WINDOW_H = 900
WINDOW_W = 1200
FRAME_OFFSET = 50

# Font files
FONTFILE_GAMEOVER = ("./data/fonts/gameover.ttf")
FONTFILE_TUTORIAL = ("./data/fonts/tutorial.ttf")
FONTFILE_BACK = ("./data/fonts/back.ttf")

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
LABEL_NEW_GAME = "New Game"
LABEL_ABOUT = "About"
LABEL_TUTORIAL = "How to play?"
LABEL_QUIT = "Quit Game"
LABEL_MAIN_MENU = "Main Menu"
LABEL_GAME_OVER = "GAME OVER"
LABEL_GAME_WIN = "YOU WON"
LABEL_BACK = "Back"
LABEL_SCORE = "Points: "
LABEL_LEVEL = "Level: "
LABEL_VERSION = "Version: "

## Need translation
TEXT_1_TUTORIAL = "Bei diesem Spiel müsst ihr schnell sein. Ihr seid die Schlange im Spielfeld. Diese Schlange könnt ihr mit den Pfeiltasten steuern: rechts, links, oben und unten. Ihr dürft nie den Rand des Spielfeldes berühren. Kommt ihr an den Rand, ist das Spiel sofort vorbei. Ziel ist es die Punkte im Spielfeld aufzusammeln. Durch die Punkte wird die Schlange nach und nach länger und schneller.\n\n\nViel Spaß"

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.imgObjects = []
		self.pack()
		self.createGameFrame()
		self.welcome_menu()
		
	def createMainMenuItem(self, canvas, x, y, anchor="center", tags=(), img_leave="", img_enter="", gotoFunc=0):
		pass
		
	def createTextExt(self, canvas, x, y, size=12, fill="white", text="", fontfile="", anchor="center", tags=(), ml=False, width=100, spacing=0, bind=False, bindfunc=0):
		
		# Create Font
		font = pilfont.truetype(fontfile, size)

		# Check if the text is multilined
		# get line lenght in char for given width
		if ml == True:
			oneCharWidth = font.getlength("O")
			numberOfChar = round(width/oneCharWidth)			
			
			words = text.split()
			lineOfText = ""
			text_new = ""		
			for word in words:
				if len(lineOfText) < numberOfChar+3 and len(lineOfText) >= numberOfChar-7:
					text_new += lineOfText
					text_new += "\n"
					lineOfText = ""
				lineOfText += word + " "
			text_new += lineOfText
			
			numberOfLines = text_new.count("\n")
			text = text_new
			
			# Find longest line and adjust the width of the widget
			ll = 0
			for line in text.splitlines():
				cl = int(font.getlength(line))
				if cl > ll:
					ll = cl
					longestline = line
					imageWidth = ll
			
		else:
			# Set width of the line
			imageWidth = int(font.getlength(text))
			
			# Set number of lines to 1
			numberOfLines = 1
		
		# Calculate image height
		imageHeight = (font.getbbox("Fj", anchor='lt')[3]) * numberOfLines
		imageHeight += (spacing * numberOfLines)
		imageHeight = int(imageHeight * 1.1)
	
		# Create image
		img1 = pilimage.new("RGBA", (imageWidth, imageHeight), "#00000000")
			
		# Add Text to image
		pildraw.Draw(img1).multiline_text((0, 0), text, fill, font=font, spacing=spacing, align="center")
		
		# Convert image to Photoimage
		imgext = ImageTk.PhotoImage(img1)
		self.imgObjects.append(imgext)
		
		objectID = "OID-" + str(randint(1, 5000))
		tags_out = (tags, objectID)
				
		# Show image
		self.imgdraw = canvas.create_image(x, y - round(img1.size[1]/size), image=imgext, anchor=anchor, tags=tags_out)
		
		if bind == True:
			self.GameFrame.tag_bind(objectID, "<Button-1>", bindfunc)
		
	def createGameFrame(self):
		self.GameFrame = tk.Canvas(self, height=WINDOW_H, width=WINDOW_W, bg=BG_COLOR)
		
		# Background image
		self.backgroundImage = tk.PhotoImage(file = "./data/bg.png")
		self.backgroundImageOnCanvas = self.GameFrame.create_image(0, 0, image=self.backgroundImage, anchor=tk.NW)

		# Draw 4 lines
		self.frame_line = self.GameFrame.create_line(FRAME_OFFSET, FRAME_OFFSET, WINDOW_W - FRAME_OFFSET - 1, FRAME_OFFSET, width=1, fill=FRAME_COLOR)
		self.frame_line = self.GameFrame.create_line(WINDOW_W - FRAME_OFFSET - 1, FRAME_OFFSET, WINDOW_W - FRAME_OFFSET - 1, WINDOW_H - FRAME_OFFSET - 2, width=1, fill=FRAME_COLOR)
		self.frame_line = self.GameFrame.create_line(FRAME_OFFSET, WINDOW_H - FRAME_OFFSET - 1, WINDOW_W - FRAME_OFFSET - 1, WINDOW_H - FRAME_OFFSET - 1, width=1, fill=FRAME_COLOR)
		self.frame_line = self.GameFrame.create_line(FRAME_OFFSET, FRAME_OFFSET, FRAME_OFFSET, WINDOW_H - FRAME_OFFSET - 1, width=1, fill=FRAME_COLOR)

		# Version in bottom right corner
		self.v_text = self.GameFrame.create_text(WINDOW_W - FRAME_OFFSET, WINDOW_H - (FRAME_OFFSET/2), anchor=tk.E, justify=tk.RIGHT, text=LABEL_VERSION + GAME_VERSION , font=('Calibri', '11'), fill=TEXT_COLOR)
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
		
		# Remove everything from screen
		self.GameFrame.delete("wmitemTag")
		
		# Tutorial Text through new font system
		self.tutorial_text = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=WINDOW_H/2, text=TEXT_1_TUTORIAL, fill=TEXT_COLOR, fontfile=FONTFILE_TUTORIAL, size=40, anchor="center", tags="tutorialItems", ml=True, width=WINDOW_W-110, spacing=25)
		
		# Back button
		self.back_Button = self.createTextExt(self.GameFrame, x=50, y=25, text=LABEL_BACK, fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="w", tags="tutorialItems", bind=True, bindfunc=self.goto_MainMenu)
		
	def goto_About(self, GameFrame):
		self.GameFrame.delete("wmitemTag")
			
		self.t1 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.40, text="Name des Spiels: " + GAME_NAME, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t2 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.45, text="Spiel Version: " + GAME_VERSION, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t3 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.50, text="Lizenz: " + GAME_LICENCE, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t4 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.55, text="Author: " + AUTHOR, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		self.t5 = self.GameFrame.create_text(WINDOW_W*0.15, WINDOW_H*0.60, text="Email: " + AUTHOR_EMAIL, font=('Calibri', '18'), fill=TEXT_COLOR, anchor=tk.W, justify=tk.LEFT, tags="aboutItems")
		
		# Back button
		self.back_Button = self.createTextExt(self.GameFrame, x=50, y=25, text=LABEL_BACK, fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="w", tags="aboutItems", bind=True, bindfunc=self.goto_MainMenu)

	def game_over(self): #### Need work
		
		# Show cursor, need to add it at game_win
		root.config(cursor="arrow")
		
		# Remove everything from the screen
		self.GameFrame.delete("gameItems")
		
		# Score
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.4, text=LABEL_SCORE + str(self.snakePoints), fill="grey", fontfile=FONTFILE_BACK, size=50, anchor=tk.CENTER, tags="goScreenItem")

		# Game over text
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.15, text=LABEL_GAME_OVER, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMEOVER, size=80, anchor=tk.CENTER, tags="goScreenItem")
		
		# Menu
		self.newGameButton_1 = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.55, text=LABEL_NEW_GAME, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.welcomeMenuButton = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.6, text=LABEL_MAIN_MENU, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		self.quitButton_1 = self.GameFrame.create_text(WINDOW_W/2, WINDOW_H*0.65, text=LABEL_QUIT, font=('Calibri', '18', "bold"), fill=MENU_TEXT_COLOR, activefill=MENU_TEXT_COLOR_OVER, tags="goScreenItem")
		
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
		root.config(cursor="none")
		
		# Calculate game grid
		gameGridWidth = round((WINDOW_W - 145)/40)
		gameGridHeight = round((WINDOW_H - 145)/40)
		
		# Set grid origins
		gridOriginX = WINDOW_W / 2 - (gameGridWidth * 20)
		gridOriginY = WINDOW_H / 2 - (gameGridHeight * 20)

		# Snake index
		snake_index = [10, 11, 9, 11, 8, 11, 7, 11, 6, 11, 5, 11]
		
		# Food index
		food_index = [17, 12]
		
		# Some vars for game
		self.snake_tail = 5
		self.foodEaten = False
		self.snakePoints = 0
		snake_level = 1
		
		# Movement vars for the snake
		self.dir_x = 40
		self.dir_y = 0
		
		# Snake moves
		self.snakeMoves = True
		
		def create_head():
			
			# Snake width is 24px
			self.snake_head_object = self.GameFrame.create_oval(gridOriginX + (snake_index[0]*40) - 32, 
																	 gridOriginY + (snake_index[1]*40) - 32, 
																	 gridOriginX + (snake_index[0]*40) - 8, 
																	 gridOriginY + (snake_index[1]*40) - 8, 
																	 fill="white", tags=("gameItems"))
																	 
		def create_tail():
			self.GameFrame.delete("tailItems")
			for i in range(1, self.snake_tail+1):
				self.snake_tail_object = self.GameFrame.create_oval(gridOriginX + (snake_index[(i*2)]*40) - 32, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 32, 
																	gridOriginX + (snake_index[(i*2)]*40) - 8, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 8, 
																	fill="yellow", tags=("tailItems", "gameItems"))
																	 
				
		def create_food():
			
			# Put some random number in food index, need work
			food_index.insert(0, randint(1, gameGridHeight))
			food_index.insert(0, randint(1, gameGridWidth))
			
			# Testing image as food
			self.foodImage = tk.PhotoImage(file = "./data/food.png")
			self.food_object = self.GameFrame.create_image(gridOriginX + (food_index[0]*40), 
																	 gridOriginY + (food_index[1]*40), anchor=tk.SE,image=self.foodImage, 
																	 tags=("foodItem", "gameItems"))
				

		def getCalories():
			
			# 10 points for food
			self.snakePoints += 10
			self.snakePoints += round(self.snake_tail/3)
			
			# Bonus for edge objects
			if food_index[0] == 1 or food_index[0] == gameGridWidth:
				self.snakePoints += 4
			if food_index[1] == 1 or food_index[1] == gameGridHeight:
				self.snakePoints += 4

					
		def define_level(x):
			
			# Bumb level up for 5 eaten food
			level = round((x/5) - 0.49)
			return level

		def update_index():
			
			# Get the position where the snake head is	
			xField = (self.GameFrame.coords(self.snake_head_object)[0] - 38) / 40
			yField = (self.GameFrame.coords(self.snake_head_object)[1] - 38) / 40
			
			# Put those field in snake_index
			snake_index.insert(0, round(yField))
			snake_index.insert(0, round(xField))
			
			# Remove last 2 items in snake_index
			if self.foodEaten == False:
				snake_index.pop()
				snake_index.pop()
			else:
				self.foodEaten = False
			
		def checkGameOver():
			
			# If snake touches the edge
			if snake_index[0] == 0 or snake_index[0] > gameGridWidth or snake_index[1] == 0 or snake_index[1] > gameGridHeight:
				self.game_over()
				return True
			
			# If snake head touches snake tail
			for x in range(1, self.snake_tail):
				if snake_index[0] == snake_index[x*2] and snake_index[1] == snake_index[(x*2)+1]:
					self.game_over()
					return True
		
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
		
		# Create text for score and level
		self.score_text = self.GameFrame.create_text(50, 25, anchor=tk.W, justify=tk.CENTER, text=LABEL_SCORE + str(self.snakePoints), font=('Calibri', '15', 'bold'), fill=TEXT_COLOR, tags="gameItems")
		self.level_text = self.GameFrame.create_text(WINDOW_W - 50, 25, anchor=tk.E, justify=tk.CENTER, text=LABEL_LEVEL + str(define_level(self.snake_tail)), font=('Calibri', '15', "bold"), fill=TEXT_COLOR, tags="gameItems")
		
		# Create a food item and snake head
		create_food()
		create_head()
		
		# Hier is function for moving the snake
		def moveSnake():
			
			# Set focus and bind keys
			self.GameFrame.focus_set()
			bind_keys()
			
			# Move head, update index acording to new head position and then create tail
			self.GameFrame.move(self.snake_head_object, self.dir_x, self.dir_y)
			update_index()
			create_tail()
			
			# If food is eaten
			if snake_index[0] == food_index[0] and snake_index[1] == food_index[1]:
				self.foodEaten = True
				getCalories()
				self.GameFrame.delete("foodItem")
				self.snake_tail += 1
				
				# Update score and points
				self.GameFrame.itemconfigure(self.score_text, text=LABEL_SCORE + str(self.snakePoints))
				self.GameFrame.itemconfigure(self.level_text, text=LABEL_LEVEL + str(define_level(self.snake_tail)))
				
				# Create new food
				create_food()
			
			# Look for gameover
			if self.snakeMoves:
				if checkGameOver() == True:
					snakeMoves = False
				else:
					self.GameFrame.after(120 - round(self.snake_tail/3), moveSnake)
			
		moveSnake()
	
	def quit_game(self, root):
		self.quit()	
			
if __name__ == '__main__':
	root = tk.Tk()
	
	# Set window size and make it unresizeable
	root.geometry(str(WINDOW_W) + "x" + str(WINDOW_H))
	root.resizable(width=False, height=False)
	
	# Start application
	app = Application(root)
	app.master.title(GAME_NAME)
	root.mainloop()
