pyinstaller --add-data "Images/*.png;Images" -n "Camera" -i "./Images/Logo.ico" -w -F ./src/main.py

#rm -rf ./dist/Camera/*.dll
#rm -rf ./dist/Camera/*.py
#rm -rf ./dist/Camera/PyQt5/ls
