# LCDSpotifyDisplay
Connects your Spotify to an LCD screen so you can flex how good your music taste is in style

Uses Arduino UNO connected to an IC2 LCD screen

Instructions to use code:
0. Make sure that you have python installed, the arduino IDE, and that the IC2 LCD screen is 
    plugged into the right SCL and SDA slots
1. upload code from the Arduino Display using the Arduino IDE
2. install the depencies (copy and paste the lines below into terminal)
    pip instal pyserial
    pip instal Flask
    pip instal requests
3. change the value of port to the COM port of where the arduino USB is plugged in
    if you don't know where that is go to device manager and look at Ports to check which one has the 
    arduino plugged in.
4. run the Python script and load the first website-generated
   There will be text output on the terminal that looks like this you will want to open the first like
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5000       <- This one
     * Running on http://
5. Then start listening to your music and look at the objectively better UI that the LCD screen offers!
