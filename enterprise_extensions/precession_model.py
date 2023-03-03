## 编写进动模型的红噪声函数和调用函数
import numpy as np


# @signal_base.function
def RedNoise_delay(t, t0, P, K, O, X, k):

    """
    ##定义红噪声函数

    @signal_base.function不明白, 
    RedNoise_delay函数作为signal_base.function函数的入参
    相当于执行signal_base.function(RedNoise_delay(,,,)),
    需要替换@signal_base.function吗?

    :param a1: 
        第一次谐波的振幅
    :param a2:
        第二次谐波的振幅
    :param P:
        进动周期
    :param Wp:
        进动频率
    :param k:
        任意偏移
    :param t:
        pulsar toas in seconds
    :param t0:
        选取的一个0时刻
    :param K: 
        与J1939的自旋向下扭矩的强度成正比
    :param O: 
        角动量和对称轴的夹角
    :param X:
        偶极矩和对称轴的夹角

    """

    #define Wp
    Wp = 2*np.pi/P  

    # define a1 and a2
    a1 = K*O*np.sin(2*X)/(1+O**2)
    a2 = K*O**2*np.sin(X)**2/(4*(1+O**2))

    # residuals
    res = k + a1*np.sin(Wp*(t-t0)) - a2*np.sin(2*Wp*(t-t0))

    return res


def RedNoise_delay_block():

    """
    调用RedNoise_delay函数
    """

    # 设置初始值  
    #
    t = np.arange(1, 1000, 0.1)
    t0 = 100
    P = 20
    K = 1
    O = 2
    X = 5
    k = 3

    # 红噪声残差
    RedNoise_d = RedNoise_delay(t,t0,P,K,O,X,k)

    return RedNoise_d

