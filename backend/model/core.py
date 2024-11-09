from sqlalchemy import Column,Integer, String, DateTime,select,func
import os
import aioredis
from sqlalchemy.orm import declarative_base
import datetime
from sqlalchemy.ext.asyncio import AsyncSession as Session,create_async_engine,async_sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    type = Column(String)
    email = Column(String, unique=True, index=True,default=None)
    first_name = Column(String)
    last_name = Column(String)
    photo_url = Column(String,default=None)
    userid = Column(String,default=None)
    username = Column(String,default=None)
    last_activity = Column(DateTime(timezone=True),default=datetime.datetime.now(datetime.timezone.utc))
    score = Column(Integer,default=0)

class ModelInterface:
    redis = aioredis.Redis(host=os.getenv('Broker_Host'),port=os.getenv('Broker_Port'),password=os.getenv('Broker_Password'))

    engine = create_async_engine(
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
    )
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
   
    @classmethod
    async def get_db(cls):
        db = cls.SessionLocal()
        try:
            yield db
        except:
            await db.rollback()
            raise
        finally:
            await db.close()    

    @classmethod
    async def set_user(cls,db: Session,type: str,first_name: str,last_name: str,photo_url: str = None,email: str = None,username: str = None,userid: str = None):
        user = User(type=type,email=email,username=username,userid=userid,first_name=first_name,last_name=last_name,photo_url=photo_url)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    @classmethod
    async def get_finduser(cls,db: Session,userid: str = None,email: str = None):
        if userid is not None:
            try:
                return await db.scalar(select(User).where(User.userid == userid))
            except:
                return None
        if email is not None:
            try:
                return await db.scalar(select(User).where(User.email == email))
            except:
                return None

    @classmethod
    async def set_pub(cls,data,fagot:int,db: Session):
        await cls.redis.publish("fagots",fagot)
        user : User = await db.scalar(select(User).where(User.id == fagot))
        user.score = user.score + 1
        await db.commit()

    @classmethod
    async def get_pidor(cls,db: Session,amount,offset):
        fully_fagot = await db.execute(select(User.id,User.first_name,User.last_name,User.photo_url,User.score).order_by((User.score.desc())).limit(amount).offset(offset))
        count_fagots = await db.scalars(select(func.count("*")).select_from(User))
        return {"users": [{"id": row[0], "first_name": row[1], "last_name": row[2], "photo":row[3], "score": row[4]} for row in fully_fagot.all()], 
        "totalUsers": count_fagots.all()[0]}