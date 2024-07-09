from setuptools import setup, find_packages

setup(
    name='django-gateway-interface',
    version='0.1.2',
    description='A Django application for configuring gateway settings with a web-based interface',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ankit Kumar',
    author_email='bantiyadav16095@gmail.com',
    url='https://github.com/ankit3388/BlockerGateway',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0,<5.0',  # Adjust version as needed
        'gunicorn',          # Optional: If you want to include a WSGI server
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django',
    ],
    python_requires='>=3.8',
    keywords='django gateway interface web configuration',
    project_urls={
        'Bug Reports': 'https://github.com/ankit3388/BlockerGateway/issues',
        'Source': 'https://github.com/ankit3388/BlockerGateway',
    },
)
