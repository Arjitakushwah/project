from flask import Blueprint, request, jsonify, send_file
from flask_caching import Cache
from flask import current_app as app
from flask_security import login_user, current_user, auth_required, roles_required
from .models import db, UserRoles
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, UserRoles, User, Creator, Album, Song, Playlist, PlaylistSong, SongRating, CreatorRating, AlbumRating
from sqlalchemy import or_, func
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone

api = Blueprint("api", __name__, url_prefix="/api")
cache = Cache()

# register
@api.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not (name and email and password):
            return jsonify({'error': 'Name, email, and password are required.'}), 400

        if app.security.datastore.find_user(email=email):
            return jsonify({'error': 'Email already exists.'}), 409

        app.security.datastore.create_user(
            name=name, email=email, password=generate_password_hash(password))
        db.session.commit()
        user = app.security.datastore.find_user(email=email)
        role = app.security.datastore.find_role(role="user")
        user_role = UserRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# login
@api.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        user = app.security.datastore.find_user(email=email)
        if not user or not check_password_hash(user.password, password):
            return {"message": "User not found!"}, 404
        else:
            login_user(user)
            user.last_login_at = datetime.now(timezone.utc)
            db.session.commit()
            roles = []
            for role in current_user.roles:
                roles.append(role.name)
            return {"roles": roles, "token": current_user.get_auth_token()}

# admin management
@api.route("/admin/dashboard")
@auth_required("token")
@roles_required("admin")
def admin():
    total_users = User.query.count()
    total_creators = Creator.query.count()
    total_albums = Album.query.count()
    total_songs = Song.query.count()
    return jsonify({
        'total_users': total_users,
        'total_creators': total_creators,
        'total_albums': total_albums,
        'total_songs': total_songs
    })

# flag creator
@api.route('/flag_creator/<int:creator_id>', methods=['POST'])
@auth_required("token")
@roles_required("admin")
def flag_creator(creator_id):
    creator = Creator.query.get_or_404(creator_id)
    if 'flagged' not in request.json:
        return jsonify({'error': 'Flagged field is missing'}), 400
    creator.flagged = request.json['flagged']
    db.session.commit()
    cache.clear()
    return jsonify({'message': f'Creator {creator_id} flagged successfully'}), 200

# whitelist creator
@api.route('/whitelist_creator/<int:creator_id>', methods=['POST'])
@auth_required("token")
@roles_required("admin")
def whitelist_creator(creator_id):
    creator = Creator.query.get_or_404(creator_id)
    if creator.flagged:
        creator.flagged = False
        db.session.commit()
        cache.clear()
        return jsonify({'message': f'Creator {creator_id} whitelisted successfully'}), 200
    else:
        return jsonify({'message': f'Creator {creator_id} is already whitelisted'}), 200

# user management
# user profile
@api.route("/user", methods=['GET'])
@auth_required("token")
def userProfile():
    user = current_user
    playlists = Playlist.query.filter_by(user_id=user.id).all()
    playlist_data = [{'id': playlist.id, 'name': playlist.name} for playlist in playlists]
    user_data = {'name': user.name,
        'email': user.email,
        'playlist': playlist_data}
    return jsonify(user_data)

# creator register
@api.route("/creator/register", methods=['POST'])
@auth_required("token")
def creator_register():
    data = request.json
    name = data.get('name')
    bio = data.get('bio')
    email = current_user.email
    creator = Creator(name=name, bio=bio, user=current_user)
    db.session.add(creator)
    db.session.commit()
    user = app.security.datastore.find_user(email=email)
    role = app.security.datastore.find_role(role="creator")
    user_role = UserRoles(user_id=user.id, role_id=role.id)
    db.session.add(user_role)
    db.session.commit()
    cache.clear()
    roles = []
    for role in current_user.roles:
        roles.append(role.name)
    print(roles)
    return {"roles": roles, "token": current_user.get_auth_token()}, 201

