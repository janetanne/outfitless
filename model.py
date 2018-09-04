from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

###############################################################

class User(db.Model, UserMixin):
    """User."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True, 
                   nullable=False)
    email = db.Column(db.String(100), nullable=False,
                      unique=True)
    name = db.Column(db.String(100), 
                     nullable=False)
    tokens = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(200))

    def get_id(self): 
        return (self.user_id)

    def __repr__(self):
        """Provides helpful info when printed."""

        return "<User id={} email={} name={}>".format(
                self.user_id, self.email, self.name)

class Piece(db.Model):
    """Piece of clothing. A closet has multiple pieces."""

    __tablename__ = "pieces"

    piece_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    times_worn = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    cost_per_use = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id),
                          nullable=False)

    # for the clarifai concept/description of item
    desc = db.Column(db.String(50), nullable=False)

    # for top/bottom/dress/jacket
    clothing_type = db.Column(db.String(50), nullable=False)

    # img url from src
    img_url = db.Column(db.String(200), nullable=False)

    # for athleisure/etc.
    categories = db.relationship('Category', 
                                 secondary="category_pieces",
                                 backref="pieces")

    user = db.relationship('User', backref="pieces")

    #### FUTURE FEATURE: for activities ####
    # activity_1 = db.Column(db.String(50), nullable=False)
    # activity_2 = db.Column(db.String(50), nullable=False)
    # activity_3 = db.Column(db.String(50), nullable=False)

    # activity = db.relationship('Activity', backref="activities")

    def __repr__(self):
        """Provide helpful info when printed."""

        return "<Piece piece_id = {} desc = {} categories = {} \
               clothing_type = {}>".format(self.piece_id, 
                                           self.desc, 
                                           self.categories, 
                                           self.clothing_type)

class Outfit(db.Model):
    """Outfit combination. Each piece can be in multiple outfits.
    Each outfit can have multiple pieces."""

    __tablename__ = "outfits"

    outfit_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    user = db.relationship('User', backref="outfits")
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id),
                          nullable=False)

    def __repr__(self):
        """Provides helpful info when printed."""

        return "<Outfit outfit_id={}>".format(self.outfit_id)

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

    ow_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)

    date_worn = db.Column(db.DateTime, nullable=False)
    outfit_id = db.Column(db.Integer, 
                        db.ForeignKey(Outfit.outfit_id),
                        nullable=False)
    outfit = db.relationship('Outfit', backref="outfitwears")

    def __repr__(self):
        """Provide helpful info when printed."""

        return "<OutfitWear ow_id = {} date_worn = {} \
                outfit_id>".format(self.ow_id, 
                                   self.date_worn, 
                                   self.outfit_id)


class Category(db.Model):
    """For each category."""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)

    category = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """Provide helpful info when printed."""

        return "<Category cat_id = {} \
                category = {}>".format(self.cat_id, 
                                      self.category)

class CategoryPiece(db.Model):
    """Association table for Category and Piece tables."""

    __tablename__ = "category_pieces"

    cp_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True, 
                        nullable=False)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey(Piece.piece_id),
                         nullable=False)
    cat_id = db.Column(db.Integer,
                         db.ForeignKey(Category.cat_id),
                         nullable=False)

    def __repr__(self):
        """Provide helpful info when printed."""

        return "<CategoryPiece cp_id = {}>".format(self.cp_id)

################## FUTURE FEATURE: CLOSETS ##################

# class Closet(db.Model):
#     """Closet. A user can have multiple closets."""

#     __tablename__ = "closets"

#     closet_id = db.Column(db.Integer, 
#                         primary_key=True,
#                         autoincrement=True, 
#                         nullable=False)
#     id = db.Column(db.Integer, db.ForeignKey(User.id),
#                         nullable=False)

#     user = db.relationship('User', backref="closets")
#     closet_name = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         """Provides helpful info when printed."""

#         return "<Closet closet_id={} closet_name={}>".format(
#             self.closet_id, self.closet_name)

################## FUTURE FEATURE: ACTIVITIES ##################

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