# -*- coding: utf-8 -*-
"""
add your model discription and calculate the computation!
"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D
from keras.engine.input_layer import Input
import keras

# VGG
model = keras.applications.vgg16.VGG16()

# make lists
layer_name = []
layer_flops = []
layer_params = []

# bunch of cal per layer
def count_linear(layers):
    MAC = layers.output_shape[1] * layers.input_shape[1]
    if layers.get_config()["use_bias"]:
        ADD = layers.output_shape[1]
    else:
        ADD = 0
    return MAC*2 + ADD

def count_conv2d(layers):
    # number of conv operations = input_h * input_w / stride
    numshifts = int(layers.input_shape[1] * layers.input_shape[2] / layers.get_config()["strides"][0])
    
    # MAC/convfilter = kernelsize^2 * InputChannels * OutputChannels
    MACperConv = layers.get_config()["kernel_size"][0] * layers.get_config()["kernel_size"][1] * layers.input_shape[3] * layers.output_shape[3]
    
    if layers.get_config()["use_bias"]:
        ADD = layers.output_shape[1] * layers.output_shape[2] * layers.output_shape[3]
    else:
        ADD = 0
        
    return MACperConv * numshifts * 2 + ADD

# TODO: relus

# run through models
for layer in model.layers:
    layer_name.append(layer.get_config()["name"])
    if "dense" in layer.get_config()["name"]:
        layer_flops.append(count_linear(layer))
    elif "conv2d" in layer.get_config()["name"]:
        layer_flops.append(count_conv2d(layer))
        
model.summary()
        
print("layers:", layer_name)
print("FLOPS:", layer_flops)

# TODO: summarize as dict