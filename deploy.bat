@echo off
REM Serverless Image Processing Deployment Script for Windows

REM Set variables
SET STACK_NAME=image-processor
SET TEMPLATE_FILE=template.yaml
SET LAMBDA_CODE_DIR=src
SET BUILD_DIR=build

echo Starting deployment of %STACK_NAME%...

REM Create build directory
if not exist %BUILD_DIR% mkdir %BUILD_DIR%

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -t %BUILD_DIR%

REM Copy Lambda function code
echo Copying Lambda function code...
copy %LAMBDA_CODE_DIR%\process_image.py %BUILD_DIR%\

REM Create deployment package
echo Creating deployment package...
cd %BUILD_DIR%
powershell Compress-Archive -Path * -DestinationPath ..\lambda_package.zip -Force
cd ..

REM Deploy the CloudFormation stack
echo Deploying CloudFormation stack...
aws cloudformation deploy --template-file %TEMPLATE_FILE% --stack-name %STACK_NAME% --capabilities CAPABILITY_IAM

REM Clean up
echo Cleaning up...
rmdir /s /q %BUILD_DIR%

echo Deployment completed successfully!