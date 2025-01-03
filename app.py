import pyaudio
import numpy as np
import scipy.signal as signal
import wave

# Parameters
CHUNK = 1024  # Audio chunk size (samples per frame)
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate (Hz)
NOISE_THRESHOLD = 0.02  # Noise suppression threshold
OUTPUT_FILE = "processed_audio.wav"  # File to save processed audio

def noise_cancellation(data, scenario="single_speaker"):
    if scenario == "single_speaker":
        sos = signal.butter(10, [300, 3400], btype='bandpass', fs=RATE, output='sos')
        filtered = signal.sosfilt(sos, data)
        filtered[np.abs(filtered) < NOISE_THRESHOLD * np.max(np.abs(filtered))] = 0
        return filtered
    elif scenario == "multiple_speakers":
        mean_signal = np.mean(data)
        filtered = np.where(np.abs(data - mean_signal) > NOISE_THRESHOLD, data, mean_signal)
        return filtered
    else:
        raise ValueError("Invalid scenario. Choose 'single_speaker' or 'multiple_speakers'.")

def main():
    p = pyaudio.PyAudio()

    # List all available input devices
    print("Available audio input devices:")
    input_devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            input_devices.append(info)
            print(f"Device {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")

    # Select the default microphone if available
    input_device_index = 0  # Default to the first device
    print(f"Using device {input_device_index}: {input_devices[input_device_index]['name']}")

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=CHUNK)
        print("Stream opened successfully!")
    except Exception as e:
        print(f"Error opening stream: {e}")
        return

    print("Recording and processing audio. Press Ctrl+C to stop.")
    frames = []

    try:
        while True:
            try:
                raw_data = stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(raw_data, dtype=np.int16)
                scenario = "single_speaker"  # Change to "multiple_speakers" as needed
                processed_data = noise_cancellation(audio_data, scenario=scenario)
                frames.append(processed_data.astype(np.int16).tobytes())
            except IOError as e:
                print(f"Error while reading audio buffer: {e}")
                break

    except KeyboardInterrupt:
        print("\nStopping audio processing.")
    except Exception as e:
        print(f"An error occurred: {e}")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(OUTPUT_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    print(f"Processed audio saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
