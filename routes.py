from operator import or_
import os
import random
from flask import render_template, request, redirect, url_for, flash, session,send_from_directory, jsonify
from sqlalchemy import desc, distinct
from app import app
from functools import wraps
from models import Album, Rating, db, User, Profile,Song,Playlist,Comment,Genre,Genrelist
from sqlalchemy.exc import SQLAlchemyError
from auth import auth_required, admin_required,creator_required

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    else:
        return render_template('welcome.html',nav="welcome")
    


# user dashboard
@app.route('/user_dashboard')
@auth_required
def user_dashboard():
    songs=Song.query.all()
    playlists=Playlist.query.filter_by(userid=session['user_id']).all()
    genres=Genre.query.all()
    comment=Comment.query.all()
    rating=Rating.query.all()
    
    playlist_distinct = Playlist.query.filter_by(userid=session['user_id']).with_entities(distinct(Playlist.playlistid), Playlist.playlistname).all()
    
    dic = {}
    for song in songs:
        rating = Rating.query.filter_by(songid=song.songid).all()
        if len(rating) == 0:
            song.avgrating = 0
        else:
            total = 0
            for i in rating:
                total += i.rating
            song.avgrating = total/len(rating)
        db.session.commit()


    for i in genres:
        genre_id = i.genreid
        song_id = i.songid
        if genre_id not in dic:
            dic[genre_id] = []
        genre_name = Genrelist.query.filter_by(genreid=genre_id).first().genrename
        if song_id is None:
            song_name = 'None'
        else:
            song_name = Song.query.filter_by(songid=song_id).first().songname
        dic[genre_id].append({
            'songid': song_id,
            'genrename': genre_name,
            'songname': song_name
        })

    songs=Song.query.order_by(Song.avgrating.desc()).all()

    album=Album.query.all()
    album_dic={}
    for i in album:
        album_id=i.albumid
        song_id=i.songid
        if album_id not in album_dic:
            album_dic[album_id]=[]
        album_name=Album.query.filter_by(albumid=album_id).first().albumname
        if song_id is None:
            song_name='None'
        else:
            song_name=Song.query.filter_by(songid=song_id).first().songname
        
        
        album_dic[album_id].append({
            'songid':song_id,
            'albumname':album_name,
            'songname':song_name
        })


    return render_template('dashboard/user_dashboard.html',nav="user_dashboard",songs=songs,playlists=playlists,genres=dic,user=User.query.filter_by(userid=session['user_id']).first(),comment=comment,playlist_distinct=playlist_distinct,albumdic=album_dic)

@app.route('/profile')
@auth_required
def profile():
    profile=(User.query.filter_by(userid=session['user_id']).first()).profileid
    return render_template('dashboard/profile.html',profile=Profile.query.filter_by(profileid=profile).first(),user=User.query.filter_by(userid=session['user_id']).first(),nav="profile")

@app.route('/profile',methods=["POST"])
@auth_required
def profile_post():
    user=User.query.filter_by(userid=session['user_id']).first()
    address=request.form.get('address')
    cpassword=request.form.get('cpassword')
    npassword=request.form.get('npassword')
    profile=Profile.query.filter_by(profileid=user.profileid).first()

    if address is None :
        flash('Please fill the required fields')
        return redirect(url_for('profile'))
    elif address!='' and cpassword=='' and npassword=='':
        profile.address=address
        db.session.commit()
    elif address!='' or cpassword!='' or npassword!='':
        if not user.check_password(cpassword):
            flash('Please check your password and try again.')
            return redirect(url_for('profile'))
        if npassword == cpassword:
            flash('New password cannot be same as old password')
            return redirect(url_for('profile'))
        else:
            user.password=npassword
            profile.address=address
            db.session.commit()
    flash(['Profile updated successfully','success'])
    return redirect(url_for('profile'))

