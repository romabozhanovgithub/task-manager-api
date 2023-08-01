from typing import Literal, Optional
from fastapi import Query


class PaginationQueryParams:
    def __call__(
        self,
        limit: Optional[int] = Query(None, ge=1, le=100),
        offset: Optional[int] = Query(None, ge=0) 
    ) -> dict[Literal["limit", "offset"], int | None]:
        return {
            "limit": limit,
            "offset": offset
        }
    

PaginationParams = PaginationQueryParams()
