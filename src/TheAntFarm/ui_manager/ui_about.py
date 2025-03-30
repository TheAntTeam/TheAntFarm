from PySide6.QtCore import QSize, Qt, QObject
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel
from PySide6.QtGui import QPixmap


class UiAbout(QObject):
    """Manage UI objects, signals and slots"""
    def __init__(self, main_win, app_settings):
        self.main_win = main_win
        self.app_settings = app_settings

    def show_about_info(self):
        qp_map = QPixmap(u":/resources/resources/logo/the_ant_farm_logo.svg")
        about_dlg = QDialog(parent=self.main_win)
        about_dlg.setModal(True)
        about_dlg.setWindowTitle("About The Ant Farm")
        about_dlg.setFixedSize(QSize(400, 350))
        grid = QGridLayout()
        about_dlg.setLayout(grid)

        ico_label = QLabel("", about_dlg)
        ico_label.setPixmap(qp_map)
        ico_label.setFixedSize(QSize(100, 100))
        ico_label.setScaledContents(True)
        grid.addWidget(ico_label, 0, 0, alignment=Qt.AlignCenter, rowSpan=1, columnSpan=1)

        version_la = QLabel("Version " + self.app_settings.app_version, about_dlg)
        version_la.setStyleSheet("QLabel{font-size: 16pt;}")
        grid.addWidget(version_la, 0, 1, alignment=Qt.AlignCenter, rowSpan=1, columnSpan=1)

        credits_la = QLabel("Developed by: ", about_dlg)
        credits_la.setStyleSheet("QLabel{font-size: 16pt;}")
        grid.addWidget(credits_la, 1, 0, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        credits_2_la = QLabel("The Ant Team and \nthe kind contributors", about_dlg)
        credits_2_la.setStyleSheet("QLabel{font-size: 16pt;}")
        credits_2_la.setWordWrap(True)
        grid.addWidget(credits_2_la, 1, 1, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        license_la = QLabel("License: ", about_dlg)
        license_la.setStyleSheet("QLabel{font-size: 16pt;}")
        grid.addWidget(license_la, 2, 0, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        license_2_la = QLabel("<a href=\"https://github.com/TheAntTeam/TheAntFarm/blob/main/LICENSE\">MIT License</a>", about_dlg)
        license_2_la.setStyleSheet("QLabel{font-size: 16pt;}")
        license_2_la.setTextFormat(Qt.RichText)
        license_2_la.setTextInteractionFlags(Qt.TextBrowserInteraction)
        license_2_la.setOpenExternalLinks(True)
        grid.addWidget(license_2_la, 2, 1, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        yt_la = QLabel("<a href=\"https://www.youtube.com/c/TheAntPCBMaker\">Youtube Here!</a>", about_dlg)
        yt_la.setStyleSheet("QLabel{font-size: 16pt;}")
        yt_la.setTextFormat(Qt.RichText)
        yt_la.setTextInteractionFlags(Qt.TextBrowserInteraction)
        yt_la.setOpenExternalLinks(True)
        grid.addWidget(yt_la, 3, 0, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        repo_la = QLabel("<a href=\"https://github.com/TheAntTeam/TheAntFarm\">Repo Here!</a>", about_dlg)
        repo_la.setStyleSheet("QLabel{font-size: 16pt;}")
        repo_la.setTextFormat(Qt.RichText)
        repo_la.setTextInteractionFlags(Qt.TextBrowserInteraction)
        repo_la.setOpenExternalLinks(True)
        grid.addWidget(repo_la, 3, 1, alignment=Qt.AlignCenter | Qt.AlignVCenter, rowSpan=1, columnSpan=1)

        about_dlg.show()


if __name__ == "__main__":
    pass
