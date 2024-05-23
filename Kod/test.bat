@echo off
chcp 65001 > nul
for /l %%i in (281, 1, 327) do (
    echo Uruchamiam program dla iteracji %%i
    python .\main.py winner old %%i >> winners_test.txt
)