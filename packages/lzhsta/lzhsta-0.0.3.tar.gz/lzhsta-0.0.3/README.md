- [1.统计参数设置](#1统计参数设置)
  - [1.1.创建一个统计参数](#11创建一个统计参数)
  - [1.2.创建一系列参数](#12创建一系列参数)
    - [方法一：自定义](#方法一自定义)
    - [方法二：从numpy (Npara \* Nsample)进行统计（自动存在cor）](#方法二从numpy-npara--nsample进行统计自动存在cor)
    - [方法三：从pandas (Npara \* Nsample)进行统计（自动存在cor）](#方法三从pandas-npara--nsample进行统计自动存在cor)
  - [1.3.给一系列参数添加相关性](#13给一系列参数添加相关性)
- [2.功能1：生成抽样](#2功能1生成抽样)
  - [2.1.根据相关性生成高斯抽样](#21根据相关性生成高斯抽样)
  - [2.2.生成高斯抽样](#22生成高斯抽样)
  - [2.3.生成均匀抽样（可以用来随机产生拟合初始值）](#23生成均匀抽样可以用来随机产生拟合初始值)
- [3.功能2：拟合](#3功能2拟合)
  - [3.1.定义拟合函数和chisq函数](#31定义拟合函数和chisq函数)
  - [3.2.获得样本点](#32获得样本点)
  - [3.3.构建拟合参数](#33构建拟合参数)
  - [3.4.拟合](#34拟合)
  - [3.5.利用拟合结果抽样、计算、统计](#35利用拟合结果抽样计算统计)
  - [3.6.画图](#36画图)


# 1.统计参数设置
## 1.1.创建一个统计参数
    import lzhsta.para
    para = lzhsta.para.Parameter(name='a', # 名字
                                 value=1, # 数值
                                 error=1, # 误差
                                 limitl=0, # 左边界
                                 limitr=10, # 右边界
                                 vary=True) # 是否为自由参数
    print(para)
    # 输出
    '''
    name         a
    value        1
    error        1
    limitl       0
    limitr      10
    vary      True
    dtype: object
    '''
## 1.2.创建一系列参数
### 方法一：自定义
    paras = lzhsta.para.Parameters()
    paras.add_para(lzhsta.para.Parameter(name='a', value=1, error=1, limitl=0, limitr=10, vary=True))
    paras.add_para(lzhsta.para.Parameter(name='b', value=1, error=1, limitl=0, limitr=10, vary=True))
    paras.add_para(lzhsta.para.Parameter(name='c', value=1, error=1, limitl=0, limitr=10, vary=True))
    print(paras)
    # 输出
    '''
      name value error limitl limitr  vary
    0    a     1     1      0     10  True
    1    b     1     1      0     10  True
    2    c     1     1      0     10  True
    '''
### 方法二：从numpy (Npara * Nsample)进行统计（自动存在cor）
    Npara = 3
    Nsample = 1000
    sample = numpy.random.rand(Npara, Nsample)
    paras = lzhsta.para.Parameters(sample)
    print(paras)
    print(paras.cor)
    # 输出
    '''  name     value     error    limitl    limitr  vary
    0   p0  0.483246  0.288123  0.000442  0.999914  True
    1   p1  0.503807  0.287451  0.000044  0.999381  True
    2   p2  0.484693  0.295005  0.000562   0.99885  True
              a         b         c
    a  1.000000 -0.000727 -0.002233
    b -0.000727  1.000000 -0.026183
    c -0.002233 -0.026183  1.000000
    '''
### 方法三：从pandas (Npara * Nsample)进行统计（自动存在cor）
    Nsample = 1000
    sample = pandas.DataFrame({'a': numpy.random.rand(Nsample),
                            'b': numpy.random.rand(Nsample),
                            'c': numpy.random.rand(Nsample)})
    paras = lzhsta.para.Parameters(sample)
    print(paras)
    print(paras.cor)
    # 输出
    '''
      name     value     error    limitl    limitr  vary
    0    a  0.499607  0.290514   0.00138  0.999621  True
    1    b  0.500115  0.292587  0.002633  0.999265  True
    2    c  0.506556  0.285257   0.00002  0.996843  True
              a         b         c
    a  1.000000 -0.000727 -0.002233
    b -0.000727  1.000000 -0.026183
    c -0.002233 -0.026183  1.000000
    '''
## 1.3.给一系列参数添加相关性
    paras.set_correlation(numpy.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]]))
    paras.set_covariance(numpy.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]]))
    print(paras.cor)
    # 输出
    '''
       a  b  c
    a  1  0  0
    b  0  1  0
    c  0  0  1
    '''

# 2.功能1：生成抽样
## 2.1.根据相关性生成高斯抽样
    Nsample = 1200
    sample_mc = paras.gen_rand_norm_cor(Nsample)
    print(sample_mc)
    # 输出
    '''
                 a         b         c
    0     1.698176  2.451555  0.274619
    1     3.553382  1.332760 -0.003639
    2     3.708011  1.647872  1.223150
    3    -0.068095  1.219805  1.543671
    4     1.045342  0.256843  0.923127
    ...        ...       ...       ...
    1195  0.879202  1.653522  1.802289
    1196  1.345888  0.720553  2.062951
    1197  0.587477  0.810850  0.164569
    1198  0.820498  2.334813  1.199177
    1199  1.710241  3.179919  1.06094
    '''
    new_paras = lzhsta.para.Parameters(sample_mc)
    print(new_paras)
    print(new_paras.cor)
## 2.2.生成高斯抽样
    Nsample = 1200
    sample_mc = paras.gen_rand_norm(Nsample)
## 2.3.生成均匀抽样（可以用来随机产生拟合初始值）
    Nsample = 1200
    sample_mc = paras.gen_rand_uniform(Nsample)



# 3.功能2：拟合
## 3.1.定义拟合函数和chisq函数
    def func(ps, x):
        return ps['a'] * x**2 + ps['b'] * x + ps['c']

    def chisq(ps, x, y, e):
        return ((y - func(ps, x)) / e)**2
## 3.2.获得样本点
    a = 2.45
    b = 3.45
    c = 4.45

    x = numpy.arange(-2, 2, 0.1)
    y = func({'a': a, 'b': b, 'c': c}, x)
    e = numpy.ones(x.shape) * 5
    re = numpy.random.normal(0, 1, x.shape) * e
    ry = y + re
## 3.3.构建拟合参数
    paras = lzhsta.para.Parameters()
    paras.add_para(lzhsta.para.Parameter(name='a', value=1, error=1, limitl=0, limitr=10, vary=True))
    paras.add_para(lzhsta.para.Parameter(name='b', value=1, error=1, limitl=0, limitr=10, vary=True))
    paras.add_para(lzhsta.para.Parameter(name='c', value=1, error=1, limitl=0, limitr=10, vary=True))
## 3.4.拟合
    result_paras = lzhsta.fit.do_lmfit(chisq, paras, x, ry, e, show_result=True) # 输出
    '''
    [[Fit Statistics]]
        # fitting method   = leastsq
        # function evals   = 57
        # data points      = 40
        # variables        = 3
        chi-square         = 70.1340844
        reduced chi-square = 1.89551579
        Akaike info crit   = 28.4611779
        Bayesian info crit = 33.5278162
    [[Variables]]
        a:  2.40179694 +/- 0.49072902 (20.43%) (init = 1)
        b:  4.43785168 +/- 0.53339439 (12.02%) (init = 1)
        c:  4.07533684 +/- 0.97774576 (23.99%) (init = 1)
    [[Correlations]] (unreported correlations are < 0.100)
        C(a, c) = -0.7483
        C(a, b) = +0.3994
    '''
## 3.5.利用拟合结果抽样、计算、统计
    result_mc = result_paras.gen_rand_norm_cor(1000)
    ymc = numpy.array([func(result_mc.iloc[i], x) for i in range(result_mc.shape[0])])
    mean = ymc.mean(axis=0)
    std = ymc.std(axis=0)
## 3.6.画图
    import matplotlib.pyplot as plt
    plt.errorbar(x, ry, yerr=e, fmt='o')
    plt.plot(x, func(result_paras, x), label='fit')
    plt.fill_between(x, mean - std, mean + std, color='gray', alpha=0.5)
    plt.show()