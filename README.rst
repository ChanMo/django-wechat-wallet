基于django_wechat_member的钱包模块
=====================================

一个基于 `django_wechat_member <http://github.com/ChanMo/django_wechat_member/>`_ 的钱包模块

功能说明：
----------

- 每个微信会员有一个唯一的钱包
- 钱包有交易记录
- 钱包可以使用微信支付进行充值

快速开始:
---------

安装 *django_wechat_member* :

    `有关django_wechat_member的详细使用说明 <http://github.com/ChanMo/django_wechat_member.git/>`_ 

安装 *django_member_wallet* :

.. code-block::

    pip install git+https://github.com/ChanMo/django_member_wallet.git

修改 *settings.py* 文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wallet',
        ...
    )

修改 *urls.py* 文件:

.. code-block::

    url(r'^wallet/', include('wallet.urls')),

更新数据库:

.. code-block::

   python manage.py migrate

版本更改:
---------
- v0.1 第一版
