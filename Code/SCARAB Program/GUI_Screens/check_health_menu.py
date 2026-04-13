# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_health_menu.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_check_health_menu(object):
    def setupUi(self, check_health_menu):
        if not check_health_menu.objectName():
            check_health_menu.setObjectName(u"check_health_menu")
        check_health_menu.resize(650, 600)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(48, 34, 93, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(72, 51, 139, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        brush3 = QBrush(QColor(60, 42, 116, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush3)
        brush4 = QBrush(QColor(24, 17, 46, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush4)
        brush5 = QBrush(QColor(32, 23, 62, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush4)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush6)
        brush8 = QBrush(QColor(255, 255, 255, 127))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush8)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush6)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush6)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush8)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush6)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush6)
        brush9 = QBrush(QColor(24, 17, 46, 127))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush9)
#endif
        brush10 = QBrush(QColor(34, 24, 65, 255))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush10)
#endif
        check_health_menu.setPalette(palette)
        check_health_menu.setAutoFillBackground(True)
        self.det_game_label = QLabel(check_health_menu)
        self.det_game_label.setObjectName(u"det_game_label")
        self.det_game_label.setGeometry(QRect(230, 20, 201, 41))
        font = QFont()
        font.setPointSize(20)
        self.det_game_label.setFont(font)
        self.check_health_button = QPushButton(check_health_menu)
        self.check_health_button.setObjectName(u"check_health_button")
        self.check_health_button.setGeometry(QRect(60, 470, 261, 71))
        self.check_health_button.setFont(font)
        self.custom_scan_button = QPushButton(check_health_menu)
        self.custom_scan_button.setObjectName(u"custom_scan_button")
        self.custom_scan_button.setGeometry(QRect(340, 470, 251, 71))
        self.custom_scan_button.setFont(font)
        self.formLayoutWidget = QWidget(check_health_menu)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(60, 293, 531, 171))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.name_label = QLabel(self.formLayoutWidget)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.rom_sz_label = QLabel(self.formLayoutWidget)
        self.rom_sz_label.setObjectName(u"rom_sz_label")
        self.rom_sz_label.setFont(font)
        self.rom_sz_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.rom_sz_label)

        self.chip_label = QLabel(self.formLayoutWidget)
        self.chip_label.setObjectName(u"chip_label")
        self.chip_label.setFont(font)
        self.chip_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.chip_label)

        self.hdr_chk_label = QLabel(self.formLayoutWidget)
        self.hdr_chk_label.setObjectName(u"hdr_chk_label")
        self.hdr_chk_label.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.hdr_chk_label)

        self.name = QLabel(self.formLayoutWidget)
        self.name.setObjectName(u"name")
        self.name.setFont(font)
        self.name.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name)

        self.rom_size = QLabel(self.formLayoutWidget)
        self.rom_size.setObjectName(u"rom_size")
        self.rom_size.setFont(font)
        self.rom_size.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rom_size)

        self.chipset = QLabel(self.formLayoutWidget)
        self.chipset.setObjectName(u"chipset")
        self.chipset.setFont(font)
        self.chipset.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chipset)

        self.checksum = QLabel(self.formLayoutWidget)
        self.checksum.setObjectName(u"checksum")
        self.checksum.setFont(font)
        self.checksum.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.checksum)

        self.cart_image = QLabel(check_health_menu)
        self.cart_image.setObjectName(u"cart_image")
        self.cart_image.setGeometry(QRect(190, 70, 266, 200))

        self.retranslateUi(check_health_menu)

        QMetaObject.connectSlotsByName(check_health_menu)
    # setupUi

    def retranslateUi(self, check_health_menu):
        check_health_menu.setWindowTitle(QCoreApplication.translate("check_health_menu", u"Frame", None))
        self.det_game_label.setText(QCoreApplication.translate("check_health_menu", u"Detected Game:", None))
        self.check_health_button.setText(QCoreApplication.translate("check_health_menu", u"Check Health", None))
        self.custom_scan_button.setText(QCoreApplication.translate("check_health_menu", u"Custom Scan", None))
        self.name_label.setText(QCoreApplication.translate("check_health_menu", u"Name:", None))
        self.rom_sz_label.setText(QCoreApplication.translate("check_health_menu", u"ROM Size:", None))
        self.chip_label.setText(QCoreApplication.translate("check_health_menu", u"Chipset:", None))
        self.hdr_chk_label.setText(QCoreApplication.translate("check_health_menu", u"Header Checksum:", None))
        self.name.setText("")
        self.rom_size.setText("")
        self.chipset.setText("")
        self.checksum.setText("")
        self.cart_image.setText("")
    # retranslateUi

