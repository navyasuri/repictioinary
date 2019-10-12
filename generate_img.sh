#!/bin/bash

cd $(pwd)/attnGAN

caption=$1

python2 gen_art.py --input_text "$caption" --data_dir data/coco --model_path models/coco_AttnGAN2.pth --textencoder_path DAMSMencoders/coco/text_encoder100.pth --output_dir ../static/images

cd $(pwd)/../static/images
mv 0_s_0_g2.png generated.png