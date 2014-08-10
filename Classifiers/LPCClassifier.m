function [LPCData] = LPCClassifier(audio, Fs, filterOrder, frameSize)

    samples = ceil(Fs * frameSize);

    LPCData = lpcauto(audio, filterOrder, [samples]);

end