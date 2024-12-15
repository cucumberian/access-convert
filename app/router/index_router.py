from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import Response
from fastapi import UploadFile
from fastapi.templating import Jinja2Templates

from schema.db_connect_schema import DbConnectSchema
from service.access_convert import access_convert

index_router = APIRouter(prefix="", tags=["index"])
templates = Jinja2Templates(directory="templates")


@index_router.get("/")
def get_html_page_template(request: Request):
    response = templates.TemplateResponse("convert.html", {"request": request})
    return response


def validate_db_connect_schema(
    host: str = Form(),
    port: int = Form(),
    user: str = Form(),
    password: str = Form(),
    database: str = Form(),
):
    return DbConnectSchema(
        host=host, port=port, user=user, password=password, database=database
    )


@index_router.post("/convert")
def get_access_db(
    access_file: UploadFile,
    # db_connect_schema: DbConnectSchema = Depends(validate_db_connect_schema),
):
    archive_bytes = access_convert(access_file)
    return Response(
        content=archive_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=converted_db.zip"},
    )
