#-----------------------------------------------
# -*- encoding=utf-8 -*-                       #
# __author__:'焉知飞鱼'                         #
# CreateTime:                                  #
#       2021/3/16 10:35                         #
#                                              #
#               天下风云出我辈，                 #
#               一入江湖岁月催。                 #
#               皇图霸业谈笑中，                 #
#               不胜人生一场醉。                 #
#-----------------------------------------------
import tensorflow as tf

def dice(_x, axis=-1, epsilon=0.000000001, name=''):
    with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
        alphas = tf.get_variable('alpha'+name, _x.get_shape()[-1],
                                 initializer=tf.constant_initializer(0.0),
                                 dtype=tf.float32)
        beta = tf.get_variable('beta'+name, _x.get_shape()[-1],
                               initializer=tf.constant_initializer(0.0),
                               dtype=tf.float32)
    input_shape = list(_x.get_shape())

    reduction_axes = list(range(len(input_shape)))
    del reduction_axes[axis]
    broadcast_shape = [1] * len(input_shape)
    broadcast_shape[axis] = input_shape[axis]

    # case: train mode (uses stats of the current batch)
    mean = tf.reduce_mean(_x, axis=reduction_axes)
    brodcast_mean = tf.reshape(mean, broadcast_shape)
    std = tf.reduce_mean(tf.square(_x - brodcast_mean) + epsilon, axis=reduction_axes)
    std = tf.sqrt(std)
    brodcast_std = tf.reshape(std, broadcast_shape)
    x_normed = tf.layers.batch_normalization(_x, center=False, scale=False, name=name, reuse=tf.AUTO_REUSE)
    # x_normed = (_x - brodcast_mean) / (brodcast_std + epsilon)
    x_p = tf.sigmoid(beta * x_normed)


    return alphas * (1.0 - x_p) * _x + x_p * _x

def parametric_relu(_x):
    with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
        alphas = tf.get_variable('alpha', _x.get_shape()[-1],
                                 initializer=tf.constant_initializer(0.0),
                                 dtype=tf.float32)
    pos = tf.nn.relu(_x)
    neg = alphas * (_x - abs(_x)) * 0.5

    return pos + neg
