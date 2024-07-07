from setuptools import setup, find_packages

setup(
    name='zenberry',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'sounddevice',
    ],
    description='A library that acts like time.sleep but beeps gently every second.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://zenberry.one',
    author='Eugene Zenberry',
    author_email='zenberry.music@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
