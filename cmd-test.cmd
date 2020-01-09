@ECHO OFF
IF EXIST vhdfile-10mb.vhd CALL cmd-unmount.cmd
IF EXIST vhdfile-10mb.vhd DEL vhdfile-10mb.vhd

CALL cmd-extract-vhd.cmd
CALL cmd-mount.cmd
IF     EXIST  mount-point\EKHwkKYU0AAQ7Bv.jpg CALL :PASS
IF NOT EXIST  mount-point\EKHwkKYU0AAQ7Bv.jpg CALL :FAIL
CALL cmd-unmount.cmd
GOTO :END

:PASS
ECHO.
ECHO.
ECHO " _____         _____ _____ "
ECHO "|  __ \ /\    / ____/ ____|"
ECHO "| |__) /  \  | (___| (___  "
ECHO "|  ___/ /\ \  \___ \\___ \ "
ECHO "| |  / ____ \ ____) |___) |"
ECHO "|_| /_/    \_\_____/_____/ "
ECHO.
ECHO.
GOTO :EOF                        "


:FAIL
ECHO.
ECHO.
ECHO " ______      _____ _       "
ECHO "|  ____/\   |_   _| |      "
ECHO "| |__ /  \    | | | |      "
ECHO "|  __/ /\ \   | | | |      "
ECHO "| | / ____ \ _| |_| |____  "
ECHO "|_|/_/    \_\_____|______| "
ECHO.
ECHO.
GOTO :EOF

@ECHO ON
:END

