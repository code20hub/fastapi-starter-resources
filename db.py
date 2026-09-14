
'''

'''

import urllib.parse
from sqlmodel import create_engine, SQLModel, Session

safe_password = urllib.parse.quote_plus("Admin11@#")
DATABASE_URL = f"mysql+pymysql://root:{safe_password}@localhost:3306/fastapi_tut"
engine = create_engine(DATABASE_URL, echo=True)

# DATABASE_URL = "sqlite:///db.sqlite" - for sqlite development

def init_db():
    # go through all models, and use the table=True function to create all models as tables, where table=True is set
    SQLModel.metadata.create_all(engine)

# faspapi dependecy to functtion to provide database session.
# Tthis will be injected into any fastapi handler that uses it
def get_session():
    with Session(engine) as session:
        yield session