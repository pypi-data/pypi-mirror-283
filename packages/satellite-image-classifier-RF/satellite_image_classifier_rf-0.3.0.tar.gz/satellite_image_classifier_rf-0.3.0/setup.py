from setuptools import setup, find_packages

setup(
    name='satellite_image_classifier_RF',  # Updated project name
    version='0.3.0',  # Incremented version number
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'rasterio',
        'numpy',
        'scikit-learn',
        'fiona',
        'shapely',
    ],
    entry_points={
        'console_scripts': [
            'classify-image=satellite_image_classification.classification:main',
        ],
    },
)
