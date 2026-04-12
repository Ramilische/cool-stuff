from os import listdir
from tinytag import TinyTag

MUSIC_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac']
albums = []


def parse_tracks():
    lst = listdir('static/audio')
    folders = []
    files = []
    for item in lst:
        if any([item.endswith(ext) for ext in MUSIC_EXTENSIONS]):
            files.append(item)
        else:
            folders.append(item)

    albums.clear()

    for album in folders:
        path = f'static/audio/{album}'
        lst = listdir(path)
        desc = 'Описание отсутствует...'
        tracks = list()
        for item in lst:
            if item.endswith('.txt'):
                with open(path+'/'+item, 'r', encoding='utf-8') as file:
                    desc = file.read().strip()
                continue
            track_path = path + '/' + item
            info = TinyTag.get(track_path)

            minutes, seconds = str(int(info.duration // 60)), int(info.duration % 60)
            if seconds < 10:
                seconds = '0' + str(seconds)

            track = {'title': item, 'artist': '', 'duration': f'{minutes}:{seconds}', 'src': f'audio/{album}/{item}', 'filename': item}

            if info.title:
                track['title'] = info.title
            if info.artist:
                track['artist'] = info.artist

            tracks.append(track)
        albums.append({
            'title': album,
            'tracks': tracks,
            'description': desc
        })
    