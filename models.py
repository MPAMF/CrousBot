from pony.orm import *
from datetime import datetime, timedelta

db = Database(provider='sqlite', filename='database.sqlite', create_db=True) # created DB only if not exists

class User(db.Entity):
    id                 = PrimaryKey(str) # == discord ID
    xp                 = Required(int, default=0)
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

class Level(db.Entity):
    level     = PrimaryKey(int)
    name      = Required(str)
    threshold = Required(int)

db.generate_mapping(create_tables=True)

levels = [
        {
            'level': 1,
            'threshold': 0,
            'name': 'Stagiaire'
        },
        {
            'level': 2,
            'threshold': 100,
            'name': 'Apprenti'
        },
        {
            'level': 3,
            'threshold': 300,
            'name': 'Freelancer'
        },
        {
            'level': 4,
            'threshold': 500,
            'name': 'Dev junior'
        },
        {
            'level': 5,
            'threshold': 1000,
            'name': 'Dev Mid-Level'
        },
        {
            'level': 6,
            'threshold': 2000,
            'name': 'Dev Senior'
        },
        {
            'level': 7,
            'threshold': 4000,
            'name': 'Lead Developer'
        },
        {
            'level': 8,
            'threshold': 8000,
            'name': 'CTO'
        },
        {
            'level': 9,
            'threshold': 20000,
            'name': 'Ultramax basement dweller'
        },
    ]

with db_session:
    for level in levels:
        existing_l = Level.get(level=level["level"])
        
        if existing_l != None:
            continue

        l = Level(level=level["level"], threshold=level["threshold"], name=level["name"])