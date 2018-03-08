# Track Guess
I'm crap at remebering my own music collection.
This is a thing meant to help with that.

Runs a local webserver that you point at your music folder. With python3 and dependancies installed, kick it of with:

python .\track_guess.py C:\directory\where\my\music\lives

When you go to 127.0.0.1:8000 it'll pick a track and play you a small clip of it before you "guess" and get played the full thing.

Bugged on firefox because of caching:
https://stackoverflow.com/questions/25821915/how-to-force-the-html5-audio-tag-to-reload-a-changing-file
