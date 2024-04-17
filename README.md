# Arbitrary Modification of Speech Characteristics in Segmental Duration 

Benjamin Harrison (bharrison49@gatech.edu)\
Sidong Guo (sguo93@gatech.edu)

## Description
This is an implementation of an algorithm that allows users to select arbitrary non-overlapping regions of duration of any spoken content, and speed up or down each audio region by a corresponding scaling factor of users' choosing, without altering other speech characteristics such as pitch, amplitude, etc. 

This implemention is based on [ScalerGAN](https://github.com/MLSpeech/scaler_gan) and [Hi-Fi GAN](https://github.com/jik876/hifi-gan/tree/4769534d45265d52a904b850da5a622601885777)

## Steps
1. Follow instruction in [ScalerGAN](https://github.com/MLSpeech/scaler_gan), exceptionally, download LJ Speech Dataset and place under scaler_gan/data/wavs
2. Follow instruction in [Hi-Fi GAN](https://github.com/jik876/hifi-gan/tree/4769534d45265d52a904b850da5a622601885777), exceptionally, the default generator model is [generator t2_v2](https://drive.google.com/drive/folders/1-eEYTB5Av9jNql0WGBlRoi-WH2J7bp5Y), --checkpointfile argument can be changed in TermProject.py

3. The Directory hierarchy should be: <br>
   --scaler_gan<br>
     --hifi_gan<br>
       --generated_files_from_mel<br>
       --test_mel_files<br>
4. Place the spoken content/audio files you want to arbitrarily time scale under directory scaler_gan/data/Project.
5. Under scaler_gan (main) directory, run python TermProject.py
6. A UI will appear that allows users to select audio files to time scale and choose arbitrary segments with "commit changes"
7. Upon all audio segments are chosen with corresponding scaling factor, click "Complete Edits", a new wav file named "New_"+Originalwavfilename will be created that has its audio regions time scaled accordingly. 

