from sqlalchemy import select



from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository



class HotelsRepository(BaseRepository):
    model = HotelsOrm


    async def get_all(
            self,
            location:str,
            title:str,
            limit:int,
            offset:int
    ):


        query = select(HotelsOrm)

        if title:
            query=query.filter(HotelsOrm.title.icontains(title))
        if location:
            query=query.filter(HotelsOrm.location.icontains(location))

        query=(
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        return result.scalars().all()

