import unittest
from music_duration.duration import get_music_duration

class TestMusicDuration(unittest.TestCase):
    
    def setUp(self):
        # You can use any small audio file for testing.
        self.test_audio_filename = 'test_audio.wav'
        # Create a test tone (A4 note at 440 Hz)
        import numpy as np
        import soundfile as sf
        sr = 22050  # Sample rate
        t = np.linspace(0, 1.0, int(sr * 1.0), endpoint=False)  # 1 second duration
        test_tone = 0.5 * np.sin(2 * np.pi * 440 * t)
        sf.write(self.test_audio_filename, test_tone, sr)

    def tearDown(self):
        import os
        os.remove(self.test_audio_filename)

    def test_get_music_duration(self):
        duration = get_music_duration(self.test_audio_filename)
        self.assertAlmostEqual(duration, 1.0, places=2)

if __name__ == '__main__':
    unittest.main()
