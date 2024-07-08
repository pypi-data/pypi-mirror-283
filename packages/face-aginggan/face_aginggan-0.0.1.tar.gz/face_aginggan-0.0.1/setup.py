from setuptools import setup, find_packages

setup(
    name='face-aginggan',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'gdown==4.7.1',
        'gradient-accumulator==0.5.1',
        'hurry.filesize==0.9',
        'matplotlib==3.7.1',
        'numpy==1.23.2',
        'pandas==2.0.1',
        'Pillow==9.5.0',
        'tensorflow==2.12.0',
        'tensorflow_datasets==4.9.2',
    ],
    author='huseyindas',
    author_email='hsyndass@gmail.com',
    description='Implementing Age Transformation using Generative Models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/huseyindas/face-agingGAN',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)