#----------------------------------------------
# -*- encoding=utf-8 -*-                      #
# __author__:'焉知飞鱼'                        #
# CreateTime:                                 #
#       2020/2/12 21:48                       #
#                                             #
#               天下风云出我辈，                 #
#               一入江湖岁月催。                 #
#               皇图霸业谈笑中，                 #
#               不胜人生一场醉。                 #
#----------------------------------------------
import tensorflow as tf

# - 1、构建TFRecords的输入数据
# - 2、使用模型进行特征列指定
# - 3、模型训练以及预估

FEATURE_COLUMN = ['channel_id', 'vector', 'user_weights', 'article_weights']


class WDL(object):
    """wide&deep训练排序模型
    """
    def __init__(self):
        pass

    @staticmethod
    def get_tfrecords_data():

        def parse_example_function(exmaple):
            """解析每个样本的example
            :param exmaple:
            :return:
            """
            # 定义解析格式，parse_single_example
            features = {
                'label': tf.FixedLenFeature([], tf.int64),
                'feature': tf.FixedLenFeature([], tf.string)
            }

            label_feature = tf.parse_single_example(exmaple, features)
            # 修改其中的特征类型和形状
            # 解码 [121]
            # feature = tf.reshape(tf.decode_raw(label_feature['feature'], tf.float32), [1, 121])
            f = tf.decode_raw(label_feature['feature'], tf.float64)
            feature = tf.reshape(tf.cast(f, tf.float32), [1, 121])

            # 计算其中向量、用户权重、文章权重的平均值
            channel_id = tf.cast(tf.slice(feature, [0, 0], [1, 1]), tf.int32)
            vector = tf.reduce_sum(tf.slice(feature, [0, 1], [1, 100]), axis=1)
            user_weights = tf.reduce_sum(tf.slice(feature, [0, 101], [1, 10]), axis=1)
            article_weights = tf.reduce_sum(tf.slice(feature, [0, 111], [1, 10]), axis=1)

            # 4个特征值进行名称构造字典
            data = [channel_id, vector, user_weights, article_weights]
            feature_dict = dict(zip(FEATURE_COLUMN, data))

            label = tf.cast(label_feature['label'], tf.int32)

            return feature_dict, label

        # Tfrecord dataset读取数据
        dataset = tf.data.TFRecordDataset(['./train_ctr_20190605.tfrecords'])
        # map 解析
        dataset = dataset.map(parse_example_function)
        dataset = dataset.batch(64)
        dataset = dataset.repeat(10)
        return dataset

    def train_eval(self):
        """
        进行训练pnggu
        :return:
        """

        # 指定wide和deep两边的features_column
        # wide ,channel_id就是一个类别具体的数字
        # num_buckets必须填写
        channel_id  = tf.feature_column.categorical_column_with_identity('channel_id',num_buckets=25)

        wide_columns = [channel_id]

        # deep ID必须embedding结果，数值类型
        # tf.feature_column.embedding_column()或者input_layer
        vector = tf.feature_column.numeric_column('vector')
        user_weights = tf.feature_column.numeric_column('user_weights')
        article_weights = tf.feature_column.numeric_column('article_weights')

        deep_columns = [tf.feature_column.embedding_column(channel_id,dimension=25),
                        vector,user_weights,article_weights]

        # 模型输入训练
        model = tf.estimator.DNNLinearCombinedClassifier(
            model_dir='./ckpt/wide_and_deep',
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_hidden_units=[1024,512,256]
        )
        model.train(WDL.get_tfrecords_data,steps=1)
        # result = model.evaluate(WDL.get_tfrecords_data)
        # print(result)

        # 模型导出
        # 1. 指定serving模型的输入特征类型
        # 2. 指定模型的特征输入函数及example
        columns = wide_columns + deep_columns
        feature_spec = tf.feature_column.make_parse_example_spec(columns)
        serving_input_receiver_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
        model.export_savedmodel("./serving_model/wdl/", serving_input_receiver_fn)

if __name__ == '__main__':
    wdl = WDL()
    wdl.train_eval()
    tf.nn.rnn_cell.MultiRNNCell()()