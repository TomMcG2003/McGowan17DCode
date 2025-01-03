ECHO OFF
set /p "KEY_FLAG=Have you already set up your key (y/N)? "

if /i "%KEY_FLAG%"=="y" (
    wsl bash -c "sh ssh_startup.sh %USERNAME%"
) else if /i "%KEY_FLAG%"=="ye" (
    wsl bash -c "sh ssh_startup.sh %USERNAME%"
) else if /i "%KEY_FLAG%"=="yes" (
    wsl bash -c "sh ssh_startup.sh %USERNAME%"
) else (
    wsl bash -c "sh setup_key_for_ssh.sh %USERNAME%; sh ssh_startup.sh %USERNAME%"
)