from setuptools import setup

setup(
    name='whatever',
    version='0.2.1',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='Easy way to make anonymous functions by partial application of operators.',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/whatever',
    license='BSD',

    py_modules=['whatever'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
