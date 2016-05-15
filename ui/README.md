# User Interface

PySide (therefore Qt) is used for the GUI.

[Qt Creator](https://www.qt.io/ide/) is a good software package that is very helpful in creating your own GUIs. You can make changes to the included gui.ui file using Qt Creator.

Once you have the updated gui.ui file, copy it to $PYTHON$/Scripts folder where $PYTHON$ is the address to your Python installation.

Open up a terminal or command window in this directory and execute the following:

    pyside-uic gui.ui -o gui.py

This will create a .py file PySide can use. Replace the gui.py in the ~/aerial folder with your modified version.

You might also need to update runtime.py as necessary to implement functionality.

You may also delete this ui folder for your end-product as it is here only for reference.
