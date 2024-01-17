from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    __TableName__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    uname = db.Column(db.String(20), nullable=False, unique=True)
    passhash = db.Column(db.String(1024), nullable=False)
    profileid = db.Column(db.String(1024), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    flag= db.Column(db.Integer, nullable=False,default=0)
     
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)
    

class Profile(db.Model):
    __TableName__ = 'profile'
    profileid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))

class Playlist(db.Model):
    __TableName__ = 'playlist'
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    playlistid = db.Column(db.Integer, nullable=False)
    playlistname = db.Column(db.String(50), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    songid = db.Column(db.Integer, db.ForeignKey('song.songid'), nullable=True)
    song= db.relationship('Song', backref='playlist', lazy=True)

class Song(db.Model):
    __TableName__ = 'song'
    songid = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    songname = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    genreid= db.Column(db.Integer, db.ForeignKey('genrelist.genreid'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    lyrics = db.Column(db.String(1024), nullable=False)
    songpath = db.Column(db.String(1024), nullable=False)
    likes = db.Column(db.Integer, nullable=True,default=0)
    dislikes = db.Column(db.Integer, nullable=True,default=0)
    flag= db.Column(db.Integer, nullable=False,default=0)
    avgrating= db.Column(db.Numeric, nullable=True,default=0)

class Rating(db.Model):
    __TableName__ = 'rating'
    ratingid = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    songid = db.Column(db.Integer, db.ForeignKey('song.songid'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Comment(db.Model):
    __TableName__ = 'comment'
    id= db.Column(db.Integer,nullable=False)
    commentid = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    comment = db.Column(db.String(1024), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    songid = db.Column(db.Integer, db.ForeignKey('song.songid'), nullable=False)
    song= db.relationship('Song', backref='comment', lazy=True)

class Genre(db.Model):
    __TableName__ = 'genre'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    genreid = db.Column(db.Integer, db.ForeignKey('genrelist.genreid'), nullable=False)
    songid = db.Column(db.Integer, db.ForeignKey('song.songid'), nullable=True)

class Genrelist(db.Model):
    __TableName__ = 'genrelist'
    genreid = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True)
    genrename = db.Column(db.String(50), nullable=False)



class Album(db.Model):
    __TableName__ = 'album'
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    albumid = db.Column(db.Integer, nullable=False)
    albumname = db.Column(db.String(50), nullable=False)
    songid = db.Column(db.Integer, db.ForeignKey('song.songid'), nullable=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)


with app.app_context():
    db.create_all()

    admin=User.query.filter_by(uname='admin').first()
    if not admin:
        admin=User(uname='admin', password='admin', role='admin', profileid='1')
        admin_profile=Profile(profileid='1', firstname='admin_firstname', lastname='admin_lastname',email='admin_email@gmail.com',phone='0000000000',address='admin_address')
        db.session.add(admin)
        db.session.add(admin_profile)

        genres = [
        {'genreid': '1', 'genrename': 'bollywood'},
        {'genreid': '2', 'genrename': 'hip_hop'},
        {'genreid': '3', 'genrename': 'jazz'},
        {'genreid': '4', 'genrename': 'classical'},
        {'genreid': '5', 'genrename': 'rock'},
        {'genreid': '6', 'genrename': 'pop'},
        {'genreid': '7', 'genrename': 'country'},
        {'genreid': '8', 'genrename': 'folk'},
        {'genreid': '9', 'genrename': 'blues'},
        {'genreid': '10', 'genrename': 'metal'},
        {'genreid': '11', 'genrename': 'reggae'},
        {'genreid': '12', 'genrename': 'soul'},
        {'genreid': '13', 'genrename': 'techno'},
        {'genreid': '14', 'genrename': 'trance'},
        {'genreid': '15', 'genrename': 'disco'},
        {'genreid': '16', 'genrename': 'house'}
        ]

        for genre_data in genres:
            genre = Genrelist(genreid=genre_data['genreid'], genrename=genre_data['genrename'])
            db.session.add(genre)

        db.session.commit()


