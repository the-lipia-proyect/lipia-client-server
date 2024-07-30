if(Test-Path lambda_layer.zip){
    rm lambda_layer.zip
}

pip install --platform manylinux2014_march64 --target=./python/lib/python3.12/site-packages --implementation cp --only-binary=:all: --python-version 3.12 --upgrade -r requirements.txt pydantic-core


Compress-Archive python lambda_layer.zip