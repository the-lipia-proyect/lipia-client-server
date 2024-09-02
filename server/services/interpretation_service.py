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
        self, user_id: str, order_by: str, descending_order: str
    ) -> GetInterpretationsUserHistoryResponseDto:
        get_interpreatations_response_list = (
            self._interpretation_repository.get_by_user_id(
                user_id, order_by, descending_order
            )
        )
        user_interpretations = [
            InterpretationDto(
                id=str(data.get("_id")),
                # this line is temporary because word.data size is so bigger
                # words=data.get("words"),
                words=[
                    {"prediction": word.get("prediction"), "data": ""}
                    for word in data.get("words", [])
                ],
                note=data.get("note"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
            )
            for data in get_interpreatations_response_list
        ]
        response = GetInterpretationsUserHistoryResponseDto(
            interpretations=user_interpretations
        ).model_dump()
        return ok(response)

    def insert_user_interpretation(
        self, user_id: str, req: GenerateUserInterpretationRequestDto
    ) -> GenerateUserInterpretationResponseDto:
        words_list = [
            WordDto(prediction=word.prediction, data=word.data) for word in req.words
        ]
        interpretation = Interpretation(words=words_list, user_id=user_id)
        db_id_result = self._interpretation_repository.insert(interpretation)
        response = GenerateUserInterpretationResponseDto(id=db_id_result).model_dump()
        return ok(response)

    def update_interpretation_note(
        self, id: str, req: UpdateInterpretationNoteRequestDto
    ) -> None:
        existing_interpretation = self._interpretation_repository.get_by_id(id)
        if not existing_interpretation:
            return not_found({"message": "The shortcut does not exist"})
        words_list = [
            WordDto(prediction=word.get("prediction"), data=word.get("data"))
            for word in existing_interpretation.get("words")
        ]
        updated_interpretation = Interpretation(
            words=words_list,
            user_id=existing_interpretation.get("user_id"),
            note=req.note,
        )
        self._interpretation_repository.update(id, updated_interpretation)
        return ok({})
