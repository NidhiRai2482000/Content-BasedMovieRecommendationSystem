# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:05:42 2021

@author: Hp
"""

import tkinter
import pandas as pd
import numpy as np
import math

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import islice

result=""
general,genre,castdir,title=0,0,0,0
top = tkinter.Tk()
top.title("Movie recommendation system")
top.geometry("700x500")
top.resizable(False,False)
bg = tkinter.PhotoImage(file="backg.png")
my_label=tkinter.Label(top,image=bg)
my_label.place(x=0,y=0)
label=tkinter.Label(top,text="Enter the movie: ",font=("Helvetica",20),fg="black")
label.pack(pady=40)

def getTextInput():
    global result
    global general
    result=entry.get("1.0","end-1c")
    general = 1
    top.destroy()
    print(result)
def getGenreInput():
    global result
    global genre
    result=entry.get("1.0","end-1c")
    genre = 1
    top.destroy()
    print(result)
def getCastInput():
    global result
    global castdir
    result=entry.get("1.0","end-1c")
    castdir = 1
    top.destroy()
    print(result)
def getTitleInput():
    global result
    global title
    result=entry.get("1.0","end-1c")
    title = 1
    top.destroy()
    print(result)
    
entry=tkinter.Text(top,height=1,width=30,font=("Helvetica",20),fg="black")
entry.pack(pady=10)
button=tkinter.Button(top,text="Recommend",width=20,font=("Helvetica",20),fg="black",command=getTextInput)

button.pack(pady=10)
buttongenre = tkinter.Button(top,text="Genre",width=20,font=("Helvetica",20),fg="black",command=getGenreInput)
buttongenre.pack(pady=10)
buttoncast = tkinter.Button(top,text="Cast and directors",width=20,font=("Helvetica",20),fg="black",command=getCastInput)
buttoncast.pack(pady=10)
buttontitle = tkinter.Button(top,text="Title",width=20,font=("Helvetica",20),fg="black",command=getTitleInput)
buttontitle.pack(pady=10)
top.mainloop()


df = pd.read_csv("movie_dataset.csv")

features = ['genres', 'keywords', 'title', 'cast', 'director']
df['cast'].isnull().values.any()
for feature in features:
    df[feature] = df[feature].fillna('')


def combine_features(row):
    return row['title']+' '+row['genres']+' '+row['director']+' '+row['keywords']+' '+row['cast']
def combine_genrefeatures(row):
    return row['genres']+' '+row['keywords']
def combine_castfeatures(row):
    return row['director']+' '+row['cast']
def combine_titlefeatures(row):
    return row['title']+' '+row['keywords']

cv = CountVectorizer()
if general == 1:    
    df['combined_features'] = df.apply(combine_features, axis = 1)
    count_matrix = cv.fit_transform(df['combined_features'])
    
if genre == 1:
    print("Inside genre")
    df['combined_features1'] = df.apply(combine_genrefeatures, axis = 1)
    count_matrix = cv.fit_transform(df['combined_features1'])
    
if castdir == 1:
    df['combined_features2'] = df.apply(combine_castfeatures, axis = 1)
    count_matrix = cv.fit_transform(df['combined_features2'])
    
if title == 1:
    df['combined_features3'] = df.apply(combine_titlefeatures, axis = 1)
    count_matrix = cv.fit_transform(df['combined_features3'])
    
print(count_matrix)
count_array = count_matrix.toarray()
nparray = np.array(count_array)
print(count_array)    

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

movie_list = df["title"].values.tolist()
print(movie_list)
titlecase = result.title();
print(titlecase)
if titlecase in movie_list:
        movie_index = get_index_from_title(titlecase)
        print(movie_index)
        
        
        sim_dict={}
        i = 0
        while i < 4803 :
          cosine_sim=cosine_similarity(nparray[movie_index],nparray[i])
          sim_dict[i] = cosine_sim
          print(sim_dict[i])
          
          i += 1
        print(sim_dict)
        sorted_dict = dict( sorted(sim_dict.items(),
                                    key=lambda item: item[1],
                                    reverse=True))
        print(sorted_dict)
        key_iterable = sorted_dict.keys()
        key_list = list(key_iterable)
        print(key_list)
        key_list.pop(0)
        
        i=1
        down = tkinter.Tk()
        down.title("Movie recommendation system")
        down.geometry("700x500")
        down.resizable(False,False)
        bg = tkinter.PhotoImage(file="backg.png")
        my_label=tkinter.Label(down,image=bg)
        my_label.place(x=0,y=0)
        x="The top 10 similar movies to "+result+" are:"
        tkinter.Label(down,text=x,font=("Helvetica",15),width=100,height=1,fg="white",bg="grey").pack(pady=2)
        for element in key_list:
            x=get_title_from_index(element)
            tkinter.Label(down,text=x,font=("Helvetica",15),width=50,height=1,fg="white",bg="darkblue").pack(pady=2)
            i=i+1
            if i>11:
                break
        down.mainloop()
else:
        down = tkinter.Tk()
        down.title("Movie recommendation system")
        down.geometry("700x500")
        down.resizable(False,False)
        bg = tkinter.PhotoImage(file="backg.png")
        my_label=tkinter.Label(down,image=bg)
        my_label.place(x=0,y=0)
        x="The movie "+result+" is not found in the dataset "
        tkinter.Label(down,text=x,font=("Helvetica",25),width=50,height=5,fg="white",bg="red").pack(pady=80)
        down.mainloop()
        