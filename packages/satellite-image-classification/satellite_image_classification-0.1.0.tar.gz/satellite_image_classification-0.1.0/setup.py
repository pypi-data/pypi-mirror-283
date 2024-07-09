from setuptools import setup, find_packages

setup(
    name='satellite_image_classification',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'rasterio',
        'numpy',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'classify-image=satellite_image_classification.classification:main',
        ],
    },
)
