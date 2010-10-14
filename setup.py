from distutils.core import setup

setup(name='data_hacks',
      version='0.1',
      description='Command line utilities for data analysis',
      author='bitly',
      author_email='support@bit.ly',
      url='http://github.com/bitly/data_analysis',
      # packages=['data_hacks'],
      scripts = ['data_hacks/histogram.py', 
                'data_hacks/nintey_five_percent.py',
                'data_hacks/run_for.py',
                'data_hacks/sample.py']
     )