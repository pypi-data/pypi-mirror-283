from setuptools import setup, find_packages

setup(
    name="text2resume",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyYAML',
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'generate-resume=text2resume.generate_resume:main',
        ],
    },
    package_data={
        'text2resume': ['templates/*.tex'],
    },
    author="Rishi Mulchandani",
    author_email="rishimulchandani100@gmail.com",
    description="A module to generate PDFs from YAML data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rishi-m100/text2resume", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
