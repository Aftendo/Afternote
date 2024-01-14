# Afternote
Modern open-source Flipnote Hatena server
# Installation
Wanna install Afternote on your server? See how:
(NOTE: This is only to install Afternote SERVER, patches are currently unavailable.)
## Requirements
- Terminal access 
- Python 3.11 or higher
- Django
- Django extensions
- Numpy
## Installation steps
- Step 1: Open Terminal


![image](https://github.com/ItsAymo/Afternote/assets/147617344/fdc9bcae-2df3-4539-ba9f-1dbd96a649a1)
- Step 2: If not already installed, install `virtualenv` with `sudo apt install virtualenv` (May depend on your Linux distribution)
- Step 3: Create the directory "python-environnements" at /home/<user> and then access it with `mkdir ~/python-environments && cd ~/python-environments
`![image](https://github.com/ItsAymo/Afternote/assets/147617344/cb511126-86d2-4617-bf80-002f623e7144)

- Step 4: Create a virtual environnement with ` virtualenv --python=python3 <Name of your virtualenv>`
![image](https://github.com/ItsAymo/Afternote/assets/147617344/660169e6-f67b-488b-b812-e58ce1ff5e97)
- Step 5: Now check your Python version with `ls env/lib`, if Python3.11 is shown, continue, if not, update Python.
![image](https://github.com/ItsAymo/Afternote/assets/147617344/58270721-d918-45e7-8c6d-4c1cbe7d9c60)
- Step 6: Activate your Virtualenv with `source env/bin/activate`


An "(<env>)" has been added to your terminal. (Depends on your environnement name)
![image](https://github.com/ItsAymo/Afternote/assets/147617344/b4111bc2-c582-42ca-87b3-1f712938cc3f)



If you havent installed dependencies, install them with `pip install django && pip install django_extensions && pip install numpy`
![image](https://github.com/ItsAymo/Afternote/assets/147617344/cf742164-8023-4be8-8476-50b2f591ea80)
- Step 7: Clone the repository with `git clone https://github.com/Aftendo/Afternote`
![image](https://github.com/ItsAymo/Afternote/assets/147617344/00fbcb2c-09a3-4e53-a2bc-b733adc94e53)
- Step 8: Enter the directory with `cd Afternote`
- Step 9: Modify `DEBUG = True` with a text editor or with `nano ugoflip/settings.py`, (Not necessary)
![image](https://github.com/ItsAymo/Afternote/assets/147617344/b8ba0b35-6adb-4e11-bf97-c0875776bba3)
![image](https://github.com/ItsAymo/Afternote/assets/147617344/bd2d8fa0-f65e-4bf1-81b1-5b5150076b14)
![image](https://github.com/ItsAymo/Afternote/assets/147617344/51ff12ee-3034-4e1b-a5fd-c9e935c1d35d)
- Step 10: Runserver with `python3 manage.py runserver` (Local only)
![image](https://github.com/ItsAymo/Afternote/assets/147617344/de55a78e-58ef-4995-a741-8e9eafc59017)
- Step 11: Check your browser with the URL: https://127.0.0.1:8000/
![image](https://github.com/ItsAymo/Afternote/assets/147617344/ad30a689-441f-4cc6-819c-633695e972d5)


If the Django 404 page shows, that means you haven't modified `settings.py` for setting `DEBUG` to False.


If you followed correctly all those steps, you should now have a Afternote server.







