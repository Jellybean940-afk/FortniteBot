def Colored(string,Color):
    return (f'%Windir%\\System32\\WindowsPowerShell\\v1.0\Powershell.exe write-host -foregroundcolor {Color} "{string}"')