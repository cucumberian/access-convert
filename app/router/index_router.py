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
    host: str | None = Form(None),
    port: int | None = Form(None),
    user: str | None = Form(""),
    password: str | None = Form(""),
    database: str | None = Form(None),
):
    try:
        schema = DbConnectSchema(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        return schema
    except Exception:
        return None


@index_router.post("/convert")
def get_access_db(
    access_file: UploadFile,
    is_to_db: bool = Form(False),
    db_connect_schema: DbConnectSchema | None = Depends(validate_db_connect_schema),
):
    if not is_to_db:
        db_connect_schema = None
    try:
        archive_bytes = access_convert(
            access_file,
            db_connection_schema=db_connect_schema,
        )
        return Response(
            content=archive_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=converted_db.zip"},
        )
    except Exception as e:
        return Response(
            content=str(e),
            media_type="text/plain",
            status_code=500,
        )
    
