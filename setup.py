from setuptools import setup, find_packages

setup(
    name='guess-the-song',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.0",
        "Werkzeug==3.1.2",
        "Flask-Login==0.6.3",
        "Flask-SocketIO==5.3.6",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-WTF==1.2.1",
        "WTForms==3.1.1",
        "yt-dlp==2026.3.3",
        "psycopg2-binary==2.9.10",
    ],
    entry_points={
        'console_scripts': [
            'guess-the-song = main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'website': ['static/*.js', 'static/*.css', 'templates/*.html'],
        'Concept Arts': ['*.jpg', '*.png'],
    },
)
