
# Final project

## Aim of the project 

The aim of the project is to create and train an ML model capable of music emotion recognition (MER). Such model would accept raw audio as an input and would return predictions in two dimensional valence-arousal (VA) space.

### Stretch goal 1 

Create a lightweight audio player, which would automatically anotate songs and would change color of light accordingly to their mood. This part would take use of a project I finished earlier, which uses an Arduino microcontroller and a NeoPixel strip to control the color of light. In this previous project, however, the VA values were downloaded from Spotify via its API.

### Stretch goal 2

Modify the model so that it could listen to audio recieved from a microphone and generate predictions in real time. However, this could be problematic, because:
- communication with a microphone seems to be significantly more complicated that accessing an audio file
- the model would have to be fast enough to generate its predictions in a reasonable time
- another model would probably have to be employed to distinguish music from non-music sounds

## Technical details

One of the possible approaches has been described [here](https://arxiv.org/pdf/1706.02292.pdf). It utilizes combination of a CNN and a RNN and has reached the same RMSE as the best model published at the time with much lower number of parameters. Furthermore, the [dataset](http://cvml.unige.ch/databases/emoMusic/) used is available to the public.

The authors trained their network both on mel spectrograms as well as on extracted features. In this project, both approaches may be tested, and extracted features with a simpler regression model can be used as a baseline.