# creator dashboard
@api.route("/creator/dashboard")
@auth_required("token")
@roles_required("creator")
def creator_dashboard():
    creator = Creator.query.filter_by(user_id=current_user.id).first()
    if not creator:
        return jsonify({'error': 'Creator not found'}), 404
    albums = Album.query.filter_by(creator_id=creator.id).all()
    album_data = [{'id': album.id, 'name': album.title} for album in albums]
    songs = Song.query.filter_by(creator_id=creator.id).all()
    song_data = [{'id': song.id, 'name': song.name} for song in songs]
    total_songs = Song.query.filter_by(creator_id=creator.id).count()
    total_albums = Album.query.filter_by(creator_id=creator.id).count()
    data = {
        'id': creator.id,
        'name': creator.name,
        'bio': creator.bio,
        'albums': album_data,
        'songs': song_data,
        'email': current_user.email,
        'total_songs': total_songs,
        'total_albums': total_albums,
        'average_rating': creator_rating(creator.id),
        'flagged': creator.flagged
    }
    return jsonify(data), 200

# calculate creator rating
def creator_rating(creator_id):
    creator = Creator.query.filter_by(id=creator_id).first()
    ratings = [rating.rating for rating in creator.ratings]
    if ratings:
        average_rating = sum(ratings) / len(ratings)
    else:
        average_rating = 0
    return average_rating

# calculate song rating
def song_rating(song_id):
    song = Song.query.filter_by(id=song_id).first()
    ratings = [rating.rating for rating in song.ratings]
    if ratings:
        average_rating = sum(ratings) / len(ratings)
    else:
        average_rating = 0
    return average_rating

# calculate album rating
def album_rating(album_id):
    album = Album.query.filter_by(id=album_id).first()
    ratings = [rating.rating for rating in album.ratings]
    if ratings:
        average_rating = sum(ratings) / len(ratings)
    else:
        average_rating = 0
    return average_rating

# songs by creator
@api.route("/creator/songs")
@cache.cached(timeout=60)
@auth_required("token")
def creator_songs():
    creator = Creator.query.filter_by(user_id=current_user.id).first()
    songs = Song.query.filter_by(creator_id=creator.id).all()
    song_data = [{'id': song.id, 'name': song.name} for song in songs]
    return jsonify(song_data), 200

# edit creator details
@api.route('/edit_creator/<int:creator_id>', methods=['PUT'])
@auth_required("token")
@roles_required("creator")
def edit_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if 'name' in request.json:
        creator.name = request.json['name']
    if 'bio' in request.json:
        creator.bio = request.json['bio']
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Creator details updated successfully'}), 200

# SONG MANAGEMENT
# upload song
@api.route("/creator/uploadsong", methods=["POST"])
@auth_required("token")
@roles_required("creator")
def upload_song():
    user = current_user
    song_name = request.form.get("songName")
    artist_name = request.form.get("artistName")
    album_name = request.form.get("albumName")
    lyrics = request.form.get("lyrics")
    duration = request.form.get("duration")
    if 'songFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['songFile']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_url = "songs/" + filename
    creator = Creator.query.filter_by(user_id=current_user.id).first()
    if album_name:
        album = Album.query.filter_by(title=album_name).first()
        if not album:
            album = Album(title=album_name, creator_id=creator.id)
        db.session.add(album)
        db.session.commit()
        new_song = Song(name=song_name, artist=artist_name, lyrics=lyrics, album_id=album.id,creator_id=creator.id, duration=duration, song_file=file_url)
    else:
        new_song = Song(name=song_name, artist=artist_name, duration=duration,lyrics=lyrics, creator_id=creator.id, song_file=file_url)
    db.session.add(new_song)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Song uploaded successfully'}), 201

