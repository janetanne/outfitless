db = SQLAlchemy()

def connect_to_db(app, db_name):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

connect_to_db(app, 'outfitless_db')

# NEED TO FIGURE OUT OAUTH FOR USER
class User(db.Model):
    """User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    email = db.Column(db.String(50), nullable=False,
                      unique=True)
    password = db.Column(db.String(25), nullable=False)

# NEED TO FIGURE OUT GOOGLE PHOTOS ALBUM CONNECTION
class Closet(db.Model):
    """Closet. A user can have multiple closets."""

    __tablename__ = "closets"

    closet_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)
    user = db.relationship('User', backref="closets")
    closet_name = db.Column(db.String(50), nullable=False)

# NEED TO FIGURE OUT CLARIFAI API CONNECTION
class Piece(db.Model):
    """Piece of clothing. A closet has multiple pieces."""

    __tablename__ = "pieces"

    piece_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    times_worn = db.Column(db.Integer, nullable=False)
    closet_id = db.Column(db.Integer, db.ForeignKey('closet.closet_id'),
                          nullable=False)
    closet = db.relationship('Closet', backref="pieces")
    # possibly add activities here


class Outfit(db.Model):
    """Outfit combination. Each piece can be in multiple outfits.
    Each outfit can have multiple pieces."""

    __tablename__ = "outfits"

    outfit_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    closet = db.relationship('Closet', backref="outfits")
    closet_id = db.Column(db.Integer, db.ForeignKey('closet.closet_id'),
                          nullable=False)

class OutfitPiece(db.Model):
    """Each item in each outfit."""

    __tablename__ = "outfitpieces"

    outfit_id = db.Column(db.Integer, 
                        db.ForeignKey('outfit.outfit_id'),
                        autoincrement=True, 
                        nullable=False)
    piece_id = db.Column(db.Integer, 
                        db.ForeignKey('piece.piece_id'),
                        autoincrement=True, 
                        nullable=False)
    outfit = db.relationship('Outfit', backref="outfitpieces")
    piece = db.relationship('Piece', backref="outfitpieces")

class OutfitWear(db.Model):
    """Each instance of an outfit being worn."""

    __tablename__ = "outfitwears"

    outfit_wear_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)

    date = db.Column(db.DateTime, nullable=False)
    outfit_id = db.Column(db.Integer, 
                        db.ForeignKey('outfit.outfit_id'),
                        nullable=False)
    outfit = db.relationship('Outfit', backref="outfitwears")

class Activity(db.Model):
    """Activity."""

    activity_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    activity = db.Column(db.String(50), nullable=False)

class ActivityPiece(db.Model):
    """Connects activity and pieces."""

    __tablename__ = "activitypieces"

    activity_id = db.Column(db.Integer,
                            db.ForeignKey('activity.activity_id'),
                            nullable=False)
    piece_id = db.Column(db.Integer,
                        db.ForeignKey('piece.piece_id'),
                        nullable=False)

    piece = db.relationship('Piece', backref="activitypieces")
    activity = db.relationship('Activity', backref="activitypieces")


db_create_all()