# RPI-Python
Master's thesis project (ME Electronic &amp; Computer Engineering)

**Thesis title**: _IoT Device for Electrocardiography Summary Statistics Monitoring_

**Submitted**: April 2018

## Project Aim:
The aim of this project was to propose and develop a solution to the problems associated with heart monitoring. The focus was on creating a novel solution for electrocardiography to provide preliminary or inital results, giving indidations of underlying cardiac issues so the patient can be referred to a cardiologist. The main consideration was to use low-cost components, which would allow the device to be used in a patient's home as well as in low income countries and regions.

The project focuses on two main objectives:
* The hardware used to capture/store the heart data.
* The softare used to analyse the patient's data, performing signal processing and unconver any underlying abnormalities.


## Motivation:
The motivation behind this project is about introducing a novel solution to the growing problem of cardiovascular (heart) diseases (CVDs). CVDs are the leading cause of mortality in the world, amounting to a total of approximately 17 million deaths globally - or 32% of all moralities. More than 80% are in low to middle-income countries such as parts of Asia, Eastern Europe and North Africa. Clearly, the less wealthy are more at risk because many do not have access to proper healthcare.


The ability to automate the monitoring process could help to reduce cardiovascular disease mortality rate, as well as to reduce the healthcare costs associated.

## Background and Theory:
### Electrocardiography
This project is based heavily on electrocardiography. Electrocardiography (ECG) is one of two main methods of heart monitoring - the other being photoplethysmography (PPG), a light-based monitoring method used by smartphones and fitness wristbands. ECG is used more in medical devices due to its increased accuracy and ability to provide more metrics compared to PPG. 


Electrocardiography (ECG) is the process of measuring the small electrical signals that are a result of the activity of the heart’s muscles, known as biopotentials. It is one of the most basic forms of non-intrusive diagnosis in medicine and is usually performed by placing small electrodes on the surface of a patient’s skin. The electrodes of an ECG machine record these changing biopotentials and the signal is represented in the form of a moving voltage versus time graph. The conventional ECG machine uses as 12-lead setup. Variations of this exist, using 5-lead or even the 3-lead configuration used in this project.


### Electrocardiogram Analysis
A typical ECG signal is represented in the form of a _PQRST_ waveform, where each letter represents a different section of the cardiac cycle. Analysis of this waveform can reveal a lot about a patient's health.
* The P wave is due to the depolarisation of the atria of the heart.
* The QRS complex is a result of the depolarisation of the left and right ventricles. The increased amplitude of the QRS complex is due to the ventricles’ larger muscle mass compared to the atria, therefore producing larger biopotentials.
* The T wave represents the repolarization of the ventricles.

<pqrst wave pic>
  

The image above shows the general shape of an ECG signal, but is unrealistic due to the absense of noise. In reality, noise exists due to the patient's movement/respiration, power line interference and muscle noise from muscles contracting in close proximity to the heart.


### Heart Rate Variability Analysis
Heart rate and heart rate variability are very different metrics. Heart rate (pulse) simply measures the averate number of beats per minute (BPM) of a patient. Since it is an average, it ignores the variation in intervals between successive beats and is not a great metric for cardiac analysis.


Heart rate variability is an analysis of the beat-to-beat variation. The interval between beats - known as the _RR_
interval or inter-beat interval (IBI) - is measured in milliseconds and these intervals can be analysed to give a good overall indication of a person’s heart health.

<pic of RR interval> 


The autonomic nervous system contains parasympathetic and sympathetic nerves which affect a human’s heart rate. Without the autonomic regulation, a resting heart rate would be around 100 BPM, known as the intrinsic heart rate. However, the _parasympathetic nervous system_ (PSNS) lowers the resting heart rate to around 70BPM. During intensive exercise, the _sympathetic nervous system_ (SNS) increases the rate rate.

HRV is the analysis of the balance between the PSNS and SNS. A high HRV is an indication of a healthy autonomic nervous system and cardiovascular response, that the heart can effectively change rate depending on the activity level and
indicates a greater cardiovascular fitness and more resilience to stress or disease.
On the contrary, a low HRV indicates the PSNS and SNS are not properly balanced and that the patient is more susceptible to heart attacks, stress, strokes etc.

Various methods of heart rate variability analysis exist, and can mostly be separated into two main categories: time-domain analysis and frequency-domain analysis. Time-domain analysis methods are more commonly used in the medical field
and are based on the beat-to-beat intervals of the ECG signal. In this project, analysis is done purely in the time-domain.


### QRS Detection
The QRS complex is the most promimant feature of the ECG signal due to its high amplitude, and as such, it is the basis of most ECG algorithms. One such QRS detection algorithm is Pan Tompkins algorithm, a series of signal processing techniques for correctly identifying QRS complexes, was developed for devices with very low processing power. The QRS detection algorithm used in this project is based heavily on Pan Tompkins algorithm.


### Internet of Things
One of the key aspects of this project revolves around the Internet of Things (IoT), which is the idea of “anything that can be connected, will be connected”. The IoT has seen billions of new devices connected to the internet in recent years, can be attributed to better networking infrastructure to wirelessly connect devices, the introduction of cloud computing
for easily scaling processing resources and, most notably in the wearable industry is Moore’s Law, which is an observation of the number of transistors on an integrated circuit doubling approximately every two years, resulting in small but powerful
devices. 

The idea of the Internet of Things is used in this project, to allow for remote and continous monitoring over the internet. Cardiac results are uploaded to a private cloud which can be monitored by a physician. 


