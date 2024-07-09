import os.path
from pathlib import Path

import typer

from ..errors import ErrorPrinter
from . import rest_helper as rest
from . import resumable_upload as upload

app = typer.Typer(
    rich_markup_mode="rich",
    help="""
Manage files ([yellow]Beta feature not available for all customers[/yellow])

Copy file from local to remote storage and vice versa, list and delete files.

""",
)


@app.command(name="ls")
def list_files(
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
    prefix: str = typer.Argument(default="rcs://", help="Remote storage path"),
):
    """
    Listing remote files

    This will list files and directories in project top level directory
    remotive cloud storage ls rcs://

    This will list all files and directories matching the path
    remotive cloud storage ls rcs://fileOrDirectoryPrefix

    This will list all files and directories in the specified directory
    remotive cloud storage ls rcs://fileOrDirectory/
    """

    if prefix.startswith("rcs://"):
        prefix = __check_rcs_path(prefix)
    else:
        ErrorPrinter.print_hint("Path must start with rcs://")
        exit(1)

    rest.handle_get(
        f"/api/project/{project}/files/storage{prefix}",
    )


@app.command(name="rm")
def delete_file(
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
    path: str = typer.Argument(default=..., help="Remote storage path to file to delete"),
):
    """
    [red]Deletes[/red] a file from remote storage, this cannot be undone :fire:

    [white]remotive cloud storage rm rcs://directory/filename[/white]
    """
    if path.startswith("rcs://"):
        prefix = __check_rcs_path(path)
    else:
        ErrorPrinter.print_hint("Path must start with rcs://")
        exit(1)

    rest.handle_delete(
        f"/api/project/{project}/files/storage{prefix}",
    )


@app.command(name="cp")
def copy_file(
    source: str = typer.Argument(default=..., help="Remote or local path to source file"),
    dest: str = typer.Argument(default=..., help="Remote or local path to destination file"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
):
    """
    Copies a file to or from remote storage

    remotive cloud storage cp rcs://dir/filename .
    remotive cloud storage cp rcs://dir/filename filename

    remotive cloud storage cp filename rcs://dir/
    remotive cloud storage cp filename rcs://dir/filename
    """

    if not source.startswith("rcs://") and not dest.startswith("rcs://"):
        ErrorPrinter.print_hint("Source or destination path must be an rcs:// path")
        exit(2)

    if source.startswith("rcs://") and dest.startswith("rcs://"):
        ErrorPrinter.print_hint("Currently one of source and destination path must be a local path")
        exit(2)

    if source.startswith("rcs://"):
        rcs_path = __check_rcs_path(source)
        filename = source.rsplit("/", 1)[-1]
        path = Path(dest)
        if path.is_dir():
            if not path.exists():
                ErrorPrinter.print_generic_error("Destination directory does not exist")
                exit(1)
            else:
                dest = os.path.join(path.absolute(), filename)

        else:
            if not path.parent.is_dir() or not path.parent.exists():
                ErrorPrinter.print_generic_error("Destination directory does not exist")
                exit(1)
        dest = Path(dest).absolute()

        res = rest.handle_get(
            f"/api/project/{project}/files/storage{rcs_path}?download=true",
            return_response=True,
        )

        rest.download_file(save_file_name=dest, url=res.text)

    else:
        path = Path(source)
        if not path.exists():
            ErrorPrinter.print_hint("Source file does not exist")
            exit(1)
        filename = source.rsplit("/", 1)[-1]
        rcs_path = __check_rcs_path(dest)
        if rcs_path.endswith("/"):
            rcs_path = rcs_path + filename
        res = rest.handle_post(f"/api/project/{project}/files/storage{rcs_path}", return_response=True)
        json = res.json()
        url = json["url"]
        content_type = json["contentType"]
        try:
            upload.upload_signed_url(url, source, content_type)
        except IsADirectoryError:
            ErrorPrinter.print_hint(f"Supplied source file '{source}' is a directory but must be a file")


def __check_rcs_path(path: str):
    rcs_path = path.replace("rcs://", "/")
    if rcs_path.startswith("/."):
        ErrorPrinter.print_hint("Invalid path")
        exit(1)
    return rcs_path
