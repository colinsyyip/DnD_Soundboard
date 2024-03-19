from flask import Flask, render_template, request, redirect
import json
from playback import Soundboard


app = Flask(__name__)
app.soundboard = Soundboard()


def get_config_json(config_map_file_path: str = "soundbite_map.json"):
    """
    Wrapper for opening and reading config JSON. 

    TBD: Should replace with something more atomic if soundbite file gets large
    """
    with open(config_map_file_path, "r") as f:
        config_file = f.read()
        f.close()
    config_dict = json.loads(config_file)
    return config_dict


def write_config_json(config_dict: dict,
                      config_map_file_path: str = "soundbite_map.json",):
    """
    Wrapper for opening and writing to config JSON. 

    TBD: Should replace with something more atomic if soundbite file gets large
    """
    with open(config_map_file_path, "w") as f:
        f.write(json.dumps(config_dict))
        f.close()
    return None


def generate_sb_dict(form_data,
                     key_append: str = ""):
    """
    Nicer utility for converting forms in the config page to the required dict format for the config file.
    """
    video_url = form_data.get("vid_url%s" % key_append)
    sb_name = form_data.get("sb_name%s" % key_append)
    video_ts = form_data.get("vid_ts%s" % key_append)
    sb_length = form_data.get("sb_length%s" % key_append)
    sb_volume = form_data.get("sb_volume%s" % key_append)

    new_conf_dict = {
        "url": video_url,
        "ts": float(video_ts),
        "clip_duration": float(sb_length),
        "name": sb_name,
        "volume": float(sb_volume)
    }

    return new_conf_dict


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
    curr_soundbites = app.soundboard.soundbite_configs
    curr_soundbite_tuples = [(v['name'], k) for k, v in curr_soundbites.items()]
    return render_template("sb_configs.html",
                           sb_tuples = curr_soundbite_tuples)


@app.route("/push_config", methods=["POST"])
def push_config():
    form_data = request.form
    sb_name = form_data.get("sb_name")
    new_conf_dict = generate_sb_dict(form_data)
    new_sb_id = sb_name.lower().replace(" ", "_")

    config_dict = get_config_json()
    config_dict[new_sb_id] = new_conf_dict
    write_config_json(config_dict)
    app.soundboard.soundbite_download(soundbite_name = new_sb_id,
                                      soundbite_info = new_conf_dict)
    app.soundboard.load_configs()
    return redirect('configs')


@app.route("/edit_sb", methods=["POST"])
def edit_sb():
    form_data = request.form
    edit_form_sb = form_data.get('sb_to_edit')
    config_dict = get_config_json()
    orig_url = config_dict[edit_form_sb]['url']

    new_conf_dict = generate_sb_dict(form_data,
                                     key_append = "_edit")
    config_dict[edit_form_sb] = new_conf_dict
    write_config_json(config_dict)
    if orig_url != new_conf_dict['url']:
        app.soundboard.soundbite_download(soundbite_name = edit_form_sb,
                                          soundbite_info = new_conf_dict)
    app.soundboard.load_configs()
    return redirect('configs')


@app.route("/del_sb", methods=["POST"])
def del_sb():
    del_form_data = request.form
    del_form_sb = del_form_data.get('sb_to_delete')
    config_dict = config_dict = get_config_json()
    config_dict.pop(del_form_sb)
    write_config_json(config_dict)
    app.soundboard.load_configs()
    return redirect("configs")


@app.route("/get_sb_details", methods=["POST"])
def get_sb_details():
    request_keys = list(request.form.keys())
    sb_name = request_keys[0]
    return app.soundboard.soundbite_configs[sb_name]


@app.route("/play_sound", methods=["GET"])
def play_sound():
   tile_name = request.args.get('tile_name')
   print("Playing sound for %s" % tile_name)
   app.soundboard.soundbite_playback(tile_name)
   return {"status": 200}


if __name__ == "__main__":
    app.run(port=8080, debug = True)