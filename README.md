# HackRF SDR Sweep Power Spectral Density

This project contains 2 python files that allows the user to scan the frequencies of the evironment using a HackRF SDR and Raspberry Pi to dump this information from the Pi to a Host PC through an ethernet cable (UDP). The project acts like a low-cost spectrum analyser. This project is for users that are...

The HackRF SDR can be tuned a center frequency and sample rate determined by the user at execution through command line arguments. An example output that will be provided on the Host PC's Terminal: "Message from Client: 'Freq: 8.243e+07 Hz, dBm: -78.215'"

## How to Use


## Installation
### Requirements

Libaries Required to Install on Raspberry Pi
```bash
    sudo apt install numpy matplotlib hackrf rtl-sdr  gr-osmosdr gnuradio
```

Tested On (Client): Raspberry Pi 3b; Raspbian Version 11 Bullseye
Tested On (Sever): Macbook Pro Apple M1 Ventura 13.0.01 Python Version 3.11.2

UDP Server should work on Linux without an issue as only library that is imported is socket.

### Setting Up
#### Hardware
![IMG_3938](https://user-images.githubusercontent.com/118889521/222162280-e1afb688-7b47-473c-a9b8-9cc9a26487f2.JPG)
Diagram indicates a Raspberry Pi 3b connected to power, an ethernet cable to the UDP Sever PC and the HackRF SDR USB Cable. THe HackRF SDR will also have to be connected to an antenna using the SMA Antenna Port.

#### IP Adress + Port Number + Filename
All 3 of these must be changed on both Client and Sever. Find and replace: 
1. SEVER IP ADDRESS
2. SEVER PORT
3. YOUR FILE NAME 

#### Server UDP Server
sdr_server.py must output "UDP Server Up and Running" before sdr_client.py is executed. This is can be done by executing this file immediately after the Ethernet Connection has been established but before the raspberry pi starts transmitting data. A screenshot and video have been included below for further reference.

#### Executing the files w/ Command Line Arguments

sdr_client.py should be run on the Raspberry Pi and will be given command line arguements in the format Center Frequency and Sample Rate. For example:

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

### How Does the Code Work
The python script that enables the format and transfer of data will be described here. Firstly, the code opens the binary file with data format of 32 Bit Floats and stores this as a numpy array.

```bash
    x = np.fromfile(open(filename), dtype=np.float32)    
```

Next the frequency step of the output is determined by calculating Sample Rate over Vector Length, an exmaple would be: $20e6/1024$. Then a numpy array is created with a range of $Center Frequency - (Sample Rate)/2$ to $Center Frequency + (Sample Rate)/2$. This will provide a range of the Sample Rate centered around the Center Frequency. This section of the code is shown here.

```bash
    f = np.arange(Fs/-2.0, Fs/2.0, Fs/N) 
    f += center_freq
```
The function update iterates every 1024 samples through the "x" Power (dBm) file by indexing the array. This is then iterated through, in the for loop, to attach a corresponding frequency to it which is then can be printed or transmitted to a UDP Server. 

```bash
    def update(length):
        i = 0
        while i < length:
            x_i = x[i*1024:(i+1)*1024]
            for j in range(len(f)):
                freq = f[j]
                dBm = x_i[j]
                msgclient = "Freq: {:.5g} Hz, dBm: {:.5g}".format(freq, dBm)
                
                ....... #Establishing UDP Connection Code Ommitted for Simplicity
                
                print(msg)
            i += 1
```

#### GNURadio Version Note
sdr_client.py works with GNURadio 3.8.2, the latest version on Raspbian as per date of publishing. sdr_server.py will work on any GNURadio version.

It can be easily recreated in any GNURadio version through these steps

1. Generating the flowchart above in your desired GNURadio Version. 
2. Cpying the python code (the section that is explained above) that is overlayed onto the GNURadio script in sdr_client which can be found in between tb.start() and tb.wait()
3. Change the variables to command line arguements using the sys library.
4. Ensure that the filename is accurate throughout the script

## Screenshots

![Screenshot2](https://user-images.githubusercontent.com/118889521/221858083-daa406ba-24f4-4b34-83eb-aca4db9b7d16.png)

This shows the Terminal of the Raspberry Pi. It will output a message indicating the connection between the server and client. Do not be alarmed by the "0" as this is simply the SDR's way of informing you that the sample rate might be too high and may affect the quality of the frequency sweeps. Lowering the sample rate will reduce the number of "0"s.

<img width="804" alt="image" src="https://user-images.githubusercontent.com/118889521/222168814-5479246d-ac94-4431-b73a-bde0de6cea09.png">
This shows the Terminal of the Sever (in this a Macbook Pro Visual Studio Code). The output can be modified in 2 ways to show "Message from Client: 'Freq: , dBM: '" or just "'Freq: , dBm: '". When you execute the file, the code will comfirm that the server is up an running with a "UDP Server up and running" and then once the Raspberry Pi collects and sends data through Ethernet it will be displayed in 1 of the 2 formats (which can be adjusted by editing the sdr_server.py file, comments have been indicating this).

## Terminal Demonstration
A link to the video can be found here: https://drive.google.com/file/d/18Gwf8aO_eVr3t64fMjhEuFfegfMWZLtG/view?usp=sharing
Similar screenshots have been included in the "Screenshot" section. The first image shows the same annotated image provided above in the "Hardware" section. The 2nd image is the Raspberry Pi Terminal if the sdr_client is executed manually. The first line initialises relevant libaries and the following lines is the comfirmation of the connection with the HackRF SDR. Zeros indicate the sample rate has been set too high. The repetitive lines is the messaged received from the sever indicating that there is a connection established. The video shows a Macbook's VSC (Sever) terminal. Intially the execution fails as the Raspberry Pi takes time to boot up and connect to the ethernet port's IP address. A pop up appears with the Macbook requesting to "Accept Incoming Connection." The terminal then outputs the message from the client. 
