# All movie-converter properties are prefixed 'mc-'

# Folders
mc_folder_in  = "/home/samsung/Videos/input"
mc_folder_out = "/home/samsung/Videos/output"
mc_folder_conv= "/home/samsung/Videos/converted"

# Database path
mc_db_path = "./db/movieconverter.db"

# FFMpeg location
mc_ffmpeg_path = "/location/to/FFMpeg"


# Video & Audio Presets

mc_video_audio_preset ={
            'format': 'mp4',
            'audio': {
                'codec': 'aac',
                'samplerate': 44100,
                'channels': 2
            },
            'video': {
                'codec': 'h264',
                'width': 720,
                'height': 400,
                'fps': 15
            }
            }



# print configuration variables
def print_configuration():
	print(mc_folder_in);
	print(mc_folder_out);
	print(mc_ffmpeg_path);
