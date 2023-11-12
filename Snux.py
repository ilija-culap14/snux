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
GAME_LICENCE = "GPLv3"
GAME_AUTHOR = "Ilija Culap <ilija.culap14@gmail.com>"

# Window vars
WINDOW_H = 900
WINDOW_W = 1200
FRAME_OFFSET = 50

# Font files
FONTFILE_GAMEOVER = ("./data/fonts/gameover.ttf")
FONTFILE_TUTORIAL = ("./data/fonts/tutorial.ttf")
FONTFILE_BACK = ("./data/fonts/back.ttf")
FONTFILE_GAMESELECTOR_HEADING = ("./data/fonts/gameselector_heading.otf")
FONTFILE_MENUITEM = ("./data/fonts/menuitem.otf")
FONTFILE_VERSION = ("./data/fonts/version.otf")

# Folders for levels, default is survival mode
FOLDER_LEVEL = ""
FOLDER_LEVELS = "./data/levels/"
FOLDER_DEFAULT = "./data/default/"

# Levels system
LEVELS_INFO = []

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
COLOR_MENU_OVER = "#1B94C6"
GAME_OVER_LABEL_COLOR = "yellow"
GAME_WIN_LABEL_COLOR = "yellow"

# Translation
LABEL_NEW_GAME = "New Game"
LABEL_CHOOSE_GAME = "Choose another game"
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

# Game selector
LABEL_GAMESELECTOR_HEADING = "Select the game mode you wish to play!"
LABEL_GAMESELECTOR_SURVIVAL = "Survival mode"
LABEL_GAMESELECTOR_LEVEL = "Choose level"

# Level selector
LABEL_LEVELSELECTOR_HEADING = "Select the level!"

HOWTOPLAY = "In this game you have to be fast. You are snake that moves in game field. You can control the snake with arrow keys, Up, Down, Left and Right. You have to avoid touching obstacles and snake itself. Goal is to eat as much as possible food elements. With every food item taken, snake is going to be longer and faster. Good Luck!!"
TEXT_ABOUT_1 = "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; version 3"
TEXT_ABOUT_2 = "Author:"
TEXT_ABOUT_3 = "Licence: "

