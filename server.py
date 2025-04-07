from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Announcement, Session, User

app = Flask("app")
app.config["JSON_AS_ASCII"] = False

class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = session.get(User, user_id)
            return jsonify(user.id_dict)

    def post(self):
        json_data = request.json
        with Session() as session:
            user = User(**json_data)
            session.add(user)
            session.commit()
            return jsonify({"id": user.id, "username": user.username})

class AnnouncementView(MethodView):
    def get(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            return jsonify(announcement.id_dict,
                           announcement.title,
                           announcement.description,
                           announcement.created_at,
                           announcement.owner,
                           )

    def post(self):
        json_data = request.json
        with Session() as session:
            owner_id = json_data["owner"]
            user = session.get(User, owner_id)
            if not User:
                return jsonify({"status": "error", "message": "User not found"})

            announcement = Announcement(**json_data)
            session.add(announcement)
            session.commit()
            return jsonify(announcement.id_dict)

    def delete(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                return jsonify({"status": "error", "message": "Announcement not found"})
            session.delete(announcement)
            session.commit()
            return jsonify({"status": "success"})

    def patch(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                return jsonify({"status": "error", "message": "Announcement not found"})
            json_data = request.json
            if "title" in json_data:
                announcement.title = json_data["title"]
            if "description" in json_data:
                announcement.description = json_data["description"]
            session.add(announcement)
            session.commit()
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