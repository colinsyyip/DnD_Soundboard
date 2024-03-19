# Soundboard for DnD

This is more or ~~less~~ (very much so) a meme project.

![alt text](banner.png)

### Overview
Short project for setting up a soundboard to make playing meme soundbites easier during Dnd. Run the webserver from `soundboard_ui.py` to get it up and running.

Config page facilitates adding/editing/deleting of soundbites, but the underlying basic format for raw adding new files is as follows:
```
"id_string": 
    {"url": "yt_link", 
    "ts": 10.0, 
    "clip_duration": 5.0, 
    "name": "ID String", 
    "volume": 0.8}
```
YT shorts not supported. When using the config UI, `id_string` will be taken from `name`. Changing the Name field will not change the `id_string`.

### To Do (Potentially):
- Move from a `json` file to store configs to a more robust (primarily atomic) storage solution
- Have dead soundbite `mp3` files deleted on `load_configs` to avoid excess storage usage
