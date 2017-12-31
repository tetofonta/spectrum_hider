# Hiding data inside  generic loseless audio file
___
There's no motivation about why developing something like this, maybe it's also already implemented in somehow, but whatever.
I was wondering about the possibility of hiding something in an existent information.
Than my little telecomunications knowledge came up.
Thanks to Fourier's theorem about his series saying something like

> We are able to see a periodic function **f(t)** observed in his time domain **t** reported to his frequency domain **F** like an opportune sinous operation with appropriate amplitude, phase and frequency sinous functions.

![Image from wikipedia](http://www.math.harvard.edu/archive/21b_fall_03/fourier/approximation.gif)

Now, thinking about an audio signal like a generic function with a frequency domain limited from 20Hz to 20kHz, as the human ear audible frequency interval.
We could just sum some sinous signal with higher frequency than 20kHz so we cannot hear them.
The only little problem on doing this is the necessity of an extended sampling rate to include an ultrasonic band big enought