# list of all songs
@api.route("/song")
@cache.cached(timeout=60)
@auth_required("token")
def song():
    songs = Song.query.all()
    data = []
    for song in songs:
        song_data = {
            'id': song.id,
            'name': song.name,
            'rating': song_rating(song.id),
            "reports": song.report_count,
            'date_created': song.date_created.strftime('%B %d, %Y')
        }
        data.append(song_data)
    return jsonify(data), 200

# particular song page
@api.route("/song/<int:song_id>")
@cache.cached(timeout=60)
@auth_required("token")
def get_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    song_data = {
        'id': song.id,
        'name': song.name,
        'singer': song.artist,
        'lyrics': song.lyrics,
        'duration': song.duration,
        'song_url': song.song_file,
        'rating': song_rating(song.id),
        'date_created': song.date_created.strftime('%B %d, %Y')
    }
    return jsonify(song_data), 200

# song file
@api.route('/song/<int:song_id>/file', methods=['GET'])
@auth_required("token")
def get_song_file(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    file_path = './application/static/' + song.song_file
    if not file_path:
        return jsonify({"error": "Song file not found"}), 404
    return send_file(file_path)

# delete song
@api.route("/deletesong/<int:song_id>", methods=['DELETE'])
@auth_required("token")
def delete_song(song_id):
    song = Song.query.get(song_id)
    SongRating.query.filter_by(song_id=song.id).delete()
    if song:
        db.session.delete(song)
        db.session.commit()
        cache.clear()
        return jsonify({'message': 'Song deleted successfully'}), 200
    else:
        return jsonify({'error': 'Song not found'}), 404

# update/edit song
@api.route("/editsong/<int:song_id>", methods=['PUT'])
@auth_required("token")
@roles_required("creator")
def edit_song(song_id):
    song = Song.query.get(song_id)
    if 'name' in request.json:
        song.name = request.json['name']
    if 'singer' in request.json:
        song.artist = request.json['singer']
    if 'lyrics' in request.json:
        song.lyrics = request.json['lyrics']
    if 'duration' in request.json:
        song.duration = request.json['duration']
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Song updated successfully'}), 200

# report songs
@api.route("/report_song/<int:song_id>", methods=["POST"])
@roles_required('user')
@auth_required("token")
def report_song(song_id):
    song = Song.query.get(song_id)
    song.report_count = song.report_count + 1
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Song reported successfully'}), 200

# ALBUM MANAGEMENT
# create album
@api.route("/creator/create_album", methods=["POST"])
@roles_required('creator')
@auth_required("token")
def create_album():
    data = request.json
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    creator = Creator.query.filter_by(user_id=current_user.id).first()
    if not creator:
        return jsonify({'error': 'Creator not found for this user'}), 404
    album = Album(title=title, creator_id=creator.id)
    db.session.add(album)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Album created successfully', 'album_id': album.id}), 201

# list of all albums
@api.route("/albums")
@cache.cached(timeout=60)
@auth_required("token")
def album():
    albums = Album.query.all()
    data = [{'id': album.id, 'title': album.title,'rating': album_rating(album.id)} for album in albums]
    return jsonify(data), 200

# particular album details
@api.route("/album/<int:album_id>")
@cache.cached(timeout=60)
@auth_required("token")
def get_album(album_id):
    album = Album.query.get(album_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    data = {
        'id': album.id,
        'title': album.title,
        'release_date': album.release_date.strftime('%B %d, %Y'),
        'creator': album.creator.name,
        'songs': [{'id': song.id, 'name': song.name} for song in album.songs],
        'rating': album_rating(album.id)
    }
    return jsonify(data), 200

# delete album
@api.route('/deleteAlbum/<int:album_id>', methods=['DELETE'])
@auth_required("token")
def delete_album(album_id):
    album = Album.query.get(album_id)
    AlbumRating.query.filter_by(album_id=album.id).delete()
    if album:
        db.session.delete(album)
        db.session.commit()
        cache.clear()
        return jsonify({'message': 'Album deleted successfully'}), 200
    else:
        return jsonify({'error': 'Album not found'}), 404

# edit album
@api.route('/editalbum/<int:album_id>', methods=['PUT'])
@roles_required('creator')
@auth_required("token")
def edit_album(album_id):
    album = Album.query.get(album_id)
    if 'title' in request.json:
        album.title = request.json['title']
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Album updated successfully'}), 200

# add songs in album
@api.route('/album/<int:album_id>/add_songs', methods=['POST'])
@roles_required('creator')
@auth_required("token")
def add_songs_to_album(album_id):
    data = request.get_json()
    song_ids = data.get('song_ids', [])
    album = Album.query.get(album_id)
    if album is None:
        return jsonify({'error': 'Album not found'}), 404
    songs = Song.query.filter(Song.id.in_(song_ids)).all()
    for song in songs:
        album.songs.append(song)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Songs added to album successfully'}), 200

# remove songs from album
@api.route('/album/<int:album_id>/remove_song/<int:song_id>', methods=['DELETE'])
@roles_required('creator')
@auth_required("token")
def remove_song_from_album(album_id, song_id):
    album = Album.query.get(album_id)
    song = Song.query.get(song_id)
    if album is None or song is None:
        return jsonify({'error': 'Album or song not found'}), 404
    album.songs.remove(song)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Song removed from album successfully'}), 200

# PLAYLIST MANAGEMENT
# create playlist
@api.route("/createplaylist", methods=["POST"])
@roles_required('user')
@auth_required("token")
def create_playlist():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required for the playlist'}), 400
    playlist = Playlist(name=name, user_id=current_user.id)
    db.session.add(playlist)
    db.session.commit()
    result = Playlist.query.filter_by(
        name=name, user_id=current_user.id).first()
    data = {
        'id': result.id,
        'name': result.name,
        'user': result.user_id
    }
    return jsonify(data), 201

# display playlist details
@api.route("/playlist/<int:playlist_id>")
@auth_required("token")
def get_playlist_details(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    playlist_data = {
        'id': playlist.id,
        'name': playlist.name,
        'user_id': playlist.user_id,
        'songs': []
    }
    playlist_songs = PlaylistSong.query.filter_by(
        playlist_id=playlist_id).all()
    for playlist_song in playlist_songs:
        song = playlist_song.song
        if song:
            song_data = {
                'id': song.id,
                'name': song.name,
                'artist': song.artist,
                'lyrics': song.lyrics,
                'album_id': song.album_id
            }
            playlist_data['songs'].append(song_data)
    return jsonify(playlist_data), 200

# delete playlist
@api.route("/deleteplaylist/<int:playlist_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("user")
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this playlist'}), 403
    PlaylistSong.query.filter_by(playlist_id=playlist_id).delete()
    db.session.delete(playlist)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Playlist deleted successfully'}), 200

# add songs in playlist
@api.route("/playlist/<int:playlist_id>/add_songs", methods=["POST"])
@roles_required('user')
@auth_required("token")
def add_songs_to_playlist(playlist_id):
    data = request.json
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    song_ids = request.json.get('song_ids', [])
    for song_id in song_ids:
        if PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first():
            continue
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Songs added to the playlist successfully'}), 200

# remove songs from playlist
@api.route("/playlist/<int:playlist_id>/remove_song/<int:song_id>", methods=["DELETE"])
@roles_required('user')
@auth_required("token")
def remove_song_from_playlist(playlist_id, song_id):
    playlist = Playlist.query.get(playlist_id)
    song = Song.query.get(song_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    playlist_song = PlaylistSong.query.filter_by(
        playlist_id=playlist_id, song_id=song_id).first()
    if not playlist_song:
        return jsonify({'error': 'Song not in playlist'}), 400
    db.session.delete(playlist_song)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Song removed from playlist successfully'}), 200

# edit playlist
@api.route('/editplaylist/<int:playlist_id>', methods=['PUT'])
@roles_required('user')
@auth_required("token")
def edit_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if 'name' in request.json:
        playlist.name = request.json['name']
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'playlist updated successfully'}), 200

# list of all creators
@api.route("/creators")
@cache.cached(timeout=60)
@auth_required("token")
def creatordetail():
    creators = Creator.query.all()
    data = [{'id': creator.id, 'name': creator.name, 'flagged': creator.flagged,'rating': creator_rating(creator.id)} for creator in creators]
    return jsonify(data), 200

# creator page
@api.route("/creator/<int:creator_id>")
@cache.cached(timeout=60)
@auth_required("token")
def get_creator(creator_id):
    creator = Creator.query.get(creator_id)
    if not creator:
        return jsonify({'error': 'Creator not found'}), 404
    albums = Album.query.filter_by(creator_id=creator_id).all()
    songs = Song.query.filter_by(creator_id=creator_id).all()
    albums_data = [{'id': album.id, 'title': album.title,'release_date': album.release_date} for album in albums]
    song_data = [{'id': song.id, 'name': song.name,'artist': song.artist} for song in songs]
    data = {
        'id': creator.id,
        'name': creator.name,
        'bio': creator.bio,
        'albums': albums_data,
        'songs': song_data,
        'rating': creator_rating(creator.id)
    }
    return jsonify(data), 200

# rate the song
@api.route('/song/<int:song_id>/rate', methods=['POST'])
@roles_required('user')
@auth_required("token")
def rate_song(song_id):
    rating_value = request.json.get('rating')
    if rating_value is None:
        return jsonify({'error': 'Rating value is required'}), 400
    if not 1 <= rating_value <= 5:
        return jsonify({'error': 'Invalid rating value'}), 400
    song_rating = SongRating(user_id=current_user.id,song_id=song_id, rating=rating_value)
    db.session.add(song_rating)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Rating submitted successfully'}), 200

# creator rate
@api.route('/creator/<int:creator_id>/rate', methods=['POST'])
@roles_required('user')
@auth_required("token")
def rate_creator(creator_id):
    rating_value = request.json.get('rating')
    if rating_value is None:
        return jsonify({'error': 'Rating value is required'}), 400
    if not 1 <= rating_value <= 5:
        return jsonify({'error': 'Invalid rating value'}), 400
    creator_rating = CreatorRating(
        user_id=current_user.id, creator_id=creator_id, rating=rating_value)
    db.session.add(creator_rating)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Rating submitted successfully'}), 200

# rate the album
@api.route('/album/<int:album_id>/rate', methods=['POST'])
@roles_required('user')
@auth_required("token")
def rate_album(album_id):
    rating_value = request.json.get('rating')
    if rating_value is None:
        return jsonify({'error': 'Rating value is required'}), 400
    if not 1 <= rating_value <= 5:
        return jsonify({'error': 'Invalid rating value'}), 400
    album_rating = AlbumRating(
        user_id=current_user.id, album_id=album_id, rating=rating_value)
    db.session.add(album_rating)
    db.session.commit()
    cache.clear()
    return jsonify({'message': 'Rating submitted successfully'}), 200

# search functionality
@api.route('/search', methods=['GET'])
@auth_required("token")
def search():
    query = request.args.get('query')

    songs = Song.query.join(Creator).filter(or_(
        Song.name.ilike(f'%{query}%'),
        Song.artist.ilike(f'%{query}%'),
        Creator.name.ilike(f'%{query}%')))
    
    albums = Album.query.join(Creator).filter(or_(
            Album.title.ilike(f'%{query}%'),
            Creator.name.ilike(f'%{query}%'))).all()
    
    creators = Creator.query.filter(Creator.name.ilike(f'%{query}%')).all()

    search_results = {'songs': [{'id': song.id, 'name': song.name} for song in songs],
        'albums': [{'id': album.id, 'name': album.title} for album in albums],
        'creators': [{'id': creator.id, 'name': creator.name} for creator in creators]}
    return jsonify(search_results)