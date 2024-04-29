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

# Game vars, name, version etc
GAME_NAME = "Snux"
GAME_VERSION = "2.0"

# Window vars
WINDOW_H = 900
WINDOW_W = 1200
FRAME_OFFSET = 50

# Font files
FONTFILE_1 = ("./data/fonts/f1.otf")
FONTFILE_2 = ("./data/fonts/f2.otf")
FONTFILE_3 = ("./data/fonts/f3.ttf")

FONTFILE_GAMEOVER = ("./data/fonts/gameover.ttf")
FONTFILE_TUTORIAL = ("./data/fonts/tutorial.ttf")
FONTFILE_VERSION = ("./data/fonts/version.otf")

# Backgrounds
BG_DEFAULT = "./data/bg/default.png"

# Food images
FOOD_1 = "./data/food/1.png"
FOOD_2 = "./data/food/2.png"

# Keys
KEY_UP = "<Up>"
KEY_DOWN = "<Down>"
KEY_RIGHT = "<Right>"
KEY_LEFT = "<Left>"

# Window colors
BG_COLOR = "black"
TEXT_COLOR = "white"
FRAME_COLOR = "white"

# Snake colors
HEAD_COLOR = "white"
TAIL_COLOR = "yellow"

# Menus and buttons
COLOR_MENU = "white"
COLOR_MENU_OVER = "#3f5768"
GAME_OVER_LABEL_COLOR = "yellow"
GAME_WIN_LABEL_COLOR = "yellow"

# Translation
LABEL_NEW_GAME = "New Game"
LABEL_ABOUT = "About this game"
LABEL_TUTORIAL = "How to play?"
LABEL_QUIT = "Quit Game"
LABEL_MAIN_MENU = "Main Menu"
LABEL_GAME_OVER = "GAME OVER"
LABEL_GAME_WIN = "YOU WON"
LABEL_BACK = "Back"
LABEL_SCORE = "Points: "
LABEL_LEVEL = "Level: "
LABEL_VERSION = "Version: "
LABEL_GREETING = "Welcome"
LABEL_GETREADY = "Get ready"

HOWTOPLAY = "In this game you have to be fast. You are snake that moves in game field. You can control the snake with arrow keys, Up, Down, Left and Right. You have to avoid touching obstacles and snake itself. Goal is to eat as much as possible food elements. With every food item taken, snake is going to be longer and faster. Good Luck!!"
TEXT_ABOUT_1 = "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; version 3"
TEXT_ABOUT_2 = "This game is created by Ilija Culap (ilija.culap14@gmail.com)"

