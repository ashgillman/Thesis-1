function [STFT] = STFTClassifier(audio, Fs, overlap, frameSize, peakCount)
    
    nf = Fs * frameSize;
    
    frameN = (nf-1)*2;
    
    win = hamming(frameN,'periodic');
    
    transforms = rfft(enframe(audio,win,nf-1),frameN,2);
    
    
    
%     % Determine the number of samples per time step
%     samplesPerStep = ceil(Fs * frameSize);
% 
%     startIndex = 1;
     count = 1;
%     audioLength = length(audio);
%
%     while startIndex < audioLength
% 
%         % Determine the end index for the STFT
%         endIndex = startIndex+samplesPerStep;
%         if endIndex > audioLength
%             endIndex = audioLength;
%         end
% 
%         % Extract the data for this time step
%         sample = audio(startIndex:endIndex);
% 
%         % Perform the fft and strip the reflection
%         transform = fft(sample);
%         transform = transform(1:ceil(length(transform)/2));
for transform = transforms
    
        % Set up the frequency data
        freq = linspace(0, Fs/2, length(transform));

        % Find all the peaks and sort them in decending order of magnitude
        [~, peakLocs] = findpeaks(abs(transform),'SortStr','descend');

        % Take only the top X peaks (specified in constants)
        noOfPeaks = length(peakLocs);
        if peakCount > noOfPeaks
            topXPeaks = peakLocs;
        else
            topXPeaks = peakLocs(1:peakCount);
            noOfPeaks = 10;
        end

        % Determine the frequency corresponding to each peak
        peakFreqs = zeros(1, peakCount);
        peakFreqs(1,1:noOfPeaks) = round(freq(topXPeaks'));
        %peakFreqs = sort(peakFreqs);
        
        STFT(count,:) = peakFreqs;

        % Increment the time step
        count = count + 1;
    end
end


