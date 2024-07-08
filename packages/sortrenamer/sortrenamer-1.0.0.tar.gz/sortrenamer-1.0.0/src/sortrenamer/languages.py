class Translation:
    languages = ("English", "Russian")

    class English:
        @staticmethod
        def mainwindow(mainwindow) -> None:
            mainwindow.setWindowTitle("SortRenamer")
            mainwindow.groupbox_tableview.setTitle("Available data")
            mainwindow.groupbox_toolbox.setTitle("Tools")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_rename), "Renaming")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_move), "Moving")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_duplicates), "Duplicates")
            mainwindow.lineedit_page_rename_exts.setPlaceholderText("Select file extensions")
            mainwindow.radiobtn_page_rename_date.setText("By creation date\n(images only)")
            mainwindow.checkbox_page_rename_exif.setText("Use exif\n(if present)")
            mainwindow.pushbtn_page_rename_show.setText("Dates")
            mainwindow.radiobtn_page_rename_template.setText("By name template")
            mainwindow.lineedit_page_rename_template.setPlaceholderText("Enter a name template")
            mainwindow.lineedit_page_move_exts.setPlaceholderText("Select file extensions")
            mainwindow.radiobtn_page_move_date.setText("By creation date\n(images only)")
            mainwindow.checkbox_page_move_exif.setText("Use exif\n(if present)")
            mainwindow.pushbtn_page_move_show.setText("Dates")
            mainwindow.radiobtn_page_move_exts.setText("By file extensions")
            mainwindow.lineedit_page_move_newdir.setPlaceholderText("Select a new directory")
            mainwindow.pushbtn_page_move_newdir.setText("Open")
            mainwindow.lineedit_page_duplicates_exts.setPlaceholderText("Select file extensions")
            mainwindow.checkbox_page_duplicates_move.setText("Move\n(all duplicates)")
            mainwindow.pushbtn_page_duplicates_show.setText("Duplicates")
            mainwindow.lineedit_page_duplicates_newdir.setPlaceholderText("Select a new directory")
            mainwindow.pushbtn_page_duplicates_newdir.setText("Open")
            mainwindow.groupbox_workdir.setTitle("Working directory and available file extensions")
            mainwindow.lineedit_workdir.setPlaceholderText("Select working directory")
            mainwindow.pushbtn_workdir.setText("Open")
            mainwindow.pushbtn_show_exts.setText("Extensions")
            mainwindow.cmdlinkbtn_exec.setText("Execute")
            mainwindow.menu_language.setTitle("Translation")
            mainwindow.menu_theme.setTitle("Themes")

        @staticmethod
        def warning_message(msgbox, warning_type: tuple) -> None:
            msgbox.setWindowTitle("Warning")
            if warning_type[0] == "nothing found":
                msgbox.setText("Nothing found in working directory")
            elif warning_type[0] == "nothing selected":
                msgbox.setText("No tools are selected")
            elif warning_type[0] == "workdir not selected":
                msgbox.setText("Working directory not selected")
            elif warning_type[0] == "exts not selected":
                msgbox.setText("File extensions not selected")
            elif warning_type[0] == "img exts not selected":
                msgbox.setText("Image extensions not selected")
                msgbox.setInformativeText(f"Available image extensions:\n{", ".join(warning_type[1])}")
            elif warning_type[0] == "template not selected":
                msgbox.setText("Template for renaming is not selected")
            elif warning_type[0] == "template long":
                msgbox.setText("Template + file extensions > 256")
            elif warning_type[0] == "newdir not selected":
                msgbox.setText("New directory not selected")

        @staticmethod
        def info_message(msgbox, info_type: tuple) -> None:
            msgbox.setWindowTitle("Information")
            if info_type[0] == "renamed images":
                msgbox.setText(f"{info_type[1]} images successfully renamed")
            elif info_type[0] == "renamed files":
                msgbox.setText(f"{info_type[1]} files successfully renamed")
            elif info_type[0] == "moved images":
                msgbox.setText(f"{info_type[1]} images successfully moved")
            elif info_type[0] == "moved files":
                msgbox.setText(f"{info_type[1]} files successfully moved")
            elif info_type[0] == "duplicates moved":
                msgbox.setText(f"{info_type[1]} duplicates successfully moved")

        @staticmethod
        def tableview_columnnames(mainwindow, data_type: str) -> None:
            if data_type == "exts":
                mainwindow.tableview_itemmodel.setHorizontalHeaderLabels(["", "Extensions", "Quantity"])
            elif data_type == "dates":
                mainwindow.tableview_itemmodel.setHorizontalHeaderLabels(["Year", "Months"])

    class Russian:
        @staticmethod
        def mainwindow(mainwindow) -> None:
            mainwindow.groupbox_tableview.setTitle("Доступные данные")
            mainwindow.groupbox_toolbox.setTitle("Инструменты")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_rename), "Переименование")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_move), "Перемещение")
            mainwindow.toolbox.setItemText(mainwindow.toolbox.indexOf(mainwindow.page_duplicates), "Дубликаты")
            mainwindow.lineedit_page_rename_exts.setPlaceholderText("Выберите расширения файлов")
            mainwindow.radiobtn_page_rename_date.setText("По дате создания\n(только изображения)")
            mainwindow.checkbox_page_rename_exif.setText("Применить exif\n(если есть)")
            mainwindow.pushbtn_page_rename_show.setText("Даты")
            mainwindow.radiobtn_page_rename_template.setText("По шаблону имени")
            mainwindow.lineedit_page_rename_template.setPlaceholderText("Введите шаблон имени")
            mainwindow.lineedit_page_move_exts.setPlaceholderText("Выберите расширения файлов")
            mainwindow.radiobtn_page_move_date.setText("По дате создания\n(только изображения)")
            mainwindow.checkbox_page_move_exif.setText("Применить exif\n(если есть)")
            mainwindow.pushbtn_page_move_show.setText("Даты")
            mainwindow.radiobtn_page_move_exts.setText("По расширению файлов")
            mainwindow.lineedit_page_move_newdir.setPlaceholderText("Выберите новую директорию")
            mainwindow.pushbtn_page_move_newdir.setText("Открыть")
            mainwindow.lineedit_page_duplicates_exts.setPlaceholderText("Выберите расширения файлов")
            mainwindow.checkbox_page_duplicates_move.setText("Переместить\n(все дубликаты)")
            mainwindow.pushbtn_page_duplicates_show.setText("Дубликаты")
            mainwindow.lineedit_page_duplicates_newdir.setPlaceholderText("Выберите новую директорию")
            mainwindow.pushbtn_page_duplicates_newdir.setText("Открыть")
            mainwindow.groupbox_workdir.setTitle("Рабочая директория и доступные расширения файлов")
            mainwindow.lineedit_workdir.setPlaceholderText("Выберите рабочую директорию")
            mainwindow.pushbtn_workdir.setText("Открыть")
            mainwindow.pushbtn_show_exts.setText("Расширения")
            mainwindow.cmdlinkbtn_exec.setText("Выполнить")
            mainwindow.menu_language.setTitle("Перевод")
            mainwindow.menu_theme.setTitle("Темы")

        @staticmethod
        def warning_message(msgbox, warning_type: tuple) -> None:
            msgbox.setWindowTitle("Предупреждение")
            if warning_type[0] == "nothing found":
                msgbox.setText("В рабочей директории ничего не найдено")
            elif warning_type[0] == "nothing selected":
                msgbox.setText("Инструменты не выбраны")
            elif warning_type[0] == "workdir not selected":
                msgbox.setText("Рабочая директория не выбрана")
            elif warning_type[0] == "exts not selected":
                msgbox.setText("Расширения файлов не выбраны")
            elif warning_type[0] == "img exts not selected":
                msgbox.setText("Расширения изображений не выбраны")
                msgbox.setInformativeText(f"Доступные расширения изображений:\n{", ".join(warning_type[1])}")
            elif warning_type[0] == "template not selected":
                msgbox.setText("Шаблон для переименования не выбран")
            elif warning_type[0] == "template long":
                msgbox.setText("Шаблон + расширения файлов > 256")
            elif warning_type[0] == "newdir not selected":
                msgbox.setText("Новая директория не выбрана")

        @staticmethod
        def info_message(msgbox, info_type: tuple) -> None:
            msgbox.setWindowTitle("Information")
            if info_type[0] == "renamed images":
                msgbox.setText(f"{info_type[1]} изображения успешно переименованы")
            elif info_type[0] == "renamed files":
                msgbox.setText(f"{info_type[1]} файла успешно переименованы")
            elif info_type[0] == "moved images":
                msgbox.setText(f"{info_type[1]} изображения успешно перемещены")
            elif info_type[0] == "moved files":
                msgbox.setText(f"{info_type[1]} файлы успешно перемещены")
            elif info_type[0] == "duplicates moved":
                msgbox.setText(f"{info_type[1]} дубликатов успешно перемещены")

        @staticmethod
        def tableview_columnnames(mainwindow, data_type: str) -> None:
            if data_type == "exts":
                mainwindow.tableview_itemmodel.setHorizontalHeaderLabels(["", "Расширения", "Количество"])
            elif data_type == "dates":
                mainwindow.tableview_itemmodel.setHorizontalHeaderLabels(["Годы", "Месяцы"])


class Translator:
    translator = {
        "English": {
            "mainwindow": Translation.English.mainwindow,
            "warning_message": Translation.English.warning_message,
            "info_message": Translation.English.info_message,
            "tableview_columnnames": Translation.English.tableview_columnnames,
        },
        "Russian": {
            "mainwindow": Translation.Russian.mainwindow,
            "warning_message": Translation.Russian.warning_message,
            "info_message": Translation.Russian.info_message,
            "tableview_columnnames": Translation.Russian.tableview_columnnames,
        },
    }
