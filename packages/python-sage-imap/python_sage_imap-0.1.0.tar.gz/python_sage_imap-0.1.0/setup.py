from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="python_sage_imap",
    version="0.1.0",
    author="Sepehr Akbarzadeh",
    author_email="info@sageteam.org",
    description="Managing IMAP connections and performing various email operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sageteamorg/python-sage-imap",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
)
