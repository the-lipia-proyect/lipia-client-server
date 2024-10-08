clear

.venv\Scripts\Activate

$zipPath = "lipia-backend.zip"
$itemsToZip = @("controllers", "database", "dtos", "repositories", "services", "utils", "app.py")
if (Test-Path $zipPath) {
    Remove-Item $zipPath
}

Compress-Archive -Path $itemsToZip -DestinationPath $zipPath

aws lambda update-function-code `
  --region us-east-1 `
  --function-name lipia-backend `
  --zip-file fileb://$zipPath `
  --profile default