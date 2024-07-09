import { AudioVisualizer } from './audio-visualizer.js';
import { WebSocketHandler } from './websocket-handler.js';
import { getBaseUrl } from './utils.js';

export class AudioRecorder {
  constructor(audioDevices, wsAudioHandler) {
    this.streams = [];
    this.audioContext = null;
    this.sources = [];
    this.merger = null;
    this.analyser = null;
    this.processor = null;
    this.isRecording = false;
    this.isListening = false;
    this.selectedAudioDevices = audioDevices || [];
    this.visualizer = new AudioVisualizer(document.getElementById('audioVisualizer'));
    
    // Setup WebSocket connection for sending audio
    this.wsAudioHandler = wsAudioHandler

    // if selectedAudioDevices is empty, add the default device
    if (this.selectedAudioDevices.length === 0) {
      console.log('No audio devices selected. Adding default device.');
      this.selectedAudioDevices.push('default');
    }

    console.log('AudioRecorder initialized with audio devices:', this.selectedAudioDevices);
  }

  /**
   * Gets the audio stream for the selected audio input devices.
   * @returns {Promise<MediaStream[]>} The audio streams.
   */
  async getAudioStreams() {
    const streams = [];
    for (const deviceId of this.selectedAudioDevices) {

      console.log('Getting audio stream for device:', deviceId);

      if (deviceId === 'system-audio') {
        // Handle system audio
        streams.push(await this.getSystemAudioStream());
      } else {
        const audioConstraints = {
          audio: {
            deviceId: deviceId ? { exact: deviceId } : undefined
          }
        };
        try {
          const newStream = await navigator.mediaDevices.getUserMedia(audioConstraints);
          streams.push(newStream);
        } catch (error) {
          if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            alert('Permission denied. Please allow access to the microphone to use this feature.');
          }
          console.error(`Error accessing microphone: ${error}`);
        }
      }
    }
    return streams;
  }

  /**
   * Gets the system audio stream.
   * @returns {Promise<MediaStream>} The system audio stream.
   */
  async getSystemAudioStream() {
    try {
      const captureStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: true,
        systemAudio: 'include'
      });

      // Stop video tracks if any (only want audio)
      captureStream.getVideoTracks().forEach(track => track.stop());

      return captureStream;
    } catch (error) {
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        alert('Audio Permissions denied: Please allow access to the microphone to use this feature.');
      }
      console.error('Error accessing system audio:', error);
      throw error;
    }
  }

  /**
   * Gets the audio context.
   * @returns {Promise<AudioContext>} The audio context.
   */
  async getAudioContext() {
    try {

      console.log('Creating new audio context');

      const newAudioContext = new (window.AudioContext || window.webkitAudioContext)();
      return newAudioContext;
    } catch (error) {
      console.error(`Error accessing microphone: ${error}`);
      return null;
    }
  }

  /**
   * Starts streaming voice and sets up audio processing and visualization.
   */
  async listenToAudioStream() {
    // Attempt to get audio streams for selected devices
    try {
      this.streams = await this.getAudioStreams();
    } catch (error) {
      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        alert('Audio Permissions denied: Please allow access to the microphone to use this feature.');
      }
      console.error(`Error getting media streams: ${error}`);
      return;
    }

    // Setup audio context and connect processing nodes (merger, analyser, processor)
    try {
      this.audioContext = await this.getAudioContext();
      if (!this.audioContext) {
        alert('Error creating audio context. Please try again.');
        return;
      }
    } catch (error) {
      console.error(`Error creating audio context: ${error}`);
      return;
    }

    // Create merger
    try {
      this.merger = this.audioContext.createChannelMerger(this.streams.length);
    } catch (error) {
      console.error(`Error creating channel merger: ${error}`);
      return;
    }

    // Connect audio streams to merger
    try {
      this.streams.forEach((stream, index) => {
        const source = this.audioContext.createMediaStreamSource(stream);
        source.connect(this.merger, 0, index);
        this.sources.push(source);
        console.log(`connected ${stream} to index ${index}`);
      });
    } catch (error) {
      console.error(`Error connecting audio sources: ${error}`);
      return;
    }

    // Setup audio analyser and processor
    
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 512;
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);
    this.merger.connect(this.analyser);
    try {
      await this.audioContext.audioWorklet.addModule(getBaseUrl() + "/static/scripts/audio-processor.js")
    } catch (error) {
      console.error(`Error setting up audio processing: ${error}`);
      return;
    }
    this.processor = new AudioWorkletNode(this.audioContext, 'audio-processor');
    this.merger.connect(this.processor);

    // Visualize the audio as waves
    this.visualizer.startDrawing(this.analyser, this.bufferLength);

    this.isListening = true;

  }

  async sendVoiceViaWebsocket() {

    // Start WebSocket connection and send audio-start message
    this.wsAudioHandler.sendMessage(JSON.stringify({ type: "audio-start", samplerate: this.audioContext.sampleRate }));

    // Update recording state
    this.isRecording = true;

    // Setup the audio processor event handler
    try {
      this.processor.port.onmessage = (event) => {
        if (!this.isRecording) {
          return;
        }
        const inputData = event.data.data;
        const outputData = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          outputData[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
        }

        // Send processed audio via WebSocket
        this.wsAudioHandler.sendMessage(outputData);
      };
    } catch (error) {
      console.error(`Error sending audio stream to backend: ${error}`);
    }
  }

  isRecordingVoice() {
    return this.isRecording;
  }


  /**
   * Stops streaming voice and cleans up audio processing and visualization.
   */
  stopListening() {

    console.log('Stopping listening');

    if (this.processor) {
      this.processor.disconnect();
      this.processor = null;
    }
    if (this.sources) {
      this.sources.forEach(source => source.disconnect());
      this.sources = [];
    }
    if (this.merger) {
      this.merger.disconnect();
      this.merger = null;
    }
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
    if (this.streams) {
      this.streams.forEach(stream => stream.getTracks().forEach(track => track.stop()));
      this.streams = [];
    }

    this.isListening = false;
  }

  pauseRecordingVoice() {
    // Update recording state
    console.log('Pausing recording');
    this.isRecording = false;
  }

  resumeRecordingVoice() {
    // Update recording state
    console.log('Resuming recording');
    this.isRecording = true;
  }

  stopRecordingVoice() {
    // Update recording state
    this.isRecording = false;

    if (this.wsAudioHandler) {
      // Send audio-end message via WebSocket
      this.wsAudioHandler.sendMessage(JSON.stringify({ type: "audio-end" }));
    }

    // Stop visualizing the audio
    // this.visualizer.stopDrawing();
  }

  /**
   * Updates the transcript textarea with the given message.
   * @param {string} message - The message to append to the transcript.
   */
  updateTranscript(message) {
    this.textareaTranscript.value += message + '\n';
  }
}
