from setuptools import find_packages, setup

setup(
    name='ignacio_bot',  # Name of your package
    version='0.3.0',  # Version of your package
    description='A simple Flask app that lets you talk to a custom bot.',  # Short description of your package
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Arpan Seth',
    author_email='aseth42@gmail.com',
    url='https://github.com/arpanseth/ignacio_bot',  # URL to your GitHub repository
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True,
    install_requires=[
        'Flask',
        'openai',
        'flask_session'
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    project_urls={
        'Source': 'https://github.com/arpanseth/ignacio_bot',
    },
    entry_points={
        'console_scripts': [
            'ignacio_bot=ignacio_bot.app:main',  # Command to run your app
        ],
    },
)