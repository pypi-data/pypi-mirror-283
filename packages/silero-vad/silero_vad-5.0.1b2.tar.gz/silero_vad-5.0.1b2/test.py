from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
import torchaudio
import torch
torch.set_num_threads(1)
import sys

if __name__ == "__main__":
    print('gavno')
    print(torchaudio.list_audio_backends())
    print(sys.version)
    audios = ['test.wav', 'test.opus', 'test.mp3']

    model = load_silero_vad(onnx=True)
    for path in audios:
        audio = read_audio(path, sampling_rate=16000)
        speech_timestamps = get_speech_timestamps(audio, model, visualize_probs=False, return_seconds=True)
        print(speech_timestamps)
    print('onnx ok')

    model = load_silero_vad(onnx=False)
    for path in audios:
        audio = read_audio(path, sampling_rate=16000)
        speech_timestamps = get_speech_timestamps(audio, model, visualize_probs=False, return_seconds=True)
        print(speech_timestamps)
    print('jit ok')