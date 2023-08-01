from uuid import UUID
from fastapi import Path, Query


class UserIDQueryParam:
    def __call__(
        self,
        user_id: str = Query(..., alias="userId", min_length=10),
    ) -> UUID:
        return UUID(user_id)
    

class UserIDPathParam:
    def __call__(
        self,
        user_id: str = Path(..., min_length=10),
    ) -> UUID:
        return UUID(user_id)
    

UserIDQuery = UserIDQueryParam()
UserIDPath = UserIDPathParam()
