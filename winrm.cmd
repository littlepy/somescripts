get-executionpolicy
set-executionpolicy remotesigned
winrm quickconfig
winrm enumerate winrm/config/listener
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm enumerate winrm/config/listener
