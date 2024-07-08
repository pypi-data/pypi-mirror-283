from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read()

setup(
    name='snaptec_resolver',
    version='0.1.0',
    author='Trung',
    author_email='trung.dinh@snaptec.co',
    description='Library supports',
    packages=find_packages(),
        include_package_data=True,

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=install_requires,

)