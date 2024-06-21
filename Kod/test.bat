@echo off
chcp 65001 > nul
for /l %%i in (301, 1, 327) do (
    echo Uruchamiam program dla iteracji %%i
    python .\main.py btts old %%i >> btts_test.txt
)