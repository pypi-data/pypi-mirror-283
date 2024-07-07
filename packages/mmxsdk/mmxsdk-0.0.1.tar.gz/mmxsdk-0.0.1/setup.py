from setuptools import setup, find_packages

setup(
    name='mmxsdk',
    version='0.0.1',
    packages=find_packages(),
    description='SDK to interact with the MMX (crypto) API either locally or through the public RPC server.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lee Preimesberger',
    author_email='pypi.org.rake262@passmail.net',
    url='https://github.com/capricallctx-com/mmxsdk',
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)