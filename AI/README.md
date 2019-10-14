# Colony Picker AI

## Create new AI

- Use the image from `training.dockerfile` (`docker build -f training.dockerfile -t <image tag> .`)
- Optionally use the `NUM_STEPS` to choose how many steps to do (default: `100`)
- Images must be labeled and have corresponding `.xml` files

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

```sh
docker run \
  --rm \
  -v <path of inference graph>:/tf/models/research/object_detection/inference_graph \
  -v <output path>:/processed \
  <image tag>
```
