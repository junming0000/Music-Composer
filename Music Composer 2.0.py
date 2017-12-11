import Tkinter
from Tkinter import *
import PIL 
from PIL import Image
from PIL import ImageTk
import tkMessageBox
import threading
import winsound
import numpy

#-----Enable main window and close the sub window-----
def UndoDisable(whatwindow):    
    Root.wm_attributes("-disabled", 0)
    whatwindow.destroy()

#-----Try to close timer before closing the main window in case timer is started.-----
def ExitProg():     
    global Root
    global Timer
    try:
        Timer.cancel()
    except:
        pass
    Root.destroy()
    
#-----Reset NoteInsertedImage and NoteInsertedLength [0~48][0~54] to 0.-----
def ResetArray():   
    global NoteInsertedImage
    global NoteInsertedLength
    NoteInsertedImage=[[] for a in range(48)]
    NoteInsertedLength=[[] for a in range(48)]
    counter=0
    while True:
       counter2=0
       while True:
          NoteInsertedImage[counter2].append(0)
          NoteInsertedLength[counter2].append(0)
          counter2=counter2+1
          if counter2>=48:
             break
       counter=counter+1  
       if counter>=54:
          break

#-----Open Song and Artist files then show. Load Length file to NoteInsertedLength. Create image by checking NoteInsertedLength[0~48][0~54] and set its tag into NoteInsertedImage.-----
def OpenArray(FileName):
    global NoteInsertedLength
    global NoteInsertedImage
    global EditedSongName
    global EditedArtistName
    LengthFileName=FileName+"Length.npy"
    SongFileName=FileName+"Song"
    ArtistFileName=FileName+"Artist"
    try:
        NoteInsertedLength=numpy.load(LengthFileName)
    except IOError:
        tkMessageBox.showwarning( "File missing", "Seems like the save file is incomplete, may be wrong entered name or the file has been removed.")
    else:
        NewProject()
        ResetArray()
        NoteInsertedLength=numpy.load(LengthFileName)
        
        counterX=0
        counterY=0
        while True:
            NoteIndexLocal=NoteInsertedLength[counterX][counterY]
            if NoteIndexLocal!=0:
                CurrentImage=Note[NoteIndexLocal]
                CurrentX=XCoordinate[counterX]
                CurrentY=YCoordinate[counterY]
                NoteInsertedImage[counterX][counterY]=canvas.create_image(CurrentX,CurrentY,image=CurrentImage)
            counterX=counterX+1
            if counterX>=48:
                counterX=0
                counterY=counterY+1
            if counterY>=54:
                break
        tkMessageBox.showwarning( "Success", "Note file loaded successfully.")
        try:
            OpenSongFile=open(SongFileName,"r")
        except IOError:
            tkMessageBox.showwarning( "File missing", "Seems like the song name's file has been removed. Please retype the song name, we are sorry for the inconvenience.")
        else:
            EditedSongName=OpenSongFile.read()
            OpenSongFile.close()
                
        try:
            OpenArtistFile=open(ArtistFileName,"r")
        except IOError:
            tkMessageBox.showwarning( "File missing", "Seems like the artist name's file has been removed. Please retype the artist name, we are sorry for the inconvenience.")
        else:
            EditedArtistName=OpenArtistFile.read()
            OpenArtistFile.close()
    EditOk(True)

#-----Check if password file's password match with entered password, if true, call OpenArray-----    
def PasswordCheck(PasswordRead,FileName):
    global PasswordEntry
    global PasswordWindow
    PasswordEntered=PasswordEntry.get()
    PasswordWindow.destroy()
    Root.wm_attributes("-disabled", 0)
    if PasswordEntered==PasswordRead:
        OpenArray(FileName)
    else:
        tkMessageBox.showwarning( "Wrong Password", "Password entered is wrong.")

