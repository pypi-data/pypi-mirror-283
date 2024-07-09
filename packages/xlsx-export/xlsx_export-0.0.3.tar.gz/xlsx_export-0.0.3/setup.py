from setuptools import setup, find_packages

setup(
    name='xlsx_export',
    version='0.0.3',
    description='Plugin for exporting test cases to XLSX format for TestY',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pandas',
        'django',
        'openpyxl',
    ],
    entry_points={
        'testy': [
            'xlsx-export = xlsx_export.views:PluginConfig',
        ],
    },
)
