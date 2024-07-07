from setuptools import setup, find_packages

setup(
    name="django-shinzo",
    version="0.2.2",
    py_modules=["git_cloner"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shinzo=git_cloner:clone_repo',
        ],
    },
    install_requires=[  # List of dependencies
        "black",
        "djangorestframework",
        "drf-spectacular",
        "drf-spectacular-sidecar",
        "Django",
        "django-jazzmin",
        "gunicorn",
        "pillow",
        "psycopg2-binary",
        "python-dotenv",
        "django-modeltranslation",
        "django-ckeditor-5",
        "django-cors-headers",
        "django-rosetta",
        "colorama",
        "PyJWT",
        "django-unfold"
    ],
    author="Jahongir Hakimjonov",
    author_email="jahongirhakimjonov@gmail.com",
    description="A Django project structure generator",
    keywords="django project structure generator",
    url="https://github.com/JahongirHakimjonov",
    classifiers=[  # Classifiers for package indexing
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

)
