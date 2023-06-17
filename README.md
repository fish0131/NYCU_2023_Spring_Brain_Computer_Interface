# NYCU_2023_Spring_Brain_Computer_Interface
## HW 2
EEG Analysis   
Reference: https://eeglab.org/
## HW 3
Deep Learning for BCI  
Reference:  
1. Lawhern, Vernon J., et al. "EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces." Journal of neural engineering 15.5 (2018): 056013.  
2. Wei, Chun-Shu, Toshiaki Koike-Akino, and Ye Wang. "Spatial component-wise convolutional network(SCCNet) for motor-imagery EEG classification." 2019 9th International IEEE/EMBS Conference on Neural Engineering (NER). IEEE, 2019.  
3. Schirrmeister, Robin Tibor, et al. "Deep learning with convolutional neural networks for EEG decoding and visualization." Human brain mapping 38.11 (2017): 5391-5420.
## Term project
FBCNet - paper reproduce  
Reference:  
1. Ravikiran Mane, Effie Chew, Karen Chua, Kai Keng Ang, Neethu Robinson, A.P. Vinod, Seong-Whan Lee, and Cuntai Guan, "FBCNet: An Efficient Multi-view Convolutional Neural Network for Brain-Computer Interface," arXiv preprint arXiv:2104.01233 (2021) https://arxiv.org/abs/2104.01233  
2. https://github.com/ravikiran-mane/FBCNet/tree/master
## Controlled car competition
Reference:  
1. SSVEP for BCI: https://github.com/HeosSacer/SSVEP-Brain-Computer-Interface/tree/master  
2. *Alpha wave*: action trigger  
```Python
peak_alpha = the sum of frequency in alpha wave(8-13Hz)/the sum of the frequency in 3-30Hz  
if (peak_alpha > threshold): 
  action point to 1  
else: 
  action point to 0  
```
- (0, 1) will have four combinations (forward, right, left, stop)
- To implement this project: `python ./src/utils.py`


