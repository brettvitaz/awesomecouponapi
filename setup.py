from setuptools import setup

setup(
    name='awesomecouponapi',
    version='1.0',
    packages=['api'],
    url='',
    license='MIT',
    author='Brett Vitaz',
    author_email='brett@vitaz.net',
    description='Coupon API demo',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
