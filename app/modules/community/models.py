from app import db
from datetime import datetime

members_association = db.Table('members_association',
                               db.Column('community_id', db.Integer, db.ForeignKey('community.id'), primary_key=True),
                               db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship('User', backref='owned_communities', lazy=True)
    members = db.relationship('User', secondary=members_association, backref='joined_communities', lazy='subquery')

    def __repr__(self):
        return f'Community<{self.id}, Name={self.name}, Owner={self.owner.username}>'
