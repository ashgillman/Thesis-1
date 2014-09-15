function [LPCData] = LPCClassifier(audio, Fs, filterOrder, frameSize)

    samples = ceil(Fs * frameSize);

    LPCData = lpccovar(audio, filterOrder, [samples]);

end