class Application(tk.Frame):	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.imgObjects = []
		self.pack()
		
		# Create Canvas
		self.GameFrame = tk.Canvas(self, height=WINDOW_H, width=WINDOW_W, bg=BG_COLOR)
		
		# Set initial background image and version number
		self.set_Background(FOLDER_DEFAULT)
		
		# Show greeting and go to MainMenu
		self.show_Greeting()
		self.goto_MainMenu(self)
			
	def createTextExt(self, canvas, x, y, size=12, fill="white", text="", fontfile="", anchor="center", tags=(), ml=False, width=100, spacing=0, bind=False, bindfunc=0):
		
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
		self.imgdraw = canvas.create_image(x, y, image=imgext, anchor=anchor, tags=tags_out)
		
		if bind == True:
			self.GameFrame.tag_bind(objectID, "<Button-1>", bindfunc)
	
	def set_Background(self, folder):
		
		# Remove old bg
		self.GameFrame.delete("initialItem")
				
		# Set initil background image
		self.backgroundImage = tk.PhotoImage(file = folder + "bg.png")
		self.backgroundImageOnCanvas = self.GameFrame.create_image(0, 0, image=self.backgroundImage, anchor=tk.NW, tags="initialItem")

		# Version in bottom right corner
		self.versionNumber = self.createTextExt(self.GameFrame, WINDOW_W - 20, WINDOW_H - 20, text=LABEL_VERSION + GAME_VERSION, fill=TEXT_COLOR, fontfile=FONTFILE_VERSION, size=17, anchor="se", tags="initialItem")
		self.GameFrame.pack()
		
	def create_BackButton(self, where):
		
		# Create back button
		self.back_Button = self.createTextExt(self.GameFrame, x=50, y=25, text=LABEL_BACK, fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="w", tags="tutorialItems", bind=True, bindfunc=where)

	def show_Greeting(self):
		
		# Say hello
		self.greeting = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H/2, text=LABEL_GREETING, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=130, anchor=tk.CENTER, tags="wmitemTag")
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

	def goto_GameSelector(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()

		# Survival mode
		def onSurvivalMode(event):
			self.gameMode = "survival"
			self.goto_PlayGame(self)
			
		# Level mode
		def onLevelMode(event):
			self.gameMode = "level"
			self.goto_LevelSelector(self)
		
		# Heading
		self.gameSelectorHeading = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.18, text=LABEL_GAMESELECTOR_HEADING, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=50, anchor=tk.CENTER, tags="wmitemTag")

		# Load images
		self.imgSurvive = tk.PhotoImage(file = "./data/gameselector/gs_survival.png")
		self.imgLevel = tk.PhotoImage(file = "./data/gameselector/gs_level.png")
		
		# Show images
		self.gs_Survive = self.GameFrame.create_image(WINDOW_W * 0.3, WINDOW_H * 0.4, image=self.imgSurvive, tags="gsItems")
		self.gs_Level = self.GameFrame.create_image(WINDOW_W * 0.7, WINDOW_H * 0.4, image=self.imgLevel, tags="gsItems")
		
		# Show labels
		self.gs_SurviveLabel = self.createTextExt(self.GameFrame, WINDOW_W * 0.3, WINDOW_H * 0.55, text=LABEL_GAMESELECTOR_SURVIVAL, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=50, anchor=tk.CENTER, tags="gsItems", bind=True, bindfunc=onSurvivalMode)
		self.gs_LevelLabel = self.createTextExt(self.GameFrame, WINDOW_W * 0.7, WINDOW_H * 0.55, text=LABEL_GAMESELECTOR_LEVEL, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=50, anchor=tk.CENTER, tags="gsItems", bind=True, bindfunc=onLevelMode)
		
		# Back button
		self.create_BackButton(self.goto_MainMenu)
		
	def goto_LevelSelector(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()

		# Heading
		self.levelSelectorHeading = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.18, text=LABEL_LEVELSELECTOR_HEADING, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=50, anchor=tk.CENTER, tags="wmitemTag")
		
		# Grid is 3x3 for levels
		# Every element has picture (thumb.png) and name from LEVELS_INFO
		
		# Read manifest file to determine what levels are installed
		global LEVELS_INFO
		with open(FOLDER_LEVELS + "manifest", "r") as f:
			for line in f.readlines():
				if line == "\n":
					pass
				else:
					LEVELS_INFO.append(line.replace("\n", "").split("@@@@@"))
			
		
		#################################
		# 
		# INFO
		#
		# Level folder containt: 
		#      - bg.png
		#      - food-1.png
		#      - food-2.png
		#      - food-3.png
		#      - food-bonus.png
		#      - thumb.png
		#      - snake.cfg
		#      - const.png
		# 
		#################################
		
		# Debug
		self.levelFolder = "level-1"
		
		# Back button
		self.create_BackButton(self.goto_GameSelector)
				
	def goto_Tutorial(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()

		# Tutorial Text through new font system
		self.tutorial_text = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=WINDOW_H/2, text=HOWTOPLAY, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=40, anchor="center", tags="tutorialItems", ml=True, width=WINDOW_W-20, spacing=25)
		
		# Back button
		self.create_BackButton(self.goto_MainMenu)
		
	def goto_About(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()
		
		# Back button
		self.create_BackButton(self.goto_MainMenu)
		
		# Create text
		self.aboutText1 = self.createTextExt(self.GameFrame, x=WINDOW_W/2, y=200, text=TEXT_ABOUT_1, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=30, anchor="center", tags="aboutItems", ml=True, width=WINDOW_W - 100, spacing=10)
		self.author1 = self.createTextExt(self.GameFrame, x=WINDOW_W*0.60, y=400, text=TEXT_ABOUT_2, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=30, anchor="w", tags="aboutItems")
		self.author2 = self.createTextExt(self.GameFrame, x=WINDOW_W*0.60, y=430, text=GAME_AUTHOR, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=30, anchor="w", tags="aboutItems")
		self.licence1 = self.createTextExt(self.GameFrame, x=WINDOW_W*0.60, y=500, text=TEXT_ABOUT_3, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=30, anchor="w", tags="aboutItems")
		self.licence2 = self.createTextExt(self.GameFrame, x=WINDOW_W*0.60, y=530, text=GAME_LICENCE, fill=TEXT_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=30, anchor="w", tags="aboutItems")
		
	def goto_GameOver(self): #### Need work
		
		# Show cursor, need to add it at game_win
		root.config(cursor="arrow")
		
		# Remove everything from the screen
		self.remove_Everything()
		
		# Set Background
		self.set_Background(FOLDER_DEFAULT)
		
		# Game over text
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.25, text=LABEL_GAME_OVER, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMEOVER, size=80, anchor=tk.CENTER, tags="goScreenItem")
		
		# Score
		self.game_over_text = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.4, text=LABEL_SCORE + str(self.snakePoints), fill="grey", fontfile=FONTFILE_BACK, size=50, anchor=tk.CENTER, tags="goScreenItem")

		# Menu
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.55, text=LABEL_NEW_GAME, fill=COLOR_MENU, fontfile=FONTFILE_MENUITEM, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.goto_PlayGame)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.6, text=LABEL_CHOOSE_GAME, fill=COLOR_MENU, fontfile=FONTFILE_MENUITEM, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.goto_GameSelector)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.65, text=LABEL_MAIN_MENU, fill=COLOR_MENU, fontfile=FONTFILE_MENUITEM, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.goto_MainMenu)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.7, text=LABEL_QUIT, fill=COLOR_MENU, fontfile=FONTFILE_MENUITEM, size=30, anchor="center", tags="goScreenItem", bind=True, bindfunc=self.quit_game)

	def goto_MainMenu(self, GameFrame):
		
		# Remove everything from screen
		self.remove_Everything()
		
		# Main menu buttons
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.35, text=LABEL_NEW_GAME, fill=TEXT_COLOR, fontfile=FONTFILE_MENUITEM, size=60, anchor="center", tags="wmitemTag", bind=True, bindfunc=self.goto_GameSelector)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.45, text=LABEL_TUTORIAL, fill=TEXT_COLOR, fontfile=FONTFILE_MENUITEM, size=60, anchor="center", tags="wmitemTag", bind=True, bindfunc=self.goto_Tutorial)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.55, text=LABEL_ABOUT, fill=TEXT_COLOR, fontfile=FONTFILE_MENUITEM, size=60, anchor="center", tags="wmitemTag", bind=True, bindfunc=self.goto_About)
		self.mmButton = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H*0.65, text=LABEL_QUIT, fill=TEXT_COLOR, fontfile=FONTFILE_MENUITEM, size=60, anchor="center", tags="wmitemTag", bind=True, bindfunc=self.quit_game)

	def goto_PlayGame(self, GameFrame):
		
		# Remove everything from the screen
		self.remove_Everything()
		
		# Determine in what mode we are
		global FOLDER_LEVEL
		if self.gameMode == "survival":
			FOLDER_LEVEL = "./data/levels/0-survival/"
			self.set_Background(FOLDER_LEVEL)
			self.start_Game()
		elif self.gameMode == "level":
			FOLDER_LEVEL = "./data/levels/" + self.levelFolder
			self.set_Background(FOLDER_LEVEL)
			self.start_Game()
		
	def start_Game(self):
		
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
		food_index_1 = [0, 0]
		food_index_2 = [0, 0]
		food_index_3 = [0, 0]
		food_index_bonus = [0, 0]
		
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
																	 fill=HEAD_COLOR, tags=("gameItems"))
																	 
		def create_tail():
			self.GameFrame.delete("tailItems")
			for i in range(1, self.snake_tail+1):
				self.snake_tail_object = self.GameFrame.create_oval(gridOriginX + (snake_index[(i*2)]*40) - 32, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 32, 
																	gridOriginX + (snake_index[(i*2)]*40) - 8, 
																	gridOriginY + (snake_index[(i*2)+1]*40) - 8, 
																	fill=TAIL_COLOR, tags=("tailItems", "gameItems"))
																	 
				
		def createFood_1():
			
			# need work
			food_index_1.insert(0, randint(1, gameGridHeight))
			food_index_1.insert(0, randint(1, gameGridWidth))
			
			# Testing image as food
			self.foodImage = tk.PhotoImage(file = FOLDER_LEVEL + "food_1.png")
			self.food_object = self.GameFrame.create_image(gridOriginX + (food_index_1[0]*40), 
																	 gridOriginY + (food_index_1[1]*40), anchor=tk.SE,image=self.foodImage, 
																	 tags=("foodItem", "gameItems"))
				
		def createFood_2():
			
			# need work
			food_index.insert(0, randint(1, gameGridHeight))
			food_index.insert(0, randint(1, gameGridWidth))
			
			# Testing image as food
			self.foodImage = tk.PhotoImage(file = FOLDER_LEVEL + "food_2.png")
			self.food_object = self.GameFrame.create_image(gridOriginX + (food_index_2[0]*40), 
																	 gridOriginY + (food_index_2[1]*40), anchor=tk.SE,image=self.foodImage, 
																	 tags=("foodItem", "gameItems"))
				
		def createFood_3():
			
			# need work
			food_index.insert(0, randint(1, gameGridHeight))
			food_index.insert(0, randint(1, gameGridWidth))
			
			# Testing image as food
			self.foodImage = tk.PhotoImage(file = FOLDER_LEVEL + "food_3.png")
			self.food_object = self.GameFrame.create_image(gridOriginX + (food_index_3[0]*40), 
																	 gridOriginY + (food_index_3[1]*40), anchor=tk.SE,image=self.foodImage, 
																	 tags=("foodItem", "gameItems"))
				
		def createFood_Bonus():
			
			# Put some random number in food index, need work
			# i need function that gets free spot on map
			# then randomly select one of them
			food_index.insert(0, randint(1, gameGridHeight))
			food_index.insert(0, randint(1, gameGridWidth))
			
			# Testing image as food
			self.foodImage = tk.PhotoImage(file = FOLDER_LEVEL + "food_bonus.png")
			self.food_object = self.GameFrame.create_image(gridOriginX + (food_index_bonus[0]*40), 
																	 gridOriginY + (food_index_bonus[1]*40), anchor=tk.SE,image=self.foodImage, 
																	 tags=("foodItem", "gameItems"))
				
		def getCalories():
			
			# 10 points for food
			self.snakePoints += 10
			self.snakePoints += round(self.snake_tail/3)
			
			# Bonus for edge objects
			if food_index_1[0] == 1 or food_index_1[0] == gameGridWidth:
				self.snakePoints += 4
			if food_index_1[1] == 1 or food_index_1[1] == gameGridHeight:
				self.snakePoints += 4
		
		def define_level(x):
			
			# Bumb level up for 5 eaten food
			level = round((x/5) - 0.49)
			return level
			
		def defineGameMode():
			# This function need to define mode and set all vars
			pass

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
			if snake_index[0] == food_index_1[0] and snake_index[1] == food_index_1[1]:
				self.foodEaten = True
				getCalories()
				self.GameFrame.delete("foodItem")
				self.snake_tail += 1
				
				# Update score and points
				self.GameFrame.delete("headerItem")
				self.scoreText = self.createTextExt(self.GameFrame, 50, 25, text=LABEL_SCORE + str(self.snakePoints), fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="w", tags="headerItem")
				self.levelText = self.createTextExt(self.GameFrame, WINDOW_W - 50, 25, text=LABEL_LEVEL + str(define_level(self.snake_tail)), fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="e", tags="headerItem")

				# Create new food
				createFood_1()
			
			# Look for gameover
			if self.snakeMoves:
				if checkGameOver() == True:
					snakeMoves = False
				else:
					self.GameFrame.after(120 - round(self.snake_tail/3), moveSnake)
		
		# Get ready
		self.getReadyLabel = self.createTextExt(self.GameFrame, WINDOW_W/2, WINDOW_H/2, text=LABEL_GETREADY, fill=GAME_OVER_LABEL_COLOR, fontfile=FONTFILE_GAMESELECTOR_HEADING, size=130, anchor=tk.CENTER, tags="getReady")
		root.update()
		self.GameFrame.after(1000)
		self.GameFrame.delete("getReady")
		
		# Create text for score and level
		self.scoreText = self.createTextExt(self.GameFrame, 50, 25, text=LABEL_SCORE + str(self.snakePoints), fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="w", tags="headerItem")
		self.levelText = self.createTextExt(self.GameFrame, WINDOW_W - 50, 25, text=LABEL_LEVEL + str(define_level(self.snake_tail)), fill=TEXT_COLOR, fontfile=FONTFILE_BACK, size=20, anchor="e", tags="headerItem")

		# Create a food item and snake head
		createFood_1()
		create_head()
		
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
