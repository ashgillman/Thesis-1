clear all

addpath('../Voicebox/')

% HTK output varaibles
STFT_OUTPUT_CODE = 9;
NNMF_OUTPUT_CODE = 9;
LPC_OUTPUT_CODE = 1;
AUDIO_DIR = '../../Audio/';
OUTPUT_DIR = '../ClassifierOutput/';
WAV_FILES = dir([AUDIO_DIR, '*.wav']); %{'C3CA010A.wav', 'C3CA010B.wav', 'C3CA010C.wav'};

% STFT Variables
FRAME_SIZE = 0.02;      % In seconds
NUMBER_OF_PEAKS = 10;
OVERLAP = 50;           % Percent overlap

% NNMF Variables

% LPC Variables
FILTER_ORDER = 12;

for n = 1:length(WAV_FILES)
    wavFile = WAV_FILES(n).name;
    wavLoc = [AUDIO_DIR, wavFile]
    [audio, Fs] = audioread(wavLoc);
    
    %% STFT
    STFTData = STFTClassifier(audio, Fs, OVERLAP, FRAME_SIZE, NUMBER_OF_PEAKS);
    
    stftHTKFile = strcat(OUTPUT_DIR, wavFile(1:end-4), '.stft');
    
    if exist(stftHTKFile, 'file')
        delete(stftHTKFile);
    end
    
    writehtk(stftHTKFile, STFTData, FRAME_SIZE, STFT_OUTPUT_CODE);
    
    
    %% LPC
    LPCData = LPCClassifier(audio, Fs, FILTER_ORDER, FRAME_SIZE);
    
    lpcHTKFile = strcat(OUTPUT_DIR, wavFile(1:end-4), '.lpc');
    
    if exist(lpcHTKFile, 'file')
        delete(lpcHTKFile);
    end
    
    writehtk(lpcHTKFile, LPCData, FRAME_SIZE, LPC_OUTPUT_CODE);
    
    %% NNMF
    % clearvars -except audio Fs
    % [phonemes, NNMFData] = NNMFClassifier(audio', Fs);
end






