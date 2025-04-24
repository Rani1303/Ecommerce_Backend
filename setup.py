from setuptools import setup, find_packages

setup(
    name="ecommerce",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "pydantic[email]",
        "python-dotenv"
    ],
) 