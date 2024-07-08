import setuptools

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
	name= "GmailBox",
	version= "1.0.0",
	author= "Hamo",
    keywords=["gmail","mail","GmailBox","inbox","email","Tempmail","Tempgmail"],
    install_requires=["requests","beautifulsoup4","aiohttp","asyncio","pypasser"],
    long_description=readme,
    long_description_content_type="text/markdown",
	description= "With this library, you can create random Gmail and receive messages",
	packages=setuptools.find_packages(),
    license="LGPLv3",
	classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)