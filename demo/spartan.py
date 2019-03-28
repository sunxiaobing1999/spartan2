#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Viki Zhao

import sys
import os
import system
import importlib
from ioutil import checkfilegz, loadedgelist


#engine
engine = system.Engine()

#model
anomaly_detection = system.AnomalyDetection()
eigen_decompose = system.EigenDecompose()
traingle_count = system.TraingleCount()

'''Input graph format: 
    src1 dst1 value1
    src2 dst2 value2
    ...
'''


def SFrame(file):
    if (file.find('/') == -1):
        file = "inputData/" + file
    freqfile = checkfilegz(file + '.edgelist')

    if freqfile is None:
        print("Can not find this file, please check the file path!\n")
        sys.exit()

    edgelist = loadedgelist(freqfile)

    return edgelist


def config(frame_name):
    global ad_policy, tc_policy, ed_policy
    frame = importlib.import_module(frame_name)
    
    #algorithm list
    ad_policy = frame.AnomalyDetection()
    tc_policy = frame.TriangleCount()
    ed_policy = frame.EigenDecompose()