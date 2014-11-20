#!/usr/bin/python
# JSON preset importer

import json
from mconverter import config
from pprint import pprint
from os.path import isfile,join

def importPreset(preset_name):
    presetPath = join(config.mc_preset_path,preset_name)

    print("Preset path is :" ,presetPath)
    if isfile(presetPath):
        #with open(presetPath,"r") as presetFile:
        #data = presetFile.read()

        json_file=open(presetPath)
        json_data = json.load(json_file)
        json_file.close()

        print(json_data["preset"][0]["format"])
        print(json_data["preset"][0]["video"][0]["codec"])
        print(json_data["preset"][0]["video"][0]["width"])
        print(json_data["preset"][0]["video"][0]["height"])
        print(json_data["preset"][0]["video"][0]["fps"])
        print(json_data["preset"][0]["audio"][0]["codec"])
        print(json_data["preset"][0]["audio"][0]["samplerate"])
        print(json_data["preset"][0]["audio"][0]["channels"])

        au_codec = json_data["preset"][0]["audio"][0]["codec"]
        au_samplerate = json_data["preset"][0]["audio"][0]["samplerate"]
        au_channels = int(json_data["preset"][0]["audio"][0]["channels"])
        vi_width = int(json_data["preset"][0]["video"][0]["width"])
        vi_height = int(json_data["preset"][0]["video"][0]["height"])
        vi_fps = int(json_data["preset"][0]["video"][0]["fps"])

        # Set a config
        preset ={
            'format': json_data["preset"][0]["format"],
            'audio': {
                'codec': au_codec,
                'samplerate': au_samplerate,
                'channels': au_channels
            },
            'video': {
                'codec': 'h264',
                'width': vi_width,
                'height': vi_height,
                'fps': vi_fps
            }
        }

        return preset

    else:
        print("Preset doesn't exists. Please check preset name")

def print_preset_configuration(preset):
    print(json_data["preset"][0]["format"])
    print(json_data["preset"][0]["video"][0]["codec"])
    print(json_data["preset"][0]["video"][0]["width"])
    print(json_data["preset"][0]["video"][0]["height"])
    print(json_data["preset"][0]["video"][0]["fps"])
    print(json_data["preset"][0]["audio"][0]["codec"])
    print(json_data["preset"][0]["audio"][0]["samplerate"])
    print(json_data["preset"][0]["audio"][0]["channels"])
