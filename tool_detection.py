# -*- coding: utf-8 -*-
"""YOLOv5 - Mongol Tori

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IrG5kH0Y1OQTJTT32MbATdivA-qFlPfQ

# How to Train YOLOv5 on Custom Objects

This tutorial is based on the [YOLOv5 repository](https://github.com/ultralytics/yolov5) by [Ultralytics](https://www.ultralytics.com/). This notebook shows training on **your own custom objects**. Many thanks to Ultralytics for putting this repository together - we hope that in combination with clean data management tools at Roboflow, this technologoy will become easily accessible to any developer wishing to use computer vision in their projects.

### Accompanying Blog Post

We recommend that you follow along in this notebook while reading the blog post on [how to train YOLOv5](https://blog.roboflow.ai/how-to-train-yolov5-on-a-custom-dataset/), concurrently.

### Steps Covered in this Tutorial

In this tutorial, we will walk through the steps required to train YOLOv5 on your custom objects. We use a [public blood cell detection dataset](https://public.roboflow.ai/object-detection/bccd), which is open source and free to use. You can also use this notebook on your own data.

To train our detector we take the following steps:

* Install YOLOv5 dependencies
* Download custom YOLOv5 object detection data
* Write our YOLOv5 Training configuration
* Run YOLOv5 training
* Evaluate YOLOv5 performance
* Visualize YOLOv5 training data
* Run YOLOv5 inference on test images
* Export saved YOLOv5 weights for future inference



### **About**

[Roboflow](https://roboflow.com) enables teams to deploy custom computer vision models quickly and accurately. Convert data from to annotation format, assess dataset health, preprocess, augment, and more. It's free for your first 1000 source images.

**Looking for a vision model available via API without hassle? Try Roboflow Train.**

![Roboflow Wordmark](https://i.imgur.com/dcLNMhV.png)
"""

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/MyDrive/yolov5

"""#Install Dependencies

_(Remember to choose GPU in Runtime if not already selected. Runtime --> Change Runtime Type --> Hardware accelerator --> GPU)_
"""

# Commented out IPython magic to ensure Python compatibility.
# clone YOLOv5 repository
!git clone https://github.com/ultralytics/yolov5  # clone repo
# %cd yolov5

!pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

"""# Download Correctly Formatted Custom Dataset 

We'll download our dataset from Roboflow. Use the "**YOLOv5 PyTorch**" export format. Note that the Ultralytics implementation calls for a YAML file defining where your training and test data is. The Roboflow export also writes this format for us.

To get your data into Roboflow, follow the [Getting Started Guide](https://blog.roboflow.ai/getting-started-with-roboflow/).

![YOLOv5 PyTorch export](https://i.imgur.com/5vr9G2u.png)
"""

!cd yolov5 & pip install -r requirements.txt

#follow the link below to get your download code from from Roboflow
!pip install -q roboflow
from roboflow import Roboflow
rf = Roboflow(model_format="yolov5", notebook="roboflow-yolov5")

import os
os.environ["DATASET_DIRECTORY"] = "/content/datasets"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/MyDrive/yolov5
#after following the link above, recieve python code with these fields filled in
#from roboflow import Roboflow
#rf = Roboflow(api_key="YOUR API KEY HERE")
#project = rf.workspace().project("YOUR PROJECT")
#dataset = project.version("YOUR VERSION").download("yolov5")

# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="fq63jZEwa2gjCmifJQ3W")
# project = rf.workspace().project("mecha-tools-classification-wqhum")
# dataset = project.version(2).download("yolov5")


# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="fq63jZEwa2gjCmifJQ3W")
# project = rf.workspace().project("mecha-tools-dataset-v2")
# dataset = project.version(1).download("yolov5")


# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="fq63jZEwa2gjCmifJQ3W")
# project = rf.workspace().project("mecha-tools-dataset-v3")
# dataset = project.version(4).download("yolov5")


# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="fq63jZEwa2gjCmifJQ3W")
# project = rf.workspace("new-workspace-5ctap").project("rocket-lander-dataset")
# dataset = project.version(1).download("yolov5")


!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="fq63jZEwa2gjCmifJQ3W")
project = rf.workspace("new-workspace-5ctap").project("mecha-tools-v5")
dataset = project.version(1).download("yolov5")

! ls /content/gdrive/MyDrive/yolov5/Mecha-Tools-Dataset-V3-4/

# Commented out IPython magic to ensure Python compatibility.
# this is the YAML file Roboflow wrote for us that we're loading into this notebook with our data
# %cat {dataset.location}/data.yaml
# %cat /content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/data.yaml

"""# Define Model Configuration and Architecture

We will write a yaml script that defines the parameters for our model like the number of classes, anchors, and each layer.

You do not need to edit these cells, but you may.
"""

# define number of classes based on YAML
import yaml
import os
with open(dataset.location + "/data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

#this is the model configuration we will use for our tutorial 
# %cd /content/yolov5/models/yolov5s.yaml

#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# %%writetemplate /content/yolov5/models/custom_yolov5s.yaml

# # parameters
# nc: {num_classes}  # number of classes
# depth_multiple: 0.33  # model depth multiple
# width_multiple: 0.50  # layer channel multiple

# # anchors
# anchors:
#   - [10,13, 16,30, 33,23]  # P3/8
#   - [30,61, 62,45, 59,119]  # P4/16
#   - [116,90, 156,198, 373,326]  # P5/32

# # YOLOv5 backbone
# backbone:
#   # [from, number, module, args]
#   [[-1, 1, Focus, [64, 3]],  # 0-P1/2
#    [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
#    [-1, 3, BottleneckCSP, [128]],
#    [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
#    [-1, 9, BottleneckCSP, [256]],
#    [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
#    [-1, 9, BottleneckCSP, [512]],
#    [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
#    [-1, 1, SPP, [1024, [5, 9, 13]]],
#    [-1, 3, BottleneckCSP, [1024, False]],  # 9
#   ]

# # YOLOv5 head
# head:
#   [[-1, 1, Conv, [512, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 6], 1, Concat, [1]],  # cat backbone P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 13

#    [-1, 1, Conv, [256, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 4], 1, Concat, [1]],  # cat backbone P3
#    [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)

#    [-1, 1, Conv, [256, 3, 2]],
#    [[-1, 14], 1, Concat, [1]],  # cat head P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)

#    [-1, 1, Conv, [512, 3, 2]],
#    [[-1, 10], 1, Concat, [1]],  # cat head P5
#    [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)

#    [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
#   ]

"""# Train Custom YOLOv5 Detector

### Next, we'll fire off training!


Here, we are able to pass a number of arguments:
- **img:** define input image size
- **batch:** determine batch size
- **epochs:** define the number of training epochs. (Note: often, 3000+ are common here!)
- **data:** set the path to our yaml file
- **cfg:** specify our model configuration
- **weights:** specify a custom path to weights. (Note: you can download weights from the Ultralytics Google Drive [folder](https://drive.google.com/open?id=1Drs_Aiu7xx6S-ix95f9kNsA6ueKRpN2J))
- **name:** result names
- **nosave:** only save the final checkpoint
- **cache:** cache images for faster training
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# %cd /content/gdrive/MyDrive/yolov5/yolov5

pwd



# train yolov5s on custom data for 100 epochs
# time its performance
# !python train.py --img 416 --batch 16 --epochs 100 --data /content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/data.yaml --cfg ./models/yolov5s.yaml --weights '' --name yolov5s_results  --cache

!python train.py --img 1388 --batch 16 --epochs 150 --data {dataset.location}/data.yaml --weights yolov5s.pt --cache

"""# Evaluate Custom YOLOv5 Detector Performance

Training losses and performance metrics are saved to Tensorboard and also to a logfile defined above with the **--name** flag when we train. In our case, we named this `yolov5s_results`. (If given no name, it defaults to `results.txt`.) The results file is plotted as a png after training completes.

Note from Glenn: Partially completed `results.txt` files can be plotted with `from utils.utils import plot_results; plot_results()`.
"""

# Commented out IPython magic to ensure Python compatibility.
# Start tensorboard
# Launch after you have started training
# logs save in the folder "runs"
# %load_ext tensorboard
# %tensorboard --logdir runs

!pip install PyYAML==5.3.1
!pip install matplotlib==3.2.2

import torch 

model = torch.hub.load('ultralytics/yolov5', 'custom', path='/content/gdrive/MyDrive/yolov5/yolov5/runs/train/exp3/weights/last.pt', force_reload=True)

"""### Curious? Visualize Our Training Data with Labels

After training starts, view `train*.jpg` images to see training images, labels and augmentation effects.

Note a mosaic dataloader is used for training (shown below), a new dataloading concept developed by Glenn Jocher and first featured in [YOLOv4](https://arxiv.org/abs/2004.10934).
"""

# first, display our ground truth data
print("GROUND TRUTH TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/test_batch0_labels.jpg', width=900)

# print out an augmented training example
print("GROUND TRUTH AUGMENTED TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/train_batch0.jpg', width=900)

"""#Run Inference  With Trained Weights
Run inference with a pretrained checkpoint on contents of `test/images` folder downloaded from Roboflow.
"""

# Commented out IPython magic to ensure Python compatibility.
# trained weights are saved by default in our weights folder
# %ls runs/

# Commented out IPython magic to ensure Python compatibility.
# %ls runs/train/yolov5s_results/weights

pwd

# when we ran this, we saw .007 second inference time. That is 140 FPS on a TESLA P100!
# use the best weights!
# %cd /content/yolov5/
!python detect.py --weights runs/train/yolov5s_results/weights/best.pt --img 416 --conf 0.4 --source ../Mecha-Tools-Classification-2/test/images

#display inference on ALL test images
#this looks much better with longer training above

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

"""# Export Trained Weights for Future Inference

Now that you have trained your custom detector, you can export the trained weights you have made here for inference on your device elsewhere
"""

from google.colab import drive
drive.mount('/content/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cp /content/yolov5/runs/train/yolov5s_results/weights/best.pt /content/gdrive/My\ Drive

"""## Congrats!

Hope you enjoyed this!

--Team [Roboflow](https://roboflow.ai)
"""

# model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp15/weights/last.pt', force_reload=True)

# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
    
#     # Make detections 
#     results = model(frame)
    
#     cv2.imshow('YOLO', np.squeeze(results.render()))
    
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

img = '/content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/train/images/Hammer--1227-_JPEG.rf.54bde77a39692af773cf16365b46cd76.jpg'

results = model(img)
results.print()

from matplotlib import pyplot as plt
import numpy as np

# %matplotlib inline 
plt.imshow(np.squeeze(results.render()))
plt.show()

img3 = '/content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/train/images/Screwdriver--1402-_JPEG.rf.0ec8058d36494b23fc0dfe372f95cdbf.jpg'

results3 = model(img3)
results3.print()

from matplotlib import pyplot as plt
import numpy as np

# %matplotlib inline 
plt.imshow(np.squeeze(results3.render()))
plt.show()

img4 = '/content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/train/images/Wrench--657-_JPEG.rf.191af72caa353306ea11032cb82956ca.jpg'

results4 = model(img4)
results4.print()

from matplotlib import pyplot as plt
import numpy as np

# %matplotlib inline 
plt.imshow(np.squeeze(results4.render()))
plt.show()

img4 = '/content/gdrive/MyDrive/yolov5/Mecha-Tools-Classification-2/train/images/Wrench--657-_JPEG.rf.191af72caa353306ea11032cb82956ca.jpg'