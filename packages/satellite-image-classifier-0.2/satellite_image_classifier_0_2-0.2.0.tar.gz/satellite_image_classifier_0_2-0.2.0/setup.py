from setuptools import setup, find_packages

setup(
    name='satellite_image_classifier_0.2',  # Updated project name
    version='0.2.0',
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
