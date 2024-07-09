from setuptools import setup, find_packages

setup(
    name="webapppacker",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Adicione as dependências necessárias aqui
    ],
    author="bruno eduardo",
    author_email="hosttimer@gmail.com",
    description="Uma biblioteca Python para empacotar aplicativos web em APKs Android",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/webapppacker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)