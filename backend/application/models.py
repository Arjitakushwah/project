from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from datetime import datetime

db= SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(),  nullable=False)
    last_login_at = db.Column(db.DateTime)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',backref=db.backref('users', lazy='dynamic'))
 
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable= False)

class UserRoles(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id", ondelete='CASCADE'), nullable= False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete='CASCADE'), nullable= False)

class Creator(db.Model):
    __tablename__ = 'creator'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    bio = db.Column(db.Text(), nullable=True)  # Nullable since bio might not be provided for all creators
    flagged = db.Column(db.Boolean, default=False)
    report_count = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('creators', lazy='dynamic'))

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    artist = db.Column(db.String(), nullable=False)
    lyrics= db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=True)
    song_file = db.Column(db.String(255), nullable=True)
    flagged = db.Column(db.Boolean, default=False)
    report_count = db.Column(db.Integer(), default=0)
    creator_id = db.Column(db.Integer(), db.ForeignKey('creator.id', ondelete='CASCADE'), nullable=False)
    creator = db.relationship('Creator', backref=db.backref('songs', lazy='dynamic'))
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id', ondelete='CASCADE'), nullable=True)
    album = db.relationship('Album', backref=db.backref('songs', lazy='dynamic'))

class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    report_count = db.Column(db.Integer(), default=0)
    release_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    creator_id = db.Column(db.Integer(), db.ForeignKey('creator.id', ondelete='CASCADE'), nullable=False)
    creator = db.relationship('Creator', backref=db.backref('albums', lazy='dynamic'))

class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('playlists', lazy='dynamic'))

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    playlist_id = db.Column(db.Integer(), db.ForeignKey('playlist.id', ondelete='CASCADE'), nullable=False)
    playlist = db.relationship('Playlist', backref=db.backref('tracks', lazy='dynamic'))
    song_id = db.Column(db.Integer(), db.ForeignKey('song.id', ondelete='CASCADE'), nullable=False)
    song = db.relationship('Song')


class SongRating(db.Model):
    __tablename__ = 'song_rating'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('song_ratings', lazy='dynamic'))
    song_id = db.Column(db.Integer(), db.ForeignKey('song.id', ondelete='CASCADE'), nullable=False)
    song = db.relationship('Song', backref=db.backref('ratings', lazy='dynamic'))
    rating = db.Column(db.Integer(), nullable=False)  # The rating given by the user (1 to 5)

class AlbumRating(db.Model):
    __tablename__ = 'album_rating'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('album_ratings', lazy='dynamic'))
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id', ondelete='CASCADE'), nullable=False)
    album = db.relationship('Album', backref=db.backref('ratings', lazy='dynamic'))
    rating = db.Column(db.Integer(), nullable=False)  # The rating given by the user (1 to 5)

class CreatorRating(db.Model):
    __tablename__ = 'creator_rating'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('creator_ratings', lazy='dynamic'))
    creator_id = db.Column(db.Integer(), db.ForeignKey('creator.id', ondelete='CASCADE'), nullable=False)
    creator = db.relationship('Creator', backref=db.backref('ratings', lazy='dynamic'))
    rating = db.Column(db.Integer(), nullable=False)  # The rating given by the user (1 to 5)
