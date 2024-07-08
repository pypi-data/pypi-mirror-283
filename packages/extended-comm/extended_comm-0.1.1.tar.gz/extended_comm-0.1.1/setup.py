import time

from setuptools import setup
import shutil

try:
    print('Removing cache data before install...')
    shutil.rmtree('./build/')
    shutil.rmtree('./dist/')
    shutil.rmtree('./extended_comm.egg-info/')
    shutil.rmtree('./.pytest_cache/')
    time.sleep(1)
except:
    ...

setup(name='extended-comm',
      version='0.1.1',
      description='wrapper for communication between external apis',
      url='https://github.com/karunkrishna/extended_comm',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_comm', 'extended_comm.google'],

      install_requires=['google-api-python-client', 'python-dotenv', 'google-auth-httplib2', 'google-auth-oauthlib'],
      zip_safe=False
      )