#-----Check if password file exist, if no, then call OpenArray, else call PasswordCheck-----         
def OpenPasswordTxt():
    global FileNameAskWindow
    global FileNameAskEntry
    global PasswordEntry
    global PasswordWindow
    FileName=FileNameAskEntry.get()
    FileNameAskWindow.destroy()
    Root.wm_attributes("-disabled", 0)
    if FileName!="":
        try:
            OpenPasswordFile=open(FileName,"r")
        except IOError:
            OpenArray(FileName)
        else: 
            PasswordRead=OpenPasswordFile.read()
            OpenPasswordFile.close()
            PasswordWindow=Tkinter.Tk()
            PasswordWindow.protocol('WM_DELETE_WINDOW', lambda:UndoDisable(PasswordWindow))
            PasswordWindow.wm_title("Open")
            PasswordWindow.iconbitmap('Icon.ico')
            Root.wm_attributes("-disabled", 1)
            PasswordWindow.geometry("200x70")
            PasswordWindow.focus_force()
            PasswordWindow.wm_attributes("-topmost", 1)
            PasswordLabel = Label(PasswordWindow, text="Password:")
            PasswordLabel.pack() 
            PasswordEntry = Entry(PasswordWindow,show="*")
            PasswordEntry.pack()    
            PasswordOk = Button( PasswordWindow, text="Ok",command=lambda:PasswordCheck(PasswordRead,FileName))
            PasswordOk.pack(side=BOTTOM)
            PasswordWindow.mainloop() 
    else:
        tkMessageBox.showinfo("Failed", "File name is required")
    
#-----Create a window for user to enter the file name they want to open-----
def FileNameAsk():
    global FileNameAskWindow
    global FileNameAskEntry
    FileNameAskWindow=Tkinter.Tk()
    FileNameAskWindow.protocol('WM_DELETE_WINDOW', lambda:UndoDisable(FileNameAskWindow))
    FileNameAskWindow.wm_title("Open")
    FileNameAskWindow.iconbitmap('Icon.ico') 
    Root.wm_attributes("-disabled", 1)
    FileNameAskWindow.geometry("200x70")
    FileNameAskWindow.focus_force()
    FileNameAskWindow.wm_attributes("-topmost", 1)
    FileNameAskLabel = Label(FileNameAskWindow, text="File Name:")
    FileNameAskLabel.pack() 
    FileNameAskEntry = Entry(FileNameAskWindow)
    FileNameAskEntry.pack()    
    FileNameAskOk = Button( FileNameAskWindow, text="Ok",command=OpenPasswordTxt)
    FileNameAskOk.pack(side=BOTTOM)
    FileNameAskWindow.mainloop()    
   
#-----Save Password, Artist, Song file-----
def SaveTxt():
    global SetPasswordWindow
    global SetPasswordEntry
    global FileNameEntry
    global PasswordBoolean
    global NoteInsertedLength
    global EditedSongName
    global EditedArtistName
    FileName=FileNameEntry.get()
    Password=SetPasswordEntry.get()
    Root.wm_attributes("-disabled", 0)
    SetPasswordWindow.destroy()
    if FileName!="" and (Password!="" or PasswordBoolean==False):
        SongFileName=FileName+"Song"
        ArtistFileName=FileName+"Artist"
        LengthFileName=FileName+"Length"
        if PasswordBoolean==True:
            SaveFile = open(FileName, "w")
            SaveFile.write(Password)
            SaveFile.close()
        SaveFile = open(SongFileName, "w")
        SaveFile.write(EditedSongName)
        SaveFile.close()
        SaveFile = open(ArtistFileName, "w")
        SaveFile.write(EditedArtistName)
        SaveFile.close()
        numpy.save(LengthFileName,NoteInsertedLength)
        tkMessageBox.showinfo( "Success", "File saved successfully.")
    else:
        tkMessageBox.showinfo("Failed", "Save failed due to empty of entry.")

#-----Enable or disable the password entry-----
def PasswordEntryState(YesOrNo):
    global PasswordBoolean
    PasswordBoolean=YesOrNo
    if PasswordBoolean==True:
        SetPasswordEntry.configure(state=NORMAL)
    else:
        SetPasswordEntry.configure(state=DISABLED)
        
