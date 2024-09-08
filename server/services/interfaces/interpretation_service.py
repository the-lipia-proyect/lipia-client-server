from abc import ABC, abstractmethod
from typing import Optional

from dtos.get_interpretations_user_history_response_dto import (
    GetInterpretationsUserHistoryResponseDto,
)
from dtos.generate_user_interpretation_request_dto import (
    GenerateUserInterpretationRequestDto,
)
from dtos.generate_user_interpretation_response_dto import (
    GenerateUserInterpretationResponseDto,
)
from dtos.update_interpretation_note_request_dto import (
    UpdateInterpretationNoteRequestDto,
)


class IInterpretationService(ABC):
    @abstractmethod
    def get_user_history(
        self,
        user_id: str,
        order_by: str,
        descending_order: str,
        page: int,
        page_size: Optional[int] = None,
        from_date: Optional[int] = None,
    ) -> GetInterpretationsUserHistoryResponseDto:
        pass

    @abstractmethod
    def insert_user_interpretation(
        self, user_id: str, req: GenerateUserInterpretationRequestDto
    ) -> GenerateUserInterpretationResponseDto:
        pass

    @abstractmethod
    def update_interpretation_note(
        self, id: str, req: UpdateInterpretationNoteRequestDto
    ) -> None:
        pass
