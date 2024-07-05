import csv
import inspect
import logging
import os
import re
import unicodedata
import uuid
from typing import Dict, Type

from fastapi import Depends, UploadFile
from pydantic import BaseModel, Field, create_model

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(10)),
    *(f"LPT{i}" for i in range(10)),
}

log = logging.getLogger(__name__)


class Line(object):
    def __init__(self):
        self._line = None

    def write(self, line):
        self._line = line

    def read(self):
        return self._line


async def generate_report(data, list_columns, label_columns):
    line = Line()
    writer = csv.writer(line, delimiter=",")

    # header
    labels = []
    for key in list_columns:
        labels.append(label_columns[key])

    # rows
    writer.writerow(labels)
    yield line.read()

    async for chunk in data:
        for item in chunk:
            row = []
            for key in list_columns:
                value = getattr(item, key)
                # if value is a function, call it
                if callable(value):
                    try:
                        value = value()
                    except Exception as e:
                        value = "Error calling function"
                if value is None:
                    value = ""
                row.append(str(value))
            writer.writerow(row)
            yield line.read()


def merge_schema(
    schema: BaseModel,
    fields: Dict[str, tuple[type, Field]],
    only_update=False,
    name: str | None = None,
) -> Type[BaseModel]:
    """
    Replace or add fields to the given schema.

    Args:
        schema (BaseModel): The schema to be updated.
        fields (Dict[str, tuple[type, Field]]): The fields to be added or updated.
        only_update (bool): If True, only update the fields with the same name. Otherwise, add new fields.
        name (str, optional): The name of the new schema. Defaults to None.

    Returns:
        BaseModel: The updated schema.
    """
    name = name or schema.__name__
    new_fields = dict()
    if only_update:
        for key, value in schema.model_fields.items():
            if key in fields:
                val = fields[key]
                if isinstance(val, tuple):
                    new_fields[key] = val
                else:
                    new_fields[key] = (value.annotation, val)
    else:
        new_fields = fields

    return create_model(
        name,
        **new_fields,
        __base__=schema,
    )


def update_self_signature(cls, f):
    """
    Update the signature of a function to replace the first parameter with 'self' as a dependency.

    Args:
        cls (class): The class that the function belongs to.
        f (function): The function to be updated.

    Returns:
        None
    """
    # Get the function's parameters
    old_signature = inspect.signature(f)
    old_parameters = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]

    # If the first parameter is self, replace it
    if old_first_parameter.name == "self":
        new_first_parameter = old_first_parameter.replace(default=Depends(lambda: cls))

        new_parameters = [new_first_parameter] + [
            parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            for parameter in old_parameters[1:]
        ]
        new_signature = old_signature.replace(parameters=new_parameters)

        setattr(
            f, "__signature__", new_signature
        )  # Set the new signature to the function


def uuid_namegen(file_data: UploadFile) -> str:
    """
    Generates a unique filename by combining a UUID and the original filename.

    Args:
        file_data (File): The file data object.

    Returns:
        str: The generated unique filename.
    """
    return str(uuid.uuid1()) + "_sep_" + file_data.filename


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    .. versionadded:: 0.5

    :param filename: the filename to secure
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename
