import boto3
import os


class S3Utils:
    def __init__(
        self, bucket_name: str, region_name=os.getenv("AWS_REGION", "us-east-1")
    ):
        """
        Initialize the S3 client.

        Args:
            region_name (str, optional): The AWS region name (e.g., "us-east-1"). If not specified, it will use the default region from the environment.
        """
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.bucket_name = bucket_name

    def upload_file(self, file_name: str, payload):
        """
        Uploads a file to the specified S3 bucket.

        Args:
            file_name (str): The desired filename for the uploaded object (without path).
            payload (file-like object): A readable file-like object containing the data to upload.

        Returns:
            str: The ETag (unique identifier) of the uploaded object, or an empty string if there's an error.

        Raises:
            Exception: If an error occurs during upload.
        """

        try:
            s3_response = self.s3_client.upload_fileobj(
                payload, self.bucket_name, file_name
            )
            return s3_response
        except Exception as e:
            print("EXCEPTION:", e)
            raise

    def generate_presigned_url(
        self, client_method: str, file_name: str, expires_in: int = 3600
    ) -> str:
        signed_url = self.s3_client.generate_presigned_url(
            client_method,
            Params={"Bucket": self.bucket_name, "Key": file_name},
            ExpiresIn=expires_in,
        )
        return signed_url
