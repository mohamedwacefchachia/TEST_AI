from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services import extraction_service
from baml_client.types import (
    Theme,
    ClassificationOutput,
    FormOutput,
    ProbabilisticClassificationOutput,
)
from fastapi.responses import StreamingResponse


router = APIRouter()


## Request schemas
class ClassificationRequest(BaseModel):
    text: str
    themes: list[Theme]


class FormRequest(BaseModel):
    text: str


class GeneralizedFormRequest(BaseModel):
    text: str
    schema_description: dict


########################################################################
########################################################################


# Classification API
@router.post("/classify", response_model=ClassificationOutput)
async def classify_endpoint(request: ClassificationRequest):
    try:
        return await extraction_service.classify_text(request.text, request.themes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Complete form API
@router.post("/complete-form", response_model=FormOutput)
async def complete_form_endpoint(request: FormRequest):
    try:
        return await extraction_service.complete_form(request.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Bonus 1 API
@router.post(
    "/classify-probabilistic", response_model=ProbabilisticClassificationOutput
)
async def classify_probabilistic_endpoint(
    request: ClassificationRequest, nbr_iterations: int = 5
):
    try:
        return await extraction_service.classify_probabilistic(
            request.text, request.themes, nbr_iterations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Bonus 1 API / Approach 2
@router.post(
    "/classify-probabilistic-2", response_model=ProbabilisticClassificationOutput
)
async def classify_probabilistic_2_endpoint(request: ClassificationRequest):
    try:
        return await extraction_service.classify_probabilistic_2(
            request.text, request.themes
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Bonus 3 API
@router.post("/complete-form-stream")
async def stream_form_endpoint(request: FormRequest):
    return StreamingResponse(
        extraction_service.stream_complete_form(request.text),
        media_type="application/x-ndjson",
    )


## Bonus 2 API
@router.post("/extract-generalized")
async def extract_generalized_endpoint(request: GeneralizedFormRequest):
    return await extraction_service.extract_generalized(
        text=request.text, schema_description=request.schema_description
    )
