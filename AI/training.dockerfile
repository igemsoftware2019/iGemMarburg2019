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

FROM tensorflow/tensorflow:1.14.0-py3

RUN pip install --user Cython contextlib2 pillow lxml matplotlib pandas && pip install --user pycocotools

COPY models /tf/models
COPY train.sh /train.sh
RUN chmod +x /train.sh

RUN export PYTHONPATH=$PYTHONPATH:/tf/models/research:/tf/models/research/object_detection:/tf/models/research/slim
RUN cd /tf/models/research && python setup.py build && python setup.py install
RUN cd /tf/models/research/slim && python setup.py build && python setup.py install

ENTRYPOINT /train.sh
