from typing import Optional

from flask_injector import inject

from utils.responses_helper import ok, not_found
from repositories.interpretation_repository import InterpretationRepository
from .interfaces.cognito_service import ICognitoService
from .interfaces.interpretation_service import IInterpretationService
from dtos.generate_user_interpretation_request_dto import (
    GenerateUserInterpretationRequestDto,
)
from dtos.generate_user_interpretation_response_dto import (
    GenerateUserInterpretationResponseDto,
)
from dtos.get_interpretations_user_history_response_dto import (
    GetInterpretationsUserHistoryResponseDto,
    InterpretationDto,
)
from dtos.update_interpretation_note_request_dto import (
    UpdateInterpretationNoteRequestDto,
)
from dtos.get_interpretation_by_id_response import GetInterpretationByIdResponseDto
from database.collection_models.interpretation_model import Interpretation, WordDto


class InterpretationService(IInterpretationService):
    @inject
    def __init__(
        self,
        cognito_service: ICognitoService,
        interpretation_repository: InterpretationRepository,
    ):
        self._cognito_service = cognito_service
        self._interpretation_repository = interpretation_repository

    def get_user_history(
        self,
        user_id: str,
        order_by: str,
        descending_order: str,
        page: int,
        page_size: Optional[int] = None,
        from_date: Optional[int] = None,
    ) -> GetInterpretationsUserHistoryResponseDto:
        get_interpreatations_response_list = (
            self._interpretation_repository.get_by_user_id(
                user_id, order_by, descending_order, page, page_size, from_date
            )
        )
        user_interpretations = [
            InterpretationDto(
                id=str(data.get("_id")),
                word=data.get("word"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                phrase_group=data.get("phrase_group"),
            )
            for data in get_interpreatations_response_list
        ]
        response = GetInterpretationsUserHistoryResponseDto(
            interpretations=user_interpretations
        )
        return ok(response)

    def insert_user_interpretation(
        self, user_id: str, req: GenerateUserInterpretationRequestDto
    ) -> GenerateUserInterpretationResponseDto:
        word_dict = (
            req.word.model_dump() if hasattr(req.word, "model_dump") else req.word
        )
        interpretation = Interpretation(
            word=word_dict, user_id=user_id, phrase_group=req.phrase_group
        )
        db_id_result = self._interpretation_repository.insert(interpretation)
        response = GenerateUserInterpretationResponseDto(id=db_id_result)
        return ok(response)

    def update_interpretation_note(
        self, id: str, req: UpdateInterpretationNoteRequestDto
    ) -> None:
        existing_interpretation = self._interpretation_repository.get_by_id(id)
        if not existing_interpretation:
            return not_found({"message": "The interpretation does not exist"})
        word = existing_interpretation.get("word")
        updated_interpretation = Interpretation(
            word=word,
            user_id=existing_interpretation.get("user_id"),
            note=req.note,
            phrase_group=existing_interpretation.get("phrase_group"),
        )
        self._interpretation_repository.update(id, updated_interpretation)
        return ok({})

    def get_interpretation_by_id(self, id: str) -> GetInterpretationByIdResponseDto:
        existing_interpretation = self._interpretation_repository.get_by_id(id)
        if not existing_interpretation:
            return not_found({"message": "The shortcut does not exist"})
        response = GetInterpretationByIdResponseDto(
            id=str(existing_interpretation.get("_id")),
            created_at=existing_interpretation.get("created_at"),
            updated_at=existing_interpretation.get("updated_at"),
            note=existing_interpretation.get("note"),
        )
        return ok(response)
