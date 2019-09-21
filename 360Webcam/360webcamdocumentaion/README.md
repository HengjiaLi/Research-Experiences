# 360 Webcam Summary
**This is a weekly summary for the 360 WebCam project.** 

**For further detailed documentation regarding all the testing for each subsystem and why previous iterations have not worked or have been changed, please see [here](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/07_Handover%20Document/Documentation%20process.md). This documentation will be part of the final Handover Document.**

**For further details regarding tasks completed and their contributors, please see [here](01_Team Structure/work log.md)**

## Week 1
No tutorials or meetings had been conducted. Team members were assigned the [360-degree Web Conferencing Device project](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/Meeting%20logs/ENGN4221_Projects_2019-02-27.pdf). 
(Project description may be viewed on page 4)



<br>

## Week 2
### Tues 5/3 
**Outline**

At such an early stage of the project, the team focused more on the Governance maturity (communication and decision-making) 
before any requirements or project outputs are outlined. Project scope was to be defined during the upcoming meeting with client.

**Determining team decision-making and communication methods**

During the first [tutorial](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_05032019.pdf), 
all group members agreed on a democratic approach for future critical decisions to be made regarding the project. This approach was chosen so all individual member ideas and proposals can be considered equally.
Two weekly meeting times
were decided based on each member's availability: 
- Monday 1:30PM with the client 
- Friday 2:00PM for just the team. 

For the Shadow Groups, each member chose a group based on personal preference:
- Jiawei, Jose, Jireh chose the Floating Buoy project
- Hongjian, Ben, Yilin, and Minh chose the VR project

In terms of online communication method, Facebook Messenger was chosen due to 
ease of use and accessibility for each member. 

### Fri 8/3
**Outline**

[Meeting log 8/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_08032019.pdf)

For the first team meeting,
the team drafted technical approaches that could be used to achieve the project goals set out in the [project description](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/Meeting%20logs/ENGN4221_Projects_2019-02-27.pdf) (page 4). 
Note that the ideas at this stage were very rough and to be refined later when the formal project scope and requirements would be given by the client. 

**Determining potential device components**

Due to a team member already owning a Raspberry Pi 3B+ (microprocessor device), the team decided that selecting potential imaging/audio hardware
should be structured around this microprocessor due to its ease of use and capability for testing. Potential components for the prototype device were thus considered:

|       Function                |       Potential component     |       Considerations and reasoning        |
|   ---                         |       ---                     |       ---                 |      
|       Microprocessor          |   Raspberry Pi 3B+            |   Inexpensive (~$50), scalable in terms of testing and prototyping
|       Visual input            |   USB based cameras                    |      Will require 4-5 cameras to capture a 360 degree view ($7-60 ea, depending on 360-1080p quality)
|       Audio input             |   1. Multichannel input audio interface <br> 2. Rotating microphone <br> 3.Multiple USB microphones <br> 4. Respeaker 4-Mic Array for Raspberry Pi  | 1. Expensive (~200), possesses pre-existing algorithm <br> 2. Medium cost (~$100) <br> 3. Cost effective (~$6 ea), requires supporting algorithm/code <br> 4. Cost effective ($24.90), specifically built for use with Raspberry Pi  
|       Other                   |  USB Hub         |    Cheap (~$10), required to divide USB ports 


Based on these potential components, the calculated estimated budget is given:
1. Min: $112.9 (Sum of cheapest components)
2. Max: $500 (Sum of expensive components)

<br>

## Week 3
### Mon 11/3 
**Determining project goals and deliverables**

[Meeting log 11/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_11032019.pdf)

During the first client meeting, the project scope was discussed with the client, with questions outlined in the [previous meeting log](02_Meeting Logs/01_March/Meeting_Minutes_08032019.pdf) being asked.
The project goal was therefore defined as follows: **to develop a 360-degree camera system for web conferencing, allowing clients to focus on the appropriate parties based on sound localisation**.
The task is to be accomplished by combining several physical devices and existing open source libraries. The core project deliverables were thus identified as a
functional prototype of the device, alongside an instruction document for device replicability. 