@app.route('/read_lyrics/<int:songid>')
@auth_required
def read_lyrics(songid):
    song=Song.query.filter_by(songid=songid).first()
    lyrics=open(song.lyrics,'r').read()
    song_file=song.songpath
    comments = Comment.query.filter_by(songid=song.songid).order_by(Comment.id.desc()).all()
    user=User.query.filter_by(userid=session['user_id']).first()
    
    rating = Rating.query.filter_by(songid=song.songid, userid=user.userid).first()
    if rating:
        rating = rating.rating
    else:
        rating = 0

    
    return render_template('dashboard/read_lyrics.html',nav="read_lyrics",song=song,lyrics=lyrics,song_file=song_file[8:],rating=rating,comments=comments,user=User.query.all())

@app.route('/update_rating', methods=["POST"])
@auth_required
def update_rating():
    data = request.get_json(force=True)
    songid = data['song_id']
    rating = data['rating']
    userid = session['user_id']
    try:
        existing_rating = Rating.query.filter_by(songid=songid,userid=userid).first()
        if existing_rating:
            existing_rating.rating = rating
            db.session.commit()
        else:
            rating = Rating(ratingid=random.randint(0,99999), songid=songid, userid=userid, rating=rating)
            db.session.add(rating)
            db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
    
@app.route('/submit_comment', methods=["POST"])
@auth_required
def add_comment():
    data = request.get_json(force=True)
    if Comment.query.all() == []:
        id = 0
    else:
        id = Comment.query.order_by(desc(Comment.id)).first().id
        id = id + 1

    songid = data['song_id']
    comment = data['comment']
    userid = session['user_id']
    try:
        comment = Comment(id=id,commentid=random.randint(0,99999), songid=songid, userid=userid, comment=comment)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/create_playlist')
@auth_required
def create_playlist():
    songs=Song.query.all()
    return render_template('dashboard/create_playlist.html',nav="create_playlist",songs=songs)

@app.route('/create_playlist',methods=["POST"])
@auth_required
def create_playlist_post():
    playlistname=request.form.get('playlistname')
    selected_songs_ids = request.form.getlist('selected_songs')
    if playlistname==None:
        flash('Please fill the required fields')
        return redirect(url_for('create_playlist'))
    if len(selected_songs_ids)==0:
        flash('Please select atleast one song')
        return redirect(url_for('create_playlist'))
    
    playlistid=random.randint(0,9999)
    for playlistid in Playlist.query.filter_by(playlistid=playlistid).all():
        playlistid=random.randint(0,9999)

    for songid in selected_songs_ids:
        playlist=Playlist(playlistid=playlistid,playlistname=playlistname,userid=session['user_id'],songid=songid)
        db.session.add(playlist)
        db.session.commit()
    flash(['Playlist created successfully','success'])
        
    return redirect(url_for('user_dashboard'))

@app.route('/view_playlist/<int:playlistid>')
@auth_required
def view_playlist(playlistid):
    if Playlist.query.filter_by(playlistid=playlistid).first() is None:
        return redirect(url_for('user_dashboard'))
    
    songs=[]
    playlist=(Playlist.query.filter_by(playlistid=playlistid).all())
    for i in playlist:
        songs.append(Song.query.filter_by(songid=i.songid).all())
    
    return render_template('dashboard/view_playlist.html',nav="view_playlist",songs=songs,playlist=playlist,user=User.query.filter_by(userid=session['user_id']).first())

@app.route('/delete_playlist_song/<int:song>/<int:playlist>')
@auth_required
def delete_playlist_song(song, playlist):
    playlistid = playlist
    playlist = Playlist.query.filter_by(songid=song, playlistid=playlistid).first()
    db.session.delete(playlist)
    db.session.commit()
    flash(['Song deleted successfully', 'success'])

    return redirect(url_for('view_playlist', playlistid=playlistid))

@app.route('/delete_playlist/<int:playlist>')
@auth_required
def delete_playlist(playlist):
    playlist = Playlist.query.filter_by(playlistid=playlist).all()
    for i in playlist:
        db.session.delete(i)
        db.session.commit()
    flash(['Playlist deleted successfully', 'success'])

    return redirect(url_for('user_dashboard'))


@app.route('/creator_register')
@auth_required
def creator_register():
    user=User.query.filter_by(userid=session['user_id']).first()
    if user.role=="creator":
        return redirect(url_for('creator_dashboard'))
    return render_template('dashboard/creator_register.html',nav="creator_register")

