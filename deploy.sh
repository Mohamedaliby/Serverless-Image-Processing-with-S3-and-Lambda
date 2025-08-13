#!/bin/bash

# Serverless Image Processing Deployment Script

# Set variables
STACK_NAME="image-processor"
TEMPLATE_FILE="template.yaml"
LAMBDA_CODE_DIR="src"
BUILD_DIR="build"

echo "Starting deployment of $STACK_NAME..."

# Create build directory
mkdir -p $BUILD_DIR

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t $BUILD_DIR

# Copy Lambda function code
echo "Copying Lambda function code..."
cp $LAMBDA_CODE_DIR/process_image.py $BUILD_DIR/

# Create deployment package
echo "Creating deployment package..."
cd $BUILD_DIR
zip -r ../lambda_package.zip .
cd ..

# Update the CloudFormation template to use the deployment package
echo "Updating CloudFormation template..."
sed -i 's/ZipFile: |/Code:\n        S3Bucket: !Ref DeploymentBucket\n        S3Key: lambda_package.zip/' $TEMPLATE_FILE

# Deploy the CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file $TEMPLATE_FILE \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM

# Clean up
echo "Cleaning up..."
rm -rf $BUILD_DIR

echo "Deployment completed successfully!"