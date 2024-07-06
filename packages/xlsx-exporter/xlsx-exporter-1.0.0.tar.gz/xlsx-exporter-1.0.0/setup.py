from setuptools import setup, find_packages

setup(
    name='xlsx-exporter',
    version='1.0.0',
    description='Plugin for exporting test cases to XLSX format',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pandas',
        'django',
        'testy',  # Подключение к TestY
    ],
    entry_points={
        'testy': [
            'import-plugin = xlsxExporter',
        ],
    },
)