@app.route('/creator_dashboard')
@auth_required
def creator_dashboard():
    user=User.query.filter_by(userid=session['user_id']).first()
    if user.role=="admin":
        flash('Admin cannot be a creator')
        return redirect(url_for('admin_dashboard'))
    
    if user.role!="creator" or user.flag!=1:
        user.role="creator"
        db.session.commit()
    else:
        flash('Admin Banned Your Account. Please contact admin to change your role')
        return redirect(url_for('user_dashboard'))
    
    songs=Song.query.filter_by(userid=session['user_id']).all()

    total = 0
    for song in songs:
        rating = Rating.query.filter_by(songid=song.songid).all()
        if len(rating) == 0:
            avgrating = 0
        else:
            
            for i in rating:
                total += i.rating
            
    if len(songs) != 0:
        avgrating=total/len(songs)
    else:
        avgrating=0

    total_albums = Album.query.filter_by(userid=session['user_id']).group_by(Album.albumid).all()
    if total_albums== "":
        total_albums=0
    albums=Album.query.filter_by(userid=session['user_id']).group_by(Album.albumid).all()
   
    dash_info={}
    dash_info['total_songs']=len(songs)
    dash_info['avg_rating']=avgrating
    dash_info['total_albums']=len(total_albums)
    return render_template('dashboard/creator_dashboard.html',nav="creator_dashboard",songs=songs,dash_info=dash_info,albums=albums)

@app.route('/upload_song')
@auth_required
@creator_required
def upload_song():
    genres=Genrelist.query.all()
    return render_template('dashboard/upload_song.html',nav="upload_song",genres=genres)

@app.route('/upload_song',methods=["POST"])
@auth_required
@creator_required
def upload_song_post():
    title=request.form.get('title')
    artist=request.form.get('singer')
    genre=request.form.get('genre')
    year=request.form.get('year')
    lyrics=request.form.get('lyrics')

    lyrics_filename='lyrics_'+str(random.randint(0,999999999))+'.txt'
    a=open(os.path.join('uploads', lyrics_filename),'w')
    a.write(lyrics)
    a.close()
    lyrics_path=os.path.join('uploads', lyrics_filename)

    if User.query.filter_by(userid=session['user_id']).first().flag==1:
        flash('Admin Banned Your Account. Please contact admin to change your role')
        return redirect(url_for('creator_dashboard'))

    if 'song' not in request.files:
        flash('No file part')
        return redirect(url_for('upload_song'))
    
    song = request.files['song']
    if song.filename == '':
        flash('No selected file')
        return redirect(url_for('upload_song'))
    
    if song:
        # Change the filename (e.g., 'any_name.mp3' --> 'song_{any integer}.mp3')
        filename = 'song_'+str(random.randint(0,999999999))+'.mp3'

        # Save the file to a specific folder
        song.save(os.path.join('uploads', filename))
        songpath=os.path.join('uploads', filename)
    else:
        flash('Please select a song')
        return redirect(url_for('upload_song'))

    genreid=Genrelist.query.filter_by(genrename=genre).first().genreid


    if title=='' or artist=='' or genreid=='' or year=='' or lyrics=='':
        flash('Please fill the required fields')
        return redirect(url_for('upload_song'))
    songid=random.randint(0,9999)
    for songid in Song.query.filter_by(songid=songid).all():
        songid=random.randint(0,9999)
    song=Song(songid=songid,songname=title,artist=artist,genreid=genreid,year=year,lyrics=lyrics_path,songpath=songpath,userid=session['user_id'])
    db.session.add(song)
    db.session.commit()

    genre=Genre(id=random.randint(0,9999),genreid=genreid,songid=songid)
    db.session.add(genre)
    db.session.commit()

    flash(['Song uploaded successfully','success'])
    return redirect(url_for('creator_dashboard'))

