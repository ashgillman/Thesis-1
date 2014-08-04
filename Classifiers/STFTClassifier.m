
WAV_FILE = 'C3CA010A.wav';
OUTPUT_FILE = 'Peaks.csv';
delete(OUTPUT_FILE);

% Initialise STFT constants
STFT_TIME_STEP = 20; % ms
NUMBER_OF_PEAKS = 10;

[audio,Fs] = audioread(WAV_FILE);

% Determine the number of samples per time step
samplesPerStep = Fs / (1000/STFT_TIME_STEP);

startIndex = 1;
audioLength = length(audio);

while startIndex < audioLength
    
    % Determine the end index for the STFT
    endIndex = startIndex+samplesPerStep;  
    if endIndex > audioLength
        endIndex = audioLength;
    end
    
    % Extract the data for this time step
    sample = audio(startIndex:endIndex);

    % Perform the fft and strip the reflection
    transform = fft(sample);    
    transform = transform(1:ceil(length(transform)/2));
    
    % Set up the frequency data
    freq = linspace(0, Fs/2, length(sample)/2+1);
  
    % Find all the peaks and sort them in decending order of magnitude
    [~, peakLocs] = findpeaks(abs(transform),'SortStr','descend');
    
    % Take only the top X peaks (specified in constants)
    topXPeaks = peakLocs(1:NUMBER_OF_PEAKS);
    
    % Determine the frequency corresponding to each peak
    peakFreqs = sort(round(freq(topXPeaks)));

    % Write the data out
    dlmwrite(OUTPUT_FILE, peakFreqs,'-append');
    
    % Increment the time step
    startIndex = startIndex + samplesPerStep;
end


