from backend.app.db import engine, Base

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")

if __name__ == "__main__":
    create_tables()