from flask_sqlalchemy import Pagination


def pagination_list(
        objs,
        page: int,
        limit: int = 20
) -> Pagination:
    return objs.paginate(page=page, per_page=limit, error_out=None)
