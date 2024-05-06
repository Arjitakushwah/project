from celery import Celery, shared_task
import requests
from flask import render_template 
from .models import User,Creator,Song,Album
from .mail_service import send_message
from .views import creator_rating, song_rating, album_rating
from datetime import datetime, timezone

# daily remainder
@shared_task(ignore_result=False)
def reminder(): 
    users = User.query.all()
    for user in users:
        last_login = user.last_login_at
        if last_login is None or last_login.date() < datetime.utcnow().date():
            html_content = daily_reminder(user)
            send_message(user.email, 'Daily Reminder',html_content)
    return 'OK'
    # requests.post("https://chat.googleapis.com/v1/spaces/AAAAThxqmYk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Lr838vtZDZrv4-_Quvk3sXLskf2EII123HfkPZKVHv4",json={"text": "visit the app and explore music"})

def daily_reminder(user):
    template_path = 'reminder.html'
    return render_template(template_path, user=user)

# generate monthly report
@shared_task(ignore_result=True)
def send_mail():
    creators = Creator.query.all()
    for creator in creators:
        html_content = generate_report(creator)
        send_message(creator.user.email, 'Monthly Activity Report',html_content)
    return 'OK'

def generate_report(creator):
    template_path = 'report.html'
    creator_id = creator.id
    total_songs = Song.query.filter_by(creator_id=creator_id).count()
    total_albums = Album.query.filter_by(creator_id=creator_id).count()
    average_rating = creator_rating(creator.id)
    return render_template(template_path, creator=creator, total_songs=total_songs,total_albums=total_albums, rating=average_rating, song_rating=song_rating, album_rating=album_rating)




