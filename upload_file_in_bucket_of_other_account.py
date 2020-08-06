import json
import boto3
from botocore.exceptions import ClientError

"""
Permit that your lambda upload a file into a bucket's out of your account. 
--
Permite que sua lambda possa fazer o upload de um determinado arquivo para um Bucket de uma conta terceira(eles devem autorizar vc fazer isso).
Alem disso, voce pode permitir que a conta hospedeira tenha permissao de leitura, etc nos arquivos carregados.

kklockk@gmail.com

"""


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def lambda_handler(event, context):
    
    # lista objetos
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('other_account_bucket_name')
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object)
    

    # faz upload
    s3 = boto3.client('s3')
    bucket_name = "other_account_bucket_name"
    file_name = "uploaded_file.txt"
    
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, bucket_name, file_name)
        
        
        # Libera o acesso para a conta hospedeira, caso deseje permitir o acesso dela.
        # IdCanonico da minha conta:
        my_cannonical_id = "3f1432a3c779b8c32dd88883ccc33344444433333bbbbb888f469b8c5679e03f"
        
        # IdCanonico da conta externo onde estou hospendando meu arquivo:
        targer_cannonical_id = "f93d2cda907f4499eeee99ssbbb3333333399999999ccxx9999992a8339afe96"
        
        response = s3.put_object_acl(
            Key=file_name,
            Bucket=bucket_name,
            AccessControlPolicy={
                'Grants': [
                    {
                        'Grantee': {
                            'DisplayName': 'permite outra conta ter acesso ao arquivo que estou hospedando lah',
                            'ID': targer_cannonical_id,
                            'Type': 'CanonicalUser'
                        },
                        'Permission': 'FULL_CONTROL'
                    }
                ],
                'Owner': {
                    'DisplayName': 'string',
                    'ID': my_cannonical_id
                }
            }

        )
    
        
        
    
    return { 'upload_retorno': response  }