class Application(tk.Frame):	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.imgObjects = []
		self.pack()
		
		# Create Canvas
		self.GameFrame = tk.Canvas(self, height=WINDOW_H, width=WINDOW_W, bg=BG_COLOR)
		
		# Set initial background image and version number
		self.set_Background(BG_DEFAULT)
		
		# Show greeting and go to MainMenu
		self.show_Greeting()
		self.goto_MainMenu(self)
			
	def createTextExt(self, canvas, x, y, size=12, fill="white", text="", fontfile="", anchor="center", state=tk.NORMAL, tags=(), ml=False, width=100, spacing=0, bind=False, bindfunc=0):
		
		# Create Font
		font = pilfont.truetype(fontfile, size)

		# Check if the text is multilined
		# get line lenght in char for given width
		if ml == True:			
			oneCharWidth = font.getbbox("O", anchor='lt')[2]
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
			
			numberOfLines = text_new.count("\n") + 1
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
		imageHeight = int((font.getbbox("Fj", anchor='lt')[3]) * numberOfLines * 1.2)
		imageHeight += spacing * numberOfLines
	
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
		self.imgdraw = canvas.create_image(x, y, image=imgext, anchor=anchor, tags=tags_out, state=state)
		
		if bind == True:
			self.GameFrame.tag_bind(objectID, "<Button-1>", bindfunc)
	
	def set_Background(self, folder):
		
		# Remove old bg
		self.GameFrame.delete("initialItem")
				
		# Set initil background image
		self.backgroundImage = tk.PhotoImage(file = folder)
		self.backgroundImageOnCanvas = self.GameFrame.create_image(0, 0, image=self.backgroundImage, anchor=tk.NW, tags="initialItem")

		# Version in bottom right corner
		self.versionNumber = self.createTextExt(self.GameFrame, WINDOW_W - 20, WINDOW_H - 20, text=LABEL_VERSION + " " + GAME_VERSION, fill=TEXT_COLOR, fontfile=FONTFILE_VERSION, size=25, anchor="se", tags="initialItem")
		self.GameFrame.pack()
		
	def create_BackButton(self, where):
		
		# Create back button
		self.back_Button = self.createTextExt(self.GameFrame, x=50, y=25, text=LABEL_BACK, fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="w", tags="tutorialItems", bind=True, bindfunc=where)

	def show_Greeting(self):
		
		# Say hello
		self.greeting = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H/2, text=LABEL_GREETING, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_1, size=130, anchor=tk.CENTER, tags="wmitemTag")
		root.update()
		self.after(2000)
		self.GameFrame.delete("wmitemTag")
		root.update()
		self.after(1000)

	def remove_Everything(self):
		
		# Remove everything from the screen
		self.GameFrame.delete("goScreenItem")
		self.GameFrame.delete("aboutItems")
		self.GameFrame.delete("gsItems")
		self.GameFrame.delete("tutorialItems")
		self.GameFrame.delete("wmitemTag")
		self.GameFrame.delete("gameItems")
		self.GameFrame.delete("headerItem")

	def goto_Tutorial(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()

		# Tutorial Text through new font system
		self.tutorial_text = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=WINDOW_H/2, text=HOWTOPLAY, fill=TEXT_COLOR, fontfile=FONTFILE_1, size=40, anchor="center", tags="tutorialItems", ml=True, width=WINDOW_W-20, spacing=25)
		
		# Back button
		self.create_BackButton(self.goto_MainMenu)
		
	def goto_About(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()
		
		# Back button
		self.create_BackButton(self.goto_MainMenu)
		
		# Load image
		self.imgIcon = tk.PhotoImage(file = "./data/icon.png")
		self.imgIcon = self.imgIcon.subsample(2)
		
		# Show image
		self.imgIconObj = self.GameFrame.create_image(WINDOW_W * 0.5, WINDOW_H * 0.5, image=self.imgIcon, tags="aboutItems")
		
		# Create text
		self.aboutText1 = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=200, text=TEXT_ABOUT_1, fill=TEXT_COLOR, fontfile=FONTFILE_1, size=30, anchor="center", tags="aboutItems", ml=True, width=WINDOW_W - 100, spacing=10)
		self.aboutText2 = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=WINDOW_H-220, text=TEXT_ABOUT_2, fill=TEXT_COLOR, fontfile=FONTFILE_1, size=30, anchor="center", tags="aboutItems", ml=True, width=WINDOW_W - 100, spacing=10)

	def goto_GameOver(self):
		
		# Show cursor, need to add it at game_win
		root.config(cursor="arrow")
		
		# Remove everything from the screen
		self.remove_Everything()
		
		# Set Background
		self.set_Background(BG_DEFAULT)
		
		# Game over text
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.25, text=LABEL_GAME_OVER, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMEOVER, size=80, anchor=tk.CENTER, tags="goScreenItem")
		
		# Score
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.4, text=LABEL_SCORE + str(self.snakePoints), fill="grey", fontfile=FONTFILE_3, size=50, anchor=tk.CENTER, tags="goScreenItem")

		# Menu
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.55, text=LABEL_NEW_GAME, fill=COLOR_MENU, fontfile=FONTFILE_2, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.goto_PlayGame)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.60, text=LABEL_MAIN_MENU, fill=COLOR_MENU, fontfile=FONTFILE_2, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.goto_MainMenu)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.65, text=LABEL_QUIT, fill=COLOR_MENU, fontfile=FONTFILE_2, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.quit_game)

	def goto_MainMenu(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()

		# Set initial background image and version number
		self.set_Background(BG_DEFAULT)
		
		# Main menu buttons, every button has rect and text
		# New game
		self.GameFrame.create_rectangle(WINDOW_W * 0.3, WINDOW_H*0.35-30, WINDOW_W * 0.7, WINDOW_H*0.35 + 45, fill="", activefill=COLOR_MENU_OVER, width=2, outline=FRAME_COLOR, tags=("wmitemTag", "newgameRect"))
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.35, text=LABEL_NEW_GAME, fill=TEXT_COLOR, fontfile=FONTFILE_2, size=60, anchor="center", state=tk.DISABLED, tags="wmitemTag")
		self.GameFrame.tag_bind("newgameRect", "<Button-1>", self.goto_PlayGame)
		
		# Tutorial
		self.GameFrame.create_rectangle(WINDOW_W * 0.3, WINDOW_H*0.45-30, WINDOW_W * 0.7, WINDOW_H*0.45 + 45, fill="", activefill=COLOR_MENU_OVER, width=2, outline=FRAME_COLOR, tags=("wmitemTag", "tutorialRect"))
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.45, text=LABEL_TUTORIAL, fill=TEXT_COLOR, fontfile=FONTFILE_2, size=60, anchor="center", state=tk.DISABLED, tags="wmitemTag")
		self.GameFrame.tag_bind("tutorialRect", "<Button-1>", self.goto_Tutorial)

		# About
		self.GameFrame.create_rectangle(WINDOW_W * 0.3, WINDOW_H*0.55-30, WINDOW_W * 0.7, WINDOW_H*0.55 + 45, fill="", activefill=COLOR_MENU_OVER, width=2, outline=FRAME_COLOR, tags=("wmitemTag", "aboutRect"))
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.55, text=LABEL_ABOUT, fill=TEXT_COLOR, fontfile=FONTFILE_2, size=60, anchor="center", state=tk.DISABLED, tags="wmitemTag")
		self.GameFrame.tag_bind("aboutRect", "<Button-1>", self.goto_About)

		# Quit
		self.GameFrame.create_rectangle(WINDOW_W * 0.3, WINDOW_H*0.65-30, WINDOW_W * 0.7, WINDOW_H*0.65 + 45, fill="", activefill=COLOR_MENU_OVER, width=2, outline=FRAME_COLOR, tags=("wmitemTag", "quitRect"))
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.65, text=LABEL_QUIT, fill=TEXT_COLOR, fontfile=FONTFILE_2, size=60, anchor="center", state=tk.DISABLED, tags="wmitemTag")
		self.GameFrame.tag_bind("quitRect", "<Button-1>", self.quit_game)

	def goto_PlayGame(self, GameFrame):
		
		# Remove everything from the screen
		self.remove_Everything()
		
		self.set_Background(BG_DEFAULT)
		self.start_Game()
		
	def start_Game(self):

		def create_head():
			
			# Snake width is 24px
			self.snake_head_object = self.GameFrame.create_oval(gridOriginX + (snake_index[0]*40) - 32, 
																	 gridOriginY + (snake_index[1]*40) - 32, 
																	 gridOriginX + (snake_index[0]*40) - 8, 
																	 gridOriginY + (snake_index[1]*40) - 8, 
																	 fill=HEAD_COLOR, tags=("gameItems"))
																	 
		def create_tail():
			self.GameFrame.delete("tailItems")
			for i in range(1, self.snake_tail+1):
				self.snake_tail_object = self.GameFrame.create_oval(gridOriginX + (snake_index[(i*2)]*40) - 32, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 32, 
																	gridOriginX + (snake_index[(i*2)]*40) - 8, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 8, 
																	fill=TAIL_COLOR, tags=("tailItems", "gameItems"))

		def findEmptySpot():
			
			# Create list for empty spots
			self.emptySpots = []

			# Generate the list with all fields
			for spotX in range(1, gameGridWidth + 1):
				for spotY in range(1, gameGridHeight + 1):
					self.emptySpots.insert(0, (spotX, spotY))
			
			# Remove spots where the snake is
			for item in range(int(len(snake_index)/2)):
				try:
					self.emptySpots.remove((snake_index[item*2], snake_index[(item*2)+1]))
				except:
					pass
			
			# Remove spots allready in use
			try:
				self.emptySpots.remove((self.food_index_1[0], self.food_index_1[1]))
				self.emptySpots.remove((self.food_index_2[0], self.food_index_1[1]))
			except:
				pass

			# Return random spot
			return self.emptySpots[randint(0, len(self.emptySpots)-1)]

		def createFood_1():
			
			# Get free spot
			self.food_index_1 = findEmptySpot()
	
			# Draw food
			self.foodImage_1 = tk.PhotoImage(file = FOOD_1)
			self.imgObjects.append(self.food_index_1)
			self.food_object_1 = self.GameFrame.create_image(gridOriginX + (self.food_index_1[0]*40) + 10, 
																	 gridOriginY + (self.food_index_1[1]*40) + 10, anchor=tk.SE, image=self.foodImage_1, 
																	 tags=("foodItem", "foodItem-1", "gameItems"))
				
		def createFood_2():
			
			# Get free spot
			self.food_index_2 = findEmptySpot()
			
			# Draw food
			self.foodImage_2 = tk.PhotoImage(file = FOOD_2)
			self.imgObjects.append(self.food_index_2)
			self.food_object_2 = self.GameFrame.create_image(gridOriginX + (self.food_index_2[0]*40) + 10, 
																	 gridOriginY + (self.food_index_2[1]*40) + 10, anchor=tk.SE,image=self.foodImage_2, 
																	 tags=("foodItem", "foodItem-2", "gameItems"))
			
			# Regenerate self.food_2_check variable
			self.food_2_check = randint(10, 50)
			
			# Control if the food-2 is shown
			self.food_2_on = True
			
		def getCalories(food, location): ## Needs rework
			
			# Points for every food object
			self.snakePoints += 10 + (food*5)
			self.snakePoints += round(self.snake_tail/3)
			
			# Bonus points for food-2
			if food == 2:
				self.snakePoints += 30
			
			# Bonus for edge objects
			if food == 1:
				pass
		
		def define_level(x):
			
			# Bump level up for 5 eaten food
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
				self.goto_GameOver()
				return True
			
			# If snake head touches snake tail
			for x in range(1, self.snake_tail):
				if snake_index[0] == snake_index[x*2] and snake_index[1] == snake_index[(x*2)+1]:
					self.goto_GameOver()
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
		
		def moveSnake():
			
			# Set focus and bind keys
			self.GameFrame.focus_set()
			bind_keys()
			
			# Move head, update index acording to new head position and then create tail
			self.GameFrame.move(self.snake_head_object, self.dir_x, self.dir_y)
			update_index()
			create_tail()
			
			# Reduce food_2_check -1
			self.food_2_check -= 1
			
			# If food-1 is eaten
			if snake_index[0] == self.food_index_1[0] and snake_index[1] == self.food_index_1[1]:
				self.foodEaten = True
				getCalories(1, self.food_index_1)
				self.GameFrame.delete("foodItem-1")
				self.snake_tail += 1
				
				# Update score and points
				self.GameFrame.delete("headerItem")
				self.scoreText = self.createTextExt(self.GameFrame, 50, 25, text=LABEL_SCORE + str(self.snakePoints), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="w", tags="headerItem")
				self.levelText = self.createTextExt(self.GameFrame, WINDOW_W - 50, 25, text=LABEL_LEVEL + str(define_level(self.snake_tail)), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="e", tags="headerItem")

				# Create new food
				createFood_1()
			
			# If food-2 is eaten
			if snake_index[0] == self.food_index_2[0] and snake_index[1] == self.food_index_2[1]:
				self.foodEaten = True
				self.food_2_on = False
				getCalories(2, self.food_index_2)
				self.GameFrame.delete("foodItem-2")
				self.snake_tail += 1
				
				# Update score and points
				self.GameFrame.delete("headerItem")
				self.scoreText = self.createTextExt(self.GameFrame, 50, 25, text=LABEL_SCORE + str(self.snakePoints), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="w", tags="headerItem")
				self.levelText = self.createTextExt(self.GameFrame, WINDOW_W - 50, 25, text=LABEL_LEVEL + str(define_level(self.snake_tail)), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="e", tags="headerItem")
			
			# If food-2 is not eaten
			if self.food_2_check == 1:
				x = randint(1, 20)
				
				# Wait for next
				if x > 7:
					self.food_2_check += randint(10, 20)
				else:
					if self.food_2_on == True:
						self.GameFrame.delete("foodItem-2")
						self.food_index_2 = [-1, -1]
						self.food_2_check = randint(20, 40)
						self.food_2_on = False
					
					elif self.food_2_on == False:
						createFood_2()
						self.food_2_on = True
			
			# Look for gameover
			if self.snakeMoves:
				if checkGameOver() == True:
					snakeMoves = False
				else:
					self.GameFrame.after(100 - round(self.snake_tail/3), moveSnake)
		
		# Disable cursor
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
		self.food_index_1 = findEmptySpot()
		self.food_index_2 = findEmptySpot()

		# Some vars for game
		self.snake_tail = 5
		self.foodEaten = False
		self.snakePoints = 0
		snake_level = 1
		
		# Movement vars for the snake
		self.dir_x = 40
		self.dir_y = 0
		
		# Get ready
		self.getReadyLabel = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H/2, text=LABEL_GETREADY, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_1, size=130, anchor=tk.CENTER, tags="getReady")
		root.update()
		self.GameFrame.after(1000)
		self.GameFrame.delete("getReady")
		
		# Create text for score and level
		self.scoreText = self.createTextExt(self.GameFrame, 50, 25, text=LABEL_SCORE + str(self.snakePoints), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="w", tags="headerItem")
		self.levelText = self.createTextExt(self.GameFrame, WINDOW_W - 50, 25, text=LABEL_LEVEL + str(define_level(self.snake_tail)), fill=TEXT_COLOR, fontfile=FONTFILE_3, size=20, anchor="e", tags="headerItem")
		
		# Generate self.food_2_check variable
		self.food_2_check = randint(10, 50)
		self.food_2_on = False
		
		# Create a food item and snake head
		createFood_1()
		create_head()
		
		# Snake moves
		self.snakeMoves = True
		
		# Start moving the snake
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
