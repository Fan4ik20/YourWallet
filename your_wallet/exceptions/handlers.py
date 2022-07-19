from fastapi import Request, status
from fastapi.responses import JSONResponse

from exceptions import exc


def object_not_exist_handler(
        _: Request, exc_: exc.ObjectNotExist
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'message': f'{exc_.model} with given identifier does not exist!',
            'place': 'Path'
        }
    )


def object_with_given_attr_exist_handler(
        _: Request, exc_: exc.ObjectWithGivenAttrExist
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            'message': f'{exc_.model} with given {exc_.attr} already exist',
            'place': 'Path'
        }
    )


def object_not_exist_in_body_handler(
        _: Request, exc_: exc.ObjectNotExistInBody
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'message': f'{exc_.model} with given identifier does not exist!',
            'place': 'Body'
        }
    )
