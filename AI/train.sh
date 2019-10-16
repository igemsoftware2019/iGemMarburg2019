#!/usr/bin/env bash

# Copyright 2019, iGEM Marburg 2019
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

mkdir /tf/trained_model

cd /tf/models/research/object_detection && python xml_to_csv.py

cd /tf/models/research && python generate_tfrecord.py \
  --csv_input=object_detection/images/train_labels.csv \
  --image_dir=object_detection/images/train \
  --output_path=mscoco_train.record
cd /tf/models/research && python generate_tfrecord.py \
  --csv_input=object_detection/images/test_labels.csv \
  --image_dir=object_detection/images/test \
  --output_path=mscoco_val.record

NUM_STEPS=${NUM_STEPS:-100}

cd /tf/models/research

python model_main.py \
  --logtostderr \
  --model_dir=/tf/trained_model \
  --num_train_steps=${NUM_STEPS} \
  --train_dir=object_detection/training/ \
  --pipeline_config_path=object_detection/training/faster_rcnn_resnet101_coco.config

suffix=$(ls /tf/trained_model | grep ".index" | tail -1 | cut -d '.' -f 2 | cut -d '-' -f 2)

cd /tf/models/research/object_detection
python export_inference_graph.py \
  --input_type=image_tensor \
  --pipeline_config_path=training/faster_rcnn_resnet101_coco.config \
  --trained_checkpoint_prefix=/tf/trained_model/model.ckpt-${suffix} \
  --output_directory=inference_graph
