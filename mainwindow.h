#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QModelIndex>
#include "document.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    Document document;
    QStringList *stringList;
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_actionExit_triggered();

    void on_actionSave_as_triggered();

    void on_actionOpen_triggered();

    void on_actionAbout_triggered();

    void on_actionFind_triggered();

    void on_listView_clicked(const QModelIndex &index);

private:
    Ui::MainWindow *ui;
    void updateWindow(Document d);
};

#endif // MAINWINDOW_H
