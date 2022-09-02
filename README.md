# CSIT321-GoClimb


Pre-Requisites
<br>
<div>
    1. django<br>
    <s>
        2. pymongo-3.12.1<br>
        3. pytz<br>
        4. djongo<br>
        5. pymongo[srv]<br>
        6. django-filter<br>
    </s>
    7. pillow<br>
    8. mysqlclient
</div>

All of these can be installed through the python package manager using the pip command.

eg:-  
if version is mentioned

      pip install django==3.2 
      
if version is not mentioned
      
      pip install pillow
     
     
Running the Server

      python manage.py makemigrations

      python manage.py migrate

      python manage.py runserver


Mac(or any system with two different versions of python installed): 

      python3 manage.py makemigrations

      python3 manage.py migrate

      python3 manage.py runserver
