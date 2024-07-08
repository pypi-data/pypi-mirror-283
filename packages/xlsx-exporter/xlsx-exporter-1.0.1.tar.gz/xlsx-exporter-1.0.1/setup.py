from setuptools import setup, find_packages



setup(
    name='xlsx-exporter',
    version='1.0.1',
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
            'xlsx-exporter = xlsxExporter.plugin:plugin_entry_point',  # Убедитесь, что путь корректен
        ],
    },
)
