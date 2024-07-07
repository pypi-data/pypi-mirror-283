from setuptools import setup, find_packages

setup(
name='Flask-Shopify-Integration',
version='0.7',
packages=find_packages(),
platforms='',
install_requires=[
'Flask==2.0.3'
,'Flask-Cors==3.0.8'
,'Flask-JWT-Extended==4.4.2'
,'Flask-JWT-Simple==0.0.3'
,'flask-marshmallow==0.10.1'
,'Flask-SQLAlchemy==2.4.1'
,'flask-swagger-ui==3.36.0'
,'Jinja2==3.0.3'
,'MarkupSafe==2.0.1'
,'marshmallow==3.3.0'
,'marshmallow-sqlalchemy==0.21.0'
,'Pillow==7.2.0'
,'PyJWT==2.4.0'
,'pyodbc==4.0.27'
,'python-dotenv==0.10.3'
,'PyYAML==5.3'
,'ShopifyAPI==12.4.0'
,'SQLAlchemy==1.3.13'
],
)