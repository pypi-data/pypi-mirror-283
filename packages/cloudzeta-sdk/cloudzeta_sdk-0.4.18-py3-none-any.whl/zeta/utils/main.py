from flask import Flask, jsonify, request
from google.cloud import pubsub
from pxr import Usd

import base64
import json
import logging

from zeta.folder import Folder
from zeta.session import Session
from zeta.routes.asset import asset_blueprint
from zeta.routes.auth import auth_blueprint
from zeta.routes.scene import scene_blueprint
from zeta.routes.vivago import VivagoProxy

app = Flask(__name__)

vivago_proxy = VivagoProxy()
app.register_blueprint(asset_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(scene_blueprint)
app.register_blueprint(vivago_proxy.blueprint)

publisher = pubsub.PublisherClient()
beta_convert_topic_path = publisher.topic_path("gozeta-beta", "zeta-beta-usd-convert")
prod_convert_topic_path = publisher.topic_path("gozeta-prod", "zeta-prod-usd-convert")
beta_export_topic_path = publisher.topic_path("gozeta-beta", "zeta-beta-usd-export")
prod_export_topic_path = publisher.topic_path("gozeta-prod", "zeta-prod-usd-export")

@app.route("/api/versions")
def user_version() -> str:
    version_info = Usd.GetVersion()

    return jsonify({
        "usd_version": version_info,
    })

def parse_data_from_request(envelope: dict) -> dict:
    if not envelope:
        msg = "no Pub/Sub message received"
        logging.error(f"error: {msg}")
        return None

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        logging.error(f"error: {msg}")
        return None

    message = envelope["message"]
    if isinstance(message, dict) and "data" in message:
        return json.loads(base64.b64decode(message["data"]).decode("utf-8").strip())
    elif isinstance(message, dict) and "session" in message:
        return message
    else:
        return None

@app.route("/api/usd/export")
def usd_export() -> str:
    session_uid: str = request.args.get("session")
    payload: str = json.dumps({"session": session_uid}).encode("utf-8")

    if request.host == "beta.gozeta.io":
        publisher.publish(beta_export_topic_path, payload)
    elif request.host == "cloudzeta.com":
        publisher.publish(prod_export_topic_path, payload)
    else:
        return do_process_export(session_uid)

    return jsonify({
        "message": "success",
    })

@app.route("/api/usd/process-export", methods=["POST"])
def usd_process_export():
    envelope = request.get_json()
    data = parse_data_from_request(envelope)

    if data is None:
        return f"Bad Request: invalid request", 400

    session_uid: str = data.get("session")
    if session_uid is None:
        return f"Bad Request: invalid session", 400

    return do_process_export(session_uid)

def do_process_export(session_uid: str):
    session: Session = Session(session_uid)

    try:
        # TODO(CZ-346): Implement session export logic
        session.process_export()
    except Exception as e:
        return f"Exception occurred: {e}", 400

    return "", 204

@app.route("/api/usd/export-failure", methods=["POST"])
def usd_export_failure():
    logging.error(f"export failure: {request.get_json()}")

    return "", 204

@app.route("/api/folder/share", methods=["GET"])
def folder_share():
    folder_uid: str = request.args.get("folder")

    if not folder_uid:
        return f"Bad Request: invalid folder", 400

    folder: Folder = Folder(folder_uid)
    if not folder.exists():
        return f"Folder does not exist: {folder_uid}", 404

    if not folder.propagate_share_policy():
        return f"Failed to propagate share policy: {folder_uid}", 500

    return "OK", 200

@app.route("/api/usd/convert")
def usd_convert() -> str:
    session_uid: str = request.args.get("session")
    payload: str = json.dumps({"session": session_uid}).encode("utf-8")

    if request.host == "beta.gozeta.io":
        publisher.publish(beta_convert_topic_path, payload)
    elif request.host == "cloudzeta.com":
        publisher.publish(prod_convert_topic_path, payload)
    else:
        return do_process_convert(session_uid)

    return jsonify({
        "message": "success",
    })

@app.route("/api/usd/process-convert", methods=["POST"])
def usd_process_convert():
    envelope = request.get_json()
    data = parse_data_from_request(envelope)

    if data is None:
        return f"Bad Request: invalid request", 400

    session_uid: str = data.get("session")
    if session_uid is None:
        return f"Bad Request: invalid session", 400

    return do_process_convert(session_uid)

def do_process_convert(session_uid: str):
    session: Session = Session(session_uid)

    if session.update_state("init", "processing"):
        try:
            session.process_convert()
            session.update_state("processing", "ready")
        except Exception as e:
            session.update_state("processing", "init")
            session.update_error(str(e))
            logging.exception(f"Exception occurred: {e}")
            return f"Exception occurred: {e}", 400
    else:
        return f"Invalid session: {session_uid}", 400

    return "", 204

@app.route("/api/usd/convert-failure", methods=["POST"])
def usd_convert_failure():
    envelope = request.get_json()
    data = parse_data_from_request(envelope)

    logging.error(f"convert failure: {data}")

    try:
        session_uid: str = data.get("session")
        session: Session = Session(session_uid)
        session.update_state("init", "error")
    except Exception as e:
        logging.error(f"Exception occurred when marking error, data={data}, error={e}")

    return "", 204


if __name__ == "__main__":
    while True:
        try:
            app.run(debug=True, host="0.0.0.0", port=8081)
        except Exception as e:
            logging.error(f"Exception occurred: {e}. Restarting...")
