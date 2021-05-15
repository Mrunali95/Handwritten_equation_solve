#!C:/Users/Lenovo/AppData/Local/Programs/Python/Python37-32/python.exe
#-*- coding:UTF-8 -*-
print ("Content-type:text/html")
print ()# Tell the server to end the header

import cgi, os
import cgitb; cgitb.enable()
 # Imports PIL module 
import io
from google.cloud import vision
from google.cloud.vision_v1 import types

form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid 
   # directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('C:/Users/Lenovo/Desktop/NCI/Extra/' + fn, 'wb').write(fileitem.file.read())

   message = 'The file "' + fn + '" was uploaded successfully'
   
   print("""\
    <html>
    <body><center>
       <p><h1> SOLUTION </h1> </p>
       <!--p><img src=/Extra/%s></p-->
    </center></body>
    </html>
    """ % (fn,))   
       
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Lenovo\Desktop\NCI\Extra\tactile-visitor-310310-2a686bf97f27.json"

   client = vision.ImageAnnotatorClient()

   def detectText(img):
        with io.open(img, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.full_text_annotation.text
        
            
        return texts


   File_name = fn
   path = r'C:/Users/Lenovo/Desktop/NCI/Extra'
   img = os.path.join(path, File_name)
    
   out = (detectText(img))  
   
   
   print("""\
    <html>
    <body><center>
       <p> <h3>Detected Equation: %s </h3></p>
    </center></body>
    </html>
    """ % (out,))   
   
   
   def removechar(out):
    for c in out:
        if c.isalpha():
            out = out.replace(c,' ')
    return out

   def add_bracs(out):
        if '(' not in out:
            out = '(' + out
    
        if ')' not in out:
            out = (')/').join(out.split('/'))
        return out
    
   def beautify1(out):
        out = out.strip("\n")
        out = out.strip("?")
        out = out.strip("=")
        out = out.replace('x','*')
        out = out.replace('X','*')
        out = out.replace('=','/')
        out = out.replace(':','/')
        
        if out.count('(') != out.count(')'):
            out = '(' + out
        
        if '(' in out or ')' in out:
            if not not ((out.split(")")[1]).lstrip(" ")) and (((out.split(")")[1]).lstrip(" "))[0]).isdigit():
                out = out.replace(')',')*')
    
            if not not ((out.split("(")[0]).lstrip(" ")) and (((out.split("(")[0]).rstrip(" "))[-1]).isdigit():
                out = out.replace('(','*(')
        
        return(out)

   out = beautify1(out)
    
   def beautify2(out):
        if '\n' in out:
            out = out.replace('\n','/')
            out = removechar(out)
            out = add_bracs(out)
        else:
            out = removechar(out)
        
        out = out.lstrip(' ')
        return out
    
   out = beautify2(out)
    
   def verify(out):
        if out[0] == '(' or out[0].isdigit():
            return out
        else:
            out = out.replace(out[0],' ')
            out = out.lstrip(' ')
            return out
     
        
   out = verify(out)
    
   print("""\
    <html>
    <body><center>
       <p><h3> Predicted Equation: %s </h3></p>
    </center></body>
    </html>
    """ % (out,))
    
   def solve(prob):
        return eval(prob)

   res = solve(out)
 
   print("""\
    <html>
    <body><center>
       <p><h3> Solution: %s </h3></p>
    </center></body>
    </html>
    """ % (res,))
   
else:
   message = 'No file was uploaded'
   
   print("""\
    <html>
    <body>
       <p><h3>%s </h3></p>
    </body>
    </html>
    """ % (message,))