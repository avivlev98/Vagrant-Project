#change to vagrant path
cd 'C:\Users\avivl\VagrantTest'
vagrant up
#Change to certs path
Import-Certificate -FilePath "C:\Users\avivl\Downloads\vagrantIM\Scripts\ca-cert\ca.crt" -CertStoreLocation 'Cert:\LocalMachine\Root' -Verbose
$file = "C:\Windows\System32\drivers\etc\hosts"
$hostfile = Get-Content $file
$hostfile += "172.23.198.32   assignment.local"
Set-Content -Path $file -Value $hostfile -Force
Start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" '--start-fullscreen "https://assignment.local/"'