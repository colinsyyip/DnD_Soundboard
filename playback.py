import json
import os
from pygame import mixer
from time import sleep
import youtube_dl


class Soundboard:
    """
    Class handling sound bite download and playback. Dependent on a mapping config file of soundbite name to YT video link
    """
    def __init__(self,
                 soundbite_directory: str = "sound_files",
                 config_file: str = "soundbite_map.json",
                 **kwargs):
        self.soundbite_directory = soundbite_directory
        self.config_file = config_file
        self.soundbite_check(**kwargs)
        mixer.init()


    def soundbite_check(self):
        """
        Check that all listed soundbites in soundboard_map.json exist
        """
        self.load_configs()
        if not os.path.exists(self.soundbite_directory):
            os.mkdir(self.soundbite_directory)
        for sb_name, sb_map in self.soundbite_configs.items():
            file_path = "%s/%s.mp3" % (self.soundbite_directory, sb_name)
            if os.path.exists(file_path):
                print("%s sound file exists" % sb_name)
                continue
            self.soundbite_download(soundbite_name = sb_name,
                                    soundbite_info = sb_map)
        
        return None


    def soundbite_download(self,
                           soundbite_name: str,
                           soundbite_info: dict):
        """
        Download file from YT
        """
        sb_url = soundbite_info['url']
        sb_file_name = "%s/%s" % (self.soundbite_directory, soundbite_name)

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': sb_file_name + ".%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sb_url])

        return None


    def soundbite_playback(self,
                           soundbite_name: str):
        """
        Search for the soundbite name within the known soundbite directory and play
        """
        soundbite_file_path = "%s/%s.mp3" % (self.soundbite_directory, soundbite_name)
        soundbite_conf = self.soundbite_configs[soundbite_name]
        playback_start = soundbite_conf['ts']
        playback_length = soundbite_conf['clip_duration']
        playback_volume = soundbite_conf['volume']

        mixer.music.load(soundbite_file_path, "mp3")
        mixer.music.set_volume(playback_volume)
        mixer.music.play(start = playback_start)
        sleep(playback_length)
        mixer.music.stop()

        return None
    

    def load_configs(self):
        """
        Loads config dict from Soundboard's config_file param
        """
        with open(self.config_file, 'r') as f:
            raw_conf_file = f.read()
            f.close()
        config_map = json.loads(raw_conf_file)
        self.soundbite_configs = config_map

        return config_map
        