# HackRF SDR Sweep Power Spectral Density

This project contains 2 python files that allows the user to scan the frequencies of the evironment using a HackRF SDR and Raspberry Pi to dump this information from the Pi to a Host PC through an ethernet cable (UDP). The project acts like a low-cost spectrum analyser. This project is for users that are...

The HackRF SDR can be tuned a center frequency and sample rate determined by the user at execution through command line arguments. An example output that will be provided on the Host PC's Terminal: "Message from Client: 'Freq: 8.243e+07 Hz, dBm: -78.215'"

## Installation
### Requirements

Libaries Required to Install on Raspberry Pi
```bash
    sudo apt install numpy matplotlib hackrf rtl-sdr  gr-osmosdr gnuradio
```
### Setting Up
#### Hardware
![IMG_3938](https://user-images.githubusercontent.com/118889521/222162280-e1afb688-7b47-473c-a9b8-9cc9a26487f2.JPG)
Diagram indicates a Raspberry Pi 3b 

#### IP Adress + Port Number + Filename
All 3 of these must be changed on both Client and Sever. Find and replace: 
1. SEVER IP ADDRESS
2. SEVER PORT
3. YOUR FILE NAME 

#### Executing the files w/ Command Line Arguments

sdr_sever.py should be run on the Raspberry Pi and will be given command line arguements in the format Center Frequency and Sample Rate. For example:

```bash
    python3 /Users/John/Desktop/Hackrf/sdr_server.py 92e6 20e6
```

#### Running File on Boot
Follow this tutorial for rc.local: https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/

One limitation of starting this script on boot is the lack of flexibility to change the Center Frequency and Sample Rate. You will have to ssh into the pi to edit the center frequency and sample rate.


## Documentation

### Testing Libraries
#### HackRF

To ensure that HackRF SDR is working, plug it in and run:
```bash
    hackrf_info
```
More details are here: https://hackrf.readthedocs.io/en/latest/getting_started_hackrf_gnuradio.html

#### GNURadio + OsmoSDR
Now open GNURadio 3.8.2 (or the latest version avaiable on Raspbian). The included file is the flowchart that will allow you to test osmosdr source. 

Open the following file included in the repository: hackrf_sweep.grc

![Screenshot](https://user-images.githubusercontent.com/118889521/221857811-5352b99a-ac51-4bbd-a882-665762195ba6.png)

If this runs properly this will provide a dynamic Power by Frequency Graph and your libraries have installed appropriately.

#### GNURadio Version Note
sdr_client.py works with GNURadio 3.8.2, the latest version on Raspbian as per date of publishing. sdr_server.py will work on any GNURadio version.

It can be easily recreated in any GNURadio version through these steps

1. Generating the flowchart above in your desired GNURadio Version. 
2. Cpying the python code that is overlayed onto the GNURadio script in sdr_client which can be found in between tb.start() and tb.wait()
3. Change the variables to command line arguements using the sys library.
4. Ensure that the filename is accurate throughout the script

## Screenshots

![Screenshot2](https://user-images.githubusercontent.com/118889521/221858083-daa406ba-24f4-4b34-83eb-aca4db9b7d16.png)

This shows the Terminal of the Raspberry Pi. It will output a message indicating the connection between the server and client. Do not be alarmed by the "0" as this is simply the SDR's way of informing you that the sample rate might be too high and may affect the quality of the frequency sweeps. Lowering the sample rate will reduce the number of "0"s.

## Terminal Demonstration

