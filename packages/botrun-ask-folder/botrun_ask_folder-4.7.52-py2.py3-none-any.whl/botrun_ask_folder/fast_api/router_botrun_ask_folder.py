from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.responses import StreamingResponse, Response
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from urllib.parse import quote
import fitz  # PyMuPDF
from PIL import Image

router = APIRouter(
    prefix='/botrun_ask_folder',
    tags=["botrun_ask_folder"]
)

@router.get("/download_file/{file_id}")
def download_file(file_id: str):
    service_account_file = "keys/google_service_account_key.json"
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        file = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file.get('name')
        file_mime_type = file.get('mimeType')

        request = drive_service.files().get_media(fileId=file_id)

        def file_stream():
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                yield fh.getvalue()
                fh.seek(0)
                fh.truncate(0)

        # Encode the filename for Content-Disposition
        encoded_filename = quote(file_name)

        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
            "Content-Type": file_mime_type
        }

        return StreamingResponse(file_stream(), headers=headers, media_type=file_mime_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_pdf_page/{file_id}")
def get_pdf_page(file_id: str, page: int = Query(1, ge=1, description="Page number to retrieve")):
    service_account_file = "keys/google_service_account_key.json"
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # Get file metadata
        file = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_mime_type = file.get('mimeType')

        # Check if the file is a PDF
        if file_mime_type != 'application/pdf':
            return Response(content="The requested file is not a PDF.", media_type="text/plain")

        # Download the file content
        request = drive_service.files().get_media(fileId=file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

        # Open the PDF
        pdf_document = fitz.open(stream=file_content, filetype="pdf")

        # Check if the requested page exists
        if page < 1 or page > len(pdf_document):
            return Response(content=f"Page {page} does not exist in this PDF. Total pages: {len(pdf_document)}", media_type="text/plain")

        # Get the requested page
        pdf_page = pdf_document[page - 1]  # PyMuPDF uses 0-based indexing

        # Render page to an image
        pix = pdf_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return Response(content=img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
