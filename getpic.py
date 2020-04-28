import os
import pathlib
import shutil

SOURCEDIR = pathlib.Path(r"C:\Users\Administrator\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets")
if not os.path.exists('PICS'):os.mkdir('PICS')
TARGETDIR = os.path.abspath('PICS')

os.chdir(SOURCEDIR)
for file in os.listdir(SOURCEDIR):
	if os.stat(file).st_size > 1024*100:
		shutil.copy2(file, os.path.join(TARGETDIR, f'{file}.jpg'))



	
