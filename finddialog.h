#ifndef FINDDIALOG_H
#define FINDDIALOG_H

#include <QDialog>
#include <QTextDocument>

namespace Ui {
class FindDialog;
}

class FindDialog : public QDialog
{
    Q_OBJECT
    QTextDocument *document;

public:
    explicit FindDialog(QWidget *parent = 0);
    ~FindDialog();

    void setDocument(QTextDocument *document);

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::FindDialog *ui;
};

#endif // FINDDIALOG_H
