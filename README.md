Here's the entire `README.md` content in markdown format:

```markdown
# Audio Noise Cancellation for Single and Multiple Speakers

This Python project processes live audio from the microphone and applies noise cancellation based on whether the scenario involves a **single speaker** or **multiple speakers**. The project uses the `pyaudio` library to capture audio, `numpy` for data manipulation, `scipy` for signal processing, and `wave` to save the processed audio into a `.wav` file.

## Features

- **Real-time Audio Processing**: Continuously records audio from the microphone and processes it on the fly.
- **Two Noise Cancellation Scenarios**:
  - **Single Speaker**: A bandpass filter isolates speech frequencies and reduces background noise.
  - **Multiple Speakers**: Adaptive thresholding is applied to handle mixed voices, allowing multiple speakers to be heard clearly.
- **Customizable Noise Threshold**: The noise suppression level can be adjusted to balance noise reduction and audio clarity.
- **Save Processed Audio**: The cleaned audio is saved as a `.wav` file for later use.

## Prerequisites

Ensure that you have the following libraries installed:

- `pyaudio`
- `numpy`
- `scipy`

You can install them using pip:

```bash
pip install pyaudio numpy scipy
```

## Usage

### Running the Script

1. **Choose the Input Device**: The script will automatically list all available audio input devices. Select the one you wish to use (typically your laptop's built-in microphone).
2. **Select the Noise Cancellation Scenario**:
   - Type `single_speaker` for noise cancellation with one speaker.
   - Type `multiple_speakers` for noise cancellation with multiple speakers.
3. The processed audio will be saved to a file named `processed_audio.wav`.

### Example Output

Once the script is running, you will see output similar to:

```bash
Available audio input devices:
Device 0: Microphone (Realtek Audio) (Input Channels: 1)
Using device 0: Microphone (Realtek Audio)
Choose noise cancellation scenario ('single_speaker' or 'multiple_speakers'): single_speaker
Recording and processing audio. Press Ctrl+C to stop.
Processed audio saved to processed_audio.wav.
```

## Code Overview

### Noise Cancellation Function
The core function, `noise_cancellation`, applies different processing strategies based on the selected scenario:
- **Single Speaker**: A bandpass filter (300-3400 Hz) is used to isolate speech frequencies and suppress background noise.
- **Multiple Speakers**: An adaptive thresholding technique is used to retain speech from multiple speakers.

```python
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
```

## Visuals

### Example Audio Processing (Visualized)

Imagine you have a scenario with multiple voices. Here’s a simplified visual representation:

#### Raw Audio Input (Multiple Speakers)
```
Voice 1 ----|----|----|--|-----------|------------------|
Voice 2 -----------|--|-----|----|------|------|----|--|
Noise -----|--|--------|----|--|-------------------------|
```

#### Processed Audio (Multiple Speakers)
After applying adaptive noise cancellation, the voices are clearer:
```
Voice 1 ----|----|----|--|----------------|--------------|
Voice 2 -----------|--|-----|----|------|------|------|
```

### Bandpass Filtering (Single Speaker)
For single speaker scenarios, the bandpass filter isolates the speaker’s voice:
```
Voice 1 ----|----|----|--|---|---|---|---|---|----------|
Noise  -----|-----|--|---------|---|------|-------------|
```

The noise suppression ensures that non-speech elements are reduced.



### Key Sections:
- **Overview**: Introduces the project and its main functionality.
- **Installation**: Shows how to set up the project and install the required dependencies.
- **Usage**: Explains how to run the script, choose the noise cancellation scenario, and where the processed audio will be saved.
- **Code Overview**: Highlights the main components of the code, particularly the noise cancellation function.
- **Visuals**: Simple visual representation of how raw audio data looks versus processed data.

