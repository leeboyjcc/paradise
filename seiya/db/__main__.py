from seiya.db.base import engine, Base

Base.metadata.create_all(engine)

print('__main__.py executed!')