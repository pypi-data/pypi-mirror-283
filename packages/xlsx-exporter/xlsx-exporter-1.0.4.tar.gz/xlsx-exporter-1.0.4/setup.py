from setuptools import setup, find_packages

setup(
    name='xlsx-exporter',
    version='1.0.4',
    description='Plugin for exporting test cases to XLSX format',
    packages=find_packages(where='xlsx_exporter'),
    package_dir={'': 'xlsx_exporter'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'django',
    ],
    entry_points={
        'testy': [
            'xlsx-exporter = xlsx_exporter.src',  # Убедитесь, что путь правильный
        ],
    },
)
