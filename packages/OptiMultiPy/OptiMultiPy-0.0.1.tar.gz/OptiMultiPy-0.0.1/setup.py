from setuptools import setup, find_packages

setup(
    name="OptiMultiPy",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Marcos Antônio Leandro",
    author_email="marcos352354@gmail.com",
    description="Sintonia do controlador PID utilizando algoritmo de otimização",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Marcos9971/OptiMultiPy.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