**Determining project requirements**

Key client requirements were identified as follows:
1. USB Powered, if not then AC current or battery for portability
2. Video output: H264 video format. Video quality: 1080p desired, 720p acceptable
3. Ability to reduce noise from external sources to avoid sound feedback
4. Device must cost <$300 in total
5. Capability to plug and play with no extra software required
6. Combine multiple sources of videos and present multiple viewpoints at once
7. Project should be open sourced
8. Simple to build and operate. Proper documentation to ensure it is replicable
9. The device should be easy to upgrade in the future


**Sub-team and subsystem planning**

Based on these initial requirements, the project was divided into five key subsystems, with each member
being delegated a responsibility (*See Table below*). In conjunction with the information discussed last meeting, 
the team also discussed the potential hardware components needed to meet these requirements:


|   Sub-team                            |   Team members            |       Component       |       Satisfied client requirement        |
|   --------                            |   --------                |       --------        |   --------
|   Sound (direction of arrival)        |       John, Jose          |       Respeaker 4-Mic Array       | Requirements 4, 5
|   I/O (file conversion)               |       Link, Jordan, Ben   |       Raspberry Pi 3B+               | Requirements 1, 4, 5, 6, 9  
|   Image (processing)                  |       Link, Jordan, Ben   |       USB based web camera               | Requirements 2, 3, 4, 5, 6 
|   Assembly (modelling/manufacturing)  |       Minh, Jireh         |       3D - printed structure/casing               | 
|   Documentation                       |       Minh, Jireh         |       x               | Requirements 7, 8, 9

(Tasks were then delegated according to these subsystems)

<br>

## Week 4
**Coding template for camera stitching system**

The camera subsystem can be divided into 2 classes: data_receiver and configuration_reader.

1. data_receiver:
This class defines the behaviour of the program about how the program reads input from cameras.
It is also possible to further integrate the audio input into this class.



2. configuration_reader:
This class defines how the program behaves depending on different user input.
The user can fully control the program's behaviour by editing the configuration file 
instead of going through the coding.
The current configuration options include a spd-say enabler and the cameras
index selection.

We then set a main function that utilises these two classes to display and stitch the
images from 2 webcam. 

**Current issue**

The stitching causes a big delay in processing (about 0.5 sec even on E5 computer). It is hard to get it work in real-time.

### Mon 18/3

[Meeting log 18/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_18032019.pdf)

The Raspberry Pi microprocessor is unable to process more than two 90 degrees at 720p resolution concurrently. 
The team initially considered using an additional Raspberry Pi as a secondary processor, this was later scrap in favour of utilising wide angle camera.

The [Concept of Operations](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/04_Design%20Source/concept%20of%20operation/Concepts_of_Operations_-_Final_Signed.pdf)
was presented to the client and was approved with positive feedbacks.


### Fri 22/3

[Meeting log 22/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_22032019.pdf)

The initial design of the 360 degrees web conferencing system utilised 4 cameras for the visual input, 
this solution was found to be limited by the Raspberry Pi computational power. Therefore, the team proposed three possible alternatives for presenting to the client.
1. Use a wide view camera lens on top of a single camera to increase FOV,
2. To continue with the image, the initial video feed will be used to create a downscale mapping. From this we can identify homography for stitching the image,
3. Using 3 x 120 degree cameras to achieve an approximate 300 degrees view.

A project budget was calculated for each of the option above for presenting to the client. 

<br>

## Week 5
**Camera switching system**

The output of this system is 3 video windows that show 2 webcam and the camera switched by embeded algorithm depending on the sound arrival direction.

To make this system work, the following packages are needed:

'''opencv3, numpy, pyaudio, pyusb'''


**Audio configuration**

Since we don't have audio input at this stage, the video only has image
stream.

**Image processing configuration**

This system export image from webcam, display them, and switch based on
audio direction from audio processing result.

There are about 0.5 sec lag in this current design. The image quality is 
acceptable for online conference.

**Current issue**

