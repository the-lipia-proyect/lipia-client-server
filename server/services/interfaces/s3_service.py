from abc import ABC, abstractmethod


class IS3Service(ABC):
    @abstractmethod
    def upload_file(self, file_name: str, payload):
        pass

    @abstractmethod
    def generate_presigned_url(
        self, client_method: str, file_name: str, expires_in: int
    ) -> str:
        pass
