import pyodbc
import tkinter
import tkinter.ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Listbox
from tkinter import Text
from PIL import ImageTk,Image
import sys
import requests
import pymongo
import io
import base64
from pymongo import MongoClient
from urllib.request import urlopen
import urllib.request
from io import BytesIO

global name						#Name of the user
global auth
global list
global selectedmovie
global input
global load
global button
global usrid
global movnum
global newreviewnum				#1 or 0 depending on if this is a new review or not
global mylistpalnums
global critic

'''Star Rating Buttons'''
global movie_btn1
global movie_btn2
global movie_btn3
global movie_btn4
global movie_btn5

load = 0
name = ""
auth = 0
critic = 0

'''Set Up Windows'''
#Login window
log = tkinter.Tk()

#Label the window
log.title("FP Movies Login")

#Window size
log.geometry('350x150')

#Window background color
log.configure(bg='ivory2')

'''Database Connection'''
#Connect to relational database
conn = pyodbc.connect('Driver={SQL Server};'
						'Server=DESKTOP-2JG1NIF\SQLEXPRESS;'
						'Database=FPMovies;'
						'Trusted_Connection=yes;')	
						
#Set up cursor (for displaying text)
cursor = conn.cursor()


'''Non-Relational Database Connection'''
client = MongoClient('localhost',27017)
db = client.FPMovies
friends = db.Friends
rvwtxt = db.Review

#Header label
lbl1 =tkinter.Label(log,text="FP Movies",font=("Times New Roman",20),bg="ivory3",width = 10)
lbl1.grid(column=1,row=0)

#Log In Screen labels and entry boxes
lblu = tkinter.Label(log,text="Username",font=("Times New Roman",20),bg="ivory3",width = 7)
lblp = tkinter.Label(log,text="Password",font=("Times New Roman",20),bg="ivory3",width = 7)
enteruser = tkinter.Entry(log,width=20)
enterpass = tkinter.Entry(log,width=20)
lblu.grid(column=0,row=1)
lblp.grid(column=0,row=2)
enteruser.grid(column=1,row=1)
enterpass.grid(column=1,row=2)

#Complete registration - activated after clicking "Finish" in Register window
def completeregister():
	global reg
	global newuser
	global newpass
	global regcombo	
	type = regcombo.get()
	
	#Insert user/critic info into SQL user/critic table
	if type=="User":
		userquery = "INSERT INTO FPMovies.dbo.usr (usid,usname,uspass) VALUES ((SELECT TOP 1 usid FROM FPMovies.dbo.usr ORDER BY usid DESC)+1,\'" + newuser.get() + "\',\'" + newpass.get() + "\')"
		cursor.execute(userquery)
		conn.commit()
	elif type=="Critic":
		criticquery = "INSERT INTO FPMovies.dbo.critic (cid,cname,cpass) VALUES ((SELECT TOP 1 cid FROM FPMovies.dbo.critic ORDER BY cid DESC)+1,\'" + newuser.get() + "\',\'" + newpass.get() + "\')"
		cursor.execute(criticquery)
		conn.commit()
		
	#Close this window
	reg.destroy()

