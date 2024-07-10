from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='pg_table_builder',
  version='0.0.1',
  author='Ben Puls',
  author_email='discordben7@gmail.com',
  description='Table builder for postgresql',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/byBenPuls/pg_table_builder',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='postgresql',
  project_urls={
    'GitHub': 'https://github.com/byBenPuls/pg_table_builder'
  },
  python_requires='>=3.9'
)