## Methodology
### Hardware
#### Rasperry Pi
The first consideration for the project was to decide the hardware used to collect and process the ECG data. The main three features required were low cost, low power and small form-factor. The device has to perform a range of different tasks:
* Interface with a seperate 3-lead ECG sensor.
* Sample the ECG signal at an appropriate rate.
* Perform analogue-to-digital conversion of the ECG signal.
* Run an algorithm to perform QRS peak detection of the ECG signal.
* Run an algorithm to perform heart rate variability (HRV) analysis on the ECG signal.
* Upload the results of the analysis to the cloud.


Initially an Arduino Uno - a simple microcomputer with no graphical interface that runs one program continously - was used.
The Arduino was then removed in favour of a Raspberry Pi (although I added functionality to allow Arduinos to gather the data and store it on a PC). The Pi is a general purpose computer that runs a Linux-based operating system that can run several programs simultaneously and provides a graphical interface to the user. The Pi had several significant advantages over the Arduino including higher processing power, a GUI, ability to run many programming languages and much higher storage capacity. The Pi allowed me to write most of the algorithms in Python and use many of the existing Python modules online, rather than writing everything from scratch.

#### Analogue-Digital Converter
The main disadvantage of the Pi is that it does not feature an on-board analogue-digital converter (ADC). A third-party ADC must be used to convert the analogue biopotential signals into digitised values. The MCP3008 ADC was used in this project, due to its low price and easy compatibility with the Pi. The MCP3008 can provide a sampling rate of 200k samples per second, with a 10-bit resolution - meaning the digitised ECG signal will be represented by values in the range 0 to 1023. The ADC uses a reference voltage - 5V for this project - to generate the output digitised value. 5V/1023 means there is a step size of approximately 4.88mV.


Communication between the ADC and the Raspberry Pi is achieved using the _serial peripheral interface_ (SPI) protocol. The SPI protocol is for serial communication in embedded systems, microcontrollers and integrated circtuits. The Raspberry Pi uses GPIO (general purpose in/out) pins for SPI communication. Four pins are used for SPI communication:
* MOSI - Master Out Slave In (data from PI to ADC).
* MISO - Master In Slave Out (data from ADC to PI).
* SCLK - Serial Clock (keep Pi and ADC in synch).
* CE - Chip Enable (used by Pi to select which device to interface with).


#### ECG Sensor
A third-party ECG sensor was used for this project. The low-cost sensor uses a 3-lead configuration to acquire ECG signals. The 3-lead configuration is suitable for this project as I use HRV analysis which only requires a 3-lead signal. The sensor uses an integrated signal-conditioning circuit to amplify ECG signals and remove unwanted noise.


The image above shows the placement of electrodes for the 3-lead sensor. The three limb electrodes - denoted I, II and III - form an Einthoven’s triangle at the right arm (RA), left arm (LA) and left leg (LL). The ECG signal we then see is a combination of these seperate potentials. 
1. Lead I: between the right and left shoulders.
  i. _I = LA − RA_
2. Lead II: between the right arm and left leg.
  ii. _II = LL − RA_
3. Lead III: between the left shoulder to the left leg.
  iii. _III = LL − LA_
  
 
### Software
The majority of the software is written in Python. The main reason for this is that there are a huge amount of modules for interfacing with various modules like the ADC, as well as modules for signal processing and data analysis.


<program structure>
  
The above image shows the basic program flow. Executing the main file allows the user to choose the sampling rate, the lenght of time to record for, and the mode in which the program will run.
1. Raspberry Pi mode (recording live data and analysing/storing data on the Pi).
2. Arduino mode (recording live data using the Arduino, analysing/storing data on a PC or Pi).
3. Debug mode (feed the program historical data, useful for debugging and experimenting).


The digitised ECG data is stored in a _.csv_ file, which the program reads from after the recording has finished. The filename records the duration of the recording as well as the date and time it was run. Following analysis, the data will be removed or stored if abnomolies are detected.

The data read from the file is scaled to the range 0 to 1023 before any processing or analysis is done. This allows for different ECG sensors/ADCs/datasets to be used - increasing the usefulness of the program. The data is loaded into a pandas dataframe.

#### Pan Tompkins
The Pan Tompkins algorithm is then used on the ECG data for feature classification. The derivative-based PT algorithm is a   series of singal processing steps to detect QRS peaks in the signal. The algorithm recognises QRS complexes based on analysis of the slope, amplitude and width.
Pan Tompkins algorithm was chosen as it very accurate, computationally efficient and well-documented. The algorithm was implemented in Python for this project. PT algorithm starts by filtering out unwanted noise before amplifying the QRS complex. Finally, a decision algorithm is used to denote where a peak is located in the signal. 

<pan tomp flow picture>
 
The Pan Tompkins algorithm follows the processing steps shown above. 
1. A band-pass filter, in the form of a low-pass cascaded with a high-pass, is used to filter the noisy input data.
2. The signal is then differentiated to identify the large slopes associated with the _QRS_ complexes of a normal ECG signal. This process suppresses the low-frequency components of the ECG signal, while amplifying the high-frequency components. The result is an ECG signal with attenuated _P_ and _T_ waves, with amplified _QRS_ complexes.
3. The squaring operation provides non-linear amplification of the signal. The ECG signal is squared point-by-point, resulting in a signal that is all positive and emphasises the high frequencies found in the _QRS_ complex.
4. A moving average, or rolling mean of the signal is calculated. By choosing an appropriate window size, the aim is to produce a single peak which represents a QRS complex.
5. The moving average signal is used as a threshold for detecting QRS complexes. The algorithm goes though each value in the derivated signal and checks if the amplitude is greater than the moving average signal at that time, which indicates a peak is detected. The position of all detected R-peaks are stored in the results dictionary.


Finally, the RR intervals are calculated using the positions of the detected peaks.
The interval is measured by getting the number of samples between each pair of
successive identified peaks and converting the interval, measured in samples, into
a time interval measured in milliseconds.


#### Heart Rate Variability Analysis
