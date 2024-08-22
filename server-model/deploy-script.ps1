clear

.venv\Scripts\Activate

$LOCATION = split-path -parent $MyInvocation.MyCommand.Definition
$DOCKERFILE = Join-Path -Path $LOCATION -ChildPath "Dockerfile"

docker build -f $DOCKERFILE `
  -t lipiaclientserver:latest $LOCATION

aws ecr get-login-password --region us-east-1 --profile default | docker login --username AWS --password-stdin 416711641372.dkr.ecr.us-east-1.amazonaws.com/anr-ia-backend-dev

docker tag $(docker images lipiaclientserver:latest --format "{{.ID}}") 416711641372.dkr.ecr.us-east-1.amazonaws.com/lipia:latest

docker push 416711641372.dkr.ecr.us-east-1.amazonaws.com/lipia:latest

aws lambda update-function-code `
  --region us-east-1 `
  --function-name lipia `
  --image-uri 416711641372.dkr.ecr.us-east-1.amazonaws.com/lipia:latest `
  --profile default