@app.route('/creator_delete_song/<int:songid>')
@auth_required
@creator_required
def creator_delete_song(songid):
    song=Song.query.filter_by(songid=songid).first()
    
    if song:

        if os.path.exists(song.songpath):
            os.remove(song.songpath)
        if os.path.exists(song.lyrics):
            os.remove(song.lyrics)

        album=Album.query.filter_by(songid=songid).all()
        for i in album:
            db.session.delete(i)
            db.session.commit()
        comment=Comment.query.filter_by(songid=songid).all()
        for i in comment:
            db.session.delete(i)
            db.session.commit()
        genre=Genre.query.filter_by(songid=songid).all()
        for i in genre:
            db.session.delete(i)
            db.session.commit()
        playlist=Playlist.query.filter_by(songid=songid).all()
        for i in playlist:
            db.session.delete(i)
            db.session.commit()
        rating=Rating.query.filter_by(songid=songid).all()
        for i in rating:
            db.session.delete(i)
            db.session.commit()

        db.session.delete(song)
        db.session.commit()
        flash(['Song deleted successfully','success'])
        return redirect(url_for('creator_dashboard'))
    else:
        flash('Please song not found')
        return redirect(url_for('creator_dashboard'))

@app.route('/edit_song/<int:songid>')
@auth_required
@creator_required
def edit_song(songid):
    song=Song.query.filter_by(songid=songid).first()
    genres=Genrelist.query.filter_by(genreid=song.genreid).first()
    return render_template('dashboard/edit_song.html',nav="edit_song",song=song,genre=genres)

@app.route('/edit_song/<int:songid>',methods=["POST"])
@auth_required
@creator_required
def edit_song_post(songid):
    title=request.form.get('title')
    artist=request.form.get('singer')
    genre=request.form.get('genre')
    year=request.form.get('year')
    

    genreid=Genrelist.query.filter_by(genrename=genre).first().genreid
    genre=Genre.query.filter_by(songid=songid).first()
    song=Song.query.filter_by(songid=songid).first()

    if title=='' or artist=='' or genreid=='' or year=='':
        flash('Please fill the required fields')
        return redirect(url_for('upload_song'))
    
    if song:
        song.songname=title
        song.artist=artist
        song.genreid=genreid
        song.year=year
        genre.genreid=genreid
        db.session.commit()
        flash(['Song updated successfully','success'])
        return redirect(url_for('creator_dashboard'))
    else:
        flash('Please select a song')
        return redirect(url_for('upload_song'))


@app.route('/create_album')
@auth_required
@creator_required
def create_album():
    songs=Song.query.filter_by(userid=session['user_id']).all()
    return render_template('dashboard/create_album.html',nav="create_album",songs=songs)

@app.route('/create_album',methods=["POST"])
@auth_required
@creator_required
def create_album_post():
    albumname=request.form.get('albumname')
    selected_songs_ids = request.form.getlist('selected_songs')
    if albumname==None:
        flash('Please fill the required fields')
        return redirect(url_for('create_album'))
    if len(selected_songs_ids)==0:
        flash('Please select atleast one song')
        return redirect(url_for('create_album'))
    
    
    albumid=random.randint(0,9999)
    for albumid in Album.query.filter_by(albumid=albumid).all():
        albumid=random.randint(0,9999)

    for songid in selected_songs_ids:
        album=Album(albumid=albumid,albumname=albumname,userid=session['user_id'],songid=songid)
        db.session.add(album)
        db.session.commit()
    flash(['Album created successfully','success'])
        
    return redirect(url_for('creator_dashboard'))


@app.route('/view_album/<int:albumid>')
@auth_required
@creator_required
def view_album(albumid):
    if Album.query.filter_by(albumid=albumid).first() is None:
        return redirect(url_for('creator_dashboard'))
    
    songs=[]
    album=(Album.query.filter_by(albumid=albumid).all())
    for i in album:
        songs.append(Song.query.filter_by(songid=i.songid).all())
    
    return render_template('dashboard/view_album.html',nav="view_album",songs=songs,album=album,user=User.query.filter_by(userid=session['user_id']).first())

