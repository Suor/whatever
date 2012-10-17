from setuptools import setup

setup(
    name='whatever',
    version='0.2',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='Perl 6 like Whatever object.',
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
