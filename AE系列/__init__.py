#----------------------------------------------
# -*- encoding=utf-8 -*-                      #
# __author__:'xiaojie'                        #
# CreateTime:                                 #
#       2019/5/24 16:42                       #
#                                             #
#               天下风云出我辈，                 #
#               一入江湖岁月催。                 #
#               皇图霸业谈笑中，                 #
#               不胜人生一场醉。                 #
#----------------------------------------------
# VAE的输入：在VAE文件中是把三维的图片输入进去，在vae_keras中输入的却是
#   一个向量，在variational_autoencoder文件中，输入的也是向量
#     注意VAE文件中，计算重构误差的方式。
# 对抗自编码器的输入:在aae文件中，输入的是一张图片，只是把它拉平了，所以才没用卷积来操作
#     在adversarial_autoencoder文件中，输入的是一个向量，其他2个文件输入的也是向量