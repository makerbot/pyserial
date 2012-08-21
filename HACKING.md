

= Distribution

To build an egg from this project:

python -c "import setuptools; execfile('setup.py')" bdist_egg

== Building an egg for python2.6

=== On Ubuntu

Install an old python2.6:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.6 python2.6-dev python-distribute-deadsnakes

Install setuptools:

	sudo easy_install-2.6 setuptools

Build the egg:

    python2.6 -c "import setuptools; execfile('setup.py')" bdist_egg


