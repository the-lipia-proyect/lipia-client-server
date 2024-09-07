from abc import ABC, abstractmethod
from typing import Optional, Any


class IS3Service(ABC):
    @abstractmethod
    def upload_file(self, file_name: str, payload):
        pass

    @abstractmethod
    def generate_presigned_url(
        self, client_method: str, file_name: str, expires_in: int, params: Optional[Any]
    ) -> str:
        pass

    @abstractmethod
    def move_file(
        self,
        source_key: str,
        destination_key: str,
    ) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> str:
        pass
