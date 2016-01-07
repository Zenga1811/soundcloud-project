#!/usr/bin/env python
import Tkinter
from Tkinter import *
import soundcloud
from soundcloud import *
import os


window = Tk()
window.minsize(800,600)
window.maxsize(800,600)

#--------Functions----------
def play(event):
	client = soundcloud.Client(client_id="2f5ba833d7393adbdd4f5a5d23af34b0")
	if len(idEntry.get())==0:
		track = client.get('/resolve', url=track_url)
		track_id = str(track.id)
	if len(idEntry.get())!=0:
		track_id = idEntry.get()
	track = client.get("/tracks/"+track_id)
	stream_url = client.get(track.stream_url, allow_redirects=False)
	print(track.title)
	os.system("vlc '"+stream_url.location+"'")	

def search(event):
	search = searchEntry.get().lower()

	client = soundcloud.Client(client_id="2f5ba833d7393adbdd4f5a5d23af34b0")

	tracks = client.get('/tracks', q=search)

	for track in tracks:
		for field_name, field_data in track.fields().items():
			if field_name=="title":
				title="Title: "+field_data+"\n"
				text.insert('1.0',title)
				#text.insert(0,"--------------------------------")
			if field_name=="id":
				field_data = str(field_data)
				id="ID: "+field_data+"\n"
				#text.insert(0,"--------------------------------")
				text.insert('1.0',id)

def download(event):
	client = soundcloud.Client(client_id="2f5ba833d7393adbdd4f5a5d23af34b0")
	if len(idEntry.get())==0:
		track_url = urlEntry.get()
		track = client.get('/resolve', url=track_url)
		track_id = str(track.id)
	if len(idEntry.get())!=0:
		track_id = idEntry.get()
	track = client.get("/tracks/"+track_id)
	stream_url = client.get(track.stream_url, allow_redirects=False)

	os.system("wget -O '"+fileEntry.get()+"' '"+stream_url.location+"'")

def clear(event):
	text.delete("1.0", END)

def redirect():
	os.system("sensible-browser soundcloud.com")
#-----------------------------------------

#---------------------DATA-----------------
ClientFrame = Frame(window)
ClientFrame.pack(side=TOP, fill=X)

urlLabel = Label(ClientFrame, text="URL(without 'www')")
urlLabel.grid(column=0,row=1)
urlEntry = Entry(ClientFrame)
urlEntry.grid(column=1,row=1)

'''
artistLabel = Label(ClientFrame, text="Artist:")
artistLabel.grid(column=0,row=2)
artistEntry = Entry(ClientFrame)
artistEntry.grid(column=1,row=2)

titleLabel = Label(ClientFrame, text="Title:")
titleLabel.grid(column=0,row=3)
titleEntry = Entry(ClientFrame)
titleEntry.grid(column=1,row=3)
'''

searchLabel = Label(ClientFrame, text="Search:")
searchLabel.grid(column=0,row=5)
searchEntry = Entry(ClientFrame)
searchEntry.grid(column=1,row=5)

fileLabel = Label(ClientFrame, text="File:")
fileLabel.grid(column=0, row=4)
fileEntry = Entry(ClientFrame)
fileEntry.grid(column=1,row=4)

idLabel = Label(ClientFrame, text="ID:")
idLabel.grid(column=0,row=0)
idEntry = Entry(ClientFrame)
idEntry.grid(column=1,row=0)

wmFrame = Frame(window)
wmFrame.pack(side=RIGHT)

text = Text(wmFrame, width=60, height=100)
text.pack()

#-------Song Controls------------------------
ControlFrame = Frame(window, height=20)
ControlFrame.pack(side=BOTTOM, fill=X)

btnPlay = Button(ControlFrame, text="OK")
btnPlay.pack(side=LEFT)

btnSearch = Button(ControlFrame, text="Search")
btnSearch.pack(side=LEFT)

btnDownload = Button(ControlFrame, text="Download")
btnDownload.pack(side=LEFT)

btnClear = Button(ControlFrame, text="Clear")
btnClear.pack(side=LEFT)

btnClear.bind("<Button-1>", clear)
btnDownload.bind("<Button-1>", download)
btnSearch.bind("<Button-1>", search)
btnPlay.bind("<Button-1>", play)

#---------------------------------------------
#----------Watermark--------------------------

watermark_img = PhotoImage(file="/home/ive/Downloads/soundcloud.png")
watermark = Button(ControlFrame, image=watermark_img, command=redirect)
watermark.pack(side=LEFT)

#---------------------------------------------
window.mainloop()
window.destroy()