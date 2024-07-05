from datetime import datetime
from sqlalchemy import (Boolean, Column, DateTime, Integer, String)

from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

class CreatedModifiedBase(object):
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, default=datetime.now())
