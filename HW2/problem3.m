[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_loadset('filename','S02_Sess05.set','filepath','/home/fish-bsp/Documents/Matlab_2021b/BCI_HW2/');

% Select the FCz channel for analysis
fcz_chan = find(strcmpi({EEG.chanlocs.labels}, 'FCz'));

% Epoch the continuous EEG with a time interval [-0.2 1.3] sec, where t=0 is the feedback onset
EEG_correct = pop_epoch( EEG, {  'FeedBack_correct'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
EEG_wrong = pop_epoch( EEG, {  'FeedBack_wrong'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
% Remove the epoch baseline mean
EEG_correct = pop_rmbase(EEG_correct, [-200 0], []);
EEG_wrong = pop_rmbase(EEG_wrong, [-200 0], []);

% Calculate the peak amplitude of the error-related potential (ERP) waveform from 0 to 1000ms after feedback onset
erp_c = squeeze(mean(EEG_correct.data(fcz_chan, :, :), 3))
erp_w = squeeze(mean(EEG_wrong.data(fcz_chan, :, :), 3))
peak_amp = max(erp_w);

% Calculate the standard deviation of the ERP waveform in the pre-stimulus interval (−200 to 0 ms)
baseline_std = std(erp_w(EEG_wrong.times < 0));

% Calculate the SNR
SNR = peak_amp / baseline_std;
disp(['SNR (Without any operation): ', num2str(SNR)]);

figure;
hold on;
plot(EEG_correct.times, erp_c, 'blue');
plot(EEG_wrong.times, erp_w, 'red');
xlabel('ms');
ylabel('amplitude');
legend('correct', 'error');


% ------------Bandpass only--------------
EEG_band = pop_eegfiltnew(EEG, 'locutoff',1,'hicutoff',48,'plotfreqz',1);

% Select the FCz channel for analysis
fcz_chan = find(strcmpi({EEG_band.chanlocs.labels}, 'FCz'));

% Epoch the continuous EEG with a time interval [-0.2 1.3] sec, where t=0 is the feedback onset
EEG_correct = pop_epoch( EEG_band, {  'FeedBack_correct'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
EEG_wrong = pop_epoch( EEG_band, {  'FeedBack_wrong'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
% Remove the epoch baseline mean
EEG_correct = pop_rmbase(EEG_correct, [-200 0], []);
EEG_wrong = pop_rmbase(EEG_wrong, [-200 0], []);

% Calculate the peak amplitude of the error-related potential (ERP) waveform from 0 to 1000ms after feedback onset
erp_c = squeeze(mean(EEG_correct.data(fcz_chan, :, :), 3))
erp_w = squeeze(mean(EEG_wrong.data(fcz_chan, :, :), 3))
peak_amp = max(erp_w);

% Calculate the standard deviation of the ERP waveform in the pre-stimulus interval (−200 to 0 ms)
baseline_std = std(erp_w(EEG_wrong.times < 0));

% Calculate the SNR
SNR = peak_amp / baseline_std;
disp(['SNR (Bandpass only): ', num2str(SNR)]);

figure;
hold on;
plot(EEG_correct.times, erp_c, 'blue');
plot(EEG_wrong.times, erp_w, 'red');
xlabel('ms');
ylabel('amplitude');
legend('correct', 'error');


% ------------IC removal only--------------
EEG_recomp = pop_loadset('filename','S02_Sess05_rmcomp.set','filepath','/home/fish-bsp/Documents/Matlab_2021b/eeglab2021.1/');

% Select the FCz channel for analysis
fcz_chan = find(strcmpi({EEG_recomp.chanlocs.labels}, 'FCz'));

% Epoch the continuous EEG with a time interval [-0.2 1.3] sec, where t=0 is the feedback onset
EEG_correct = pop_epoch( EEG_recomp, {  'FeedBack_correct'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
EEG_wrong = pop_epoch( EEG_recomp, {  'FeedBack_wrong'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
% Remove the epoch baseline mean
EEG_correct = pop_rmbase(EEG_correct, [-200 0], []);
EEG_wrong = pop_rmbase(EEG_wrong, [-200 0], []);

% Calculate the peak amplitude of the error-related potential (ERP) waveform from 0 to 1000ms after feedback onset
erp_c = squeeze(mean(EEG_correct.data(fcz_chan, :, :), 3))
erp_w = squeeze(mean(EEG_wrong.data(fcz_chan, :, :), 3))
peak_amp = max(erp_w);

% Calculate the standard deviation of the ERP waveform in the pre-stimulus interval (−200 to 0 ms)
baseline_std = std(erp_w(EEG_wrong.times < 0));

% Calculate the SNR
SNR = peak_amp / baseline_std;
disp(['SNR (IC removal only): ', num2str(SNR)]);

figure;
hold on;
plot(EEG_correct.times, erp_c, 'blue');
plot(EEG_wrong.times, erp_w, 'red');
xlabel('ms');
ylabel('amplitude');
legend('correct', 'error');


% ------------Bandpass+IC removal--------------
EEG_band_recomp = pop_loadset('filename','S02_Sess05_filter_rmcomp.set','filepath','/home/fish-bsp/Documents/Matlab_2021b/eeglab2021.1/');

% Select the FCz channel for analysis
fcz_chan = find(strcmpi({EEG_band_recomp.chanlocs.labels}, 'FCz'));

% Epoch the continuous EEG with a time interval [-0.2 1.3] sec, where t=0 is the feedback onset
EEG_correct = pop_epoch( EEG_band_recomp, {  'FeedBack_correct'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
EEG_wrong = pop_epoch( EEG_band_recomp, {  'FeedBack_wrong'  }, [-0.2         1.3], 'newname', 'S02_Sess05 epochs', 'epochinfo', 'yes');
% Remove the epoch baseline mean
EEG_correct = pop_rmbase(EEG_correct, [-200 0], []);
EEG_wrong = pop_rmbase(EEG_wrong, [-200 0], []);

% Calculate the peak amplitude of the error-related potential (ERP) waveform from 0 to 1000ms after feedback onset
erp_c = squeeze(mean(EEG_correct.data(fcz_chan, :, :), 3))
erp_w = squeeze(mean(EEG_wrong.data(fcz_chan, :, :), 3))
peak_amp = max(erp_w);

% Calculate the standard deviation of the ERP waveform in the pre-stimulus interval (−200 to 0 ms)
baseline_std = std(erp_w(EEG_wrong.times < 0));

% Calculate the SNR
SNR = peak_amp / baseline_std;
disp(['SNR (Bandpass+IC removal): ', num2str(SNR)]);

figure;
hold on;
plot(EEG_correct.times, erp_c, 'blue');
plot(EEG_wrong.times, erp_w, 'red');
xlabel('ms');
ylabel('amplitude');
legend('correct', 'error');


