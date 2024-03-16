from flask import Flask, render_template, request
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


@app.route("/play_sound", methods=["GET"])
def play_sound():
   tile_name = request.args.get('tile_name')
   print("Playing sound for %s" % tile_name)
   app.soundboard.soundbite_playback(tile_name)
   return {"status": 200}


if __name__ == "__main__":
    app.run(port=8080, debug = True)