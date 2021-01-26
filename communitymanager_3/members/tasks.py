from communitymanager_3.members.intergrations import (
    add_user_to_wt_room,
    remove_user_from_wt_room,
)
from config.celery_app import app


@app.task
def add_to_wt_room(email, room_id):
    if add_user_to_wt_room(email=email, room_id=room_id):
        return True
    return False


@app.task
def remove_from_wt_room(email, room_id):
    if remove_user_from_wt_room(email=email, room_id=room_id):
        return True
    return False
