import soundfile as sf

def get_music_duration(filename):
    """
    Get the duration of a music file.

    :param filename: Path to the music file.
    :return: Duration of the music file in seconds.
    """
    data, samplerate = sf.read(filename)
    duration = len(data) / samplerate
    return duration
