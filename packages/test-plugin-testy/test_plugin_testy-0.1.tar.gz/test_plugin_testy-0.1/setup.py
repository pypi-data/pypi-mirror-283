from setuptools import setup, find_packages

setup(
    name='test_plugin_testy',
    version='0.1',
    description='Test plugin for uploading files',
    packages=find_packages(),
    install_requires=[
        'django',
        'testy',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'testy': ['test_plugin_testy=test_plugin'],
    },
)
