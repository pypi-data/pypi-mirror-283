from setuptools import setup, find_packages

setup(
    name='gateapp',
    version='0.1.0',
    description='A Django application for configuring gateway settings with a web-based interface',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ankit Kumar',
    author_email='bantiyadav16095@gmail.com',
    url='https://github.com/ankit3388/BlockerGateway',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0,<5.0',
        'gunicorn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    python_requires='>=3.8',
    keywords='django gateway interface web configuration',
    project_urls={
        'Bug Reports': 'https://github.com/ankit3388/BlockerGateway/issues',
        'Source': 'https://github.com/ankit3388/BlockerGateway',
    },
)