#-----Window for user to enter file name and password of save file-----
def SetPassword():
    global SetPasswordWindow
    global SetPasswordEntry
    global FileNameEntry
    global PasswordBoolean
    file = open("newfile.txt", "w")
    SetPasswordWindow=Tkinter.Tk()
    SetPasswordWindow.protocol('WM_DELETE_WINDOW', lambda:UndoDisable(SetPasswordWindow))
    SetPasswordWindow.wm_title("Save")
    SetPasswordWindow.iconbitmap('Icon.ico')
    Root.wm_attributes("-disabled", 1)
    SetPasswordWindow.focus_force()
    SetPasswordWindow.wm_attributes("-topmost", 1)
    SetPasswordLabel = Label(SetPasswordWindow, text="Do you want to save the file with password?")
    SetPasswordLabel.pack(side=TOP)
    SetPasswordLabel2 = Label(SetPasswordWindow, text="File Name:")
    SetPasswordLabel2.pack(side=TOP) 
    FileNameEntry = Entry(SetPasswordWindow)
    FileNameEntry.pack(side=TOP)    
    SetPasswordYes = Radiobutton( SetPasswordWindow, text="Password:",value=1,command=lambda:PasswordEntryState(True))
    SetPasswordYes.pack()
    SetPasswordYes.select()
    PasswordBoolean=True
    SetPasswordEntry = Entry(SetPasswordWindow,show="*")
    SetPasswordEntry.pack()
    SetPasswordOk = Button( SetPasswordWindow, text="Ok",command=SaveTxt)
    SetPasswordOk.pack(side=BOTTOM)
    SetPasswordNo = Radiobutton( SetPasswordWindow, text="I don't want to save password.",value=2,command=lambda:PasswordEntryState(False))
    SetPasswordNo.pack(side=BOTTOM)
    SetPasswordWindow.mainloop()

#-----Reset NoteInsertedImage and NoteInsertedLength, and also remove the stave images-----
def NewProject():
    global NoteInsertedImage
    global NoteInsertedLength
    global EditedSongName
    global EditedArtistName
    counterX=0
    counterY=0
    EditedSongName="Default Song Name"
    EditedArtistName="Default Artist Name"
    EditOk(True)
    while True:
        canvas.delete(NoteInsertedImage[counterX][counterY])
        NoteInsertedImage[counterX][counterY]=0
        NoteInsertedLength[counterX][counterY]=0
        counterX=counterX+1
        if counterX>=48:
            counterX=0
            counterY=counterY+1
        if counterY>=54:
            break

#-----Play the note of current time, then add one time to call it next time. Also, create a timer to call this function again in 0.55 seconds.-----
def RepeatPlaying():
    global NoteInsertedImage
    global NoteInsertedLength
    global Frequency
    global KeyHigh
    global PlayingRow
    global PlayingX
    global PlayingY
    global Stop
    global LastLine
    global Timer
    SomethingToPlay=False
    while Stop==False:
        if NoteInsertedLength[PlayingX][PlayingY]!=0:
            SomethingToPlay=True
            CurrentFrequency= int(Frequency[PlayingY]*(2**KeyHigh))
            CurrentLength=500/(2**(NoteInsertedLength[PlayingX][PlayingY]-1))
            PlayingY=(PlayingRow*18)
        PlayingY=PlayingY+1
        if PlayingY>=(PlayingRow*18):
            canvas.delete(LastLine)
            LastLine=canvas.create_line((XCoordinate[PlayingX], (PlayingRow*200)-60,XCoordinate[PlayingX], (PlayingRow*200)+70), fill="blue")
            Timer=threading.Timer(0.55,RepeatPlaying)
            Timer.start()
            PlayingX=PlayingX+1
            PlayingY=((PlayingRow-1)*18)
            if SomethingToPlay==True:
                winsound.Beep(CurrentFrequency,CurrentLength)
                SomethingToPlay=False
            break
    if PlayingX>=48:
        PlayingRow=PlayingRow+1
        PlayingX=0
        PlayingY=(PlayingRow-1)*18
    if PlayingRow>=4:
        Stop=True
        canvas.delete(LastLine)

#-----Set Stop=True-----
def StopClicked():
    global Stop
    global LastLine
    canvas.delete(LastLine)
    Stop=True

#-----Set default value of current time then call RepeatPlaying-----
def PlayClicked():
    global PlayingRow
    global PlayingX
    global PlayingY
    global Stop
    global Pause
    global LastLine
    if Stop==True:
        PlayingRow=1
        PlayingX=0
        PlayingY=0
        Stop=False
        LastLine=canvas.create_line((XCoordinate[PlayingX], (PlayingRow*200)-75,XCoordinate[PlayingX], (PlayingRow*200)+75), fill="blue")
        RepeatPlaying()

