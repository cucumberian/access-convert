import os
import subprocess
import shutil
from enum import Enum
from fastapi import UploadFile
from schema.db_connect_schema import DbConnectSchema

from config import Config


def _save_file(file: UploadFile, save_dir: str) -> str:
    if file.filename is None:
        raise ValueError("Файл не найден")
    random_name_part = os.urandom(4).hex()
    filename = f"{random_name_part}_{file.filename}"

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    save_filename = os.path.join(save_dir, filename)

    with open(file=save_filename, mode="wb") as f:
        f.write(file.file.read())
    return save_filename


class ExportSchemaFormat(Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgres"
    SQLITE = "sqlite"
    ORACLE = "oracle"


class ExportFormat(Enum):
    CSV = "csv"
    MYSQL = "mysql"
    POSTGRESQL = "postgres"
    SQLITE = "sqlite"
    ORACLE = "oracle"


def _export_schema(
    access_file_path: str, output_dir: str, export_format: ExportSchemaFormat
) -> bool:
    schema_file = os.path.join(output_dir, "schema.sql")
    with open(schema_file, "w", encoding="utf-8") as f:
        subprocess.run(
            ["mdb-schema", access_file_path, export_format.value], stdout=f, check=True
        )
    return True


def _get_tables(access_file_path: str) -> list[str]:
    result = subprocess.run(
        ["mdb-tables", "-1", access_file_path],
        capture_output=True,
        text=True,
    )
    tables = result.stdout.splitlines()
    tables = [*filter(lambda tablename: not tablename.startswith("MSys"), tables)]
    return tables


def _export_table(
    access_file_path: str, table: str, output_dir: str, export_format: ExportFormat
) -> str:
    export_extension = "csv" if export_format == ExportFormat.CSV else "sql"
    table_file = os.path.join(output_dir, f"{table}.{export_extension}")

    export_args = [
        "mdb-export",
        "-I",
        export_format.value,
        access_file_path,
        table,
    ]
    if export_format == ExportFormat.CSV:
        export_args = [
            "mdb-export",
            "-d",
            "\t",
            access_file_path,
            table,
        ]

    out = subprocess.run(
        export_args,
        capture_output=True,
        text=True,
        check=True,
    )
    out_text = out.stdout
    if out_text:
        with open(table_file, "w", encoding="utf-8") as f:
            f.write(out_text)
    return table_file


def _export_tables(
    access_file_path: str,
    output_dir: str,
    export_format: ExportFormat,
) -> bool:
    if not os.path.isfile(access_file_path):
        raise FileNotFoundError(f"Файл {access_file_path} не найден")

    tables = _get_tables(access_file_path)

    for table in tables:
        print("exporting table:", table)
        _export_table(
            access_file_path,
            table,
            output_dir,
            export_format=export_format,
        )

    return True


def _zip_dir(dir_to_archive: str, archive_name: str, save_dir: str) -> bytes:
    zip_filename = os.path.join(save_dir, archive_name)
    zip_command = ["zip", "-r", zip_filename, dir_to_archive]
    subprocess.run(zip_command, check=True)
    with open(zip_filename, "rb") as f:
        bytes = f.read()
        return bytes


def access_convert(
    access_file: UploadFile, db_connect_schema: DbConnectSchema
) -> bytes:
    save_dir = Config.SAVE_DIR
    save_filename = _save_file(file=access_file, save_dir=save_dir)
    random_subdir_name = os.urandom(8).hex()

    export_dir_name = os.path.join(save_dir, random_subdir_name)
    if not os.path.isdir(export_dir_name):
        os.makedirs(export_dir_name, exist_ok=True)

    _export_schema(
        save_filename,
        export_dir_name,
        export_format=ExportSchemaFormat.POSTGRESQL,
    )
    _export_tables(
        access_file_path=save_filename,
        output_dir=export_dir_name,
        export_format=ExportFormat.CSV,
    )
    _export_tables(
        access_file_path=save_filename,
        output_dir=export_dir_name,
        export_format=ExportFormat.POSTGRESQL,
    )

    archive_name = f"{random_subdir_name}.zip"
    archive_bytes = _zip_dir(
        dir_to_archive=export_dir_name,
        archive_name=archive_name,
        save_dir=save_dir,
    )
    os.remove(save_filename)
    os.remove(os.path.join(save_dir, archive_name))
    shutil.rmtree(export_dir_name)
    return archive_bytes
