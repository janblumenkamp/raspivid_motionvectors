This is a small tool written in Python 3 to visualize and process the Raspberry Pi Cameras H264 motion vectors.

#Option 1: Record the motion vectors and save it to a file on the Raspberry Pi to re-play it later:
1. Run `raspivid -o /dev/null -x vect.txt -t 0` on the Raspberry Pi.
The `-t 0` option means that it will record until you quit, `-t 5` would quit after five seconds. If you also want to save the corresponding video, you can specifiy the out file `-o vid.avi`.
2. Copy the file to the computer where you want to re-play it. If you want to re-play it on the Raspberry Pi just leave it there. You can copy for example with `scp`.
3. Assuming your file is named `vect.txt` run `cat vect.txt | python proc.py`. The file should be re-played now.

#Option 2: Transfer the motion vectors via TCP to a client that runs the processing:
This is especially handy if you are working on a Raspberry Pi zero with no screen attached.

1. Run `raspivid -l -o /dev/null -x tcp://0.0.0.0:1234 -t 0` on the Raspberry Pi. This runs raspivid and makes it listen on TCP port 1234 on the local IP address.
(hint: as soon as you connect to the port and disconnect afterwards, raspivid will terminate. You can run it in a loop on the Raspberry Pi with `while true; do raspivid -l -o /dev/null -x tcp://0.0.0.0:1234 -t 0; done`).
2. Run `nc raspberrypi.local 1234 | python proc.py` on the computer where you want to visualize the optical flow. If you have Avahi running then `raspberrypi.local` should work, otherwise replace it with the IP address of your Raspberry Pi.

#Option 3: Run the processing directly on the Raspberry Pi:
This is useful if you want to process the motion vectors directly on the Raspberry Pi.
1. Run `raspivid -o - -x | python proc.py`
