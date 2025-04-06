from flask import Flask, jsonify


app = Flask("app")

def start():

    http_response = jsonify({"hi": "i'm here"})
    http_response.status_code = 201
    return http_response

app.add_url_rule("/1", view_func=start)

app.run()