#-----Put or remove image from the stave due to the click of user, also update the NoteInsertedLength.-----
def ClickEvent(x,y,LeftOrRight):
    global NoteIndex
    global Note
    global NoteInsertedImage
    NoteIndexLocal=NoteIndex.get()
    XIndex=0
    YIndex=0
    counter=0
    OnTheLine=0
    while True:
        XDifference=abs(XCoordinate[counter]-x)
        if XDifference<=10:
            XIndex=counter
            counter=48
            OnTheLine=OnTheLine+1
        else:
            counter=counter+1
        if counter>=48:
            break
                
    counter=0
    while True:
        YDifference=abs(YCoordinate[counter]-y)
        if YDifference<=3:
            YIndex=counter
            counter=54
            OnTheLine=OnTheLine+1
        else:
            counter=counter+1
        if counter>=54:
            break
    if OnTheLine==2:
        XShow=XCoordinate[XIndex]
        YShow=YCoordinate[YIndex]
        if LeftOrRight==0:
            #Check nothing is putting at the same line same row
            if YIndex<=17:
                counter=17
            elif YIndex<=35:
                counter=35
            else:
                counter=53
            counter2=0
            NothingSameLine=True
            while True:
                if NoteInsertedLength[XIndex][counter]==0:
                    counter=counter-1
                    counter2=counter2+1
                else:
                    NothingSameLine=False
                    counter2=18
                if counter2>=18:
                    break
                #Check Done
            if NoteInsertedLength[XIndex][YIndex]==0 and NothingSameLine==True:
                CurrentSelectedNote=Note[NoteIndexLocal]
                NoteInsertedImage[XIndex][YIndex]=canvas.create_image(XShow,YShow,image=CurrentSelectedNote)
                NoteInsertedLength[XIndex][YIndex]=NoteIndexLocal
        else:
            canvas.delete(NoteInsertedImage[XIndex][YIndex])
            NoteInsertedImage[XIndex][YIndex]=0
            NoteInsertedLength[XIndex][YIndex]=0

#-----Call ClickEvent and pass event x,y to it-----
def LeftClick(event):
    X = event.x
    Y = event.y
    ClickEvent(X,Y,0)
def RightClick(event):
    X = event.x
    Y = event.y
    ClickEvent(X,Y,1)

#-----Set a series of stave coordinate by giving the top line coordinate-----
def SetYCoordinate(Top):
    global YCoordinate
    YToExtend=[Top,(Top+5),(Top+9),(Top+13),(Top+18),(Top+21),(Top+26),(Top+29),(Top+34)]
    YCoordinate.extend(YToExtend)

#-----Check if key high value is the value we want-----
def IsEntryValid():
    global KeyHighEntry
    KeyHighGet=KeyHighEntry.get()
    try:
        KeyHighGet=int(KeyHighGet)
    except ValueError:
        ReturnValue = False
    else:
        if KeyHighGet>=1 and KeyHighGet<=4 and KeyHighGet%1==0:
            ReturnValue = True
        else:
            ReturnValue = False
    return ReturnValue

#-----User press ok in key high, calls IsEntryValid then set KeyHigh-----
def KeyHighConfirm():
    global Play
    global KeyHighEntry
    global KeyHigh
    CheckIfValid=IsEntryValid()  
    if CheckIfValid==True:
        tkMessageBox.showinfo( "Success!", "Key High has changed successfully.")
        KeyHigh=int(KeyHighEntry.get())
    else:
        tkMessageBox.showinfo( "Invalid Value", "Key High should be an integer between 1 to 4.")
        KeyHighEntry.delete(0,END)
        KeyHighEntry.insert(0,KeyHigh)

#-----Create a window to let user set artist and song name-----
def Editor():
    global EditorWindow
    global SongNameEntry
    global ArtistNameEntry
    EditorWindow=Tkinter.Tk()
    EditorWindow.protocol('WM_DELETE_WINDOW', lambda:UndoDisable(EditorWindow))
    EditorWindow.wm_title("Editor")
    EditorWindow.iconbitmap('Icon.ico') 
    Root.wm_attributes("-disabled", 1)
    EditorWindow.focus_force()
    EditorWindow.wm_attributes("-topmost", 1)
    EditorWindow.geometry("200x110")
    EditedSongName=StringVar()
    EditedArtistName=StringVar()
    SongNameLabel = Label(EditorWindow, text="Song Name:")
    SongNameLabel.pack()
    SongNameEntry = Entry(EditorWindow)
    SongNameEntry.pack()
    ArtistNameLabel = Label(EditorWindow, text="Artist Name:")
    ArtistNameLabel.pack()
    ArtistNameEntry = Entry(EditorWindow)
    ArtistNameEntry.pack()
    EditOkButton = Button( EditorWindow, text="Ok",command=lambda:EditOk(False) )
    EditOkButton.pack(anchor=CENTER)
    EditorWindow.mainloop()

