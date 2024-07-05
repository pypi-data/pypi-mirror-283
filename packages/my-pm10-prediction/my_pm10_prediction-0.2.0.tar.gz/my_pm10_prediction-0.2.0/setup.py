# setup.py

from setuptools import setup, find_packages

setup(
    name='my_pm10_prediction',
    version='0.2.0',
    description='A package for PM10 air quality prediction and data cleaning',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_pm10_prediction',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'keras',
        'joblib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
