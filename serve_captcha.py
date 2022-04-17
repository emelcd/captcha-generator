from curses.ascii import alt
from flask import Flask, send_file, request, make_response
from flask_cors import CORS
from captcha_generator import main_generator
import json
import pymongo
import shutil

connect = pymongo.MongoClient("localhost", 27017)
db = connect.captcha
collection = db.captcha


app = Flask(__name__)
CORS(app)



@app.route("/", methods=["GET"])
def index():
    text, name_file = main_generator()
    uuid_file = name_file.split("/")[-1].split(".")[0]
    collection.insert_one({"uuid": uuid_file, "text": text})
    return {"uuid": uuid_file}


@app.route("/", methods=["POST"])
def check():
    data = json.loads(request.data)
    uuid_file = data["uuid"]
    text = data["text"]
    if collection.find_one({"uuid": uuid_file, "text": text}):
        # shutil.rmtree(f'file/{uuid_file}.png')
        return json.dumps({"result": True})
    else:
        return json.dumps({"result": False})


@app.route("/<uuid>", methods=["GET"])
def get_image(uuid):
    return send_file(f"file/{uuid}.png")


if __name__ == "__main__":
    app.run()
