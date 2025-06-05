import boto3

def send_ses_email(to_email, subject, body):
    ses_client = boto3.client('ses', region_name='us-east-1')  # Europe region
    

    response = ses_client.send_email(
        Source='ahtidev@gmail.com',  # Must be verified in SES
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body}
            }
        }
    )
    return response
