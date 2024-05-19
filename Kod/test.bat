@echo off
chcp 65001 > nul
for /l %%i in (281, 1, 324) do (
    echo Uruchamiam program dla iteracji %%i
    python .\main.py goals_total old %%i >> goals_test.txt
)