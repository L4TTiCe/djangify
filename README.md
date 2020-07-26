# Djangify
A Python script that converts HTML Files / Templates to Django compatible HTML Templates. 
Brought to you by : <a href="https://ohuru.tech/">Ohuru</a>

## Installation

    pip install djangify

## Usage Info
    
    username@hostname $ djangify -h
    usage: djangify.py [-h] [-d [BASE_DIRECTORY]] [-a [APP_NAME]] [f [f ...]]

    Converts specified html files or all html files to django format within a
    specified directory.

    positional arguments:
      f                    provide file names to convert

    optional arguments:
      -h, --help           show this help message and exit
      -d [BASE_DIRECTORY]  Provide base directory
      -a [APP_NAME]        provide django app name
    
## Description
Converts all the HTML files specified in the files (' f ') argument into Django templates, replacing the contents of 'src', 'href' and 'url' tags with their Django compatible static conterparts with their Django App name prefixed.

#### For Example:
To process a set of HTML files, copy the djangify.py script to the directory containing these HTML files, and run the following command, (Here 'blog' refers to the App name for which we are processing these files)
    
    $ djangify -a blog
  
This command will replace all local files referenced in 'src', 'href' and 'url' tags in the following way :
  
Original :
```python
    <img class="mySlides" src="res/landreg/1.jpg" style="width:100%">
    <li><a href="register.html">Register</a></li>
```

After script execution :
 ```python
    <img class="mySlides" src=" {% static 'blog/res/landreg/1.jpg' %} " style="width:100%">
    <li><a href=" {% static 'blog/register.html' %} ">Register</a></li>
```

The generated files from app `Blog` will reside inside `Modified_Files`
