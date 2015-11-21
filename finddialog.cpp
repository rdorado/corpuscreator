#include "finddialog.h"
#include "ui_finddialog.h"

#include <QMessageBox>

FindDialog::FindDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::FindDialog)
{
    ui->setupUi(this);
}

FindDialog::~FindDialog()
{
    delete ui;
}



void FindDialog::on_pushButton_clicked()
{
    QString searchString = ui->lineEdit->text();
    if(searchString.isEmpty()) return;

    QTextCursor highlightCursor(document);
    QTextCursor cursor(document);

    cursor.beginEditBlock();

    QTextCharFormat plainFormat(highlightCursor.charFormat());
    QTextCharFormat colorFormat = plainFormat;
    colorFormat.setForeground(Qt::red);

    colorFormat.setUnderlineColor(QColor(20,20,20));
    colorFormat.setUnderlineStyle(QTextCharFormat::WaveUnderline);

    colorFormat.setBackground(QBrush(QColor(255,255,0)));

    while (!highlightCursor.isNull() && !highlightCursor.atEnd()) {
        highlightCursor = document->find(searchString, highlightCursor, QTextDocument::FindWholeWords);
        if (!highlightCursor.isNull()) {
            highlightCursor.movePosition(QTextCursor::WordRight, QTextCursor::KeepAnchor);
            highlightCursor.mergeCharFormat(colorFormat);
        }
    }

    cursor.endEditBlock();

    QDialog::accept();
}

void FindDialog::on_pushButton_2_clicked()
{
       QDialog::reject();
}

void FindDialog::setDocument(QTextDocument *document){
    this->document=document;
}
