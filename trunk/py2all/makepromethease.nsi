!define py2exeOutputDir 'dist'
!define exe             'demo.exe'
!define compressor      'lzma'  ;one of 'zlib', 'bzip2', 'lzma'

;comment in and customize, if you have an icon
;!define icon            'icon1.ico'


; if you only want to allowing one instance to run at a time, remove the ; from the next line
;!define onlyOneInstance




; - - - - do not edit below this line, normally - - - -
!ifdef compressor
    SetCompressor ${compressor}
!else
    SetCompress Off
!endif
Name ${exe}
OutFile ${exe}
SilentInstall silent
!ifdef icon
    Icon ${icon}
!endif


; - - - - Allow only one installer instance - - - - 
!ifdef onlyOneInstance
Function .onInit
 System::Call "kernel32::CreateMutexA(i 0, i 0, t '$(^Name)') i .r0 ?e"
 Pop $0
 StrCmp $0 0 launch
  Abort
 launch:
FunctionEnd
!endif
; - - - - Allow only one installer instance - - - - 


Section
    InitPluginsDir
    SetOutPath '$PLUGINSDIR'
    File /r '${py2exeOutputDir}\*.*'
    SetOutPath '$EXEDIR'        ; uncomment this line to start the exe in the PLUGINSDIR
    nsExec::Exec '$PLUGINSDIR\${exe}'   
SectionEnd



