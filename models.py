from pony.orm import *
from datetime import datetime, timedelta

db = Database(provider='sqlite', filename='database.sqlite', create_db=True) # created DB only if not exists

class User(db.Entity):
    id                 = PrimaryKey(str)
    display_avatar_url = Required(str)
    name               = Required(str)
    mention            = Required(str)
    pendu_completed    = Required(int, default=0)
    puissance4_won     = Required(int, default=0)
    is_admin           = Required(bool, default=False)
    money              = Required(int, default=0)
    time_limits        = Optional('TimeLimits', cascade_delete=True)

class TimeLimits(db.Entity):
    user       = Required(User)
    freelance  = Required(datetime, default=datetime.now() - timedelta(hours=1))
    alternance = Required(datetime, default=datetime.now() - timedelta(hours=6))

db.generate_mapping(create_tables=True)