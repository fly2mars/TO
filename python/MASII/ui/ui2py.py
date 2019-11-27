import subprocess
subprocess.call("pyuic5 main_window.ui -o ui_mainwindow.py")
subprocess.call("pyuic5 about.ui -o ui_about.py")
subprocess.call("pyrcc5 resource.qrc -o ../resource_rc.py")