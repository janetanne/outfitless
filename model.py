from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

###############################################################

class User(db.Model, UserMixin):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True, 
                   nullable=False)
    email = db.Column(db.String(100), nullable=False,
                      unique=True)
    name = db.Column(db.String(100), 
                     nullable=False)
    tokens = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(200))

    def __repr__(self):
        """Provides helpful info when printed."""

        return "<User id={} email={}>".format(
                self.user_id, self.email)

class Closet(db.Model):
    """Closet. A user can have multiple closets."""

    __tablename__ = "closets"

    closet_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    id = db.Column(db.Integer, db.ForeignKey(User.id),
                        nullable=False)

    user = db.relationship('User', backref="closets")
    closet_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provides helpful info when printed."""

        return "<Closet closet_id={} closet_name={}>".format(
            self.closet_id, self.closet_name)

class Piece(db.Model):
    """Piece of clothing. A closet has multiple pieces."""

    __tablename__ = "pieces"

    piece_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    times_worn = db.Column(db.Integer, nullable=False)
    closet_id = db.Column(db.Integer, db.ForeignKey(Closet.closet_id),
                          nullable=False)

    # for the clarifai concepts
    desc = db.Column(db.String(50), nullable=False)

    # for top/bottom/one-piece/jacket
    clothing_type = db.Column(db.String(50), nullable=False)

    # for athleisure/etc.
    category = db.Column(db.String(50), nullable=False)

    closet = db.relationship('Closet', backref="pieces")

    # TODO: for activities; ask about foreign key
    # activity_1 = db.Column(db.String(50), nullable=False)
    # activity_2 = db.Column(db.String(50), nullable=False)
    # activity_3 = db.Column(db.String(50), nullable=False)

    # activity = db.relationship('Activity', backref="activities")

    def __repr__(self):
        """Provide helpful info when printed."""

        return "<Piece piece_id = {} desc_1 = {} category = {}".format(
            self.piece_id, self.desc_1, self.category)

class Outfit(db.Model):
    """Outfit combination. Each piece can be in multiple outfits.
    Each outfit can have multiple pieces."""

    __tablename__ = "outfits"

    outfit_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    closet = db.relationship('Closet', backref="outfits")
    closet_id = db.Column(db.Integer, db.ForeignKey(Closet.closet_id),
                          nullable=False)

    def __repr__(self):
        """Provides helpful info when printed."""

        return "<Outfit outfit_id={} closet_id={}>".format(
               self.outfit_id, self.title)

class OutfitPiece(db.Model):
    """Each item in each outfit."""

    __tablename__ = "outfitpieces"

    outfitpiece_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)

    outfit_id = db.Column(db.Integer, 
                        db.ForeignKey(Outfit.outfit_id),
                        autoincrement=True, 
                        nullable=False)
    piece_id = db.Column(db.Integer, 
                        db.ForeignKey(Piece.piece_id),
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
                        db.ForeignKey(Outfit.outfit_id),
                        nullable=False)
    outfit = db.relationship('Outfit', backref="outfitwears")

# add activities later

# class Activity(db.Model):
#     """Activity."""

#     activity_id = db.Column(db.Integer, 
#                         primary_key=True,
#                         autoincrement=True, 
#                         nullable=False)
#     activity = db.Column(db.String(50), nullable=False)

# class ActivityPiece(db.Model):
#     """Connects activity and pieces."""

#     __tablename__ = "activitypieces"

#     activity_id = db.Column(db.Integer,
#                             db.ForeignKey('activity.activity_id'),
#                             nullable=False)
#     piece_id = db.Column(db.Integer,
#                         db.ForeignKey('piece.piece_id'),
#                         nullable=False)

#     piece = db.relationship('Piece', backref="activitypieces")
#     activity = db.relationship('Activity', backref="activitypieces")

##################################################################

def connect_to_db(app, db_name):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# connect_to_db(server.app, 'outfitless_db')

# db_create_all()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app, 'outfitless_db')
    db.create_all()

    print("Connected to DB.")