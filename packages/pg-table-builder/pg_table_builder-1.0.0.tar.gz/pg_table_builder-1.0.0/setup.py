from distutils.core import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pg_table_builder',
    version='1.0.0',
    maintainer="Ben Puls",
    maintainer_email="discordben7@gmail.com",
    url="https://github.com/byBenPuls/pg_table_builder",
    packages=['pg_table_builder'],
    install_requires=[],
    license='LICENSE.md',
    description='Table builder for postgresql',
    keywords=["postgres", "builder", "postgresql"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)