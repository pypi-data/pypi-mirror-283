from setuptools import setup, find_packages

setup(
    name='syncmqtt',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'paho-mqtt',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Josh Lin',
    author_email='postor@gmail.com',
    description='A library to synchronize MQTT topics with Python class attributes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/postor/sync-mqtt',  # Replace with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)