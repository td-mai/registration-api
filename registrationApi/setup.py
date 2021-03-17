from setuptools import setup, find_packages

setup(
    name='RegistrationApi',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[  'flask~=1.1',
                        'python-dotenv==0.15.0',
                        'mysql-connector-python~=8.0',
                        'redis~=3.5',
                        'requests~=2.25']
)