The result from DOA is not stable and sensitive to noises. We need a better algorithm for determining the sound direction, as well as sound cancellation function.


### Mon 25/3

[Meeting log 25/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_25032019.pdf)

The alternative options was proposed and received support from the client to proceed.  
The client acknowledges the increased processing time for more cameras, and agrees with this solution for requiring less parts/expenses. 
The team has therefore collectively decided that this will be the approach used going forward in the prototyping stage.



### Fri 29/3

[Meeting log 29/3](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/01_March/Meeting_Minutes_29032019.pdf)

Anonymous reviews from the audit provided some good points of possible improvement
for the group. A list of action items (as aforementioned) were produced to be follow up by
the team where possible and response were given where not applicable.


<br>


## Week 6

### Mon 1/4

[Meeting log 1/4](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/02_April/Meeting_Minutes_01042019.pdf)

Through the client's approval, the team has purchased the ELP OV 2710 (180 degree camera). The cost is $121. As
aforementioned, this is the last meeting with the client for a month due to his travel overseas.

The camera was renegotiate over email and both the team and client settled on AHD digital video camera (fish-eye camera). The cost is $93.

### Fri 5/4
**Determining a coherent documentation for the project**

[Meeting log 5/4](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/02_April/Meeting_Minutes_05042019.pdf)

The team has developed a more coherent documentation process for software and hardware
<br>
1) A document outlining a clear method to follow to reproduce the product (still to be created)
2) A more [detailed documentation](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/07_Handover%20Document/Documentation%20process.md) regarding all the testing for each subsystem and why previous iterations have not worked or have been changed 

## Midsem break - Week 1

### Fri 12/4
**Testing new fish-eye camera**

[Meeting log 12/4](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/02_April/Meeting_Minutes_12042019.pdf)

As may be viewed in the meeting log, the AHD digital video camera (fish-eye camera) arrived, and was tested. Placed on a table approximately 70cm in height, 
the FOV of the camera was found to be approximately 3.5m in radius. Additionally, the face detection algorith mis functional although experiences slight delay. 

## Midsem break - Week 2

### Fri 19/4
**Planning assembly of hardware components**

[Meeting log 19/4](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/02_April/Meeting_Minutes_19042019.pdf)

Based on the hardware component dimensions, the team drafted a design to be created through 3D modelling. 

## Week 7 

### Fri 26/4
**Team task review**

[Meeting log 26/4](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/02_April/Meeting_Minutes_26042019.pdf)

**Note: At this stage of the project, the team is focused less on governance of the project, and more towards completing the tasks and project outputs.
From this point, more Task Review and minor decisions regarding sub-team task delegation will be made, as will be evident in this meeting log and for 
the coming meeting logs in the next few weeks.**

## Week 8

### Fri 3/5
[Meeting log 3/5](02_Meeting Logs/03_May/Meeting_Minutes_03052019.pdf)

The team looked through the assessment guide together, and planned core repository changes to be made. 

## Week 9 

### Thurs 9/5
[Meeting log 9/5](02_Meeting Logs/03_May/Meeting_Minutes_09052019.pdf)

Team planned what to demonstrate to the client in the next meeting (first meeting in a month since client was overseas).
Critical issues encountered and preparation for the poster was conducted. 

### Fri 10/5
**Discussing final deliverable with client**

[Meeting log 10/5](https://gitlab.cecs.anu.edu.au/u5613613/360webcamdocumentaion/blob/master/02_Meeting%20Logs/03_May/Meeting_Minutes_10052019.pdf)

Client recognises knowledge barrier for software and coding required, that is outside the scope of this project. At this point, client wants 
the team to show that the device is feasible on a Linux platform as a proof of concept more than a complete product. The device will have to enter another phase,
perhaps for another project for students in a Software Engineering background. 

## Week 10 

### Fri 17/5
**Creating presentation poster**

[Meeting log 17/5](02_Meeting Logs/03_May/Meeting_Minutes_17052019.pdf)

The team has created the presentation poster, and is preparing for the upcoming showcase. 
