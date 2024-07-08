from setuptools import setup, find_packages

setup(
    name="Abdulaziz",
    version="0.1.0",
    packages=find_packages(),
    author="Abdulaziz Faqihi",
    author_email="your.email@example.com",
    description="A simple greeting library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Abdulaziz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
