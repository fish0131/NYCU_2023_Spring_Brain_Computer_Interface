% EEGLAB history file generated on the 07-Apr-2023
% ------------------------------------------------
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_loadset('filename','S02_Sess05.set','filepath','/home/fish-bsp/Documents/Matlab_2021b/BCI_HW2/');
[ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );
EEG = eeg_checkset( EEG );
figure; topoplot([],EEG.chanlocs, 'style', 'blank',  'electrodes', 'labelpoint', 'chaninfo', EEG.chaninfo);
EEG = pop_eegfiltnew(EEG, 'locutoff',1,'hicutoff',48,'plotfreqz',1);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'savenew','S02_Sess05_filter','gui','off'); 
EEG = eeg_checkset( EEG );
% Start the timer
tic;
EEG = pop_runica(EEG, 'icatype', 'runica', 'extended',1,'interrupt','on');
% Stop the timer and print the elapsed time in seconds
elapsed_time = toc;
disp(['ICA running time: ', num2str(elapsed_time), ' seconds']);
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
EEG = eeg_checkset( EEG );
pop_topoplot(EEG, 0, [1:56] ,'S02_Sess05',[7 8] ,0,'electrodes','on');
EEG = eeg_checkset( EEG );
EEG = pop_iclabel(EEG, 'default');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
EEG = eeg_checkset( EEG );
pop_selectcomps(EEG, [1:56] );
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
EEG = eeg_checkset( EEG );
EEG = pop_subcomp( EEG, [1   9  11  16  17  18  20  21  22  24  26  27  30  31  32  34  35  37  40  43  44  49  51  56], 0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'savenew','S02_Sess05_filter_rmcomp','gui','off'); 
EEG = eeg_checkset( EEG );
EEG = pop_select( EEG, 'time',[0 10] );
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 3,'gui','off'); 
EEG = eeg_checkset( EEG );
pop_eegplot( EEG, 1, 1, 1);
pop_saveh( EEG.history, 'eeglabhist2.m', '/home/fish-bsp/Documents/Matlab_2021b/eeglab2021.1/');
eeglab redraw;
