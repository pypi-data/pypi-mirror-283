from setuptools import setup, find_packages

setup(
    name="django-shinzo",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'django-shinzo=django_default.django_default:clone_repo',
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
    classifiers=[  # Classifiers for package indexing
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

)
