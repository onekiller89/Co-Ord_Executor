@echo off
REM Start the existing MegaMind systemd user service in Ubuntu WSL.
REM For Task Scheduler, launch this batch file at logon.
REM The trailing # absorbs Windows line endings in the WSL shell.
echo systemctl --user start megamind.service # | wsl.exe -d Ubuntu -u aaa
