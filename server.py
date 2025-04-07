from flask import Flask, jsonify, request, Response
from flask.views import MethodView

from errors import HttpError
from models import Announcement, Session, User

app = Flask("app")
app.config["JSON_AS_ASCII"] = False

@app.before_request
def before_request():
    request.session = Session()

@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_resonse = jsonify({"error:": err.message})
    http_resonse.status_code = err.status_code
    return http_resonse

def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if not user:
        raise HttpError(404, "User not found")
    return user

def get_announcement_by_id(announcement_id: int):
    announcement = request.session.get(Announcement, announcement_id)
    if not announcement:
        raise HttpError(404, "Announcement not found")
    return announcement

class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.id_dict)

    def post(self):
        json_data = request.json
        user = User(**json_data)
        request.session.add(user)
        request.session.commit()
        return jsonify({"id": user.id, "username": user.username})

class AnnouncementView(MethodView):
    def get(self, announcement_id: int):
        announcement = get_announcement_by_id(announcement_id)
        return jsonify(announcement.id_dict,
                       announcement.title,
                       announcement.description,
                       announcement.created_at,
                       announcement.owner,
                       )

    def post(self):
        json_data = request.json
        owner_id = json_data.get("owner")

        user = request.session.get(User, owner_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"})

        announcement = Announcement(**json_data)
        request.session.add(announcement)
        request.session.commit()
        return jsonify(announcement.id_dict)

    def delete(self, announcement_id: int):
        announcement = get_announcement_by_id(announcement_id)
        if not announcement:
            return jsonify({"status": "error", "message": "Announcement not found"})
        request.session.delete(announcement)
        request.session.commit()
        return jsonify({"status": "success"})

    def patch(self, announcement_id: int):
        announcement = get_announcement_by_id(announcement_id)
        if not announcement:
            return jsonify({"status": "error", "message": "Announcement not found"})
        json_data = request.json
        if "title" in json_data:
            announcement.title = json_data["title"]
        if "description" in json_data:
            announcement.description = json_data["description"]
        request.session.add(announcement)
        request.session.commit()
        return jsonify(announcement.title,
                       announcement.description,
                       announcement.created_at,
                       announcement.owner
                       )

user_view = UserView.as_view("user_view")
announcement_view = AnnouncementView.as_view("announcement_view")

app.add_url_rule("/api/v1/user", view_func=user_view, methods=["POST"])
app.add_url_rule("/api/v1/user/<int:user_id>", view_func=user_view, methods=["GET"])

app.add_url_rule("/api/v1/announcement", view_func=announcement_view, methods=["POST"])
app.add_url_rule("/api/v1/announcement/<int:announcement_id>",
                 view_func=announcement_view,
                 methods=["GET", "DELETE", "PATCH"]
)

app.run()
