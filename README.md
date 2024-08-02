## My implementation of the "One Bilion Row Challange" in Python

Original post and rulles - https://www.morling.dev/blog/one-billion-row-challenge/

###### TL;DR
The 1 Billion Row Challenge is a competition originally created by [Gunnar Morling](https://github.com/gunnarmorling) aimed towards Java developers. 
The scope of the competition is to parse a 1 billion row file with weather data (in the format of `weather station;temperature`) and 
calculate the `minimum`, `maximum` and the `average` temperature for each station as quickly as possible using Java with no external libraries.

## Prerequisites
```bash
...
Abéché;37.1
Baguio;10.6
Milan;15.8
...
```
`sample.txt` is the file with the data, it is around 13GB large so in order to obtain it you can generate it using a script.
The script is availible in many languages, the python version I was using was taken from here - https://github.com/ifnesi/1brc/blob/main/createMeasurements.py

#### Time of execution was measured using [hyperfine](https://github.com/sharkdp/hyperfine)
```bash
hyperfine --prepare 'sync; echo 3 | sudo tee /proc/sys/vm/drop_caches' --runs 3 'pypy3 file.py'
```
* disc cache was cleared before each run
* 5 min wait between individual runs to drop temperatures

#### System info:
* OS: Ubuntu 22.04 jammy
* Kernel: x86_64 Linux 6.5.0-35-generic
* CPU: 12th Gen Intel Core i5-1240P @ 16x 4,4GHz
* RAM: 16GB
#### Software versions:
* Python 3.12.4
* PyPy 7.3.15 with GCC 10.2.1

## Benchmarks
| Interpreter | Version | Time |
| ----------- | ------ | ---- |
| PyPy | [[PyPy Iteration 6] Float is heavy, Int is good](https://github.com/v-fol/1brc/blob/031f877e94ba70647828435950fe853d1b9770b6/calculate_average_mmap_pypy_int.py) | 1.841 s ±  0.035 s |
| PyPy | [[PyPy Iteration 5] Forget buffer, chunking chunks](https://github.com/v-fol/1brc/blob/ffc55f4ff4ace3fcc6df70aaef69006366b0dd29/calculate_average_mmap_pypy.py) |  |
| PyPy | [[PyPy Iteration 4] Mmap with buffer](https://github.com/v-fol/1brc/blob/df5756213758d6b522ab9c7dd9d5fae981a7c120/calculate_average_mmap_pypy.py) |  |
| PyPy | [[PyPy Iteration 3] Mmap and no buffer](https://github.com/v-fol/1brc/blob/64687458dd68ef19d9f6b8573af8cbf1c2ddd285/calculate_average_mmap_pypy.py) |  |
| PyPy | [[PyPy Iteration 2] From split to find and buffersize](https://github.com/v-fol/1brc/blob/05deb6f17156e069e67240a2ecd0663febdc6827/calculate_average_pypy.py) |  |
| PyPy | [[PyPy Iteration 1] Back to drawing board](https://github.com/v-fol/1brc/blob/96e20767567d03ee744cf6ae6f8c2ee54270bd88/calculate_average_pypy.py) |  |
| Python | [[Iteration 5] Say hello to ALLOCATIONGRANULARITY](https://github.com/v-fol/1brc/blob/fea65037f7b62c1bc17e9bc1172cd8818a2f8a38/calculate_average.py) |  |
| Python | [[Iteration 4] Cpu go brrr (multiprocessing to the rescue)](https://github.com/v-fol/1brc/blob/df3ba9d7b19462af0598dd52f5bd57f11e2191ee/calculate_average.py) |  |
| Python | [[Iteration 3] Byte by byte (and say hello to mister defaultdict)](https://github.com/v-fol/1brc/blob/dd9f1f5e40e087f0fb66a25d28da2d0f26828962/calculate_average.py) |  |
| Python | [[Iteration 2] Ditching the classes](https://github.com/v-fol/1brc/blob/2655e3e34e18a1115ed196fca80e59d684efe517/calculate_average.py) |  |
| Python | [[Iteration 1] Pythonic way (this is the way)](https://github.com/v-fol/1brc/blob/9f960155bb1d9c6e1a4157bf2c82e477b125ff93/calculate_average.py) |  |
