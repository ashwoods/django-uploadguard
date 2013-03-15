import os
import sys
from setuptools import setup, find_packages


uploadguard = __import__('uploadguard')
readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
try:
    long_description = open(readme_file).read()
except IOError as err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

if sys.version_info >= (3,):
    extra_kwargs = {'use_2to3': True}
else:
    extra_kwargs = {}

setup(
    name = 'django-uploadguard',
    version = uploadguard.get_version(),
    url = 'http://github.com/ashwoods/django-uploadguard',
    author = 'Ashley Camba',
    author_email = 'ashwoods@gmail.com',
    description = uploadguard.__doc__.strip(),
    long_description = long_description,
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    license = 'BSD',
    install_requires = [
        'Django>=1.2',
    ],
    tests_require = [
        'mock',
    ],
    classifiers = ['Development Status :: 3 - Alpha/Unstable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Security',
    ],
    **extra_kwargs
)
