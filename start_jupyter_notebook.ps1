param($Work)

if (!$Work) {
    powershell -noexit -file $MyInvocation.MyCommand.Path 1
    return
}

$rootFile = $PSScriptRoot
cd $rootFile
cd ..\scripts
./activate
cd $rootFile
jupyter notebook