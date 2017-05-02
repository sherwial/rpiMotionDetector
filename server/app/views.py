from app import app
from flask import render_template, send_file
import os
import uuid
name = 'Adam'

def buildLibrary():
    posts = []
    path = "/Users/sherwin1408/Music/iTunes/iTunes Media/Music"
    directory = os.listdir(path)
    song_id = 0
    for item in directory:
        artist = path + '/' + item
        if os.path.isdir(artist):
            current_artist = {}
            current_artist["artist"] = item
            albums = os.listdir(artist)
            current_artist["albums"] = []
            for album in albums:
                if os.path.isdir(artist + '/' + album):
                    current_album = {}
                    current_album["title"] = ascii(album)
                    current_album["songs"] = []
                    songs = os.listdir(artist + '/' + album)
                    for song in songs:
                        original = song
                        if (ord(song[0]) > 47 and ord(song[0]) < 59 and song[2] == ' '):
                            song = song[2:]
                        current_album["songs"].append({"song": ascii(song), "link": "/song/" + str(song_id), "song_id":str(song_id), "original":original})
                        song_id += 1
                    current_artist["albums"].append(current_album)
            posts.append(current_artist)
    return posts

posts = buildLibrary()

def getInfoFromHex(hex):
    for item in posts:
        for album in item["albums"]:
            for song in album["songs"]:
                if str(hex) == song["song_id"]:
                    link = ("/Users/sherwin1408/Music/iTunes/iTunes Media/Music/" + item["artist"] + "/" + album["title"] + "/" + song["original"])
                    return link, song["song"]

@app.route('/')
def home():
    return render_template("home.html", title='Adams iTunes Library')

@app.route('/song/<songlink>')
def song(songlink):
    link, song_name = getInfoFromHex(songlink)
    return send_file(link, attachment_filename=song_name, as_attachment=True)

@app.route('/observations')
def library():
    return render_template("users.html",
                           post = posts)