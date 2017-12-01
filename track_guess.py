import os
import glob
import shutil
import random
from pydub import AudioSegment
from sys import argv
from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler

def prepare_track():
    music_dir = argv[1]
    track_list = list(glob.iglob(music_dir + '/**/*.wav', recursive=True))
    original_track = random.choice(track_list)
    track_name = original_track.split("/")[-1]
    track = AudioSegment.from_wav(original_track)
    length_of_clip = 5*1000
    start_of_clip = random.randrange(len(track-length_of_clip))
    end_of_clip = start_of_clip + length_of_clip
    clip = track[start_of_clip:end_of_clip]
    out_f = open("./clip", 'wb')
    clip.export(out_f, format='wav')
    #todo: send an extedned clip (10sec either side, instead of whole thing?)
    shutil.copy(original_track, "./track")
    with open("./index.template.html", "rt") as template:
        with open("./index.html", "wt") as result:
            for line in template:
                result.write(line.replace('[answer]', track_name))
    return

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/clip", "/track"]:
            self.send_response(200)
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-type', 'audio/wav')
            self.end_headers()
            if self.path == '/clip' :
                f = open('./clip', 'rb')
                self.wfile.write(f.read())
                f.close()
            elif self.path == "/track":
                f = open('./track', 'rb')
                self.wfile.write(f.read())
                f.close()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            prepare_track()
            f = open('./index.html', 'rb')
            self.wfile.write(f.read())


def run(server_class=HTTPServer, handler_class=S):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()