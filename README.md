
# UAS Microservice CRUD API PL/SQL UNSIA

Sebuah project app API CRUD menggunakan framework Django REST Framework (DRF) dan PostgreSQL.
- [Dokumen & SDLC](https://drive.google.com/file/d/1hu6VQ-laLVIq8oaTdnS0H_yrRSwCl0zI/view?usp=drive_link)
- [Dokumen Postman](https://drive.google.com/drive/folders/1IQTpZ_VNiW3fGSZRT8hGHfSxMt10Ff1w?usp=sharing)


## How to Run

Berikut yang harus kamu ikuti untuk menjalankan app ini:

1. Setelah clone projek dan membukanya
2. Sesuaikan config database anda di unsia/settings.py
    ```bash
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_unsia',
            'USER': 'postgres', -> change your user postgres
            'PASSWORD': '123456789', -> your password postgres
            'HOST': 'localhost'
        }
    }
    ```

3. Install Python 3

   WindowsOS\
   [How to Install Python on Windows](https://www.digitalocean.com/community/tutorials/install-python-windows-10)

   MacOS
    ```bash
    brew install python3
    ```

4. Install virtualEnv

   WindowsOS
    ```bash
    pip3 install virtualenv
    ```

    MacOS
    ```bash
    sudo pip3 install virtualenv
    ```

6. Create Virtualenv di path projek ini

    WindowsOS
    ```bash
    python -m venv venv
    ```

    MacOS
    ```bash
    virtualenv venv -p python3
    ```

8. Aktifasikan Virtualenv

   WindowsOS
    ```bash
    venv\Scripts\activate
    ```

    MacOS
    ```bash
    source venv/bin/activate
    ```

    untuk nonaktikannya
    ```bash
    deactivate
    ```

10. Install requirement dengan command:
    ```bash
    pip install -r requirements.txt
    ```
    
14. Makemigrations Database
    ```bash
    python manage.py makemigrations users
    python manage.py migrate
    ```
    
16. Jalan kan server
    ```bash
    python manage.py runserver
    ```
