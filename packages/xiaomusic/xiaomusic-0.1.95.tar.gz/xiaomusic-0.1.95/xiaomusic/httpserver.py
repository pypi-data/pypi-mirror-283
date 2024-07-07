#!/usr/bin/env python3
import os
from dataclasses import asdict
from threading import Thread

from flask import Flask, request, send_file, send_from_directory
from flask_httpauth import HTTPBasicAuth
from waitress import serve

from xiaomusic import (
    __version__,
)
from xiaomusic.utils import (
    deepcopy_data_no_sensitive_info,
    downloadfile,
)

app = Flask(__name__)
auth = HTTPBasicAuth()

host = "0.0.0.0"
port = 8090
static_path = "music"
xiaomusic = None
log = None


@auth.verify_password
def verify_password(username, password):
    if xiaomusic.config.disable_httpauth:
        return True

    if (
        xiaomusic.config.httpauth_username == username
        and xiaomusic.config.httpauth_password == password
    ):
        return username


@app.route("/allcmds")
@auth.login_required
def allcmds():
    return xiaomusic.config.key_word_dict


@app.route("/getversion", methods=["GET"])
def getversion():
    log.debug("getversion %s", __version__)
    return {
        "version": __version__,
    }


@app.route("/getvolume", methods=["GET"])
@auth.login_required
def getvolume():
    volume = xiaomusic.get_volume_ret()
    return {
        "volume": volume,
    }


@app.route("/searchmusic", methods=["GET"])
@auth.login_required
def searchmusic():
    name = request.args.get("name")
    return xiaomusic.searchmusic(name)


@app.route("/playingmusic", methods=["GET"])
@auth.login_required
def playingmusic():
    return xiaomusic.playingmusic()


@app.route("/isplaying", methods=["GET"])
@auth.login_required
def isplaying():
    return xiaomusic.isplaying()


@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static", "index.html")


@app.route("/cmd", methods=["POST"])
@auth.login_required
async def do_cmd():
    data = request.get_json()
    cmd = data.get("cmd")
    if len(cmd) > 0:
        log.debug("docmd. cmd:%s", cmd)
        xiaomusic.set_last_record(cmd)
        return {"ret": "OK"}
    return {"ret": "Unknow cmd"}


@app.route("/getsetting", methods=["GET"])
@auth.login_required
async def getsetting():
    config = xiaomusic.getconfig()
    data = asdict(config)
    alldevices = await xiaomusic.call_main_thread_function(xiaomusic.getalldevices)
    log.info(f"getsetting alldevices: {alldevices}")
    data["mi_did_list"] = alldevices["did_list"]
    data["mi_hardware_list"] = alldevices["hardware_list"]
    return data


@app.route("/savesetting", methods=["POST"])
@auth.login_required
async def savesetting():
    data = request.get_json()
    debug_data = deepcopy_data_no_sensitive_info(data)
    log.info(f"saveconfig: {debug_data}")
    await xiaomusic.saveconfig(data)
    return "save success"


@app.route("/musiclist", methods=["GET"])
@auth.login_required
async def musiclist():
    return xiaomusic.get_music_list()


@app.route("/curplaylist", methods=["GET"])
@auth.login_required
async def curplaylist():
    return xiaomusic.get_cur_play_list()


@app.route("/delmusic", methods=["POST"])
@auth.login_required
def delmusic():
    data = request.get_json()
    log.info(data)
    xiaomusic.del_music(data["name"])
    return "success"


@app.route("/downloadjson", methods=["POST"])
@auth.login_required
def downloadjson():
    data = request.get_json()
    log.info(data)
    url = data["url"]
    try:
        ret = "OK"
        content = downloadfile(url)
    except Exception as e:
        log.warning(f"downloadjson failed. url:{url} e:{e}")
        ret = "Download JSON file failed."
    return {
        "ret": ret,
        "content": content,
    }


@app.route("/downloadlog", methods=["GET"])
@auth.login_required
def downloadlog():
    return send_file(xiaomusic.config.log_file, as_attachment=True)


@app.route("/playurl", methods=["GET"])
@auth.login_required
async def playurl():
    url = request.args.get("url")
    log.info(f"play_url:{url}")
    return await xiaomusic.call_main_thread_function(xiaomusic.play_url, arg1=url)


@app.route("/debug_play_by_music_url", methods=["POST"])
@auth.login_required
async def debug_play_by_music_url():
    data = request.get_json()
    log.info(f"data:{data}")
    return await xiaomusic.call_main_thread_function(
        xiaomusic.debug_play_by_music_url, arg1=data
    )


def static_path_handler(filename):
    log.debug(filename)
    log.debug(static_path)
    absolute_path = os.path.abspath(static_path)
    log.debug(absolute_path)
    return send_from_directory(absolute_path, filename)


def run_app():
    serve(app, host=host, port=port)


def StartHTTPServer(_port, _static_path, _xiaomusic):
    global port, static_path, xiaomusic, log
    port = _port
    static_path = _static_path
    xiaomusic = _xiaomusic
    log = xiaomusic.log

    app.add_url_rule(
        f"/{static_path}/<path:filename>", "static_path_handler", static_path_handler
    )

    server_thread = Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()
    xiaomusic.log.info(f"Serving on {host}:{port}")
