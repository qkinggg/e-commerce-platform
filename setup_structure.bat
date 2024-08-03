@echo off
mkdir app
cd app
echo. > __init__.py
echo. > models.py
mkdir routes
cd routes
echo. > __init__.py
echo. > auth.py
echo. > product.py
echo. > cart.py
echo. > order.py
echo. > admin.py
cd ..
mkdir templates
cd templates
echo. > base.html
echo. > index.html
echo. > product.html
cd ..
cd ..
mkdir static
cd static
mkdir css
mkdir js
cd ..
echo. > config.py
echo. > requirements.txt
echo. > run.py
echo. > README.md