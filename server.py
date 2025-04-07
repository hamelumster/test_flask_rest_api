from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Announcement, Session

app = Flask("app")

class AnnouncementView(MethodView):
    def get(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            return jsonify(announcement.id_dict)
    def post(self, announcement_id: int):
        json_data = request.json
        with Session() as session:
            announcement = Announcement(**json_data)
            session.add(announcement)
            session.commit()
            return jsonify(announcement.id_dict)
    def delete(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            session.delete(announcement)
            session.commit()
            return jsonify({"status": "success"})
    def patch(self, announcement_id: int):
        with Session() as session:
            announcement = session.get(Announcement, announcement_id)
            json_data = request.json
            if "title" in json_data:
                announcement.title = json_data["title"]
            if "description" in json_data:
                announcement.description = json_data["description"]
            session.add(announcement)
            session.commit()
            return jsonify(announcement.id_dict)

announcement_view = AnnouncementView.as_view("announcement_view")
app.add_url_rule("/api/v1/announcement", view_func=announcement_view, methods=["POST"])
app.add_url_rule("/api/v1/announcement/<int:announcement_id>",
                 view_func=announcement_view,
                 methods=["GET", "DELETE", "PATCH"]
)

app.run()