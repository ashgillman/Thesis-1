addpath('../Voicebox/')

frameSize = 0.02;

[audio, Fs] = audioread('C3CA010B.wav');

val = STFTClassifier(audio, Fs, 50, frameSize, 10);