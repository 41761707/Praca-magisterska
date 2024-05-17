@echo off
chcp 65001 > nul
for /l %%i in (11, 1, 327) do (
    echo Uruchamiam program dla iteracji %%i
    python .\main.py %%i >> goals_test.txt
)