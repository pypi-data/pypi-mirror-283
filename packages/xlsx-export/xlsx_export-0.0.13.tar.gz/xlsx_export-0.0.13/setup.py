from setuptools import setup, find_packages

setup(
    name='xlsx_export',
    version='0.0.13',
    description='Plugin for exporting test cases to XLSX format for TestY',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'django',
        'openpyxl',
        'testy',
    ],
    entry_points={
        'testy': [
            'xlsx_export = xlsx_export',
        ],
    },
)
