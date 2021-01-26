import urllib.parse
from json import dumps

import requests
from django.conf import settings

BASE_URL = settings.CISCO_WEBEX_BASE_URL
HEADERS = {
    "Content-type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + settings.CISCO_WEBEX_ACCESS_TOKEN,
}


def add_user_to_wt_room(room_id, email, isModerator="null"):
    ENDPOINT = "memberships/"
    URL = urllib.parse.urljoin(BASE_URL, ENDPOINT)
    PAYLOAD = {"roomId": room_id, "personEmail": email, "isModerator": isModerator}
    user = requests.post(URL, headers=HEADERS, data=dumps(PAYLOAD))
    if user.status_code == 200:
        return True
    return False


def get_membership_info_from_wt_room(room_id=None, email=None):
    ENDPOINT = "memberships/"
    URL = urllib.parse.urljoin(BASE_URL, ENDPOINT)
    PAYLOAD = {"roomId": room_id, "personEmail": email}

    membershipId = requests.get(URL, headers=HEADERS, params=PAYLOAD)
    if membershipId.status_code == 200 and len(membershipId.json()["items"]) == 1:
        return membershipId.json()["items"][0]["id"]
    return False


def remove_user_from_wt_room(room_id=None, email=None):
    membershipId = get_membership_info_from_wt_room(room_id=room_id, email=email)
    if membershipId:
        ENDPOINT = "memberships/{membershipid}/".format(membershipid=membershipId)
        URL = urllib.parse.urljoin(BASE_URL, ENDPOINT)
        result = requests.delete(URL, headers=HEADERS)
        if result.status_code == 200:
            return True
        return False
    return False
