# Cybersecurity Mini-Project
This repository is created for the mini project integration related to the "Cybersecurity" subject at the University of Salerno. 

## Group Members
* [Michele Barbella](https://github.com/michelebarbella)
* [Andrea Valitutto](https://github.com/andrewvali)
* [Salvatore Ventre](https://github.com/salventre)
___
# Problem Description
The integration work consists of a mini project related to [Proximity Tracing DP-3T protocol](https://github.com/DP-3T/documents), with the following target: the Government Authority is using a decentralized contact tracing system, like DP-3T, and wants to do a modification to have on the Server a counter of the risk notifications displayed on users' devices.</br>
The main aspects of this project are:
* identify *Privacy* and *Integrity* properties.
* design a mechanism for risk notification counter.
* analyze the design with respect to properties.
* implement a small module that show the mechanism.

The collection of these data would help the optimization process of resources allocation. In fact, estimating the number of users that the system will notify can help the National Health Service to allocate its availabilities efficiently for fight Covid-19.

## Documentation
For more information, read the [report](https://github.com/unisa-project-barbella-valitutto-ventre/Cybersecurity-MiniProject/tree/main/doc).
___
# How to launch a Demo
Here are some steps to follow if you want to launch a simulation of the developed module. First of all, you have to launch a Configuration Script, then launch the demo.

### Prerequisites
*   [Python](https://www.python.org/downloads/) ≥ 3.6
*   [OpenSSL](https://www.openssl.org/source/)

### Configuration Script
This script is implemented to prepare initialize the workspace. In particular, it removes previous old files, builds the new tree directory, initializes the notificatios counter to ZERO, installing the libraries (in the case you don't have them). Finally, the script creates new certificates for entities and populates the database with updated entries. In order to prepare the workspace you need to run this script with these commands:
```shell
cd ~/Cybersecurity-MiniProject
./configurationScript.sh
```

### Launch the Demo
Now it is possible to launch a demo to see how the module works. If you are using Ubuntu, you can simply launch the demo with a script. But if you use Ubuntu, but you are not interested in the use of the script, you can follow the step in section **with Linux Distros** that shows how to launch a simulation with every Linux distro (including Ubuntu).

#### with Ubuntu
To make things easier to run, we have decided to integrate the ```runSimulation.sh``` script that automatically opens three terminal windows and runs the implemented code. The only thing to do is to run the following command:
```bash
./runSimulation.sh
```
#### with Linux Distros
If you want to launch a demo, you have to open three terminal and follow these steps:</br>
* Terminal 1:
```bash
cd authorityServer/
python3 authorityServer.py
```
* Terminal 2:
```bash
cd analyticsServer/
python3 analyticsServer.py
```
* Terminal 3:
```bash
cd client/
python3 client.py
```

##### Barbella, Valitutto, Ventre
