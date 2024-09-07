import boto3
import os
from typing import Optional, Any

from .interfaces.s3_service import IS3Service


class S3Service(IS3Service):
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
                payload, self.bucket_name, file_name, ExtraArgs={"ACL": "public-read"}
            )
            return s3_response
        except Exception as e:
            print("EXCEPTION:", e)
            raise

    def generate_presigned_url(
        self,
        client_method: str,
        file_name: str,
        expires_in: int = 3600,
        params: Optional[Any] = None,
    ) -> str:
        final_params = {"Bucket": self.bucket_name, "Key": file_name}
        if params:
            final_params = {**final_params, **params}
        signed_url = self.s3_client.generate_presigned_url(
            client_method,
            Params=final_params,
            ExpiresIn=expires_in,
        )
        return signed_url

    def move_file(self, source_key: str, destination_key: str) -> None:
        """
        Moves a file from source_key to destination_key within the same bucket.

        Args:
            source_key (str): The key of the source file.
            destination_key (str): The key of the destination file.

        Raises:
            Exception: If an error occurs during the move operation.
        """
        try:
            # Copy the file to the new location
            self.s3_client.copy_object(
                Bucket=self.bucket_name,
                CopySource={"Bucket": self.bucket_name, "Key": source_key},
                Key=destination_key,
                ACL="public-read",  # Optional: Set ACL if needed
            )
            # Delete the file from the source location
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=source_key)
        except Exception as e:
            print("Error in s3_service.move_file:", e)
            raise

    def delete_file(self, file_name: str) -> None:
        """
        Deletes a file from the specified S3 bucket.

        Args:
            file_name (str): The key (name) of the file to delete.

        Raises:
            Exception: If an error occurs during the delete operation.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)
            print(
                f"File {file_name} successfully deleted from bucket {self.bucket_name}."
            )
        except Exception as e:
            print(f"Error in s3_service.delete_file: {e}")
            raise
