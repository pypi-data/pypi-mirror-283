from setuptools import setup, find_packages


def readme():
	with open('README.md', 'r') as f:
		return f.read()


setup(
	name='Xgua',
	version='0.0.2',
	author='Xpeawey',
	author_email='girectx@gmail.com',
	description='Logger with saving logs to s3 storage',
	long_description=readme(),
	long_description_content_type='text/markdown',
	url='https://github.com/SikWeet/Xgua',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3.11',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	keywords='Xgua Logger S3 s3logger',
	project_urls={
		'GitHub': 'https://github.com/SikWeet/Xgua'
	},
	python_requires='>=3.6'
)