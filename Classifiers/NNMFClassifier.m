function [phonemes, otherthing] = NNMFClassifier(audio, Fs)

    PHONEME_COUNT = 42;
   
    for n = 1:PHONEME_COUNT
        audio(n,:) = audio(1,:);
    end
        
    [rows, columns] = size(audio);
    [phonemes, otherthing] = nnmf(audio, PHONEME_COUNT);


























end