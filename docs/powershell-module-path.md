# PowerShell module installation path fix (OneDrive/Documentos)

`Install-Module` writes user-scoped packages to the current user's
`Documents\WindowsPowerShell\Modules` folder. When OneDrive is configured or the
Documents folder is localized (for example, `Documentos`), the install can
fail with a message similar to:

```
Could not find a part of the path 'C:\Users\<user>\OneDrive\Documentos\WindowsPowerShell\Modules\ps2exe\1.0.17'
```

Create the module directory in your actual Documents path and prepend it to
`$env:PSModulePath` before installing:

```powershell
# Resolve the real Documents path even when localized or redirected to OneDrive
$docs = [Environment]::GetFolderPath('MyDocuments')
$moduleRoot = Join-Path $docs 'WindowsPowerShell\Modules'

# Ensure the module directory exists
New-Item -ItemType Directory -Force -Path $moduleRoot | Out-Null

# Make sure PowerShell can write to it for this session
$env:PSModulePath = "$moduleRoot;" + $env:PSModulePath

# Retry the installation
Install-Module -Name ps2exe -Scope CurrentUser -Force
```

If you prefer a different location (for example, `C:\PowerShellModules`), use
that path for `$moduleRoot` instead and keep it in `$env:PSModulePath` so
PowerShell can find installed modules in future sessions.