#-----Set artist and song name-----
def EditOk(NotFromEntry):
    global EditorWindow
    global canvas
    global SongName
    global ArtistName
    global EditedSongName
    global EditedArtistName
    global SongNameEntry
    global ArtistNameEntry
    if NotFromEntry==False:
        EditedSongName=SongNameEntry.get()
        EditedArtistName=ArtistNameEntry.get()
        EditorWindow.destroy()
        Root.wm_attributes("-disabled", 0)
    canvas.delete(SongName)
    SongName=canvas.create_text(650,30,text = EditedSongName,fill = 'black',font=("Times New Roman",35)    )
    canvas.pack()
    canvas.delete(ArtistName)    
    ArtistName=canvas.create_text(650,90,text = EditedArtistName,fill = 'black',font=("Times New Roman",20)    )
    canvas.pack()

#-----Set a series of x coordinate by giving the most left one-----
def SetXCoordinate(counter):
    global XCoordinate
    counterEnd=counter+345
    while True:
        XCoordinate.append(counter)
        counter=counter+23
        if counter>counterEnd:
            break
   
#-----Initialize all the variable-----
def InitializeVariable():
    global XCoordinate
    global YCoordinate
    global Stop
    global EditedSongName
    global EditedArtistName
    global Frequency
    global KeyHigh
    XCoordinate=[]
    YCoordinate=[]
    Stop=True
    EditedSongName="Default Song Name"
    EditedArtistName="Default Artist Name"
    #X
    SetXCoordinate(75)
    SetXCoordinate(500)
    SetXCoordinate(925)
    #Y
    counter=140
    counterplus=97
    while True:
        SetYCoordinate(counter)
        counter=counter+counterplus
        if counterplus==97:
            counterplus=103
        else:
            counterplus=97
        if counter>637:
            break
        
    #NoteID&Length
    ResetArray()

    #Default Frequency
    Frequency=[]
    Frequency=[349.23,329.63,293.66,261.63,246.94,220.00,196.00,174.61,164.81,110.00,98.00,87.31,82.41,73.42,65.41,61.74,55.00,49.00,349.23,329.63,293.66,261.63,246.94,220.00,196.00,174.61,164.81,110.00,98.00,87.31,82.41,73.42,65.41,61.74,55.00,49.00,349.23,329.63,293.66,261.63,246.94,220.00,196.00,174.61,164.81,110.00,98.00,87.31,82.41,73.42,65.41,61.74,55.00,49.00]
    KeyHigh = 1

##############################Main Window GUI##############################
Root = Tkinter.Tk()             #Create Window
Root.state('zoomed')            #Maximize Window
Root.minsize(1400, 700)         #Set Minimum Size of Window

Root.wm_title("Music Composer") #Set Title of Window
Root.iconbitmap('Icon.ico')     #Set Icon of Window

