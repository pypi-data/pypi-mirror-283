from setuptools import setup, find_packages

setup(
    name='visionlit',
    version='1.0.4',
    author='Jessica Nono',
    author_email='jessicanono@filparty.com',
    description='A Python library implementing Visionlit computer vision methods with model access.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jessicaNono/visionlitpy',
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/jessicaNono/visionlitpy/docs',
        'Source': 'https://github.com/jessicaNono/visionlitpy',
    },
)
