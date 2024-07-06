from ShopifyTupperware.data import db

_db = db.db

class UserDb(_db.Model):
    __tablename__ = "user"
    __table_args__ = {'implicit_returning':False}

    id = _db.Column(_db.Integer, primary_key=True)
    username = _db.Column(_db.String, unique=True, nullable=False)
    password = _db.Column(_db.String, nullable=False)
    secret = _db.Column(_db.String, nullable=False)


    @staticmethod
    def create_or_update(user):
        _db.session.add(user)
        _db.session.commit()
        return user

    @staticmethod
    def valid_user(username, password):
        return _db.session.query(UserDb).with_hint(UserDb, 'WITH (NOLOCK)').filter((UserDb.username == username) & (UserDb.password == password)).first()

    @staticmethod
    def get_valid_user_secret(username, secret):
        return _db.session.query(UserDb).with_hint(UserDb, 'WITH (NOLOCK)').filter((UserDb.username == username) & (UserDb.secret == secret)).first()


