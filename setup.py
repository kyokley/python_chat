from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Python Chats!',
    version='0.1',
    description='',
    long_description=readme(),
    url='http://github.com/kyokley/python_chat',
    author='Kevin Yokley',
    author_email='kyokley2@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['blessings', 'tabulate'],
    tests_require=['pytest', 'black', 'bpython', 'isort'],
    entry_points={
    },
    zip_safe=False,
)
