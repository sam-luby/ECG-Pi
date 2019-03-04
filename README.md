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


Heart rate variability is an analysis of the beat-to-beat variation. The interval between beats - known as the RR
interval or inter-beat interval (IBI) - is measured in milliseconds and these intervals can be analysed to give a good overall indication of a person’s heart health.

<pic of RR interval> 




