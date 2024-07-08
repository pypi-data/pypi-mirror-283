import sys
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from sortrenamer.languages import Translation, Translator
from sortrenamer.toolbox import Toolkit


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.mainwidget_init()
        self.translator_init()

    def mainwidget_init(self) -> None:
        self.setFixedSize(QtCore.QSize(960, 540))
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.layout_centralwidget = QtWidgets.QGridLayout(parent=self.centralwidget)
        self.pixmaps_init()
        self.groupbox_tableview_init()
        self.groupbox_toolbox_init()
        self.groupbox_workdir_init()
        self.groupbox_exec_init()
        self.menu_init()
        self.setCentralWidget(self.centralwidget)

    def pixmaps_init(self) -> None:
        self.pixmap_home = QtWidgets.QStyle.StandardPixmap.SP_DirHomeIcon
        self.pixmap_opendir = QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton
        self.pixmap_apply = QtWidgets.QStyle.StandardPixmap.SP_DialogApplyButton
        self.pixmap_cancel = QtWidgets.QStyle.StandardPixmap.SP_DialogCancelButton
        self.pixmap_info = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxInformation
        self.pixmap_warning = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning
        self.setWindowIcon(self.style().standardIcon(self.pixmap_home))

    def groupbox_tableview_init(self) -> None:
        self.groupbox_tableview = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.layout_groupbox_tableview = QtWidgets.QGridLayout(parent=self.groupbox_tableview)
        self.tableview = QtWidgets.QTableView(parent=self.groupbox_tableview)
        self.tableview.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.tableview_itemmodel = QtGui.QStandardItemModel(parent=self.tableview)
        self.tableview_itemmodel.itemChanged.connect(self.select_item_in_tableview)
        self.tableview.setModel(self.tableview_itemmodel)
        self.layout_groupbox_tableview.addWidget(self.tableview, 0, 0, 1, 1)
        self.layout_centralwidget.addWidget(self.groupbox_tableview, 0, 0, 1, 1)

    def groupbox_toolbox_init(self) -> None:
        self.groupbox_toolbox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.layout_groupbox_toolbox = QtWidgets.QGridLayout(parent=self.groupbox_toolbox)
        self.toolbox = QtWidgets.QToolBox(parent=self.groupbox_toolbox)
        self.toolbox.currentChanged.connect(self.toolbox_change_page)
        self.page_rename_init()
        self.page_move_init()
        self.page_duplicates_init()
        self.layout_groupbox_toolbox.addWidget(self.toolbox, 0, 0, 1, 1)
        self.layout_centralwidget.addWidget(self.groupbox_toolbox, 0, 1, 1, 1)

    def page_rename_init(self) -> None:
        self.page_rename = QtWidgets.QWidget()
        self.layout_page_rename = QtWidgets.QGridLayout(parent=self.page_rename)
        self.lineedit_page_rename_exts = QtWidgets.QLineEdit(parent=self.page_rename)
        self.lineedit_page_rename_exts.setReadOnly(True)
        self.layout_page_rename.addWidget(self.lineedit_page_rename_exts, 0, 0, 1, 3)
        self.line_1_page_rename = QtWidgets.QFrame(parent=self.page_rename)
        self.line_1_page_rename.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1_page_rename.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_rename.addWidget(self.line_1_page_rename, 1, 0, 1, 3)
        self.radiobtn_page_rename_date = QtWidgets.QRadioButton(parent=self.page_rename)
        self.radiobtn_page_rename_date.clicked.connect(self.check_radiobtn_page_rename)
        self.layout_page_rename.addWidget(self.radiobtn_page_rename_date, 2, 0, 1, 1)
        self.checkbox_page_rename_exif = QtWidgets.QCheckBox(parent=self.page_rename)
        self.layout_page_rename.addWidget(self.checkbox_page_rename_exif, 2, 1, 1, 1)
        self.pushbtn_page_rename_show = QtWidgets.QPushButton(parent=self.page_rename)
        self.pushbtn_page_rename_show.setIcon(self.style().standardIcon(self.pixmap_info))
        self.pushbtn_page_rename_show.clicked.connect(self.find_image_dates)
        self.layout_page_rename.addWidget(self.pushbtn_page_rename_show, 2, 2, 1, 1)
        self.line_2_page_rename = QtWidgets.QFrame(parent=self.page_rename)
        self.line_2_page_rename.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2_page_rename.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_rename.addWidget(self.line_2_page_rename, 3, 0, 1, 3)
        self.radiobtn_page_rename_template = QtWidgets.QRadioButton(parent=self.page_rename)
        self.radiobtn_page_rename_template.clicked.connect(self.check_radiobtn_page_rename)
        self.layout_page_rename.addWidget(self.radiobtn_page_rename_template, 4, 0, 1, 1)
        self.lineedit_page_rename_template = QtWidgets.QLineEdit(parent=self.page_rename)
        self.regex_valid_name = QtCore.QRegularExpression(r"[0-9a-zA-Zа-яА-ЯёЁ _(){}[\]-]{250}+$")
        self.validator = QtGui.QRegularExpressionValidator(self.regex_valid_name)
        self.lineedit_page_rename_template.setValidator(self.validator)
        self.layout_page_rename.addWidget(self.lineedit_page_rename_template, 4, 1, 1, 2)
        self.toolbox.addItem(self.page_rename, "")

    def page_move_init(self) -> None:
        self.page_move = QtWidgets.QWidget()
        self.layout_page_move = QtWidgets.QGridLayout(parent=self.page_move)
        self.lineedit_page_move_exts = QtWidgets.QLineEdit(parent=self.page_move)
        self.lineedit_page_move_exts.setReadOnly(True)
        self.layout_page_move.addWidget(self.lineedit_page_move_exts, 0, 0, 1, 3)
        self.line_1_page_move = QtWidgets.QFrame(parent=self.page_move)
        self.line_1_page_move.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1_page_move.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_move.addWidget(self.line_1_page_move, 1, 0, 1, 3)
        self.radiobtn_page_move_date = QtWidgets.QRadioButton(parent=self.page_move)
        self.radiobtn_page_move_date.clicked.connect(self.check_radiobtn_page_move)
        self.layout_page_move.addWidget(self.radiobtn_page_move_date, 2, 0, 1, 1)
        self.checkbox_page_move_exif = QtWidgets.QCheckBox(parent=self.page_move)
        self.layout_page_move.addWidget(self.checkbox_page_move_exif, 2, 1, 1, 1)
        self.pushbtn_page_move_show = QtWidgets.QPushButton(parent=self.page_move)
        self.pushbtn_page_move_show.setIcon(self.style().standardIcon(self.pixmap_info))
        self.pushbtn_page_move_show.clicked.connect(self.find_image_dates)
        self.layout_page_move.addWidget(self.pushbtn_page_move_show, 2, 2, 1, 1)
        self.line_2_page_move = QtWidgets.QFrame(parent=self.page_move)
        self.line_2_page_move.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2_page_move.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_move.addWidget(self.line_2_page_move, 3, 0, 1, 3)
        self.radiobtn_page_move_exts = QtWidgets.QRadioButton(parent=self.page_move)
        self.radiobtn_page_move_exts.clicked.connect(self.check_radiobtn_page_move)
        self.layout_page_move.addWidget(self.radiobtn_page_move_exts, 4, 0, 1, 1)
        self.line_3_page_move = QtWidgets.QFrame(parent=self.page_move)
        self.line_3_page_move.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3_page_move.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_move.addWidget(self.line_3_page_move, 5, 0, 1, 3)
        self.lineedit_page_move_newdir = QtWidgets.QLineEdit(parent=self.page_move)
        self.lineedit_page_move_newdir.setReadOnly(True)
        self.layout_page_move.addWidget(self.lineedit_page_move_newdir, 6, 0, 1, 2)
        self.pushbtn_page_move_newdir = QtWidgets.QPushButton(parent=self.page_move)
        self.pushbtn_page_move_newdir.setIcon(self.style().standardIcon(self.pixmap_opendir))
        self.pushbtn_page_move_newdir.clicked.connect(self.select_newdir)
        self.layout_page_move.addWidget(self.pushbtn_page_move_newdir, 6, 2, 1, 1)
        self.toolbox.addItem(self.page_move, "")

    def page_duplicates_init(self) -> None:
        self.page_duplicates = QtWidgets.QWidget()
        self.layout_page_duplicates = QtWidgets.QGridLayout(parent=self.page_duplicates)
        self.lineedit_page_duplicates_exts = QtWidgets.QLineEdit(parent=self.page_duplicates)
        self.lineedit_page_duplicates_exts.setReadOnly(True)
        self.layout_page_duplicates.addWidget(self.lineedit_page_duplicates_exts, 0, 0, 1, 3)
        self.line_1_page_duplicates = QtWidgets.QFrame(parent=self.page_duplicates)
        self.line_1_page_duplicates.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1_page_duplicates.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_duplicates.addWidget(self.line_1_page_duplicates, 1, 0, 1, 3)
        self.checkbox_page_duplicates_move = QtWidgets.QCheckBox(parent=self.page_duplicates)
        self.layout_page_duplicates.addWidget(self.checkbox_page_duplicates_move, 2, 0, 1, 1)
        self.pushbtn_page_duplicates_show = QtWidgets.QPushButton(parent=self.page_duplicates)
        self.pushbtn_page_duplicates_show.setIcon(self.style().standardIcon(self.pixmap_info))
        self.pushbtn_page_duplicates_show.clicked.connect(self.find_file_duplicates)
        self.layout_page_duplicates.addWidget(self.pushbtn_page_duplicates_show, 2, 1, 1, 1)
        self.line_2_page_duplicates = QtWidgets.QFrame(parent=self.page_duplicates)
        self.line_2_page_duplicates.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2_page_duplicates.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.layout_page_duplicates.addWidget(self.line_2_page_duplicates, 3, 0, 1, 3)
        self.lineedit_page_duplicates_newdir = QtWidgets.QLineEdit(parent=self.page_duplicates)
        self.lineedit_page_duplicates_newdir.setReadOnly(True)
        self.layout_page_duplicates.addWidget(self.lineedit_page_duplicates_newdir, 4, 0, 1, 2)
        self.pushbtn_page_duplicates_newdir = QtWidgets.QPushButton(parent=self.page_duplicates)
        self.pushbtn_page_duplicates_newdir.setIcon(self.style().standardIcon(self.pixmap_opendir))
        self.pushbtn_page_duplicates_newdir.clicked.connect(self.select_newdir)
        self.layout_page_duplicates.addWidget(self.pushbtn_page_duplicates_newdir, 4, 2, 1, 1)
        self.toolbox.addItem(self.page_duplicates, "")

    def groupbox_workdir_init(self) -> None:
        self.groupbox_workdir = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.layout_groupbox_workdir = QtWidgets.QGridLayout(parent=self.groupbox_workdir)
        self.lineedit_workdir = QtWidgets.QLineEdit(parent=self.groupbox_workdir)
        self.lineedit_workdir.setReadOnly(True)
        self.layout_groupbox_workdir.addWidget(self.lineedit_workdir, 0, 0, 1, 5)
        self.pushbtn_workdir = QtWidgets.QPushButton(parent=self.groupbox_workdir)
        self.pushbtn_workdir.setIcon(self.style().standardIcon(self.pixmap_opendir))
        self.pushbtn_workdir.clicked.connect(self.select_workdir)
        self.layout_groupbox_workdir.addWidget(self.pushbtn_workdir, 1, 1, 1, 1)
        self.pushbtn_show_exts = QtWidgets.QPushButton(parent=self.groupbox_workdir)
        self.pushbtn_show_exts.setIcon(self.style().standardIcon(self.pixmap_info))
        self.pushbtn_show_exts.clicked.connect(self.find_file_exts)
        self.layout_groupbox_workdir.addWidget(self.pushbtn_show_exts, 1, 3, 1, 1)
        self.layout_centralwidget.addWidget(self.groupbox_workdir, 1, 0, 1, 1)

    def groupbox_exec_init(self) -> None:
        self.groupbox_exec = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.layout_groupbox_exec = QtWidgets.QGridLayout(parent=self.groupbox_exec)
        self.cmdlinkbtn_exec = QtWidgets.QCommandLinkButton(parent=self.groupbox_exec)
        self.cmdlinkbtn_exec.clicked.connect(self.execute)
        args = (self.cmdlinkbtn_exec, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout_groupbox_exec.addWidget(*args)
        self.layout_centralwidget.addWidget(self.groupbox_exec, 1, 1, 1, 1)

    def menu_init(self) -> None:
        self.menubar = QtWidgets.QMenuBar()
        self.menu_language_init()
        self.menu_theme_init()
        self.setMenuBar(self.menubar)

    def menu_language_init(self) -> None:
        self.menu_language = QtWidgets.QMenu()
        self.actions_language = {}
        for language in Translation.languages:
            action = QtGui.QAction(language, self)
            action.triggered.connect(self.select_language)
            action.setText(language)
            self.menu_language.addAction(action)
            self.actions_language[language] = action
        self.actions_language[Translation.languages[0]].setCheckable(True)
        self.actions_language[Translation.languages[0]].setChecked(True)
        self.actions_language[Translation.languages[0]].setDisabled(True)
        self.menubar.addMenu(self.menu_language)

    def menu_theme_init(self) -> None:
        self.menu_theme = QtWidgets.QMenu()
        self.actions_themes = {}
        self.theme = QtWidgets.QStyleFactory.keys()[-1]
        for theme in QtWidgets.QStyleFactory.keys():
            action = QtGui.QAction(theme, self)
            action.triggered.connect(self.select_theme)
            self.menu_theme.addAction(action)
            self.actions_themes[theme] = action
        self.actions_themes[self.theme].setCheckable(True)
        self.actions_themes[self.theme].setChecked(True)
        self.actions_themes[self.theme].setDisabled(True)
        self.menubar.addMenu(self.menu_theme)

    def translator_init(self) -> None:
        self.language = Translation.languages[0]
        self.translator = Translator.translator
        self.translator[self.language]["mainwindow"](self)

    def select_language(self) -> None:
        selected_language = self.sender()
        self.language = selected_language.text()
        self.translator[self.language]["mainwindow"](self)
        self.translator[self.language]["tableview_columnnames"](self, self.tableview_datatype)
        for language in Translation.languages:
            self.actions_language[language].setChecked(False)
            self.actions_language[language].setCheckable(False)
            self.actions_language[language].setEnabled(True)
        self.actions_language[self.language].setCheckable(True)
        self.actions_language[self.language].setChecked(True)
        self.actions_language[self.language].setDisabled(True)

    def select_theme(self) -> None:
        global app
        selected_theme = self.sender()
        self.theme = selected_theme.text()
        for theme in self.actions_themes:
            self.actions_themes[theme].setChecked(False)
            self.actions_themes[theme].setCheckable(False)
            self.actions_themes[theme].setEnabled(True)
        self.actions_themes[self.theme].setCheckable(True)
        self.actions_themes[self.theme].setChecked(True)
        self.actions_themes[self.theme].setDisabled(True)
        app.setStyle(self.theme)

    def toolbox_change_page(self) -> None:
        self.tableview_itemmodel.clear()
        self.tableview_datatype = ""

    def select_workdir(self) -> None:
        workdir = QtWidgets.QFileDialog.getExistingDirectory(self)
        if workdir:
            self.tableview_itemmodel.clear()
            self.tableview_datatype = ""
            self.lineedit_workdir.clear()
            self.lineedit_workdir.insert(workdir)

    def select_newdir(self) -> None:
        newdir = QtWidgets.QFileDialog.getExistingDirectory(self)
        if newdir:
            indices = (
                self.lineedit_page_move_newdir,
                self.lineedit_page_duplicates_newdir,
            )
            page_index = self.toolbox.currentIndex()
            indices[page_index - 1].clear()
            indices[page_index - 1].insert(newdir)

    def select_item_in_tableview(self) -> None:
        indices = (
            self.lineedit_page_rename_exts,
            self.lineedit_page_move_exts,
            self.lineedit_page_duplicates_exts,
        )
        page_index = self.toolbox.currentIndex()
        result = []
        for row in range(self.tableview_itemmodel.rowCount()):
            if self.tableview_itemmodel.item(row, 0).checkState() == QtCore.Qt.CheckState.Checked:
                index = self.tableview_itemmodel.index(row, 1)
                data = self.tableview_itemmodel.data(index)
                result.append(data)
        indices[page_index].clear()
        indices[page_index].insert(" ".join(result))

    def select_all_in_tableview_icon(self, column) -> None:
        if column == 0:
            args = (
                self.tableview_itemmodel.horizontalHeaderItem(0).icon().cacheKey(),
                self.style().standardIcon(self.pixmap_apply).cacheKey(),
            )
            if args[0] == args[1]:
                args = (
                    0,
                    QtCore.Qt.Orientation.Horizontal,
                    self.style().standardIcon(self.pixmap_cancel),
                    QtCore.Qt.ItemDataRole.DecorationRole,
                )
                self.tableview_itemmodel.setHeaderData(*args)
                for row in range(self.tableview.model().rowCount()):
                    index = self.tableview_itemmodel.index(row, 0)
                    args = (
                        index,
                        QtCore.Qt.CheckState.Checked,
                        QtCore.Qt.ItemDataRole.CheckStateRole,
                    )
                    self.tableview_itemmodel.setData(*args)
            else:
                args = (
                    0,
                    QtCore.Qt.Orientation.Horizontal,
                    self.style().standardIcon(self.pixmap_apply),
                    QtCore.Qt.ItemDataRole.DecorationRole,
                )
                self.tableview_itemmodel.setHeaderData(*args)
                for row in range(self.tableview.model().rowCount()):
                    index = self.tableview_itemmodel.index(row, 0)
                    args = (
                        index,
                        QtCore.Qt.CheckState.Unchecked,
                        QtCore.Qt.ItemDataRole.CheckStateRole,
                    )
                    self.tableview_itemmodel.setData(*args)

    def find_file_exts(self) -> None:
        self.setCursor(QtCore.Qt.CursorShape.BusyCursor)
        workdir = self.lineedit_workdir.text()
        if workdir:
            exts = Toolkit.folders_by_exts(Path(workdir))
            if exts:
                self.show_file_extensions(exts)
            else:
                self.warning_message(warning_type=("nothing found", None))
        else:
            self.warning_message(warning_type=("workdir not selected", None))
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def show_file_extensions(self, exts: dict) -> None:
        self.tableview_itemmodel.clear()
        self.tableview_datatype = "exts"
        self.translator[self.language]["tableview_columnnames"](self, self.tableview_datatype)
        args = (
            0,
            QtCore.Qt.Orientation.Horizontal,
            self.style().standardIcon(self.pixmap_apply),
            QtCore.Qt.ItemDataRole.DecorationRole,
        )
        self.tableview_itemmodel.setHeaderData(*args)
        self.tableview.horizontalHeader().setSectionsClickable(True)
        self.tableview.horizontalHeader().sectionClicked.connect(self.select_all_in_tableview_icon)
        for ext, quantity in exts.items():
            item_checkbox = QtGui.QStandardItem()
            item_checkbox.setCheckable(True)
            item_ext = QtGui.QStandardItem(ext)
            item_quantity = QtGui.QStandardItem(str(quantity))
            self.tableview_itemmodel.appendRow([item_checkbox, item_ext, item_quantity])
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def find_image_dates(self) -> None:
        self.setCursor(QtCore.Qt.CursorShape.BusyCursor)
        workdir = self.lineedit_workdir.text()
        exts = (
            self.lineedit_page_rename_exts.text().split(),
            self.lineedit_page_move_exts.text().split(),
        )
        exif = (
            self.checkbox_page_rename_exif.isChecked(),
            self.checkbox_page_move_exif.isChecked(),
        )
        page_index = self.toolbox.currentIndex()
        if workdir:
            img_only_exts = tuple(set(exts[page_index]) & set(Toolkit.img_exts))
            if img_only_exts:
                dates = Toolkit.folders_by_date(Path(workdir), img_only_exts, exif[page_index])
                if dates:
                    self.show_image_dates(dates)
                else:
                    self.warning_message(warning_type=("nothing found", None))
            else:
                self.warning_message(warning_type=("img exts not selected", Toolkit.img_exts))
        else:
            self.warning_message(warning_type=("workdir not selected", None))
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def show_image_dates(self, dates: dict) -> None:
        self.tableview_itemmodel.clear()
        self.tableview_datatype = "dates"
        self.translator[self.language]["tableview_columnnames"](self, self.tableview_datatype)
        self.tableview.horizontalHeader().setSectionsClickable(False)
        for year, months in dates.items():
            item_year = QtGui.QStandardItem(year)
            item_months = QtGui.QStandardItem(", ".join(months))
            self.tableview_itemmodel.appendRow([item_year, item_months])
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def find_file_duplicates(self) -> None:
        self.setCursor(QtCore.Qt.CursorShape.BusyCursor)
        workdir = self.lineedit_workdir.text()
        exts = self.lineedit_page_rename_exts.text().split()
        if workdir:
            if exts:
                duplicates = Toolkit.find_duplicates(Path(workdir), tuple(exts))
                if duplicates:
                    self.show_file_duplicates(duplicates)
                else:
                    self.warning_message(warning_type=("nothing found", None))
            else:
                self.warning_message(warning_type=("exts not selected", None))
        else:
            self.warning_message(warning_type=("workdir not selected", None))
        self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)

    def show_file_duplicates(self, duplicates: list) -> None:
        self.tableview_itemmodel.clear()
        columns_count = max(len(duplicate) for duplicate in duplicates)
        columns_name = [str(column) for column in range(1, columns_count + 1)]
        self.tableview_itemmodel.setHorizontalHeaderLabels(columns_name)
        self.tableview.horizontalHeader().setSectionsClickable(False)
        for i in range(len(duplicates)):
            row = []
            for duplicate in duplicates[i]:
                item = QtGui.QStandardItem(duplicate)
                row.append(item)
            self.tableview_itemmodel.appendRow(row)
        self.tableview.resizeColumnsToContents()

    def check_radiobtn_page_rename(self) -> None:
        if self.radiobtn_page_rename_date.isChecked():
            self.checkbox_page_rename_exif.setEnabled(True)
            self.pushbtn_page_rename_show.setEnabled(True)
            self.lineedit_page_rename_template.clear()
            self.lineedit_page_rename_template.setDisabled(True)
        elif self.radiobtn_page_rename_template.isChecked():
            self.checkbox_page_rename_exif.setChecked(False)
            self.checkbox_page_rename_exif.setDisabled(True)
            self.pushbtn_page_rename_show.setDisabled(True)
            self.lineedit_page_rename_template.setEnabled(True)

    def check_radiobtn_page_move(self) -> None:
        if self.radiobtn_page_move_date.isChecked():
            self.checkbox_page_move_exif.setEnabled(True)
            self.pushbtn_page_move_show.setEnabled(True)
        elif self.radiobtn_page_move_exts.isChecked():
            self.checkbox_page_move_exif.setChecked(False)
            self.checkbox_page_move_exif.setDisabled(True)
            self.pushbtn_page_move_show.setDisabled(True)

    def warning_message(self, warning_type: tuple) -> None:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowIcon(self.style().standardIcon(self.pixmap_home))
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.translator[self.language]["warning_message"](msgbox, warning_type)
        msgbox.exec()

    def info_message(self, info_type: tuple) -> None:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowIcon(self.style().standardIcon(self.pixmap_home))
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.translator[self.language]["info_message"](msgbox, info_type)
        msgbox.exec()

    def execute(self) -> None:
        indices = (
            self.execute_page_rename,
            self.execute_page_move,
            self.execute_page_duplicates,
        )
        page_index = self.toolbox.currentIndex()
        indices[page_index]()

    def execute_page_rename(self) -> None:
        workdir = self.lineedit_workdir.text()
        exts = self.lineedit_page_rename_exts.text().split()
        if not workdir:
            self.warning_message(warning_type=("workdir not selected", None))
        elif not exts:
            self.warning_message(warning_type=("exts not selected", None))
        elif self.radiobtn_page_rename_date.isChecked():
            img_only = set(exts) & set(Toolkit.img_exts)
            if not img_only:
                self.warning_message(warning_type=("img exts not selected", None))
            else:
                if self.checkbox_page_rename_exif.isChecked():
                    count = Toolkit.rename_by_date(Path(workdir), tuple(exts), True)
                    self.info_message(info_type=("renamed images", count))
                else:
                    count = Toolkit.rename_by_date(Path(workdir), tuple(exts), False)
                    self.info_message(info_type=("renamed images", count))
        elif self.radiobtn_page_rename_template.isChecked():
            template = self.lineedit_page_rename_template.text()
            if not template:
                self.warning_message(warning_type=("template not selected", None))
            elif max(len(ext) for ext in exts) + len(template) > 256:
                self.warning_message(warning_type=("template long", None))
            else:
                count = Toolkit.rename_by_template(Path(workdir), tuple(exts), template)
                self.info_message(info_type=("renamed files", count))
        else:
            self.warning_message(warning_type=("nothing selected", None))

    def execute_page_move(self) -> None:
        workdir = self.lineedit_workdir.text()
        newdir = self.lineedit_page_move_newdir.text()
        exts = self.lineedit_page_rename_exts.text().split()
        if not workdir:
            self.warning_message(warning_type=("workdir not selected", None))
        elif not exts:
            self.warning_message(warning_type=("exts not selected", None))
        elif not newdir:
            self.warning_message(warning_type=("newdir not selected", None))
        elif self.radiobtn_page_move_date.isChecked():
            img_only = set(exts) & set(Toolkit.img_exts)
            if not img_only:
                self.warning_message(warning_type=("img exts not selected", None))
            else:
                if self.checkbox_page_move_exif.isChecked():
                    count = Toolkit.move_by_date(Path(workdir), tuple(exts), Path(newdir), True)
                    self.info_message(info_type=("moved images", count))
                else:
                    count = Toolkit.move_by_date(Path(workdir), tuple(exts), Path(newdir), False)
                    self.info_message(info_type=("moved images", count))
        elif self.radiobtn_page_move_exts.isChecked():
            count = Toolkit.move_by_exts(Path(workdir), tuple(exts), Path(newdir))
            self.info_message(info_type=("moved files", count))
        else:
            self.warning_message(warning_type=("nothing selected", None))

    def execute_page_duplicates(self) -> None:
        workdir = self.lineedit_workdir.text()
        newdir = self.lineedit_page_duplicates_newdir.text()
        exts = self.lineedit_page_rename_exts.text().split()
        if not workdir:
            self.warning_message(warning_type=("workdir not selected", None))
        elif not exts:
            self.warning_message(warning_type=("exts not selected", None))
        elif not newdir:
            self.warning_message(warning_type=("newdir not selected", None))
        elif self.checkbox_page_duplicates_move.isChecked():
            duplicates = Toolkit.find_duplicates(Path(workdir), tuple(exts))
            if duplicates:
                Toolkit.move_duplicates(Path(newdir), duplicates)
                count = sum(len(duplicate) for duplicate in duplicates)
                self.info_message(info_type=("duplicates moved", count))
            else:
                self.warning_message(warning_type=("nothing found", None))
        else:
            self.warning_message(warning_type=("nothing selected", None))


def main() -> None:
    global app
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
