@echo off

rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
pyinstaller --clean run_yl_sticky_note.spec