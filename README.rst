钱包模块
=====================================

一个基于django和wechat的钱包模块

功能说明：
----------

- 每个微信会员有一个唯一的钱包
- 钱包有交易记录

快速开始:
---------

安装 *django-wechat-wallet* :

.. code-block::

    pip install django-wechat-wallet

修改 *settings.py* 文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wallet',
        ...
    )

修改 *urls.py* 文件:

.. code-block::

    url(r'^wallet/', include('wallet.urls', namespace='wallet')),

更新数据库:

.. code-block::

   python manage.py makemessage wallet

   python manage.py migrate


版本更改:
---------
- v0.1 第一版
