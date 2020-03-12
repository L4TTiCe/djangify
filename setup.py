from setuptools import setup, find_packages 


with open("README.md", "r") as fh:
    long_description = fh.read()

setup( 
		name ='djangify', 
		version ='1.0.0', 
		author ='amartya', 
		author_email ='amarkaushik1999@gmail.com', 
		url ='https://github.com/L4TTiCe/djangify', 
		description ='A Python script that converts HTML Files / Templates to Django compatible HTML Templates.', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'djangify = djangify.djangify:main'
			] 
		}, 
		classifiers =[ 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		], 
		keywords ='djangify django templates', 
		zip_safe = False
) 
