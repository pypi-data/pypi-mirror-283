/**
 * AudioWorkletProcessor to handle audio processing tasks.
 * This processor handles multiple input channels, copies the input data,
 * sends it to the main thread, and optionally mixes down to mono for output.
 */
class MyAudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
    }

    /**
     * Processes the audio data.
     * @param {Array} inputs - The input audio data.
     * @param {Array} outputs - The output audio data.
     * @param {Object} parameters - Additional parameters.
     * @returns {boolean} - Indicates whether the processor should remain active.
     */
    process(inputs, outputs, parameters) {
        // The first index of inputs corresponds to the first input connection
        const input = inputs[0];

        // Check if there are multiple channels (inputs)
        if (input.length > 0) {
            // Create an array to hold data from all channels
            let allChannelsData = [];

            // Iterate over each channel
            for (let channel = 0; channel < input.length; channel++) {
                if (input[channel].length > 0) {
                    // Make a copy of the inputData to avoid modifying the original buffer
                    const inputDataCopy = input[channel].slice();

                    // Add copied inputData to the allChannelsData array
                    allChannelsData.push(inputDataCopy);

                    // Pass the audio data of this channel to the main thread
                    this.port.postMessage({ channel: channel, data: inputDataCopy });
                }
            }

            // mix down to mono:
            if (outputs[0].length > 0) {
                const outputData = outputs[0][0];
                for (let i = 0; i < outputData.length; i++) {
                    // Simple mix down to mono - summing all channels
                    outputData[i] = allChannelsData.reduce((sum, channelData) => sum + channelData[i], 0) / input.length;
                }
            }
        }

        return true; // Keep the processor alive
    }
}

// Register the processor with the given name
registerProcessor('audio-processor', MyAudioProcessor);
