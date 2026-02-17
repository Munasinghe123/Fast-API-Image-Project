from fastapi import APIRouter, UploadFile, File, Form,Query
from typing import List

from controllers.survey.check_existing_lines import check_existing_lines 
from controllers.survey.check_existing_poles import check_existing_poles
from controllers.survey.upload_line_images import upload_line_images
from controllers.survey.upload_pole_images import upload_pole_images
from controllers.survey.replace_pole_images import replace_pole_images_controller
from controllers.survey.replace_line_images import replace_line_images

router = APIRouter()

@router.post("/upload-pole-images")
async def upload_pole_images_route(
    poleCode: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return await upload_pole_images(poleCode, files)

@router.get("/check-existing-lines")
def check_existing_lines_route(
    startPole: str = Query(..., description="Start pole code"),
    endPole: str = Query(..., description="End pole code")
):
    return check_existing_lines(startPole, endPole)

@router.get("/check-existing-poles")
def check_existing_poles_route(
    poleCode: str = Query(..., description="Pole code to check")
):
    return check_existing_poles(poleCode)

@router.post("/upload-line-images")
async def upload_line_images_route(
    startPoleCode: str = Form(...),
    endPoleCode: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return await upload_line_images(startPoleCode, endPoleCode, files)

@router.post("/replace-pole-images")
async def replace_pole_images_route(
    poleCode: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return await replace_pole_images_controller(
        poleCode=poleCode,
        files=files
    )
@router.post("/replace-line-images")
async def replace_line_images_route(
    startPoleCode: str = Form(...),
    endPoleCode: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return await replace_line_images(
        startPoleCode=startPoleCode,
        endPoleCode=endPoleCode,
        files=files
    )