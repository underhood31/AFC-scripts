@ECHO OFF
ECHO Eye tracker starting
REM SET /P name="What Is Your Name? "
CD /D
START D:\ADHD-Protocol\eye-tracker\tobii\samples\cs\bin\Debug\cs_sample_streams.exe  %1

if %ERRORLEVEL% == 9059 (CD C:\Users\iiitd\source\repos\tobii\samples\cs
dotnet publish -c Debug -r win10-x64
START D:\ADHD-Protocol\eye-tracker\tobii\samples\cs\bin\Debug\cs_sample_streams.exe \win10-x64\cs_sample_streams.exe %name%
)