@echo off

mkdir minet\docs
xcopy /YS ..\..\src\* minet\
copy /Y ..\..\*.txt minet\docs\
move minet\minet-gui.py minet\minet-gui.pyw
copy /Y setup.py minet\
copy /Y minet.nsi minet\
cd minet
"C:\Python25\python.exe" setup.py py2exe
"C:\Program Files\7-zip\7z.exe" x -odist ..\gtk.zip
"C:\Program Files\NSIS\makensis.exe" minet.nsi
move minet-setup-*.exe ..\
cd ..
rmdir /S /Q minet
echo "OK!"
pause
