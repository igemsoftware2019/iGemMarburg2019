FROM tensorflow/tensorflow:1.14.0-py3

RUN pip install --user Cython contextlib2 pillow lxml matplotlib pandas && pip install --user pycocotools

COPY models /tf/models
COPY train.sh /train.sh
RUN chmod +x /train.sh

RUN export PYTHONPATH=$PYTHONPATH:/tf/models/research:/tf/models/research/object_detection:/tf/models/research/slim
RUN cd /tf/models/research && python setup.py build && python setup.py install
RUN cd /tf/models/research/slim && python setup.py build && python setup.py install

ENTRYPOINT /train.sh
