# ZebraCrossDensityDetector

## Introduction
This project is based on [ssd.pytorch](https://github.com/amdegroot/ssd.pytorch).It is aimed to detect the density of people at all types of zebra-crossing.

## Quick Start Guide
To run my program,first you should check for the things below:
- Make sure you have an GPU compatible for the training.
- Make a directory under project root named weights/, download **vgg16_reducedfc.pth** base trainning network.
- Make a directory under project root named **my_dataset/**.
- Under two subdirectories  **my_dataset/zebra_cars** and **my_dataset/zebra_people** , put in your test images.remember to named them with thier index.like,`1.jpg` at image mode.In video mode image saving is auto.
- Download your VOC train dataset to data/, use shell script in data/script to help you do that.

&nbsp;
Also,make sure you have set up your environment as what [ssd.pytorch](https://github.com/amdegroot/ssd.pytorch) project told you.

&nbsp;
If you finish all the above,then you are good to go.

>I can also write a shell script for these steps,maybe later..

### Basic steps of the whole process
1. run `train.py` to train network. feel free to adjust the parameters yourself cause I don't really know what's the best parameter either.
2. run `eval.py` to caculate the APs and mAP to see how precise can the network be.
3. run `density_cal.py` to caculate density of each image.

## Notification
The whole project is just started.Many parts of it can be vary every day.
So I will post my job under `log/`.

## TODO
The part I hope to complete in the near future
- Still to come:
  * [x] Complete support for image and video steam detect.
  * [x] Add ploty figure to draw chart of the result as record.
  * [x] Build an elegant ui based on PyQt5.
  * [ ] Figure out the best wait to caulate density.
  * [ ] Add more chart types for result display if needed.
  * [ ] Do refactor to make codes more readable.
  * [ ] 编写开题和中期检查表
  * [x] Add video read support for current video detect function.

