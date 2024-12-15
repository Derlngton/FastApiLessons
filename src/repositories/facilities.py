from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facilitie


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilitie


