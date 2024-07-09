from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog


def BoxInfo(text):
    """
    Open A simple info box
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Information")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def BoxWarning(text):
    """
    Open A simple warning box
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle("Warning")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def BoxError(text):
    """
    Open A simple error box
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def BoxSelectFolder(argself, default_path=None):
    """
    return "" if nothing was selected else the path
    """
    if default_path == None or default_path == "":
        folder = QFileDialog.getExistingDirectory()
    else:
        folder = QFileDialog.getExistingDirectory(argself, caption="Select a folder", directory=default_path)
    return folder.replace("\\", "/")


def BoxYesNo(question):
    """
    return True if Yes is clicked, False in other cases
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(question)
    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    ret = msg.exec()
    if ret == msg.Yes:
        return True
    return False