###MenuBar###
menubar = Menu(Root)        #CreateMenu
#Open Images
StaveOpen           = Image.open("Stave.png")
StaveImg            = ImageTk.PhotoImage(StaveOpen)
WholeNoteOpen       = Image.open("Whole Note.png")
WholeNoteImg        = ImageTk.PhotoImage(WholeNoteOpen)
HalfNoteOpen        = Image.open("Half Note.png")
HalfNoteImg         = ImageTk.PhotoImage(HalfNoteOpen)
HalfNote2Open       = Image.open("Half Note 2.png")
HalfNote2Img        = ImageTk.PhotoImage(HalfNote2Open)
QuarterNoteOpen     = Image.open("Quarter Note.png")
QuarterNoteImg      = ImageTk.PhotoImage(QuarterNoteOpen)
QuarterNote2Open    = Image.open("Quarter Note 2.png")
QuarterNote2Img     = ImageTk.PhotoImage(QuarterNote2Open)
EighthNoteOpen      = Image.open("Eighth Note.png")
EighthNoteImg       = ImageTk.PhotoImage(EighthNoteOpen)
EighthNote2Open     = Image.open("Eighth Note 2.png")
EighthNote2Img      = ImageTk.PhotoImage(EighthNote2Open)
SixteenthNoteOpen   = Image.open("Sixteenth Note.png")
SixteenthNoteImg    = ImageTk.PhotoImage(SixteenthNoteOpen)
SixteenthNote2Open  = Image.open("Sixteenth Note 2.png")
SixteenthNote2Img   = ImageTk.PhotoImage(SixteenthNote2Open)
PlayOpen            = Image.open("Play.png")
PlayImg             = ImageTk.PhotoImage(PlayOpen)
StopOpen            = Image.open("Stop.png")
StopImg             = ImageTk.PhotoImage(StopOpen)
Note=[WholeNoteImg,WholeNoteImg,HalfNoteImg,QuarterNoteImg,EighthNoteImg,SixteenthNoteImg]
#File of Menubar
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label="New", command=NewProject)
filemenu.add_command(label="Edit Names", command=Editor)
filemenu.add_command(label="Open", command=FileNameAsk)
filemenu.add_command(label="Save", command=SetPassword)
menubar.add_cascade(label="File", menu=filemenu)
#Show Menubar
Root.config(menu=menubar)
##Toolbar##
Toolbar = Frame(Root)
#Buttons
StopButton = Button(Toolbar,image=StopImg, command=StopClicked)
StopButton.pack(side=BOTTOM, padx=1,pady=1)
PlayButton = Button(Toolbar,image=PlayImg, command=PlayClicked)
PlayButton.pack(side=BOTTOM, padx=1,pady=1)
#Note
NoteIndex = IntVar()
WholeNoteSelect = Radiobutton(Toolbar, image=WholeNoteImg, variable=NoteIndex, value=1)
WholeNoteSelect.pack( anchor = W,side=BOTTOM )
WholeNoteSelect.select()
HalfNoteSelect = Radiobutton(Toolbar, image=HalfNote2Img, variable=NoteIndex, value=2)
HalfNoteSelect.pack( anchor = W,side=BOTTOM  )
QuarterNoteSelect = Radiobutton(Toolbar, image=QuarterNote2Img, variable=NoteIndex, value=3)
QuarterNoteSelect.pack( anchor = W,side=BOTTOM )
EighthNoteSelect = Radiobutton(Toolbar, image=EighthNote2Img, variable=NoteIndex, value=4)
EighthNoteSelect.pack( anchor = W,side=BOTTOM )
SixteenthNoteSelect = Radiobutton(Toolbar, image=SixteenthNote2Img, variable=NoteIndex, value=5)
SixteenthNoteSelect.pack( anchor = W,side=BOTTOM  )
Toolbar.pack(side=LEFT,fill=X)
NoteLabel = Label(Toolbar, text="Note length\n(Left click\nto put,\nright click\nto remove.)")
NoteLabel.pack( anchor = W,side=BOTTOM )
#SecondsPerBar
KeyHighLine = Label(Toolbar, text="---------")
KeyHighLine.pack( anchor = W,side=BOTTOM )
KeyHighButton = Button(Toolbar, text="Ok", command=KeyHighConfirm)
KeyHighButton.pack( anchor = W,side=BOTTOM )
KeyHighEntry = Entry( Toolbar,width="5")
KeyHighEntry.pack(anchor = W,side=BOTTOM)
KeyHighEntry.insert(0,1)
KeyHighLabel = Label(Toolbar, text="Key High\nto play:")
KeyHighLabel.pack( anchor = W,side=BOTTOM )
#Create Canvas
canvas = Canvas(Root,width=1300,height=700,bg='white')  
#Put Staves
canvas.create_image(650,200,image=StaveImg)
canvas.create_image(650,400,image=StaveImg)
canvas.create_image(650,600,image=StaveImg)
SongName=canvas.create_text(650,30, text = 'Default Song Name' ,fill = 'black',font=("Times New Roman",35)    )       
ArtistName=canvas.create_text(650,90,text = 'Default Artist Name',  fill = 'black',font=("Times New Roman",20)  )
canvas.pack()

##############################End of Main Window GUI##############################

InitializeVariable()
#Event
Root.bind('<Button-1>', LeftClick)
Root.bind('<Button-3>', RightClick)
Root.protocol('WM_DELETE_WINDOW', ExitProg)

Root.mainloop()
