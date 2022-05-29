from fastapi import HTTPException, status

from database.models import WalletBase


def raise_not_found_if_none(
        model_object: WalletBase | None, model_name: str,
        message: str | None = None
) -> None:
    if model_object is None:
        message = (
            message if message
            else f'{model_name} with given id does not exist'
        )

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=message)