@app.route('/delete_album_song/<int:song>/<int:albumid>')
@auth_required
@creator_required
def delete_album_song(song, albumid):
    albumid = albumid
    album = Album.query.filter_by(songid=song, albumid=albumid).first()
    db.session.delete(album)
    db.session.commit()
    flash(['Song deleted successfully', 'success'])

    return redirect(url_for('view_album', albumid=albumid))

@app.route('/delete_album/<int:albumid>')
@auth_required
@creator_required
def delete_album(albumid):
    album = Album.query.filter_by(albumid=albumid).all()
    for i in album:
        db.session.delete(i)
        db.session.commit()
    flash(['Album deleted successfully', 'success'])

    return redirect(url_for('creator_dashboard'))

@app.route('/edit_album/<int:albumid>')
@auth_required
@creator_required
def edit_album(albumid):
    album=Album.query.filter_by(albumid=albumid).all()
    list=[]
    for i in album:
        list.append(i.songid)
    songs=Song.query.filter_by(userid=session['user_id']).all()
    return render_template('dashboard/edit_album.html',nav="edit_album",album=album,songs=songs,list=list)

@app.route('/edit_album/<int:albumid>',methods=["POST"])
@auth_required
@creator_required
def edit_album_post(albumid):
    albumname=request.form.get('albumname')
    selected_songs_ids = request.form.getlist('selected_songs')
    if albumname==None:
        flash('Please fill the required fields')
        return redirect(url_for('edit_album'))
    if len(selected_songs_ids)==0:
        flash('Please select atleast one song')
        return redirect(url_for('edit_album'))
    
    album=Album.query.filter_by(albumid=albumid).all()
    for i in album:
        db.session.delete(i)
        db.session.commit()

    for songid in selected_songs_ids:
        album=Album(albumid=albumid,albumname=albumname,userid=session['user_id'],songid=songid)
        db.session.add(album)
        db.session.commit()
    flash(['Album updated successfully','success'])
        
    return redirect(url_for('creator_dashboard'))


@app.route('/recommendations')
@auth_required
def recommendations():
    songs=Song.query.order_by(Song.avgrating.desc()).all()

    return render_template('dashboard/recommendations.html',nav="recommendations",songs=songs)

@app.route('/admin_dashboard')
@auth_required
@admin_required
def admin_dashboard():
    dic={}
    dic['user_count'] = User.query.filter_by(role='user').count()
    dic['creator_count'] = User.query.filter_by(role='creator').count()
    dic['track_count'] = Song.query.count()
    dic['album_count'] = Album.query.group_by(Album.albumid).count()
    dic['genre_count'] = Genrelist.query.count()
    user=User.query.filter_by(userid=session['user_id']).first()

    song_data = Song.query.all()  
    data_for_chart = [{'name': song.songname, 'rating': song.avgrating} for song in song_data]
    
    return render_template('dashboard/admin_dashboard.html',nav="admin_dashboard",dic=dic,user=user, song_data=data_for_chart)




@app.route('/tracks')
@auth_required
@admin_required
def tracks():
    songs=Song.query.all()
    genre_list = Genre.query.with_entities(distinct(Genre.genreid)).all()
    genre=Genre.query.all()
    dic={}
    gen=[]
    if genre_list!='' or genre_list!=[]:
        for i in genre:
            genre_id=i.genreid
            song_id=i.songid
            if genre_id not in dic:
                dic[genre_id]=[]
            genre_name=Genrelist.query.filter_by(genreid=genre_id).first().genrename
            if song_id is None:
                song_name='None'
            else:
                song_name=Song.query.filter_by(songid=song_id).first().songname
            dic[genre_id].append({
                'songid':song_id,
                'genrename':genre_name,
                'songname':song_name,
            })
        for i in genre_list:
            gen.append(i[0])
    return render_template('dashboard/admin_tracks.html',nav="tracks",songs=songs,genre=genre,genre_list=gen,dic=dic)


