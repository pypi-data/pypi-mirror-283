from setuptools import setup, find_packages
import pathlib

def main():
    # The directory containing this file
    HERE = pathlib.Path(__file__).parent

    # The text of the README file
    README = (HERE / "README.md").read_text()

    # Read the dependencies from requirements.txt
    with open(HERE / "requirements.txt") as f:
        requirements = f.read().splitlines()

    setup(
        name='myinternshipcalculator2024',
        version='0.3.7',
        author='Abdallah Abdelsameia',
        author_email='aabdelsameia1@gmail.com',
        maintainer="Abdallah Abdelsameia",
        maintainer_email="aabdelsameia1@gmail.com",
        description='A simple internship hours calculator.',
        long_description=README,
        long_description_content_type='text/markdown',
        url='https://github.com/aabdelsameia1/myinternshipcalculator2024',
        packages=find_packages(),
        install_requires=requirements,
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )

if __name__ == "__main__":
    main()
