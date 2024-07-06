from distutils.core import setup
setup(
  name = 'UOFast',         # How you named your package folder (MyLib)
  packages = ['UOFast'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'UOFast is a 3rd party U2 UOPY restful service which pools U2 connections',   # Give a short description about your library
  author = 'Kurt Konchadi',                   # Type in your name
  author_email = 'tech@rokipark.ai',      # Type in your E-Mail
  url = 'https://github.com/RoKiPaRk/UOFast',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RoKiPaRk/UOFast/archive/refs/tags/v1.1.7.tar.gz',    # I explain this later on
  keywords = ['uopy', 'restful', 'UniObject Connection'],   # Keywords that define your package best
  install_requires=['anyio==3.6.1',
          'certifi',
          'cffi'
          'charset-normalizer',
          'click',
          'colorama==0.4.5',
          'fastapi',
          'gevent',
          'greenlet',
          'h11==0.13.0',
          'idna',
          'pycparser',
          'pydantic',
          'requests',
          'sniffio',
          'starlette',
          'typing',
        'typing_extensions',
        'uopy',
        'urllib3',
        'uvicorn',
        'zope.event==4.5.0',
        'zope.interface==5.4.0',
        'langchain',
        'langchain_community'
  ],    
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)