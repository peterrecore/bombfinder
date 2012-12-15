## Author: Manan Shah
## Email: manyshah@gmail.com
## Date: 03.08.2007
## Description: A better version of the Windows game Minesweeper
## Anyone may use this file in part or entirety for non-commercial use.  Just cite the author.

from Tkinter import *
from random import *
import tkSimpleDialog
import pickle

class MyMinesweeper:
    def __init__(self,parent):
        self.myparent = parent
        self.Container = Frame(parent, bg = "black", relief = SUNKEN, bd = 1)
        self.Container.pack(ipadx = "1m", ipady = "1m")
        self.GameContainer = Frame(self.Container, bg = "gray", relief = RAISED)
        self.GameContainer.grid(row = 0, column = 0, ipadx = "1m", ipady = "1m", sticky = NW)
        self.OutputContainer = Frame(self.Container, bg = "black")
        self.OutputContainer.grid(row = 1, column = 0, ipadx = "1m", ipady = "1m", sticky = SW)
        self.rowsize = 10
        self.colsize = 10
        self.itemprobability = 0.25
        self.numdetectors = 1
        self.numlisteningposts = 1
        self.count = 0
        self.btns = []
        self.replay = 0
        self.score = 0
        self.highscore = 0
        self.winloserestart = 0 # 1 = win, -1 = lose, 0 = restart without win or lose

        self.LoadBoardSize()
        self.LoadScores()
        self.PlaceItem()
        self.MakeButtons()
        self.ShowSomeButtons()
        self.MakeMenu()

    def __del__(self):
        self.ExitClick()

    def MakeMenu(self):
        self.menu = Menu(self.myparent)
        self.myparent.config(menu = self.menu)
        self.filemenu = Menu(self.menu)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.filemenu)
        self.menu.add_cascade(label="Help",menu=self.helpmenu)
        self.filemenu.add_command(label = "New ...", command = self.NewClick)
#        filemenu.add_command(label = "Finished", command = self.FinishedClick)
        self.filemenu.add_command(label = "Load Game", command = self.LoadGame)
        self.filemenu.add_command(label = "Restart", command = self.RestartClick_a)
        self.filemenu.add_command(label = "Save Settings and Exit", command = self.ExitClick)
        self.helpmenu.add_command(label = "Help On ItemFinder", command = self.HelpClick)

    def MakeButtons(self):
        a = range(self.rowsize)
        b = range(self.colsize)
        for i in a:
            for j in b:
                self.pos = [i, j, 0]
                self.btns.append(Button(self.GameContainer))
                self.btns[j+i*self.colsize] = Button(self.GameContainer,text = "", fg = "black", bg = "gray",
                                                    command = lambda arg1=self.pos: self.ButtonClick(arg1),
                                                     width = 1, height = 1, wraplength = 70, relief = RAISED,
                                                     padx = "1m", pady = "1m", disabledforeground = "black")
                self.btns[j+i*self.colsize].bind("<3>", lambda event, arg1=self.pos: self.Button2Click(arg1))
                self.btns[j+i*self.colsize].bind("m", lambda event, arg1=self.pos: self.Button2Click(arg1))
                self.btns[j+i*self.colsize].bind("a", lambda event, arg1=self.pos,arg2='left': self.SetFocus(arg1,arg2))
                self.btns[j+i*self.colsize].bind("s", lambda event, arg1=self.pos,arg2='down': self.SetFocus(arg1,arg2))
                self.btns[j+i*self.colsize].bind("d", lambda event, arg1=self.pos,arg2='right': self.SetFocus(arg1,arg2))
                self.btns[j+i*self.colsize].bind("w", lambda event, arg1=self.pos,arg2='up': self.SetFocus(arg1,arg2))
                
                self.btns[j+i*self.colsize].grid(row = i, column = j)
        if self.replay == 0:
            self.FinishedButton = Button(self.OutputContainer, text = "Finished", bg = "gray", command = self.FinishedClick,
                                         padx = "1m", pady="1m", width = 9, height = 1, justify = LEFT)
            self.FinishedButton.bind("<3>", lambda event: self.RestartClick(self.rowsize,self.colsize))
            self.FinishedButton.grid(row = 0, column = 0, sticky = W)
            self.ScoreLabel = Label(self.OutputContainer, text = "Score: " + str(self.score) + "\nHigh Score: " + str(self.highscore),
                                    bg = "black", fg = "green", pady = "1m", width = 14, height = 2, justify = LEFT)
            self.ScoreLabel.grid(row= 2,column = 0, sticky = W)
