# HackRF SDR Sweep Power Spectral Density

This project contains 2 python files that allow the user to scan the frequencies of the environment using a HackRF SDR and Raspberry Pi to dump this information from the Pi to a Host PC through an ethernet cable (UDP). The project acts like a low-cost spectrum analyser. This project is for users that are interested in analysing the power of frequencies in their environment such as FM Radio, Wifi or simply just noise.

The HackRF SDR can be tuned to a centre frequency and sample rate determined by the user at execution through command line arguments. An example output that will be provided on the Host PC's Terminal: "Message from Client: 'Freq: 8.243e+07 Hz, dBm: -78.215'"

## Table of Contents
# Table of Contents

 - How to Use
 - Installation
   - Requirements
   - Setting up
     - Hardware
     - Setting Up UDP Server 
     - Editing the Files
     - Transferring sdr_client.py to Raspberry Pi
     - Executing the files w/ Command Line Arguments
     - Running File on Boot
 - Documentation
   - Testing Libraries
     - HackRF SDR
     - GNURadio + OsmoSDR
   - How Does the Code Work
   - GNURadio Version Note
 - Screenshots
 - Terminal Demonstration

## How to Use
Description of the files in this repo:

sdr_client.py is the file that will be executed on the Raspberry Pi that will do 99% of the function of this project. It will interface with the HackRF Software Defined Radio (SDR) (More info on the HackRF SDR here: https://greatscottgadgets.com/sdr/), create and work with GNURadio Blocks (More info here: https://wiki.gnuradio.org/index.php/Main_Page), and finally formatting the data and sending the desired output to a UDP Server. 

sdr_server.py provides the user to create a UDP Server that will work over Wireless Lan or Ethernet.

requirements.txt is the Python Environment Requirements for the Raspberry Pi.

flowchart.grc is the GNURadio 3.8 flowchart used to interface with the HackRF SDR through the OsmocomSDR library, compute the FFT of the signal and convert this to Power (dBm) and write it to a binary file alongside a detached metadata file.

## Installation
### Requirements

Libraries Required to Install on Raspberry Pi
```bash
    sudo apt install python3-numpy python3-matplotlib hackrf rtl-sdr gr-osmosdr gnuradio
```

Tested On (Client): Raspberry Pi 3b; Raspbian Version 11 Bullseye; Python Version 3.9.2

Tested On (Server): Macbook Pro Apple M1 Ventura 13.0.01 Python Version 3.11.2

### Setting Up
#### Hardware
![IMG_3938](https://user-images.githubusercontent.com/118889521/222162280-e1afb688-7b47-473c-a9b8-9cc9a26487f2.JPG)
The diagram indicates a Raspberry Pi 3b connected to power, an ethernet cable to the UDP Server PC and the HackRF SDR USB Cable. THe HackRF SDR will also have to be connected to an antenna using the SMA Antenna Port.

#### Setting Up UDP Server
sdr_server.py must output "UDP Server Up and Running" before sdr_client.py is executed. This is can be done by executing this file immediately after the Ethernet Connection has been established but before the raspberry pi starts transmitting data. A screenshot and video have been included below for further reference.

Currently, when you disconnect and reconnect the Ethernet cable on a Macbook, the Macbook will reassign the IP Address of the Server. Hence you must alter the Ethernet connection in the network settings of the Macbook (This will be updated in the future for tutorials for Linux and Windows too). 

1. Click on "details" of the Ethernet connection. 
2. Navigate to "TCP/IP"
3. Change "Configure IPv4" to "Using DHCP with Manual Address"
4. Configure the IP Address as you please. This will be the SERVER ADDRESS you will edit on the sdr_client.py and sdr_server.py files.

An example is shown below. 

<img width="676" alt="image" src="https://user-images.githubusercontent.com/118889521/226114761-43c16796-c10e-44e5-96ae-c2be6532a75d.png">


#### Editing the Files: IP Address + Port Number + Filename
sdr_client.py will be run on the Raspberry Pi and sdr_server.py will be run on the PC that is going to receive the data. Before this, the user must replace key information on the files. 

All 3 of these must be changed on the Client file. Find and replace with your own details: 
1. SERVER IP ADDRESS
    - This will be the Ethernet's IP Address.
2. SERVER PORT
    - A port that isn't being utilised by your PC.
3. YOUR FILE NAME 
    - The directory and file name of where the raw binary data file will be stored.

Only 2 have to be changed on the Server file. Find and replace with your own details:
1. SERVER IP ADDRESS
    - This will be the Ethernet's IP Address.
2. SERVER PORT
    - A port that isn't being utilised by your PC.

#### Transferring sdr_client.py to Raspberry Pi

Using SCP to transfer files wirelessly, such that you can transfer the edited sdr_client.py to the Raspberry Pi.

Details here: https://spellfoundry.com/docs/copying-files-to-and-from-raspberry-pi-and-mac/#:~:text=Copying%20Files%20From%20Raspberry%20Pi%20To%20A%20Mac,-SCP&text=Open%20a%20terminal%20window%20and,the%20filename%20and%20the%20%E2%80%9C.%E2%80%9D

To find the IP Address of the Raspberry Pi to SCP a file follow these steps. 

```bash
    ssh [username]@[hostname].local
```

More details of SSH without an IP Address can be found here: https://www.makeuseof.com/how-to-ssh-into-raspberry-pi-remote/

Once you have established an SSH connection. Run this command. This is the IP Address of the Raspberry Pi. Note this is different from the Server IP Address.

```bash
    hostname -I
```

This IP Address will allow you to transfer files between your Computer and Raspberry Pi.

#### Executing the files w/ Command Line Arguments

sdr_client.py should be run on the Raspberry Pi and will be given command line arguments in the format:
1. Number of SDRs
2. Filename 1
3. Filename 2 [Only if you have 2 SDRs]
4. Server Port
5. IP Address of Server
6. Vector Length
7. Sample Rate
8. Center Frequency of SDR 1
9. Center Frequency of SDR 2 [Only if you have 2 SDRs]

For example:

```bash
    python3 /Users/John/Desktop/Hackrf/sdr_server.py 2 /home/pi/Desktop/sdr1 /home/pi/Desktop/sdr2 20001 169.450.690.82 512 400e6 200e6 600e6
```

#### Running File on Boot
Follow this tutorial for rc.local: https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/

One limitation of starting this script on boot is the lack of flexibility to change the Center Frequency and Sample Rate. You will have to ssh into the pi to customise the centre frequency and sample rate. To terminate the script remove it from rc.local and reboot the Raspberry Pi.

## Documentation

### Testing Libraries
#### HackRF SDR

To ensure that HackRF SDR is working, plug it in and run:
```bash
    hackrf_info
```
More details are here: https://hackrf.readthedocs.io/en/latest/getting_started_hackrf_gnuradio.html

Ensure that the Hackrf One SDR firmware is up to date with the lastest version

Details on how to do so can be found here: https://www.youtube.com/watch?v=0L7H0qu7Zmg&ab_channel=SecureTechware

#### GNURadio + OsmoSDR
Now open GNURadio 3.8.2 (or the latest version available on Raspbian). The included file is the flowchart that will allow you to test osmosdr source.

Open the following file included in the repository: hackrf_sweep.grc

![Screenshot](https://user-images.githubusercontent.com/118889521/221857811-5352b99a-ac51-4bbd-a882-665762195ba6.png)

If this runs properly this will provide a dynamic Power by Frequency graph which indicates that the libraries have been installed appropriately.

### How Does the Code Work
The python script that enables the format and transfer of data will be described here. Firstly, the code opens the binary file with the data format of 32 Bit Floats and stores this as a NumPy array.

```bash
    x = np.fromfile(open(filename), dtype=np.float32)    
```

Next the frequency step of the output is determined by calculating Sample Rate over Vector Length, an example would be: $20e6/1024$. Then a NumPy array is created with a range of $Center Frequency - (Sample Rate)/2$ to $Center Frequency + (Sample Rate)/2$. This will provide a range of the Sample Rate centred around the Center Frequency. This section of the code is shown here.

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
                
                ....... #Establishing UDP Connection Code Omitted for Conciseness
                
                print(msg)
            i += 1
```

#### GNURadio Version Note
sdr_client.py works with GNURadio 3.8.2, the latest version on Raspbian as per the date of publishing. sdr_server.py will work on any GNURadio version.

It can be easily recreated in any GNURadio version through these steps

1. Generating the flowchart above in your desired GNURadio Version. 
2. Copying the python code (the section that is explained above) that is overlayed onto the GNURadio script in sdr_client which can be found in between tb.start() and tb.wait()
3. Change the variables to command line arguments using the sys library.
4. Ensure that the filename is accurate throughout the script

## Screenshots

![Screenshot2](https://user-images.githubusercontent.com/118889521/221858083-daa406ba-24f4-4b34-83eb-aca4db9b7d16.png)

This shows the Terminal of the Raspberry Pi. It will output a message indicating the connection between the server and the client. Do not be alarmed by the "0" as this is simply the SDR's way of informing you that the sample rate might be too high and may affect the quality of the frequency sweeps. Lowering the sample rate will reduce the number of "0"s.

<img width="804" alt="image" src="https://user-images.githubusercontent.com/118889521/222168814-5479246d-ac94-4431-b73a-bde0de6cea09.png">
This shows the Terminal of the Server (in this a Macbook Pro Visual Studio Code). The output can be modified in 2 ways to show "Message from Client: 'Freq: , dBM: '" or just "'Freq: , dBm: '". When you execute the file, the code will confirm that the server is up and running with a "UDP Server up and running" and then once the Raspberry Pi collects and sends data through Ethernet it will be displayed in 1 of the 2 formats (which can be adjusted by editing the sdr_server.py file, comments have been indicating this).

## Terminal Demonstration
A link to the video can be found here: https://drive.google.com/file/d/18Gwf8aO_eVr3t64fMjhEuFfegfMWZLtG/view?usp=sharing

Similar screenshots have been included in the "Screenshot" section. The first image shows the same annotated image provided above in the "Hardware" section. The 2nd image is the Raspberry Pi Terminal if the sdr_client is executed manually. The first line initialises relevant libraries and the following lines are the confirmation of the connection with the HackRF SDR. Zeros indicate the sample rate has been set too high. The repetitive lines are the messages received from the server indicating that there is a connection established. The video shows a MacBook's VSC (Server) terminal. Initially, the execution fails as the Raspberry Pi takes time to boot up and connect to the ethernet port's IP address. A pop-up appears with the Macbook requesting to "Accept Incoming Connection." The terminal then outputs the message from the client.

Note: From boot to UDP data transfer will take approximately 30 seconds.
