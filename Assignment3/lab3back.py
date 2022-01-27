#Weilin Shu
#Lab3back is going to https://www.fandango.com/movie-reviews to get the list of current movies that are playing. Eventually it will 
#make a list of movies that have a unique id, name, rate, genre and releasedate

import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import collections
import pickle 
import json
import sqlite3


class Lab3back:
    def __init__(self):
        '''
        The constructor
        '''
        self.movielist=[]
        #self.GetMainPage()
        #self.WritetoDisk()
        #self.CreateDateBase()
                  

    def GetMainPage(self):
        '''
        This fuction go to the movie-review page and get Movie name, rate and links for each review page.
        '''
        page = requests.get('https://www.fandango.com/movie-reviews') # how to use request to download webpage
        soup = BeautifulSoup(page.content, "lxml")

        #page = ur.urlopen('https://www.fandango.com/movie-reviews')  # how to use urllib to download webpage
        #soup = BeautifulSoup(page.read(), "lxml")

        link = []
        
        movieid = 1
        for elem in soup.find_all('tr',class_ ='reviews-row'):       #find_all find all elements with the tag, tr is tag name, reviews-row is class name
            name = re.sub(r'\bReview\b',"",elem.get_text()).strip()  #sub get rid of "Review" in the text, get_text() print the text only without header
            starint = 0
            for star in elem.find_all('div', class_ = 'star-rating-container'):   #find all tag div in tag tr, this is dealing nested tags
                for fullstar in star.find_all('span', class_ = 'star-icon full'): # Everything find a tag with star-icon full, add 1
                    starint= starint+1
                for halfstar in star.find_all('span', class_ = 'star-icon half'):  # Everything find a tag with star-icon half, add 0.5
                    starint= starint+0.5
    
            for innerelem in elem.find_all('a'):
                try:
                    genre,releaseDate = self.GetSubPageData(innerelem['href'])   #'href' is getting everthing links in tr tag review-row class
                except KeyError:
                    pass       
            print(movieid,name,starint,genre,releaseDate)
            self.movielist.append([movieid ,name,starint,genre,releaseDate])     #put all elements in a list
            movieid +=1
        print(self.movielist)

    
    
    def GetSubPageData(self,link):
        '''
        This funtion go to each review page and get release date and genre
        '''
        subpage = requests.get(link)
        subsoup = BeautifulSoup(subpage.content, "lxml")
        releaseDate = ''
        genre =''
        for elem in subsoup.find_all('ul',class_ ='movie-details__detail'):   
            for rd in elem.find_all('li', class_= 'movie-details__release-date'):
                releaseDate = rd.get_text()
            lineindex = 0
            for gen in elem.find_all('li',class_ = ''):
                if lineindex == 2:
                    genre = gen.get_text()
                    if not genre.strip():
                        genre = "N/A"
                lineindex += 1
        return genre,releaseDate

    def WritetoDisk(self):
        '''
        This function create a pickle file and a json file
        '''
        pickle.dump(self.movielist, open("movie.pickle", 'wb'))   #Create a pickle file
        with open('movie.json', 'w') as fh:                       #Create a Json file
            json.dump(self.movielist, fh)
        
        
    def CreateDateBase(self):
        '''
        This fuction create a database using the pickle file
        '''
        conn = sqlite3.connect('movie.db')                       #Have to have this line
        cur = conn.cursor()                                      #Have to have this line
        cur.execute("DROP TABLE IF EXISTS Genres")               #Create a table called Genres, no repeating elements, id is the key, genre unique
        cur.execute('''CREATE TABLE Genres(                         
                       id INTEGER NOT NULL PRIMARY KEY,
                       genre TEXT UNIQUE ON CONFLICT IGNORE)''')
        cur.execute("DROP TABLE IF EXISTS MovieDB")                 #Create a table called MoveDB, no reapeating elements
        cur.execute('''CREATE TABLE MovieDB( 
                       movieid INTEGER NOT NULL PRIMARY KEY UNIQUE,
                       name TEXT,
                       rate REAL,
                       genre_id INTEGER,
                       releasedate TEXT)''')      
        
        movieslist = pickle.load(open("movie.pickle", 'rb'))        #load the pickle file
        for movie in movieslist:
            cur.execute('''INSERT INTO  (genre) VALUES (?)''', (movie[3], ))   #Insert the genre into Genres table, the inserting must be a tuple
            cur.execute('SELECT id FROM Genres WHERE genre = ? ', (movie[3], ))
            genre_id = cur.fetchone()[0]                                             #Make id for each genre in Genres table, so they can be called in movieDB, still tuple, don't forget [0]
            
            cur.execute('''INSERT INTO MovieDB
                           (movieid, name, rate, genre_id, releasedate) 
                           VALUES ( ?, ?, ?, ?, ? )''', (movie[0], movie[1], movie[2], genre_id, movie[4]) )    #Insert everything else in MovieDB with genre using genre_id
        conn.commit()                                               #Save, if not, change won't be saved
 
    
    def GetGenreList(self):
        '''
        This function return the genre list
        '''
        listGenre = []
        conn = sqlite3.connect('movie.db')              #always have
        cur = conn.cursor()                             #always have
        cur.execute("SELECT * from Genres")
        for genre in cur.fetchall() :
            listGenre.append(genre[1])     
        return (listGenre)
    
    

    def GetMoviesByGenre(self,choice):
        '''
        This function return a list of movie from a selected choice of genre
        '''
        conn = sqlite3.connect('movie.db')                             #always have
        cur = conn.cursor()                                            #always have
        cur.execute('''SELECT * From MovieDB JOIN Genres ON MovieDB.genre_id = Genres.id AND Genres.id ='''+str(choice)) #find the choice genre
        movlist = []
        for movie in cur.fetchall():
            movlist.append(movie)
        return movlist
            
    def GetMoviesByRate(self, choice):
        '''
        This function return a list of movie from a selected choice of rate
        '''
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()        
        cur.execute('''SELECT * From MovieDB JOIN Genres ON MovieDB.genre_id = Genres.id AND MovieDB.rate ='''+str(choice))  #find the choice rate
        movlist = []
        for movie in cur.fetchall() :     
            movlist.append(movie)
        return movlist        

