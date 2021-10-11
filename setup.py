# Импорт недавно установленного пакета setuptools.
# Upload package to PyPi.
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository testpypi dist/*
# python3 -m twine upload --repository pypi dist/*
from setuptools import setup

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
    name="digital-sport",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.1.0",
    # Имя автора.
    author="Andrey Plugin",
    # Его почта.
    author_email="9keepa@gmail.com",
    # Краткое описание, которое будет показано на странице PyPi.
    description="Sport Api - structured data.",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    long_description=long_description,
    # Определяет тип контента, используемый в long_description.
    long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    url="https://github.com/repen/digital-sport",
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=["sport"],
    # requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
    install_requires=["requests"],
    # Требуемая версия Python.
    python_requires='>=3.6',
    # лицензия
    license='MIT',
)