""" 
	Name: Mohit Khare
	CSE - MNNIT Allahabad
	never give up and love python!!
	Basic GUI tool to fetch rating and details of movies and tv series
"""
from tkinter import *
import tkinter.messagebox
from tkinter import simpledialog
import requests
from bs4 import BeautifulSoup

#Taking input movie / tv series string and returns results
def Ratemovie(inp):
	print()
	s=""
	s+="\n"

	#Search request
	page = requests.get("http://www.google.com/search?q=" + inp + "imdb rating")
	soup = BeautifulSoup(page.content,'html.parser')
	find_links = soup.find(id="search")
	find_movie_div = find_links.find(class_="kv").find('cite').getText()

	#the imdb link for request to be made
	imdb_link = find_movie_div
	#print(imdb_link)

	#fetching movie page
	imdbpage = requests.get("http://"+imdb_link)
	soup = BeautifulSoup(imdbpage.content,'html.parser')

	#movie name
	movie_name = soup.find(class_="title_wrapper").find_all('h1')[0].getText().strip()
	print(movie_name+"\n")
	s+=movie_name+"\n\n"

	#reach the rating class to fetch rating
	find_rating_class = soup.find(class_="ratingValue")
	if(find_rating_class==None):
		s+="Not Rated\n\n"
		print("Not Rated\n")
	else:
		movie_rating = find_rating_class.find('span').getText()
		#print(find_rating_class.prettify())
		s+="Rating : "+movie_rating+"/10\n\n"
		print("Rating : "+movie_rating+"/10\n")

	#genre movie belongs to
	genre = soup.find(class_="subtext").find_all('a')
	#print(type(genre))
	#print(len(genre))
	s+=("Genre : ")
	print("Genre :",end=" ")
	for index in range(0,len(genre)-1): 
		s+=(genre[index].getText()+" , ")
		print(genre[index].getText(),end=" , ")
	
	s+="\n\n"	
	print("\n")
	#release year and date
	#release_year = soup.find(id="titleYear").find('a').getText()
	#print("Release Year : "+release_year)
	s+= ("Release date : "+genre[len(genre)-1].getText().strip()+"\n\n")
	print("Release date : "+genre[len(genre)-1].getText().strip()+"\n")

	if(soup.find(class_="subtext").find_all('time')==[]):
		s+="Time duration not avialable yet.\n\n"
		print("Time duration not avialable yet.\n")
	else:
		time_dur = soup.find(class_="subtext").find_all('time')[0].getText().strip()
		s+="Time Duration : "+time_dur+"\n\n"
		print("Time Duration : "+time_dur+"\n")
	#Summary
	s+="Summary : "
	print("Summary :",end=" ")
	summary = soup.find(class_="summary_text").getText().strip()
	print(summary+"\n\n")
	s+=summary+"\n\n"


	#fetch director , writers and cast
	if(soup.find(class_="credit_summary_item").find('a')==None):
		s+="Director data not avialable\n\n"
		print("Director data not avialable\n")
	else:	
		director = soup.find(class_="credit_summary_item").find('a').getText().strip()
		s+="Director : "+director+"\n\n"
		print("Director : "+director+"\n")


	if(len(soup.find_all(class_="credit_summary_item")) < 2):
		s+="Writers data not avialable\n\n"
		print("Writers data not avialable\n")
	else:		
		writers = soup.find_all(class_="credit_summary_item")[1].find_all('a')
		s+="\nWriters : "
		print("Writers :",end=" ")
		for index in writers:
			s+=index.getText().strip()+" , "
			print(index.getText().strip(), end=" , ")

		s+="\n \n"	
		print('\n')
	if(len(soup.find_all(class_="credit_summary_item")) < 3):
		s+="StarCast data not avialable\n\n"
		print("StarCast data not avialable\n")
	else:		
		starcast = soup.find_all(class_="credit_summary_item")[2].find_all('a')
		s+="StarCast : "
		print("StarCast :",end=" ")
		for index in starcast:
			s+=index.getText().strip()+" , "
			print(index.getText().strip(), end=" , ")

		s+="\n\n"	
		print('\n')
		return s

#GUI part

root = Tk()
root.title('RateMyMovie')
label = Label(root)
label.pack()

name = simpledialog.askstring('Movie/Tv-Series' ,"Input the movie/tvseries name?")

inp = "%s" %name
print(inp)
s = Ratemovie(inp)
tkinter.messagebox.showinfo("Result :" ,s )
print(inp)