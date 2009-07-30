@echo off

mkdir minet\docs
xcopy /YS ..\..\src\* minet\
copy /Y ..\..\*.txt minet\docs\
move minet\minet-gui.py minet\minet-gui.pyw
copy /Y setup_4_py2exe.py minet\
copy /Y minet_nb.nsi minet\
cd minet
"C:\Python25\python.exe" setup_4_py2exe.py py2exe
"C:\Program Files\7-zip\7z.exe" x -odist ..\gtk.zip
pause
"C:\Program Files\NSIS\makensis.exe" minet_nb.nsi
move minet-setup.exe ..\
cd ..
rmdir /S /Q minet
echo "OK!"
pause
