
from setuptools import setup , find_packages

with open('README.md','r') as f:
    long_descreption = f.read()

setup (
    name='JdateConverter' , # base folder name 
    version="0.1.1",  
    packages=find_packages(), 
    description="A package for converting to and from Jalali datetime",
    long_description=open('README.md').read() ,
    long_description_content_type='text/markdown',
    author="Mohammad Namjoo" ,
    author_email="namjoo.mohammad111@gmail.com" ,
    #url="https://github.com/mamadgeek/CONVERTOR_5040" ,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        "jdatetime",  # 
    ],
    extras_require={
        'dev':["jdatetime>=5.0.0" ,
               "jalali_core>=1.0.0",
                "twine>=5.1.1"
               ]
    },
    
    python_requires = ">=3.12",
)

# ! pip install wheel twine jdatetime

#python setup.py bdist_wheel
# python setup.py bdist_wheel sdist

# locally  if you want 
# pip install . 


#generally 
# twine upload -r testpypi dist/*



# Name              5040dataanalytics
#  Email address    5040dataanalytics@gmail.com
# Username          5040_dataanalytics
# Password          maamd951219644002@    #dacf4a2ef0ff932c


# https://test.pypi.org/project/CONVERTOR-5040/0.1.0/

# token:
# pypi-AgENdGVzdC5weXBpLm9yZwIkNzcyYWQzOTEtYjgyZC00NDFlLWE2Y2MtNGQ5ZjNkMjI3ZWM5AAIqWzMsIjExZWIxZjlkLTExNjEtNDZhYS04ZTUwLWM1YzkwNzk2MDlmNSJdAAAGIDkDU-VSsKe7neeuO3tHW4_GAZFyp0qoQbdqMR1JYXZD




# lastly it returns like this:
# pip install -i https://test.pypi.org/simple/ JdateConverter==0.1.1

