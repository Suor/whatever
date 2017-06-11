from setuptools import setup

setup(
    name='whatever',
    version='0.4.3',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
