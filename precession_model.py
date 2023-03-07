## 编写进动模型的红噪声函数和调用函数
import numpy as np
from enterprise.signals import (deterministic_signals, parameter, signal_base,
                                utils)

@signal_base.function
def RedNoise_delay(t, t0, P, K, O, X, k):

    """
    ##定义红噪声函数

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


def RedNoise_delay_block(name='RedNoise',
                         t_lower=1, t_upper=10,
                         t0_lower=1, t0_upper=10,
                         P_lower=1, P_upper=10,
                         K_lower=1, K_upper=10,
                         O_lower=1, O_upper=10,
                         X_lower=1, X_upper=10,
                         k_lower=1, k_upper=10):

    """
    调用RedNoise_delay函数
    
    """

    # RedNoise_delay parameters
    t_name = '{}_log10_t'.format(name)
    log10_t_RedNoise = parameter.Uniform(t_lower, t_upper)(t_name)

    t0_name = '{}_log10_t0'.format(name)
    log10_t0_RedNoise = parameter.Uniform(t0_lower, t0_upper)(t0_name)

    P_name = '{}_log10_P'.format(name)
    log10_P_RedNoise = parameter.Uniform(P_lower, P_upper)(P_name)

    K_name = '{}_log10_K'.format(name)
    log10_K_RedNoise = parameter.Uniform(K_lower, K_upper)(K_name)

    O_name = '{}_log10_O'.format(name)
    log10_O_RedNoise = parameter.Uniform(O_lower, O_upper)(O_name)

    X_name = '{}_log10_X'.format(name)
    log10_X_RedNoise = parameter.Uniform(X_lower, X_upper)(X_name)

    k_name = '{}_log10_k'.format(name)
    log10_k_RedNoise = parameter.Uniform(k_lower, k_upper)(k_name)


    # 红噪声残差
    RedNoise_d = RedNoise_delay(log10_t=log10_t_RedNoise, log10_t0=log10_t0_RedNoise, 
                                log10_P=log10_P_RedNoise, log10_K=log10_K_RedNoise, 
                                log10_O=log10_O_RedNoise, log10_X=log10_X_RedNoise, 
                                log10_k=log10_k_RedNoise)
    
    RedNoise = deterministic_signals.Deterministic(RedNoise_d, name=name)

    return RedNoise
