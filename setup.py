import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Tonberry",
    version="0.0.1",
    description="ASGI compliant web microframework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anthony Post",
    author_email="postanthony3000@gmail.com",
    license="MIT License",
    url="https://github.com/Ayehavgunne/Tonberry/",
    packages=["tonberry"],
    install_requires=["dacite", "user-agents"],
    extras_require={"dev": ["mypy", "black", "isort"]},
    python_requires=">=3.7",
)
