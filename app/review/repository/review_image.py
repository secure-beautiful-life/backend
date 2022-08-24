from app.review.model import ReviewImage
from core.repository import BaseRepoORM


class ReviewImageRepo(BaseRepoORM):
    model = ReviewImage
