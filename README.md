# ZebraCrossDensityDetector

## Introduction
This project is based on [ssd.pytorch](https://github.com/amdegroot/ssd.pytorch).It is aimed to detect the density of people at all types of zebra-crossing.

## Quick Start Guide
To run my program,first you should check for the things below:
- Make sure you have an GPU compatible for the training.
- Make a directory under project root named weights/, download **vgg16_reducedfc.pth** base trainning network.
- Use `快速部署` to set up necessary data folders for detecting.
- Download your VOC train dataset to data/, use shell script in data/script to help you do that.

&nbsp;
Also,make sure you have set up your environment as what [ssd.pytorch](https://github.com/amdegroot/ssd.pytorch) project told you.

&nbsp;
If you finish all the above,then you are good to go.


## Basic steps of the whole process
1. Run `train.py` to train network. feel free to adjust the parameters yourself cause I don't really know what's the best parameter either.
2. Run `eval.py` to caculate the APs and mAP to see how precise can the network be.
3. Run `gui.py` and choose your mode to calculate the density of image or video stream.

## Notification
1. Currently the image directory function will need you to put images under `my_dataset/zebra_people` and `my_dataset/zebra_cars`.Do it with `快速部署` menu.
2. Currently the video `camera` mode only support type `one_zebra`,which means it won't caculate the cars in the camera.This program is only a simulation of traffic camera ,so it is meaningless to let it compatible with detecting cars and people on camera at the same time.In a word,no car will be in the dorm or classroom while testing.It should have two cameras,one for people caculation and the other for cars on the road.Then combine them to do the final prediction,just like what `image directory` mode do.So the best way to use the program is to use mode `video_file`.
3. Make sure the cars and people image have **the same count**.If not,it may have an effect on final result.

## How is the whole process of my design
1.First the program **do the detect**.
&nbsp;

2.Then program **do caculation of the detect**,give user the density of each image.
&nbsp;

3.And according to whether is gaofeng or not,it decide whether people or cars can go first when the density **exceed** the max density.
&nbsp;

4.Finally,the max density will **auto adjust** to best fit current road condition under pre-specified mode.


## New features compared to last push!
`多线程显示界面去卡顿` ，`进度条（模拟）显示运行时长`

## TODO
The part I hope to complete in the near future
- Still to come:
  * [x] Figure out the best wait to caulate density.
  * [x] Do refactor to make codes more readable.
  * [x] Combine `auto_prepare.py` with user interface.
  * [x] 编写开题和中期检查表
  * [ ] 完善README
  * [x] 完成论文初稿


