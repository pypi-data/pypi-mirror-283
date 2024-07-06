from setuptools import setup, find_packages

setup(
    name="pack_xpub",
    version="0.1.0.2",
    author="xiaolong",
    author_email="longx888@126.com",
    description="public package",
    long_description="常用库",
    long_description_content_type="text/markdown",
    url="http://localhost:8080",
    #packages=find_packages(exclude=['dist.*','dist','tests.*','tests']),
    packages=find_packages(),
    classifiers = [
            # 发展时期,常见的如下
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # 开发的目标用户
            'Intended Audience :: Developers',

            # 类型
            'Topic :: Software Development :: Build Tools',

            # 许可证信息
            'License :: OSI Approved :: MIT License',

            # 目标 Python 版本
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
        ],
        python_requires='>=3.6',

        install_requires=[
        #"requests",
        #"numpy",

    ],
)
