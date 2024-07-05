from setuptools import setup, find_packages

setup(
    name='easyRTML',
    version='1.1',
    description='A package for signal classification and deployment in any microcontroller board with no expertise requires.',
    author='Aryan Jadhav',
    author_email='easyrtml@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'xgboost',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'tqdm',
        'pyserial',  # for serial communication
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # specify the required Python version
)
