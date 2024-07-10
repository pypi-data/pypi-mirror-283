from setuptools import setup, find_packages

setup(
    name='xlsx_export',
    version='0.0.8',
    description='Plugin for exporting test cases to XLSX format for TestY',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'django',
        'openpyxl',
    ],
    entry_points={
        'testy': [
            'xlsx_export = xlsx_export.views:PluginConfig',
        ],
    },
)
