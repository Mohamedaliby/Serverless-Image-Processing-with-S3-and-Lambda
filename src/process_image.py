import boto3
import os
import json
from PIL import Image
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda function that processes images uploaded to a source S3 bucket.
    The function resizes the image and uploads it to a destination bucket.
    
    Parameters:
    event (dict): The event dict containing the S3 event details
    context (object): Lambda context object
    
    Returns:
    dict: Response containing status and processing details
    """
    # Get the source bucket and key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Get the destination bucket from environment variables
    destination_bucket = os.environ['DESTINATION_BUCKET']
    
    try:
        # Download the image from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        image_content = response['Body'].read()
        
        # Process the image (resize)
        with Image.open(io.BytesIO(image_content)) as image:
            # Resize to 50% of original size
            width, height = image.size
            resized_image = image.resize((int(width * 0.5), int(height * 0.5)))
            
            # Save the processed image to a buffer
            buffer = io.BytesIO()
            resized_image.save(buffer, format=image.format)
            buffer.seek(0)
            
            # Upload the processed image to the destination bucket
            s3_client.put_object(
                Bucket=destination_bucket,
                Key=f"resized-{source_key}",
                Body=buffer,
                ContentType=response['ContentType']
            )
        
        print(f"Successfully processed image {source_key} from {source_bucket} to {destination_bucket}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image processed successfully',
                'source_bucket': source_bucket,
                'source_key': source_key,
                'destination_bucket': destination_bucket,
                'destination_key': f"resized-{source_key}"
            })
        }
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f"Error processing image: {str(e)}"
            })
        }