[Setup]
AppName=SCARAB
AppVersion=1.0
DefaultDirName={autopf}\SCARAB
DefaultGroupName=SCARAB
OutputDir=installer
OutputBaseFilename=SCARAB_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\SCARAB\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SCARAB"; Filename: "{app}\SCARAB.exe"
Name: "{commondesktop}\SCARAB"; Filename: "{app}\SCARAB.exe"

[Run]
Filename: "{app}\SCARAB.exe"; Description: "Launch SCARAB"; Flags: nowait postinstall skipifsilent