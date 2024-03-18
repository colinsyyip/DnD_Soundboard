from flask import Flask, render_template, request
import json
from playback import Soundboard


app = Flask(__name__)
app.soundboard = Soundboard()


@app.route("/")
def soundboard_ui():
    sb_data = app.soundboard.soundbite_configs
    sb_names = [v['name'] for _, v in sb_data.items()]
    sb_id = list(sb_data)
    sb_tiles = [(x, y) for x, y in zip(sb_id, sb_names)]
    n_item_row = 4
    sublisted_sb_tiles = [sb_tiles[x:x+n_item_row] for x in range(0, len(sb_tiles), n_item_row)]
    return render_template("sb_ui.html",
                           tiles = sublisted_sb_tiles)


@app.route("/configs")
def soundboard_configs():
    return render_template("sb_configs.html")


@app.route("/push_config", methods=["POST"])
def push_config():
    form_data = request.form
    video_url = form_data.get("vid_url")
    sb_name = form_data.get("sb_name")
    video_ts = form_data.get("vid_ts")
    sb_length = form_data.get("sb_length")
    sb_volume = form_data.get("sb_volume")

    new_conf_dict = {
        "url": video_url,
        "ts": float(video_ts),
        "clip_duration": float(sb_length),
        "name": sb_name,
        "volume": float(sb_volume)
    }
    new_sb_id = sb_name.lower().replace(" ", "_")

    config_map_file_path = "soundbite_map.json"
    with open(config_map_file_path, "r") as f:
        config_file = f.read()
        f.close()
    config_dict = json.loads(config_file)
    config_dict[new_sb_id] = new_conf_dict
    with open(config_map_file_path, "w") as f:
        f.write(json.dumps(config_dict))
        f.close()
    app.soundboard.soundbite_download(soundbite_name = new_sb_id,
                                      soundbite_info = new_conf_dict)
    app.soundboard.load_configs()
    return render_template("sb_configs.html")


@app.route("/play_sound", methods=["GET"])
def play_sound():
   tile_name = request.args.get('tile_name')
   print("Playing sound for %s" % tile_name)
   app.soundboard.soundbite_playback(tile_name)
   return {"status": 200}


if __name__ == "__main__":
    app.run(port=8080, debug = True)