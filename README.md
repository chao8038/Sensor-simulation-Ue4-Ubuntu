Sensor data collection in Unreal-Engine4
===

## Table of Contents

* Sensor data collection in Unreal-Engine4
  * Requirement
  * Beginners Guide
  * Feature
    * record road images
      * User story
      * User flows
      * Steps

## Requirement
1. OS: Ubuntu 18.04LTS
2. Python: 3.6.9

## Beginners Guide

If you are a total beginner to this, start here!

### Create project
---
1. Create virtual environment and activate:
Ubuntu:
```shell=
virtualenv venv
source venv/bin/activate
```
windows:
```shell=
virtualenv venv
venv\Scripts\activate
```
2. intstall requirement.txt
Ubuntu:
```shell=
python -m pip install -r requirements.txt 
```
Windows:
```shell=
python -m pip install -r requirements_windows.txt 
```
### Unreal Engine sensor setting
1. move setting.json to document/Airsim/

## Feature 
### record road images
---

#### User story
---

Feature: record road images

* Scenario: record road images and pointclod image automatically
* When the User starts a process
* Then Simulated vehicle of AirSim will start to ahead and record the images automatically

#### User flows
---
![](https://i.imgur.com/DtEP32K.png)

#### Steps
---
1. start the Unreal Project of vehicle simulation.
2. excute the code PythonClient/road_record.py
    * you can see the vehicle will go ahead automatically. and output images will be save to PythonClient/output

