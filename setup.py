import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='pymodoro-cli',
    version='0.1',
    author='Hristo Todorov',
    author_email='httodoroff@gmail.com',
    description='Lightweight and simple pomodoro tracker running entirely inside the shell',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rozver/pymodoro-cli/',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':[
            'pymodoro-cli = tracker.main'
        ]
    },
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',   
)
