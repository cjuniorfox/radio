Install pulseaudio and pulseaudio-utils

Compile FFMpeg. Do not forget the to enable the OpenSSL Option.

```
./configure --arch=armel \
  --target-os=linux \
  --enable-gpl \
  --enable-libx264 \
  --enable-nonfree \
  --extra-ldflags="-latomic" \
  --enable-openssl && \
make && sudo make install
```

Optionally, you can cross compile ffmpeg on your computer.
https://trac.ffmpeg.org/wiki/CompilationGuide/RaspberryPi
