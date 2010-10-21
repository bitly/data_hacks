from distutils.core import setup

version = "0.2"
setup(name='data_hacks',
      version=version,
      description='Command line utilities for data analysis',
      author='Jehiah Czebotar',
      author_email='jehiah@gmail.com',
      url='http://github.com/bitly/data_analysis',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Intended Audience :: System Administrators',
            'Topic :: Terminals',
            ],
      download_url="http://github.com/downloads/bitly/data_hacks/data_hacks-%s.tar.gz" % version,
      scripts = ['data_hacks/histogram.py', 
                'data_hacks/nintey_five_percent.py',
                'data_hacks/run_for.py',
                'data_hacks/bar_chart.py',
                'data_hacks/sample.py']
     )