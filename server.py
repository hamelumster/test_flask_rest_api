from flask import Flask, jsonify
from flask.views import MethodView

app = Flask("app")

class AnnouncementView(MethodView):
    def get(self, announcement_id: int):
        pass
    def post(self, announcement_id: int):
        pass
    def delete(self, announcement_id: int):
        pass
    def patch(self, announcement_id: int):
        pass

announcement_view = AnnouncementView.as_view("announcement_view")
app.add_url_rule("api/v1/announcement", view_func=announcement_view, methods=["POST"])
app.add_url_rule("api/v1/announcement/<int:announcement_id>",
                 view_func=announcement_view,
                 methods=["GET", "DELETE", "PATCH"]
)

app.run()