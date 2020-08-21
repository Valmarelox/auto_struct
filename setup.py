from setuptools import setup

setup(
    name='auto_struct',
    version='0.421',
    packages=['auto_struct', 'auto_struct.data_types', 'auto_struct.data_types.int', 'auto_struct.data_types.array', 'auto_struct.data_types.string'],
    url='https://github.com/Valmarelox/auto_struct/tree/master',
    license='MIT',
    author='efi',
    author_email='valmarelox@gmail.com',
    description='Easily parse binary file in python3.8',
    zip_safe=False,
    python_requires='>=3.8'
)
