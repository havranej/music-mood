
# Music Mood to Light Color

A responsive light changing its color to match the mood of your music. Powered by recurrent neural networks (running on laptop) & Arduino. 

[See it in action here](https://youtu.be/xi0QlckEt9w).

Result of a final project for ML course 2020/2021. For technical details, see the [report](report.pdf). 

There were two parts of the project – training the ML model for valence (positivity/negativity) & arousal (energy) predictions from audio, which is located in the `notebooks` directory, and development of an app (in the `app` directory), which would use this model for nearly-real-time adjustments of the light color.

## The Light

The Light was built with Arduino-controlled NeoPixel RGB LED ring. The controlling pin is set to be digital pin 6, but you can change it in the sketch. You can run the app without The Light, if you omit the `--port` parameter – in that case, you can still get valence & arousal predictions for your music, along with the name of the nearest CSS color.

## Environment

The [environment](app/environment.yml) file should contain everything you need to run the app, except for [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) library, which needs to be installed manually. Big thanks to Theodoros Giannakopoulos, author of this library, for it, and also for his [article](https://hackernoon.com/how-to-use-machine-learning-to-color-your-lighting-based-on-music-mood-bi163u8l), which inspired me greatly.
