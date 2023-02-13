import datetime

from aiogram import types
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, VARCHAR, INTEGER, DateTime, BigInteger, sql, String

from tgbot.config import Config, load_config

db = Gino()


class User(db.Model):
    __tablename__ = 'user'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), unique=True)
    lang = Column(String(length=2))
    name = Column(VARCHAR(100))
    phone = Column(VARCHAR(15))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class Cargo(db.Model):
    __tablename__ = 'cargo'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    cargo_id = Column(VARCHAR(200))
    user_name = Column(VARCHAR(200))
    container_type = Column(VARCHAR(200))
    cargo_number = Column(VARCHAR(200))
    load_date = Column(DateTime)
    load_address = Column(VARCHAR(200))
    send_date = Column(DateTime)
    dislocation = Column(VARCHAR(200))
    delivery_address = Column(VARCHAR(200))
    arrival_date = Column(DateTime)
    burning_address = Column(VARCHAR(200))
    phone = Column(VARCHAR(15))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class Admin(db.Model):
    __tablename__ = 'admin'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), unique=True)
    name = Column(VARCHAR(50))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class DBCommands:

    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.tg_id == user_id).gino.first()
        return user

    async def add_new_user(self, lang) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        return await User.create(tg_id=user.id, lang=lang)

    async def set_language(self, language) -> None:
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(lang=language).apply()

    async def add_admin(self, admin_id, admin_name) -> Admin:
        return await Admin.create(tg_id=admin_id, name=admin_name)

    async def add_or_update(self, **kwargs) -> None:
        cargo = await Cargo.query.where(Cargo.cargo_number == kwargs['cargo_number']).gino.first()
        if cargo is not None:
            await cargo.update(user_name=kwargs["user_name"], container_type=kwargs["container_type"],
                               load_date=kwargs["load_date"], load_address=kwargs["load_address"],
                               send_date=kwargs["send_date"], dislocation=kwargs["dislocation"],
                               delivery_address=kwargs["delivery_address"], arrival_date=kwargs["arrival_date"],
                               burning_address=kwargs["burning_address"], phone=kwargs["phone"]).apply()
        else:
            await Cargo.create(cargo_id=kwargs["cargo_id"], user_name=kwargs["user_name"],
                               container_type=kwargs["container_type"], cargo_number=kwargs["cargo_number"],
                               load_date=kwargs["load_date"], load_address=kwargs["load_address"],
                               send_date=kwargs["send_date"], dislocation=kwargs["dislocation"],
                               delivery_address=kwargs["delivery_address"], arrival_date=kwargs["arrival_date"],
                               burning_address=kwargs["burning_address"], phone=kwargs["phone"])

    async def get_cargos(self, cargo_id):
        cargo = await Cargo.query.where(Cargo.cargo_id == cargo_id).gino.all()
        if len(cargo) == 0:
            return False
        return cargo

    async def get_cargo(self, id) -> Cargo:
        cargo = await Cargo.query.where(Cargo.id == id).gino.first()
        return cargo


async def create_db():
    config: Config = load_config(".env")
    await db.set_bind(f'postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}')

    # Create tables
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
