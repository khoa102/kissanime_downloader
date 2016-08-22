from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='kissanime_downloader',
      version='0.2',
      description='A program to download anime episode from Kissanime',
      url='http://github.com/khoa102/kissanime_downloader',
      author='Khoa102',
      author_email='khoa102@gmail.com',
      license='MIT',
      packages=['kissanime_downloader'],
      install_requires=[
          'lxml>=3.6.0 ',
          'cfscrape>=1.6.6',
          'requests>=2.11.1',
      ],
      zip_safe=False,
      include_pakage_data=True
)
