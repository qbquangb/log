color 0A
:: -----------------------------------------------------------------------------------
if exist "D:\Duan\1log\log_run.txt" (
    echo chay 2 file a.pyw va b.pyw
    start "" "D:\Duan\1log\a.pyw"
    start "" "D:\Duan\1log\b.pyw"
) else (
    echo khong tim thay file log_run.txt, khong chay a.pyw va b.pyw
)
:: -----------------------------------------------------------------------------------
if exist "D:\Duan\1log\protect_run.txt" (
    cd /d D:\Duan\2s_home
    cls
    start /wait "" "C:\Users\Hii\AppData\Local\Programs\Python\Python310\pythonw.exe" "D:\Duan\2s_home\check_mail.pyw"
    cls
    if not exist "D:\Duan\2s_home\response.pyw" (
        echo File response.pyw khong ton tai, dang copy file backup...
        copy "D:\Duan\2s_home\backup\response.pyw" "D:\Duan\2s_home\response.pyw"
    ) else (
        echo File response.pyw da ton tai.
    )
    start "" "D:\Duan\2s_home\response.pyw"
    if not exist "D:\Duan\2s_home\main2.pyw" (
        echo File main2.pyw khong ton tai, dang copy file backup...
        copy "D:\Duan\2s_home\backup\main2.pyw" "D:\Duan\2s_home\main2.pyw"
    ) else (
        echo File main2.pyw da ton tai.
    )
    start "" cmd /c "cd /d D:\Duan\2s_home && pythonw main2.pyw > output2.log 2> error2.log"
    if not exist "D:\Duan\2s_home\main1.pyw" (
        echo File main1.pyw khong ton tai, dang copy file backup...
        copy "D:\Duan\2s_home\backup\main1.pyw" "D:\Duan\2s_home\main1.pyw"
    ) else (
        echo File main1.pyw da ton tai.
    )
    cls
    start "" cmd /c "cd /d D:\Duan\2s_home && pythonw main1.pyw > output1.log 2> error1.log"
    if exist "D:\Duan\2s_home\prog_add.pyw" (
        start "" "D:\Duan\2s_home\prog_add.pyw"
    ) else (
        echo Không tim thay file prog_add.pyw, không chạy.
    )
    cls
) else (
    echo khong tim thay file protect_run.txt, khong chay check_mail.pyw, response.pyw, main2.pyw, main1.pyw và prog_add.pyw.
)
:: -----------------------------------------------------------------------------------
if exist "D:\Duan\1log\assistant_run.txt" (
    echo chay file my_assistant.pyw.
    cd /d D:\Duan\17assistant
    start "" "D:\Duan\17assistant\my_assistant.pyw"
) else (
    echo khong tim thay file assistant_run.txt, khong chay my_assistant.pyw.
)
cls
:: -----------------------------------------------------------------------------------