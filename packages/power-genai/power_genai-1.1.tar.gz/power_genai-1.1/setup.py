from setuptools import setup, find_packages

setup(name='power_genai',
		version='1.1',
		description='power genai',
		url='https://github.com/ExpertOfAI/power_genai',
		author='ExpertOfAI',
		license='MIT',
		packages=find_packages(),
		include_package_data=True,
		classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		],
		python_requires='>=3.6',
		install_requires = []
		)
