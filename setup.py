from setuptools import setup, find_packages

setup(
    name='guess-the-song',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Tutaj możesz umieścić zależności Twojego projektu
    ],
    entry_points={
        'console_scripts': [
            'guess-the-song = website.main:run',
        ],
    },
    include_package_data=True,
    package_data={
        'website': ['static/*.js', 'static/*.css', 'templates/*.html'],
        'Concept Arts': ['*.jpg', '*.png'],
    },
)
