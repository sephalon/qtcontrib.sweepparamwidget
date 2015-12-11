from setuptools import setup, find_packages

setup(name='qtcontrib.sweepparamwidget',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      namespace_packages=['qtcontrib'],
      packages=find_packages(),
      package_data = {
	'': ['*.ui']
      },
      zip_safe=False)