#Registration - activated after clicking "Register" in login window
def register():
	global reg
	global newuser
	global newpass
	global regcombo
	
	#Format tkinter window
	reg = tkinter.Tk()
	reg.title("Registration")
	reg.geometry('250x200')
	
	#Labels
	lblr = tkinter.Label(reg,text="Register",font=("Times New Roman", 20),bg="ivory3",width=7)
	lblr.grid(column=1,row=0,columnspan=2,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	reg.configure(bg="ivory2")
	lblut=tkinter.Label(reg,text="User Type",font=("Times New Roman", 15),bg="ivory3",width=7)
	lblut.grid(column=0,row=1)
	
	#Combobox
	regcombo = tkinter.ttk.Combobox(reg,width=10)
	regcombo['values'] = ("User","Critic")
	regcombo.grid(column=1,row=1)
	
	#Labels and text entry boxes
	lblnu=tkinter.Label(reg,text="Username",font=("Times New Roman", 15),bg="ivory3",width=7)
	lblnu.grid(column=0,row=2)
	newuser=tkinter.Entry(reg,width=20)
	newuser.grid(column=1,row=2)
	lblnp=tkinter.Label(reg,text="Password",font=("Times New Roman", 15),bg="ivory3",width=7)
	lblnp.grid(column=0,row=3)
	newpass=tkinter.Entry(reg,width=20)
	newpass.grid(column=1,row=3)
	
	#Finish registration button
	finishreg=tkinter.Button(reg,text="Finish",bg="royal blue",fg="white",font=("Times New Roman", 15),width=7,command=completeregister)
	finishreg.grid(column=1,row=4)	
	reg.mainloop()

#Submit - activated when user clicks submit on login screen
def clickedsubmit():
	global passw
	global name
	global auth
	
	#Retrieve username and password
	name = enteruser.get()
	passw = enterpass.get()
	
	#Look up passwords from critic and user tables
	passquery = "SELECT cpass FROM FPMovies.dbo.critic where cname = \'" + name + "\'"
	cursor.execute(passquery)
	crow = str(cursor.fetchone())
	crow = crow.replace("(", "")
	crow = crow.replace("'", "")
	crow = crow.replace(")", "")
	crow = crow.replace(",", "")
	crow = crow.replace(" ", "")
	passquery = "SELECT uspass FROM FPMovies.dbo.usr where usname = \'" + name + "\'"
	cursor.execute(passquery)
	row = str(cursor.fetchone())
	row = row.replace("(", "")
	row = row.replace("'", "")
	row = row.replace(")", "")
	row = row.replace(",", "")
	row = row.replace(" ", "")
	global critic
	
	#Compare to the passwords that match the username entered (if any)
	#Then set critic variable and close window
	if row == passw:
		auth = 1
		print("Welcome")
		critic = 0
		log.destroy()
	elif crow == passw:
		auth = 1
		print("Welcome")
		critic = 1
		log.destroy()		
	else:
		print("Incorrect Password")
	
#Submit and register buttons
btnsubmit = tkinter.Button(log,text="Submit",bg="royal blue",fg="white",font=("Times New Roman", 15),width=7,command=clickedsubmit)
btnsubmit.grid(column=2,row=2)	
btnregister = tkinter.Button(log,text="Register",bg="royal blue",fg="white",font=("Times New Roman", 15),width=7,command=register)
btnregister.grid(column=2,row=1)

log.mainloop()

print(name)


global usrid
#Find user id from either user or critic table
if critic == 0:
	cursor.execute("SELECT usid FROM FPMovies.dbo.usr WHERE usname = \'" + name + "\'")
else:
	cursor.execute("SELECT cid FROM FPMovies.dbo.critic WHERE cname = \'" + name + "\'")
usrid = str(cursor.fetchone())
usrid = usrid.replace("(", "")
usrid = usrid.replace("'", "")
usrid = usrid.replace(")", "")
usrid = usrid.replace(",", "")
usrid = usrid.replace(" ", "")

#Rate - activated when a movie (from main window) is selected and then a rating (from movie review window) is clicked
def rate(stars):
	global load
	load = stars
	global list
	global usrid
	global name
	global movnum
	global critic
	
	#Find movie id
	numquery = "SELECT mid FROM FPMovies.dbo.movie WHERE mname = \'" + list.get('anchor') + "\'"
	cursor.execute(numquery)
	movnum = str(cursor.fetchone())
	movnum = movnum.replace("(", "")
	movnum = movnum.replace("'", "")
	movnum = movnum.replace(")", "")
	movnum = movnum.replace(",", "")
	movnum = movnum.replace(" ", "")
	
	#Update rating based on rating clicked and update the tables
	if(stars=="1" or stars=="2" or stars=="3" or stars=="4" or  stars=="5"):
		if critic==0:
			starquery = "UPDATE FPMovies.dbo.review SET review.r_score = \'" + stars + "\' WHERE r_uid = \'" + usrid + "\' AND r_mid = \'" + movnum + "\'"
		else:
			starquery = "UPDATE FPMovies.dbo.critic_review SET critic_review.c_score = \'" + stars + "\' WHERE c_cid = \'" + usrid + "\' AND c_mid = \'" + movnum + "\'"
		cursor.execute(starquery)
		conn.commit()
		
	#Update the button colors depending on if one has been clicked
	if(stars == "1"):
		movie_btn1.configure(bg="tomato")
		movie_btn2.configure(bg="ivory3")
		movie_btn3.configure(bg="ivory3",fg="white")
		movie_btn4.configure(bg="ivory3")
		movie_btn5.configure(bg="ivory3")
	elif(stars == "2"):
		movie_btn1.configure(bg="ivory3")
		movie_btn2.configure(bg="tan1")
		movie_btn3.configure(bg="ivory3",fg="white")
		movie_btn4.configure(bg="ivory3")
		movie_btn5.configure(bg="ivory3")
	elif(stars == "3"):
		movie_btn1.configure(bg="ivory3")
		movie_btn2.configure(bg="ivory3")
		movie_btn3.configure(bg="gold2",fg="black")
		movie_btn4.configure(bg="ivory3")
		movie_btn5.configure(bg="ivory3")
	elif(stars == "4"):
		movie_btn1.configure(bg="ivory3")
		movie_btn2.configure(bg="ivory3")
		movie_btn3.configure(bg="ivory3",fg="white")
		movie_btn4.configure(bg="SeaGreen3")
		movie_btn5.configure(bg="ivory3")
	elif(stars == "5"):
		movie_btn1.configure(bg="ivory3")
		movie_btn2.configure(bg="ivory3")
		movie_btn3.configure(bg="ivory3",fg="white")
		movie_btn4.configure(bg="ivory3")
		movie_btn5.configure(bg="SlateBlue1")
	else:
		print(stars)

		
#Display review text - activated when a movie is selected
def displayrvwtxt():
	global load
	global reviewtext
	global critic
	
	if(load != "None"):
		#Load previous review comments
		if critic == 0:
			myrvw = rvwtxt.find({'mid':movnum,'id':usrid,'type':'User'})
		else:
			myrvw = rvwtxt.find({'mid':movnum,'id':usrid,'type':'Critic'})
		
		for ld in myrvw:
			ld = str(ld)
			print(ld)
			start=ld.find('\'review\': \'')
			end=ld.rfind('}')
			print(ld[start+11:end-1])
			reviewtext.insert(tkinter.END,ld[start+11:end-1])

		
#Submit review - activated when submit button is clicked in review window		
def submitreview():
	global mov
	global load
	global movnum
	global usrid
	global reviewtext
	global newreviewnum
	global critic
	
	#Display some movie information in console window
	print("MOVNUM = " + movnum)
	print("USRID = " + usrid)
	print("RVWTXT = " + reviewtext.get("1.0",'end-1c'))
	
	#Find review based on whether this is a critic or user reviewing the movie
	if critic == 0:
		check = rvwtxt.find_one({'mid':movnum,'id':usrid,'type':'User'})
	else:
		check = rvwtxt.find_one({'mid':movnum,'id':usrid,'type':'Critic'})
	print(check)
		
	#Update the movie review
	if("None" not in str(check)):
		if critic==0:
			result = rvwtxt.update_one({'mid':movnum,'id':usrid,'type':'User'},{'$set': {'review':reviewtext.get("1.0",'end-1c')}})
		else:
			result = rvwtxt.update_one({'mid':movnum,'id':usrid,'type':'Critic'},{'$set': {'review':reviewtext.get("1.0",'end-1c')}})
	else:
		if critic==0:
			myreview={'mid':movnum,'type':'User','id':usrid,'review':reviewtext.get("1.0",'end-1c')}
		else:
			myreview={'mid':movnum,'type':'Critic','id':usrid,'review':reviewtext.get("1.0",'end-1c')}
		result = rvwtxt.insert_one(myreview)
	
	#Print the result in console window
	print("RESULT = " + str(result))
	mov.destroy()
	
	
#Window for movie review - activated by selecting a movie in main window	
def movie():
	global mov
	mov = tkinter.Tk()
	global list
	global critic
	
	#Format tkinter window
	mov.title(list.get('anchor'))
	mov.geometry('425x400')
	
	#Window background color
	mov.configure(bg='ivory2')
	
	global newreviewnum
	global movnum
	
	#Find movie number
	numquery = "SELECT mid FROM FPMovies.dbo.movie WHERE mname = \'" + list.get('anchor') + "\'"
	cursor.execute(numquery)
	movnum = str(cursor.fetchone())
	movnum = movnum.replace("(", "")
	movnum = movnum.replace("'", "")
	movnum = movnum.replace(")", "")
	movnum = movnum.replace(",", "")
	movnum = movnum.replace(" ", "")
	
	
	#Display movie cover image
	'''#Movie cover image
	#try:
	picquery = "SELECT imlink FROM FPMovies.dbo.movie WHERE mname = \'" + list.get('anchor') + "\'"
	cursor.execute(picquery)
	url = str(cursor.fetchone())
	url = url.replace("(", "")
	url = url.replace("'", "")
	url = url.replace(")", "")
	url = url.replace(",", "")
	url = url.replace(" ", "")
	
	try:
		req = requests.get(url)
	except requests.exceptions.RequestException as e:
		print ("ERROR Making request")
		
	urllib.request.urlretrieve(url,"cover.jpg")	
	
	try:
		image = Image.open('cover.jpg')
	except IOError:
		print("ERROR Can't open image")
	
	#canvas = tkinter.Canvas(mov,width=10,height=10,bg='white')
	cover = ImageTk.PhotoImage(image)
	#canvas.create_image((0,0),image=cover,state="normal",anchor=tkinter.NW)	
	#canvas.grid(row=0,column=0)	
	label = tkinter.Label(mov,image=cover)
	label.image=cover
	#label.grid(row=0,column=0)
	label.place(x=0,y=0)'''
	
	#Find movie score
	if critic==0:
		initquery = "SELECT review.r_score FROM FPMovies.dbo.review INNER JOIN FPMovies.dbo.movie ON review.r_mid = movie.mid INNER JOIN FPMovies.dbo.usr ON review.r_uid = usr.usid WHERE usr.usname = \'" + name + "\' AND movie.mname = \'" + list.get('anchor') + "\'"
	else:
		initquery = "SELECT critic_review.c_score FROM FPMovies.dbo.critic_review INNER JOIN FPMovies.dbo.movie ON critic_review.c_mid = movie.mid INNER JOIN FPMovies.dbo.critic ON critic_review.c_cid = critic.cid WHERE critic.cname = \'" + name + "\' AND movie.mname = \'" + list.get('anchor') + "\'"
	cursor.execute(initquery)
	
	#Loaded movie score
	global load
	load = str(cursor.fetchone())
	load = load.replace("(", "")
	load = load.replace("'", "")
	load = load.replace(")", "")
	load = load.replace(",", "")
	load = load.replace(" ", "")
	print(load)		
		
	temp = load
		
	'''Next, load the score and review data into the window'''	
	movie_label1 = tkinter.Label(mov,text="My Review",font=("Times New Roman",15),bg="royal blue",fg="white")
	movie_label1.grid(column=0,row=0,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	
	movie_label2 = tkinter.Label(mov,text=list.get('anchor'),font=("Times New Roman",15),bg="royal blue",fg="white")
	movie_label2.grid(column=0,row=1,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	
	global mylistpalnums
	if critic == 0:
		#Friend Score
		scorequeryfriend = "SELECT ROUND(AVG(CAST(review.r_score AS FLOAT)),3) FROM FPMovies.dbo.review WHERE review.r_uid IN (" + str(mylistpalnums)[1:len(str(mylistpalnums))-1] + ") AND review.r_mid = \'" + movnum + "\'"
		cursor.execute(scorequeryfriend)
		score = str(cursor.fetchone())
		score = score.replace("(", "")
		score = score.replace("'", "")
		score = score.replace(")", "")
		score = score.replace(",", "")
		score = score.replace(" ", "")
		score = score.replace("\"","")
		friendscore = tkinter.Label(mov, text= "Friend Avg Score = " + score,font=("Times New Roman",14),bg = "royal blue",fg="white")
		friendscore.grid(column=0,row=2,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	
	#User Score
	scorequeryuser = "SELECT ROUND(AVG(CAST(review.r_score AS FLOAT)),3) FROM FPMovies.dbo.review WHERE review.r_mid = \'" + movnum + "\'"
	cursor.execute(scorequeryuser)
	score = str(cursor.fetchone())
	score = score.replace("(", "")
	score = score.replace("'", "")
	score = score.replace(")", "")
	score = score.replace(",", "")
	score = score.replace(" ", "")
	score = score.replace("\"","")
	friendscore = tkinter.Label(mov, text= "User Avg Score = " + score,font=("Times New Roman",14),bg = "royal blue",fg="white")
	friendscore.grid(column=0,row=3,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)	
	
	#Critic Score
	scorequerycritic = "SELECT ROUND(AVG(CAST(critic_review.c_score AS FLOAT)),3) FROM FPMovies.dbo.critic_review WHERE critic_review.c_mid = \'" + movnum + "\'"
	cursor.execute(scorequerycritic)
	score = str(cursor.fetchone())
	score = score.replace("(", "")
	score = score.replace("'", "")
	score = score.replace(")", "")
	score = score.replace(",", "")
	score = score.replace(" ", "")
	score = score.replace("\"","")
	friendscore = tkinter.Label(mov, text= "Critic Avg Score = " + score,font=("Times New Roman",14),bg = "royal blue",fg="white")
	friendscore.grid(column=0,row=4,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
		
	#Movie rating buttons
	global movie_btn1
	global movie_btn2
	global movie_btn3
	global movie_btn4
	global movie_btn5
	movie_btn1=tkinter.Button(mov,text="1 Star >:(",bg="ivory3",fg="white",font=("Times New Roman",14),command=lambda: rate("1"))
	movie_btn1.grid(column=0,row=5)
	movie_btn2=tkinter.Button(mov,text="2 Stars :(",bg="ivory3",fg="white",font=("Times New Roman",14),command=lambda: rate("2"))
	movie_btn2.grid(column=1,row=5)
	movie_btn3=tkinter.Button(mov,text="3 Stars :/",bg="ivory3",fg="white",font=("Times New Roman",14),command=lambda: rate("3"))
	movie_btn3.grid(column=2,row=5)
	movie_btn4=tkinter.Button(mov,text="4 Stars :)",bg="ivory3",fg="white",font=("Times New Roman",14),command=lambda: rate("4"))
	movie_btn4.grid(column=3,row=5)
	movie_btn5=tkinter.Button(mov,text="5 Stars :D",bg="ivory3",fg="white",font=("Times New Roman",14),command=lambda: rate("5"))
	movie_btn5.grid(column=4,row=5)
	
	#Find review based on movie id, user id, and type of review
	global usrid
	global rvwtxt
	load = temp
	if critic == 0:
		check = rvwtxt.find_one({'mid':movnum,'id':usrid,'type':'User'});
	else:
		check = rvwtxt.find_one({'mid':movnum,'id':usrid,'type':'Critic'});
	print(check)
	
	#If there is an existing review, launch the rating for that review
	if(load != "None" and check != "None"):
		rate(load)
		newreviewnum = 0
	elif(load != "None" and check == "None"):
		rate(load)
		newreviewnum = 1
	#Otherwise, make a new review and commit the changes to the database
	else:
		print("USRID = " + usrid)
		print("MOVNUM = " + movnum)
		if critic==0:
			newreview = "INSERT INTO FPMovies.dbo.review (r_mid, r_uid, r_score) VALUES (\'" + movnum + "\',\'" + usrid + "\',\'" + str(1) + "\')"
		else:
			newreview = "INSERT INTO FPMovies.dbo.critic_review (c_mid, c_cid, c_score) VALUES (\'" + movnum + "\',\'" + usrid + "\',\'" + str(1) + "\')"
		cursor.execute(newreview)
		conn.commit()
		newreviewnum = 1
	
	#Set up review text entry and submit button
	global reviewtext
	reviewtext = tkinter.Text(mov,width=30,height=10)
	reviewtext.grid(column=0,row=7,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	
	btnsubmitrvw = tkinter.Button(mov,text="Submit",bg="royal blue",fg="white",font=("Times New Roman",14),command=lambda: submitreview())
	btnsubmitrvw.grid(column=0,row=8,columnspan=5,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	
	#If there is an existing review, load the review text
	if(load != "None" or check != "None"):
		displayrvwtxt()
			
	mov.mainloop()	

#This closes the window if login failed and/or user clicked exit before logging in
if auth == 0:
	sys.exit()

#Tkinter window
top = tkinter.Tk()

#Label the window
top.title("FP Movies")

#Window size
top.geometry('400x300')

#Window background color
top.configure(bg='ivory2')

menu = Menu(top)
menu.add_command(label = name)
top.config(menu=menu)

#Header label
lbl1 =tkinter.Label(top,text="FP Movies",font=("Times New Roman",20),bg="ivory3",width = 10)
lbl1.grid(column=1,row=0)

#Search entry box
search=tkinter.Entry(top,width=20)
search.grid(column=1,row=1)

#Scrollbar
scroll = tkinter.Scrollbar(top)
scroll.grid(column=3,row=3,rowspan=30,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)

#Listbox for Scrollbar
list = Listbox(top, yscrollcommand=scroll.set)
list.grid(column=0,columnspan=2,row=3,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)

#Dropdown menu for search
combo = tkinter.ttk.Combobox(top,width=10)
combo['values'] = ("All","Movies","People","Settings")
combo.current(0)
combo.grid(column=0,row=1)
	
#Suggested movie listing which displays when movie button is clicked in main window
def suggestedmovies():
	#Clear the list area in the window
	list.delete(0,'end')
	
	#Find the current user's friends
	pals = friends.find({'user':name})
	
	#Count the number of friends
	numfriends = friends.count_documents({'user':name})
	print("Num of Friends: " + str(numfriends))

	index1 = 0
	index2 = 0
	mylistpals = []
	sum = 0
	count = 0
	avg = 0.0
	
	#Add friend entries to a list of friends
	for ppl in pals:
		ppl = str(ppl)
		start=ppl.find('\'friend\': \'')
		end=ppl.rfind('}')
		print(ppl[start+11:end-2])
		mylistpals.append(ppl[start+11:end-2])
		print(mylistpals)
	
	#Convert those friend names in the list to a list of friend numbers
	global mylistpalnums
	mylistpalnums = []
	frquery = "SELECT usr.usid FROM FPMovies.dbo.usr WHERE usr.usname IN (" + str(mylistpals)[1:len(str(mylistpals))-1] + ")"
	print(frquery)
	cursor.execute(frquery)
	for fr in cursor:
		fr = str(fr)
		fr = fr.replace("(", "")
		fr = fr.replace("'", "")
		fr = fr.replace(")", "")
		fr = fr.replace(",", "")
		mylistpalnums.append(fr)
	
	#List the movies that have been reviewed by friends in order based on the average rating for the movie
	avgquery1 = "SELECT movie.mname FROM FPMovies.dbo.review LEFT OUTER JOIN FPMovies.dbo.movie ON review.r_mid = movie.mid WHERE review.r_uid IN (" + str(mylistpalnums)[1:len(str(mylistpalnums))-1] + ") GROUP BY movie.mname ORDER BY ROUND(AVG(CAST(review.r_score AS FLOAT)),3) DESC"
	cursor.execute(avgquery1)

	#Display the movie name
	for res in cursor:
		res = str(res)
		res = res.replace("(", "")
		res = res.replace("'", "")
		res = res.replace(")", "")
		res = res.replace(",", "")
		list.insert(tkinter.END,res)
		print(res)
	
#List movies based on "srchm" criteria
def listmovies(srchm):
	#Clear the list area in the window
	list.delete(0,'end')
	
	#Specify the query based on search criteria
	if srchm == "All":
		query = "SELECT mname FROM FPMovies.dbo.Movie"
	else:
		query = "SELECT mname FROM FPMovies.dbo.movie where mname like \'%" + srchm + "%\'"
	cursor.execute(query)
	
	#Display the movie name
	for row in cursor:
		row = str(row)
		row = row.replace("(", "")
		row = row.replace("'", "")
		row = row.replace(")", "")
		row = row.replace(",", "")
		list.insert(tkinter.END,row)
		print(row)
	list.grid(column=0,columnspan=3,row=3,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	scroll.config(command=list.yview)
	
#Add friend - activated by selecting a person and clicking "add friend"
def addfriend():
	global list
	newfriend = list.get('anchor')
	print("USER = " + name)
	print("FRIEND = " + str(newfriend))
	friendship={'user':name,'friend':newfriend}
	if newfriend != "" and newfriend != "None":
		fresult = friends.insert_one(friendship)
	print("FRESULT = " + str(fresult))
	clickedf()
	
#Remove friend - activated by selecting a friend and then clicking "remove friend"
def removefriend():
	global list
	notfriend = list.get('anchor')
	print("USER = " + name)
	print("FRIEND = " + str(notfriend))
	unfriend={'user':name,'friend':notfriend}
	fresult = friends.delete_one(unfriend)
	print("FRESULT = " + str(fresult))
	clickedf()
	
#List people based on "srchp" criteria
def listpeople(srchp):
	#Clear the list area in the window
	list.delete(0,'end')
	
	#Specify the query based on the search criteria
	if srchp == "All":
		query = "SELECT usname FROM FPMovies.dbo.usr"
	else:
		query = "SELECT usname FROM FPMovies.dbo.usr where usname like \'%" + srchp + "%\'"
	cursor.execute(query)
	
	#Display the results of the query
	for row in cursor:
		row = str(row)
		row = row.replace("(", "")
		row = row.replace("'", "")
		row = row.replace(")", "")
		row = row.replace(",", "")
		#mn = tkinter.Label(top,text=row,font=("Times New Roman",12),width=10)
		list.insert(tkinter.END,row)
		#txt1.insert(tkinter.END,mn)
		#txt1.insert(tkinter.END,"\n")
		print(row)
	list.grid(column=0,columnspan=3,row=3,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)
	scroll.config(command=list.yview)
	
#List friends based on "srchf" criteria
def listfriends(srchf):
	#Clear the list area in the window
	list.delete(0,'end')
	
	#Specify the query based on the search criteria
	if srchf == "All":
		#Find friends in NOSQL database
		pals = friends.find({'user':name})
		
		#Display results
		for ppl in pals:
			ppl = str(ppl)
			start=ppl.find('\'friend\': \'')
			#print("START = " + str(start))
			end=ppl.rfind('}')
			#print("END = " + str(end))
			print(ppl[start+11:end-1])
			list.insert(tkinter.END,ppl[start+11:end-1])

#Action for when search button is clicked
def clickedsrch():
	global list
	global critic
	
	#Clear list area in the window, configure the window
	list.delete(0,'end')
	lbl1.configure(text="Search")
	txt1.delete('1.0',tkinter.END)
	
	#Retrieve the combobox selection and typed search information
	key = search.get()
	comb = combo.get()
	
	global button
	
	#Set up the select button based on the combobox selection
	if comb == "People":
		query = "SELECT usname FROM FPMovies.dbo.usr where usname like \'%" + key + "%\'"
		cursor.execute(query)
		if critic==0:
			button = tkinter.Button(top,text="Add Friend",font=("Times New Roman",15),width=9,command=lambda x=list.get('anchor'): addfriend())
			button.grid(column=2,row=3)
		for row in cursor:
			row = str(row)
			row = row.replace("(", "")
			row = row.replace("'", "")
			row = row.replace(")", "")
			row = row.replace(",", "")
			list.insert(tkinter.END,row)
			txt1.insert(tkinter.END,row)
			txt1.insert(tkinter.END,"\n")
			print(row)
	elif comb == "Movies":
		listmovies(key)	
		button = tkinter.Button(top,text="Select",font=("Times New Roman",15),width=9,command=lambda x=list.get('anchor'): movie())
		button.grid(column=2,row=3)
	
#Search button
btnsrch=tkinter.Button(top,text="Search",bg="royal blue",fg="white",font=("Times New Roman",15),width=7,command=clickedsrch)
btnsrch.grid(column=2,row=1)

#Clicked friends button
def clickedf():
	global list
	global critic
	list.delete(0,'end')
	lbl1.configure(text="Friends")
	txt1.delete('1.0',tkinter.END)
	combo.current(2)
	#listpeople("All")
	listfriends("All")
	global button
	if critic==0:
		button = tkinter.Button(top,text="Remove",font=("Times New Roman",15),width=9,command=lambda x=list.get('anchor'): removefriend())
		button.grid(column=2,row=3)
	
#Friends button
btnf=tkinter.Button(top,text="Friends",bg="ivory3",font=("Times New Roman",15),width=7,command=clickedf)
btnf.grid(column=0,row=10)

#Clicked movies button
def clickedm():
	global critic
	list.delete(0,'end')
	lbl1.configure(text="Movies")
	'''cursor.execute('SELECT mname FROM FPMovies.dbo.Movie')
	txt1.delete('1.0',tkinter.END)'''
	combo.current(1)
	all = "All"
	if critic==0:
		suggestedmovies()
	else:
		listmovies(all)
	button = tkinter.Button(top,text="Select",font=("Times New Roman",15),width=9,command=lambda x=list.get('anchor'): movie())
	button.grid(column=2,row=3)	
		
#Movies button		
btnm=tkinter.Button(top,text="Movies",bg="ivory3",font=("Times New Roman",15),width=7,command=clickedm)
btnm.grid(column=1,row=10)

#Clicked settings button
def clickeds():
	list.delete(0,'end')
	lbl1.configure(text="Settings")
	txt1.delete('1.0',tkinter.END)
	combo.current(3)

#Settings button
btns=tkinter.Button(top,text="Settings",bg="ivory3",font=("Times New Roman",15),width=7,command=clickeds)
btns.grid(column=2,row=10)

#Text box
txt1=scrolledtext.ScrolledText(top,height=20,width=10,yscrollcommand=scroll.set)
#txt1.grid(column=0,columnspan=3,row=3,sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S)

top.mainloop()

