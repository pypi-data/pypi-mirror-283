from setuptools import find_packages, setup


def get_version():
    with open('version') as version_file:
        return version_file.read()


def get_requirements():
    with open('requirements.txt') as requirements_file:
        return [dependency.strip() for dependency in requirements_file if dependency.strip()]


setup_requires = [
    'flake8',
]

setup(name='credit_service_client',
      version=get_version(),
      packages=find_packages(),
      include_package_data=True,
      install_requires=get_requirements(),
      setup_requires=setup_requires,
      )
