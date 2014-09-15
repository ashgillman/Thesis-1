clear all

addpath('../Voicebox/')
WAV = 'wav';

% HTK output varaibles
STFT_OUTPUT_CODE = 9;
NNMF_OUTPUT_CODE = 9;
LPC_OUTPUT_CODE = 1;

OUTPUT_DIR = 'F:/Thesis/External/ClassifierTraining/Classifiers/';

TRAINING_AUDIO_DIR = 'F:/Thesis/External/ConvertData/ThesisData/Desk/Testing/Development/';
TRAINING_OUTPUT_DIR = strcat(OUTPUT_DIR, 'Training/');
TRAINING_FILES = getAllFiles(TRAINING_AUDIO_DIR);

%TRAINING_WAV_FILES = dir([TRAINING_AUDIO_DIR, '*.wav']); %{'C3CA010A.wav', 'C3CA010B.wav', 'C3CA010C.wav'};

EVAL_AUDIO_DIR = 'F:/Thesis/External/ConvertData/ThesisData/Desk/Testing/Evaluation/';
EVAL_OUTPUT_DIR = strcat(OUTPUT_DIR, 'Eval/');
EVAL_FILES = getAllFiles(EVAL_AUDIO_DIR);

% STFT Variables
FRAME_SIZE = 0.02;      % In seconds
NUMBER_OF_PEAKS = 10;
OVERLAP = 50;           % Percent overlap

% NNMF Variables

% LPC Variables
FILTER_ORDER = 12;

for n = 1:length(EVAL_FILES)
    file = EVAL_FILES{n};
    
    path = strsplit(file, '.');
    
    ext = path{2};
    
    splitpath = strsplit(path{1}, '\\');
    name = splitpath{end};
    
    if ~strcmp(ext, WAV)
        continue
    end
    
    [audio, Fs] = audioread(file);
    
    %% STFT
    STFTData = STFTClassifier(audio, Fs, OVERLAP, FRAME_SIZE, NUMBER_OF_PEAKS);
    
    stftHTKFile = strcat(EVAL_OUTPUT_DIR, name, '.stft');
    
    if exist(stftHTKFile, 'file')
        delete(stftHTKFile);
    end
    
    writehtk(stftHTKFile, STFTData, FRAME_SIZE, STFT_OUTPUT_CODE);
    
    
    %% LPC
    LPCData = LPCClassifier(audio, Fs, FILTER_ORDER, FRAME_SIZE);
    
    lpcHTKFile = strcat(EVAL_OUTPUT_DIR, name, '.lpc');
    
    if exist(lpcHTKFile, 'file')
        delete(lpcHTKFile);
    end
    
    writehtk(lpcHTKFile, LPCData, FRAME_SIZE, LPC_OUTPUT_CODE);
    
    %% NNMF
    % clearvars -except audio Fs
    % [phonemes, NNMFData] = NNMFClassifier(audio', Fs);
end






