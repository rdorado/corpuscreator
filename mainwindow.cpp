#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "about.h"
#include "finddialog.h"

#include <QFileDialog>
#include <QTextStream>
#include <QMessageBox>

#include <iostream>
using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    updateWindow(document);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_actionExit_triggered()
{
   //QApplication::quit();
   qApp->quit();
}


void MainWindow::updateWindow(Document d){
  this->setWindowTitle( QString::fromStdString( d.getFilename() ) );
}

void MainWindow::on_actionSave_as_triggered()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"), QString::fromStdString( document.getFilename() ), tr("")); //"Text Files (*.txt);;C++ Files (*.cpp *.h)")

    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (!file.open(QIODevice::WriteOnly)){
            QMessageBox::critical(this, tr("Error"), tr("Could not save file"));
            return;
        }
        else{
            QTextStream out(&file);
            out << ui->textEdit->toPlainText(); //  QString text = ;
            out.flush();
            file.close();
        }
    }

}

void MainWindow::on_actionOpen_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"), QString(), tr(""));  //tr("Text Files (*.txt);;C++ Files (*.cpp *.h)")
    if (!fileName.isEmpty()) {
         QFile file(fileName);
         if (!file.open(QIODevice::ReadOnly)) {
              QMessageBox::critical(this, tr("Error"), tr("Could not open file"));
              return;
         }
         QTextStream in(&file);
         ui->textEdit->setText(in.readAll());
         file.close();
    }


}

void MainWindow::on_actionAbout_triggered()
{
     About *about = new About(this);
     about->setWindowModality(Qt::WindowModal);
     about->show();
}

void MainWindow::on_actionFind_triggered()
{
    FindDialog *find = new FindDialog(this);
    find->setDocument(ui->textEdit->document());
    find->setWindowModality(Qt::ApplicationModal);
    find->show();

}
