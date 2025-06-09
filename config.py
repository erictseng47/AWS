from decouple import Config, RepositoryEnv
import os

def load_config(env_path=None):
    try:
        if env_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            env_path = os.path.join(base_dir, '.env')

        config = Config(repository=RepositoryEnv(env_path))
        aws_access_key = config('AWS_ACCESS_KEY_ID')
        aws_secret_key = config('AWS_SECRET_ACCESS_KEY')
        region = config('REGION')
        ami_id = config('AMI_ID')
        queue_name = config('queue_name')
        file_path = config('file_path')
        object_name = config('object_name')
        return {
            'AWS_ACCESS_KEY_ID': aws_access_key,
            'AWS_SECRET_ACCESS_KEY': aws_secret_key,
            'REGION': region,
            'AMI_ID': ami_id,
            'queue_name': queue_name,
            'file_path': file_path,
            'object_name': object_name
        }
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        raise