@app.route('/admin_delete_song/<int:songid>')
@auth_required
@admin_required
def admin_delete_song(songid):
    song=Song.query.filter_by(songid=songid).first()
    
    if song:

        if os.path.exists(song.songpath):
            os.remove(song.songpath)
        if os.path.exists(song.lyrics):
            os.remove(song.lyrics)

        album=Album.query.filter_by(songid=songid).all()
        for i in album:
            db.session.delete(i)
            db.session.commit()
        comment=Comment.query.filter_by(songid=songid).all()
        for i in comment:
            db.session.delete(i)
            db.session.commit()
        genre=Genre.query.filter_by(songid=songid).all()
        for i in genre:
            db.session.delete(i)
            db.session.commit()
        playlist=Playlist.query.filter_by(songid=songid).all()
        for i in playlist:
            db.session.delete(i)
            db.session.commit()
        rating=Rating.query.filter_by(songid=songid).all()
        for i in rating:
            db.session.delete(i)
            db.session.commit()

        db.session.delete(song)
        db.session.commit()
        flash(['Song deleted successfully','success'])
        return redirect(url_for('tracks'))
    else:
        flash('Please song not found')
        return redirect(url_for('tracks'))
    
@app.route('/all_tracks/<int:genreid>')
@auth_required
@admin_required
def all_tracks(genreid):
    songs=Song.query.filter_by(genreid=genreid).order_by(Song.avgrating.desc()).all()

    return render_template('dashboard/admin_all_tracks.html',nav="admin_all_tracks",songs=songs)

@app.route('/admin_albums')
@auth_required
@admin_required
def admin_albums():
    songs=Song.query.all()
    album_list = Album.query.with_entities(distinct(Album.albumid)).all()
    album=Album.query.all()
    dic={}
    gen=[]
    if album_list!='' or album_list!=[]:
        for i in album:
            album_id=i.albumid
            song_id=i.songid
            if album_id not in dic:
                dic[album_id]=[]
            album_name=Album.query.filter_by(albumid=album_id).first().albumname
            if song_id is None:
                song_name='None'
            else:
                song_name=Song.query.filter_by(songid=song_id).first().songname
            dic[album_id].append({
                'songid':song_id,
                'albumname':album_name,
                'songname':song_name,
                'albumid':album_id
            })
        for i in album_list:
            gen.append(i[0])
    return render_template('dashboard/admin_albums.html',nav="admin_albums",songs=songs,album=album,album_list=gen,dic=dic)

@app.route('/admin_delete_song_album/<int:songid>/<int:albumid>')
@auth_required
@admin_required
def admin_delete_song_album(songid, albumid):
    album = Album.query.filter_by(songid=songid, albumid=albumid).first()
    db.session.delete(album)
    db.session.commit()
    flash(['Song deleted successfully', 'success'])

    return redirect(url_for('admin_albums'))

@app.route('/admin_album_allsongs/<int:albumid>')
@auth_required
@admin_required
def admin_album_allsongs(albumid):
    songs=[]
    album=Album.query.filter_by(albumid=albumid).all()
    for i in album:
        a=Song.query.filter_by(songid=i.songid).order_by(Song.avgrating.desc()).first()
        songs.append(a)

    return render_template('dashboard/admin_album_allsongs.html',nav="admin_album_allsongs",songs=songs,albumid=album[0].albumid)



@app.route('/admin_creator_management/')
@auth_required
@admin_required
def admin_creator_management():
    creators = User.query.filter(or_(User.role == 'creator', User.flag == 1)).all()
    return render_template('dashboard/admin_creator_management.html',nav="admin_creator_management",creators=creators)

@app.route('/admin_creator_managements/<int:userid>')
@auth_required
@admin_required
def admin_creator_managements(userid):
    creators=User.query.filter_by(userid=userid).first()
    if creators.role=='user':
        creators.role='creator'
        creators.flag=0
        db.session.commit()
    else:
        creators.role='user'
        creators.flag=1
        db.session.commit()

    return redirect(url_for('admin_creator_management'))

@app.route('/search')
@auth_required
def search():
    search = request.args.get('query')
    songs=Song.query.all()
    if search is None:
        return render_template('dashboard/search.html',nav="search",songs=songs)
    else:
        songs=Song.query.filter(Song.songname.like('%'+search+'%')).all()
    return render_template('dashboard/search.html',nav="search",songs=songs)