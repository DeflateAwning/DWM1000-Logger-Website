#!/usr/bin/env python3

# app/models.py

# Describes the database layout

from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime


class RangingRequest(db.Model):

    __tablename__ = 'RangingRequests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anchorNumber = db.Column(db.Float, nullable=False)
    rangeDistance = db.Column(db.Float, nullable=False)
    receivePower = db.Column(db.Float, nullable=False)
    receiveTime = db.Column(db.DateTime, nullable=False)
    transmitTime = db.Column(db.DateTime, nullable=False)
    success = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        #self.password = plaintext_password # old, broken maybe
        self.set_password(plaintext_password)
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)

