from setuptools import setup, find_packages
import platform

install_requires = [

]

if platform.system() == "Windows":
    install_requires.append("windows-curses")
setup(
    name="simple_screen",
    version="0.1.17",
    packages=find_packages(),
    include_package_data=True,
    description="Ease of managing color and positioning prints and supplies for teaching purposes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mon Maldonado",
    author_email="monterdi@gmail.com",
    url="https://github.com/digestiveThinking/simple_screen",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
