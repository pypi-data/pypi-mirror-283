import functools

import keras as ks
import tensorflow as tf

import mlable.masking

# ACCURACY ####################################################################

def group_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor, group: int=4) -> tuple:
    # category indexes
    __yt = ks.ops.argmax(y_true, axis=-1)
    __yp = ks.ops.argmax(y_pred, axis=-1)
    # matching
    __match = ks.ops.equal(__yt, __yp)
    # group all the predictions for a given token
    if group and group > 1:
        # repeat values so that the reduced tensor has the same shape as the original
        __match = mlable.masking.reduce_all(mask=__match, group=group, axis=-1, keepdims=True)
    # cast
    return ks.ops.cast(__match, dtype='float32')

class CategoricalGroupAccuracy(ks.metrics.MeanMetricWrapper):
    def __init__(self, group: int=4, name: str='categorical_group_accuracy', dtype: tf.dtypes.DType='float32', **kwargs):
        # adapt the measure
        __fn = functools.partial(group_accuracy, group=group)
        # init
        super(CategoricalGroupAccuracy, self).__init__(fn=__fn, name=name, dtype=dtype, **kwargs)
        # group predictions
        self._group = group
        # sould be maximized
        self._direction = 'up'

    def get_config(self) -> dict:
        __config = super(CategoricalGroupAccuracy, self).get_config()
        __config.update({'group': self._group})
        return __config

# LOSS ########################################################################
