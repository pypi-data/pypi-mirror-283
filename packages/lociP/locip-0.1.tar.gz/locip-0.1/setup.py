from setuptools import setup, find_packages

setup(
    name='lociP',
    version='0.1',
    packages=find_packages(),
    package_data={
        'lociP': ['QAmodel_lociPARSE.pt'],  # Adjust 'model.pt' to your actual model file name
    },
    include_package_data=True,
    install_requires=[
        'numpy==1.22.3',
        'tqdm==4.64.0',
        'torch==1.12.0',  # This might need to be customized depending on CUDA version
        'scipy==1.7.3',
        'scikit-learn==1.1.1',
        'pandas==1.4.4',
        'openpyxl',
        'seaborn==0.12.0',
        'matplotlib==3.5.2',
    ],
    entry_points={
        'console_scripts': [
            # You can define command-line scripts here
        ]
    },
)
