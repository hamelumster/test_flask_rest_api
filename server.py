from flask import Flask, jsonify
from flask.views import MethodView

app = Flask("app")

class AnnouncementView(MethodView):
    def get(self):
        pass
    def post(self):
        pass
    def delete(self):
        pass
    def patch(self):
        pass

app.run()