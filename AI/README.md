# Colony Picker AI

Copyright 2019, iGEM Marburg 2019 <br/>  
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. <br/>
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Setup

To copy the code to your local machine use:

```sh
$ git clone https://github.com/wab8/iGemMarburg2019.git
$ cd iGemMarburg2019/AI
```

**Note:** Make sure you have installed [Docker](https://docs.docker.com/v17.12/install/).

## Create new AI

- Use the image from `training.dockerfile` (`docker build -f training.dockerfile -t <image tag> .`)
- Optionally use the `NUM_STEPS` to choose how many steps to do (default: `100`)
- Images must be labeled (the label needs to be `colony`) and have corresponding `.xml` files

```sh
docker run \
  --rm \
  -v <path to train images>:/tf/models/research/object_detection/images/train \
  -v <path to test images>:/tf/models/research/object_detection/images/test \
  -v <output path of inference graph>:/tf/models/research/object_detection/inference_graph \
  <image tag>
```

## Analyze images

- Use the image from `process.dockerfile` (`docker build -f process.dockerfile -t <image tag> .`)
- There is a pretrained inference graph inside the `trained` folder

```sh
docker run \
  --rm \
  -v <path of inference graph>:/tf/models/research/object_detection/inference_graph \
  -v <path of test images folder>:/tf/models/research/object_detection/test_images \
  -v <output path>:/processed \
  <image tag>
```

### Example

![picture of picked colonies](https://raw.githubusercontent.com/wab8/iGemMarburg2019/master/AI/example.jpg "Picked Colonies")
