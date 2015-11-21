#-------------------------------------------------
#
# Project created by QtCreator 2015-11-20T19:21:10
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = lincs-corpuscreator
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    about.cpp \
    finddialog.cpp

HEADERS  += mainwindow.h \
    about.h \
    document.h \
    finddialog.h

FORMS    += mainwindow.ui \
    about.ui \
    finddialog.ui

OTHER_FILES += \
    lincs-corpuscreator.pro.user
