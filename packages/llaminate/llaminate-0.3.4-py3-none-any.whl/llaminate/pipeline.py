import functools

import tensorflow as tf

import mlable.utils
import tokun.pipeline

# PREPROCESS ##################################################################

def preprocess(inputs: tf.Tensor, token_dim: int, embed_dim: int, batch_dim: int, sample_dim: int, features: list, separator: str='\x1d') -> tf.data.Dataset:
    # specialized operations
    __encode = functools.partial(tokun.pipeline.encode, token_size=token_dim, sample_size=sample_dim)
    __reshape = functools.partial(tf.reshape, shape=(batch_dim, 4 * sample_dim))
    # combine the features
    __inputs = tf.strings.join(inputs=[inputs[__f] for __f in features], separator=separator)
    # (input, target) where target is the next token for each input
    __inputs, __targets = (tokun.pipeline.offset(data=__inputs, ticks=token_dim // 4), __inputs)
    # encode => (4 * S,) int
    __inputs, __targets = (__encode(__inputs), __encode(__targets))
    # reshape => (4 * S,) int
    __inputs, __targets = (__reshape(__inputs), __reshape(__targets))
    # one-hot encoding for the targets => (4 * S, E) int (bool)
    __inputs, __targets = __inputs, tf.one_hot(__targets, depth=embed_dim, axis=-1)
    # chain the operations
    return (__inputs, __targets)