##            self.DetectMeButton = Button(self.OutputContainer, text = "!",bg = "green", fg = "black",
##                                         disabledforeground = "green", state = NORMAL, padx = "1m", pady = "1m",
##                                         width = 1, height = 1)
##            self.DetectMeButton.grid(row = 1, column = 1, sticky = W)
            self.DetectorLabel = Label(self.OutputContainer, text = "Detectors Left: " + str(self.numdetectors),
                                       bg = "black", fg = "green", pady = "1m", width = 14, height = 2, justify = LEFT)
            self.DetectorLabel.grid(row = 1, column = 0, sticky = W)
            self.ListeningPostLabel = Label(self.OutputContainer, text = "Listening Posts Left: " + str(self.numlisteningposts),
                                             bg = "black", fg = "green", pady = "1m", width = 18, height = 2, justify = LEFT)
            self.ListeningPostLabel.grid(row = 1, column = 1, sticky = W)
        self.FinishedButton['text'] = "Finished"
        self.FinishedButton['bg'] = "gray"

        
    def ButtonClick(self, pos):
        index = pos[0]*self.colsize + pos[1]
        count = 0
        if self.btns[index]['bg'] == "gray":
            if pos in self.loc and self.winloserestart != -1 and self.btns[index]['bg']!="yellow":
                count = self.GiveNeighborhood(pos,count)
                if self.btns[index]['bg'] == "gray":
                    self.btns[index]['bg'] = "white"
                    self.btns[index]['relief'] = SUNKEN
                    self.btns[index]['text'] = count
                    self.btns[index]['state'] = DISABLED
                    if count != 0:
                        self.score = self.score + 1
                        if self.highscore < self.score:
                            self.highscore = self.score
                        self.UpdateScore()
                    else:
                        self.btns[index]['text'] = ""
                        if pos[0] - 1 >= 0 and pos[1] - 1 >= 0:
                            temp_pos = [pos[0]-1, pos[1]-1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[0] - 1 >= 0:
                            temp_pos = [pos[0]-1, pos[1],0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[0] - 1 >= 0 and pos[1] + 1 < self.colsize:
                            temp_pos = [pos[0]-1, pos[1]+1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[1] + 1 < self.colsize:
                            temp_pos = [pos[0], pos[1]+1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[0] + 1 < self.rowsize and pos[1] + 1 < self.colsize:
                            temp_pos = [pos[0]+1, pos[1]+1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[0] + 1 < self.rowsize:
                            temp_pos = [pos[0]+1, pos[1],0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[0] + 1 < self.rowsize and pos[1] - 1 >= 0:
                            temp_pos = [pos[0]+1, pos[1]-1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                        if pos[1] - 1 >= 0:
                            temp_pos = [pos[0], pos[1]-1,0]
                            temp_index = temp_pos[0]*self.colsize + temp_pos[1]
                            if self.btns[temp_index]['bg'] == "gray" and self.FinishedButton['text'] != "You Win!":
                                self.ButtonClick(temp_pos)
                    self.FinishedClick()
            else:
                temp_pos = [pos[0],pos[1],1]
                if self.btns[index]['bg'] != "red" and temp_pos in self.loc and self.FinishedButton['text'] != "You Lose!" and self.numdetectors == 0:
                    self.btns[index]['bg'] = "red"
                    self.btns[index]['text'] = ""
                    self.FinishedButton['bg'] = "red"
                    self.FinishedButton['text'] = "You Lose!"
                    self.btns[index]['state'] = DISABLED
                    self.winloserestart = -1
                else:
                    self.btns[index]['bg'] = "yellow"
                    self.ButtonClick(pos)
#        elif self.btns[index]['bg'] == "yellow" and self.DetectMeButton['state'] == NORMAL:
        elif self.btns[index]['bg'] == "yellow" and self.numdetectors > 0:
            if [pos[0],pos[1],1] in self.loc:
                self.btns[index]['bg'] = "blue"
                self.btns[index]['text'] = ""
            else:
                self.btns[index]['bg'] = "gray"
                self.ButtonClick(pos)
#            self.ToggleDetectMeButton()
            self.numdetectors = self.numdetectors - 1
            self.DetectorLabel['text'] = "Detectors Left: " + str(self.numdetectors)
            self.FinishedClick()
        elif self.btns[index]['bg'] == "green" and self.numlisteningposts > 0:
            self.numlisteningposts = self.numlisteningposts - 1
            self.ListeningPostLabel['text'] = "Listening Posts Left: " + str(self.numlisteningposts)
            if [pos[0],pos[1],1] in self.loc:
                self.btns[index]['bg'] = "red"
                self.btns[index]['text'] = ""
            else:
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        k = (pos[0]+i)*self.colsize + (pos[1]+j)
                        if [pos[0]+i,pos[1]+j,1] in self.loc:
                            self.btns[k]['bg'] = "blue"
                            self.btns[k]['text'] = ""
#                        elif k >= 0 and k < self.rowsize*self.colsize:
                        elif [pos[0] + i, pos[1] + j, 0] in self.loc:
                            temppos = [pos[0] + i, pos[1] + j, 0]
#                            if [i,j] == [0,0]:
                            if self.btns[k]['bg'] != "white":
                                self.btns[k]['bg'] = "gray"
                                self.btns[k]['text'] = ""
                            self.ButtonClick(temppos)
                        else:
                            pass
            self.FinishedClick()
        else:
            pass

    def Button2Click(self,pos):
        index = pos[0]*self.colsize + pos[1]
        if self.FinishedButton['text'] != "You Lose!":
            if self.btns[index]['bg'] == "blue":
                self.btns[index]['bg'] = "yellow"
                self.btns[index]['text'] = "?"
            elif self.btns[index]['bg'] == "yellow":
                self.btns[index]['bg'] = "green"
                self.btns[index]['text'] = "?"
            elif self.btns[index]['bg'] == "green":
                self.btns[index]['bg'] = "gray"
                self.btns[index]['text'] = ""
            elif self.btns[index]['bg'] != "white" and self.btns[index]['bg'] != "red":
                self.btns[index]['bg'] = "blue"
                self.btns[index]['text'] = ""
            else:
                pass
            self.FinishedClick()

    def SetFocus(self, position, direction):
        y = position[0]
        x = position[1]
        index = y* self.colsize + x
        if direction == 'up' and y - 1 >= 0:
            target = (y-1) * self.colsize + x
            self.btns[target].focus_force()
        elif direction == 'down' and y + 1 < self.rowsize:
            target = (y+1) * self.colsize + x
            self.btns[target].focus_force()
        elif direction == 'left' and x - 1 >= 0:
            target = (y) * self.colsize + x-1
            self.btns[target].focus_force()
        elif direction == 'right' and x + 1 < self.colsize:
            target = (y) * self.colsize + x+1
            self.btns[target].focus_force()
        else:
            pass



    def ToggleDetectMeButton(self):
        if self.DetectMeButton['state'] == NORMAL:
            self.DetectMeButton['state'] = DISABLED
        else:
            self.DetectMeButton['state'] = NORMAL

    def NewClick(self):
        temp = [0,0]
        newgameflag = [0]
        class DimensionInput(tkSimpleDialog.Dialog):
            def __init__(self,parent):
                self.subparent = parent
                self.subContainer = Frame(self.subparent)
                self.subContainer.grid(row = 0, columnspan = 2, ipadx = "1m", ipady = "1m")
                self.subsubContainer = Frame(self.subparent)
                self.subsubContainer.grid(row = 1, column = 0, ipadx = "1m", ipady = "1m")
                self.label1 = Label(self.subContainer, text = 'New Number of Rows', justify = RIGHT)
                self.label1.grid(row = 0, column = 0, sticky = E)
                self.label2 = Label(self.subContainer, text = 'New Number of Columns', justify = RIGHT)
                self.label2.grid(row = 1, column = 0, sticky = E)
                self.e1 = Entry(self.subContainer)
                self.e1.grid(row = 0, column = 1)
                self.e2 = Entry(self.subContainer)
                self.e2.grid(row = 1, column = 1)
                self.b1 = Button(self.subsubContainer, text = 'Ok', command = self.getEntry)
                self.b1.grid(row = 0, column = 0, padx = "1m")
                self.b2 = Button(self.subsubContainer, text = 'Cancel', command = self.CancelClick)
                self.b2.grid(row = 0, column = 1, padx = "1m")
            def getEntry(self):
                if self.e1.get() != "" and self.e2.get() != "" and int(self.e1.get()) > 0 and int(self.e2.get()) > 0:
                    temp[0] = int(self.e1.get())
                    temp[1] = int(self.e2.get())
                    newgameflag[0] = 1
                    self.doNothing()
                else:
                    temp[0] = 10
                    temp[1] = 10
                    newgameflag[0] = 1
                    self.doNothing()
            def CancelClick(self):
                self.doNothing()
            def doNothing(self):
                self.subparent.destroy()

        self.subroot = Toplevel(self.myparent)
        self.dimensionchange = DimensionInput(self.subroot)
        self.subroot.wait_window()

        if newgameflag[0] == 1:
            self.RestartClick(temp[0],temp[1])

    def HelpClick(self):
        class HelpDisplay(tkSimpleDialog.Dialog):
            def __init__(self,parent):
                self.subparent = parent
                self.subContainer = Frame(self.subparent)
                self.subContainer.pack()
                self.subContainer.focus_force()
                self.helptext = Text(self.subContainer, state = NORMAL, fg = "black", wrap = WORD, height = 40, width = 120)
                self.helptext.pack()
                self.helptext.insert(END,"Hello this is the Help menu for Bomb Finder!\n\n")
                self.helptext.insert(END,"Here's how you play:\n")
                self.helptext.insert(END,"- Each tile may or may not contain a bomb.\n")
                self.helptext.insert(END,"- If the tile contains a number, then that tile has that many bombs surrounding it - no more, no less.\n")
                self.helptext.insert(END,"- Your task is to find all the tiles that do NOT have bombs.\n\n")
                self.helptext.insert(END,"- Left-click on a tile to reveal its contents.\n")
                self.helptext.insert(END,"- Right-click on a tile to mark it as a bomb.  You may be wrong, though!\n")
                self.helptext.insert(END,"- Right-clicking a few more times will allow you to cycle between using a bomb detector, a listening post, or unmarking the tile altogether.\n")
                self.helptext.insert(END,"- You start the game with one detector that gives you a free peek at a tile.\n")
                self.helptext.insert(END,"- To use it, right-click on the tile until you get the yellow \"?\" and then left-click on the tile.\n")
                self.helptext.insert(END,"- If the detector finds a bomb then it will be marked automatically for you, else the tile will be reveald.\n")
                self.helptext.insert(END,"- You earn one detector for every board you complete.\n")
                self.helptext.insert(END, "- Additionally, you start the game with one listening post.\n")
                self.helptext.insert(END, "- To use it, right-click on the tile until you get the green \"?\" and then left-click on the tile.\n")
                self.helptext.insert(END, "- If the listening post was sitting on a bomb tile, then you lose, otherwise it will expose the tile on which it was placed, plus all the surrounding tiles.\n")
                self.helptext.insert(END, "- The listening post will mark all the bombs and reveal all the numbers of all the tiles adjacent to the tile on which it was placed.\n")
                self.helptext.insert(END, "- You earn one listening post for every board you complete\n")
                self.helptext.insert(END,"- Right-click on the \"Keep Going!\" button to start a new game.  This will erase your current score.\n\n")
                self.helptext.insert(END,"- Victory is automatically confirmed for you and clicking on the \"You Win!\" button starts a new level.\n")
                self.helptext.insert(END,"- If you lose, then clicking on the \"You Lose!\" button will start a new game.\n")
                self.helptext.insert(END,"- Ultimately, the goal is to have fun and to use this as a minor distraction from work.\n")
                self.helptext.insert(END,"- Try to get as a high a score as possible!\n\n")
                self.helptext.insert(END,"- You can use the keyboard as well!  WASD for moving through the tiles, <space> to reveal the tile, and \"m\" acts as right-clicking.\n")
                self.helptext.insert(END,"- Great for multiplayer!")
                self.helptext['state'] = DISABLED

        self.subroot = Toplevel(self.myparent)
        self.subroot.title("Help")
        self.helpdisplay = HelpDisplay(self.subroot)
        self.subroot.wait_window()

    def FinishedClick(self):
        x = 1
        if self.FinishedButton['text'] == "You Lose!":
            self.replay = 1
            self.RestartClick(self.rowsize, self.colsize)
        elif self.FinishedButton['text'] == "You Win!":
            self.replay = 1
            self.RestartClick(self.rowsize,self.colsize)
        else:
            for a in self.loc:
                index = a[0]*self.colsize + a[1]
                if self.btns[index]['bg'] == "gray" or self.btns[index]['bg'] == "yellow" or self.btns[index]['bg'] == "green":
                    x = -1
                elif (a[2] == 1 and self.btns[index]['bg'] != "blue") or self.winloserestart == -1:
                    x = 0
                    break
                elif (a[2] == 0 and (self.btns[index]['bg'] == "blue" or self.btns[index] == "yellow" or self.btns[index]['bg'] == "green")):
                    x = -1
                    break
                else:
                    pass
            if x!=-1 and x!=0:
                x = 1
            if x == 0:
                self.FinishedButton['bg'] = "red"
                self.FinishedButton['text'] = "You Lose!"
                self.winloserestart = -1
            elif x==-1:
                self.FinishedButton['bg'] = "yellow"
                self.FinishedButton['text'] = "Keep Going!"
            else:
                self.FinishedButton['bg'] = "blue"
                self.FinishedButton['text'] = "You Win!"
                self.winloserestart = 1

    def RestartClick_a(self):
        self.RestartClick(self.rowsize, self.colsize)

    def RestartClick(self, r, c):
        if r <= 0 or c <= 0:
            r = 10
            c = 10
        for a in self.btns:
            a.destroy()

        del self.btns
        self.btns = []
        
        self.replay = 1
        self.UpdateScore()
        if self.winloserestart != 1 or self.FinishedButton['bg'] == "yellow":
            self.score = 0
            self.winloserestart = 0
            self.numdetectors = 1
            self.numlisteningposts = 1
            self.DetectorLabel['text'] = "Detectors Left: " + str(self.numdetectors)
            self.ListeningPostLabel['text'] = "Listening Posts Left: " + str(self.numlisteningposts)
##            if self.DetectMeButton['state'] == DISABLED:
##                self.ToggleDetectMeButton()
        else:
            self.numdetectors = self.numdetectors + 1
            self.numlisteningposts = self.numlisteningposts + 1
            self.DetectorLabel['text'] = "Detectors Left: " + str(self.numdetectors)
            self.ListeningPostLabel['text'] = "Listening Posts Left: " + str(self.numlisteningposts)
##            if self.DetectMeButton['state'] == DISABLED:
##                self.ToggleDetectMeButton()
            
        self.rowsize = r
        self.colsize = c
        self.LoadScores()
        self.PlaceItem()
        self.MakeButtons()
        self.ShowSomeButtons()

    def ExitClick(self):
        self.scorefile = open(str(self.rowsize) + 'x' + str(self.colsize) + '.txt', 'w + b')
        self.scorefile.write(str(self.highscore))
        self.scorefile.close()
        self.boardsizefile = open("boardsize.txt",'w+b')
        self.boardsizefile.write(str(self.rowsize) + "\n" + str(self.colsize))
        self.boardsizefile.close()
        self.savefile = open("savefile.sav",'w+b')
        pickle.dump(MyMinesweeper,self.savefile,0)
        self.myparent.destroy()

    def GiveNeighborhood(self,pos, count):
        count = 0
        count = self.PeekNW(pos,count)
        count = self.PeekN(pos,count)
        count = self.PeekNE(pos,count)
        count = self.PeekE(pos,count)
        count = self.PeekSE(pos,count)
        count = self.PeekS(pos,count)
        count = self.PeekSW(pos,count)
        count = self.PeekW(pos,count)
        return count
        
    def PeekNW(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] - 1
        temp_pos[1] = temp_pos[1] - 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekN(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] - 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekNE(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] - 1
        temp_pos[1] = temp_pos[1] + 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekE(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] + 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekSE(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] + 1
        temp_pos[1] = temp_pos[1] + 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekS(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[1] = temp_pos[1] + 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekSW(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[0] = temp_pos[0] + 1
        temp_pos[1] = temp_pos[1] - 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def PeekW(self,pos,count):
        temp_pos = [pos[0],pos[1], 1]
        temp_pos[1] = temp_pos[1] - 1
        if temp_pos in self.loc:
            count = count + 1
        return count

    def ShowSomeButtons(self):
        count = 0
        for a in self.loc:
            if a[2] != 1 and random() < 0.25 and count < self.rowsize:
                self.ButtonClick(a)
                count = count + 1
        
    def PlaceItem(self):
        # creates item grid [x,y,item] x, y represent coordinates, item = 0 if no item, 1 if item
        a = range(self.rowsize)
        b = range(self.colsize)
        self.loc = [[]]
        for i in a:
            for j in b:
                x = 0
                if random() <= self.itemprobability:
                    x = 1
                self.loc = self.loc + [[i,j,x]]
        del self.loc[0]

    def UpdateScore(self):
        self.ScoreLabel['text'] = "Score: " + str(self.score) + "\nHigh Score: " + str(self.highscore)
        self.scorefile = open(str(self.rowsize) + 'x' + str(self.colsize) + '.txt', 'w + b')
        self.scorefile.write(str(self.highscore))
        self.scorefile.close()

    def LoadScores(self):
        self.scorefile = open(str(self.rowsize) + 'x' + str(self.colsize) + '.txt', 'a + b')
        self.scorefile.close()
        self.scorefile = open(str(self.rowsize) + 'x' + str(self.colsize) + '.txt', 'r + b')
        temp = self.scorefile.read()
        if temp != "":
            self.highscore = int(temp)
        else:
            self.highscore = 0
        self.scorefile.close()

    def LoadBoardSize(self):
        self.boardsizefile = open("boardsize.txt",'a+b')
        self.boardsizefile.close()
        self.boardsizefile = open("boardsize.txt",'r+b')
        temp1 = self.boardsizefile.readline()
        temp2 = self.boardsizefile.readline()
        if temp1 == "" or temp2 == "" or int(temp1) <= 0 or int(temp2) <= 0:
            self.rowsize = 10
            self.colsize = 10
        else:
            self.rowsize = int(temp1)
            self.colsize = int(temp2)
        self.boardsizefile.close()

    def LoadGame(self):
        self.savefile = open("savefile.sav","r+b")
        game = pickle.load(self.savefile)

root = Tk()
root.title("Bomb Finder!")
myfirstgame = MyMinesweeper(root)
root.mainloop()
