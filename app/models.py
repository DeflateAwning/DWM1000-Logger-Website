#!/usr/bin/env python3

# app/models.py

# Describes the database layout

from app import db, bcrypt
from app import bandtools400

#from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime


class RangingRequest(db.Model):

    __tablename__ = 'RangingRequests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anchorNumber = db.Column(db.Integer, nullable=False)
    tagNumber = db.Column(db.Integer, nullable=False)
    accountNumber = db.Column(db.Integer, nullable=False)
    rangeDistance = db.Column(db.Float, nullable=False)
    receivePower = db.Column(db.Float, nullable=False)
    rangeTime = db.Column(db.DateTime, nullable=False) # time the ranging occured
    transmitTime = db.Column(db.DateTime, nullable=False) # time transmission from uC occured
    receiveTime = db.Column(db.DateTime, nullable=False) # time received here
    success = db.Column(db.Boolean, nullable=False, default=False)
    errorMessage = db.Column(db.String, nullable=True, default=None)

    def __init__(self, rangeRequestInfo):
        self.receiveTime = datetime.now()

        self.rangeDistance = rangeRequestInfo.get("Range", 0)
        self.anchorNumber = rangeRequestInfo.get("AnchorNumber")
        self.accountNumber = rangeRequestInfo.get("AccountNumber")
        self.tagNumber = rangeRequestInfo.get("TagNumber")
        self.receivePower = rangeRequestInfo.get("ReceivePower", 0)
        self.transmitTime = rangeRequestInfo.get("TransmitDate")
        self.rangeTime = rangeRequestInfo.get("RangeDate")
        self.success = rangeRequestInfo.get("Success", False)

        self.errorMessage = rangeRequestInfo.get("ErrorMessage", {True: None, False: "No Error Supplied from uC"}[rangeRequestInfo.get("Success", False)])

    def __repr__(self):
        return '<Ranging Request #{0}, range={1}>'.format(self.id, self.rangeDistance)

class AnchorSettings(db.Model):
    __tablename__ = "AnchorSettings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anchorNumber = db.Column(db.Integer, nullable=False, unique=True)

    anchorCoordX = db.Column(db.Float, nullable=False)
    anchorCoordY = db.Column(db.Float, nullable=False)

    anchorCoordXSteps = db.Column(db.Float, nullable=False)
    anchorCoordYSteps = db.Column(db.Float, nullable=False)

    enabled = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, anchorNumber, enabled=True, anchorCoord=(None, None), anchorCoordSteps=(None, None)):
        """
        Creates new settings for an anchor

        Provide either anchorCoord (in meters, x and y components), or anchorCoordSteps (in 8-to-5 steps); NOT BOTH.

        This means that 0,0 is the center of the field at the front sideline.
        """

        self.anchorNumber = anchorNumber
        self.enabled = enabled

        if anchorCoord != (None, None):
            self.anchorCoordX = anchorCoord[0]
            self.anchorCoordY = anchorCoord[1]

            self.anchorCoordXSteps = bandtools400.convertMetersToSteps(anchorCoord[0])
            self.anchorCoordYSteps = bandtools400.convertMetersToSteps(anchorCoord[1])

            print("Set on Meters, " + str(anchorCoord))


        elif anchorCoordSteps != (None, None):
            self.anchorCoordXSteps = anchorCoordSteps[0]
            self.anchorCoordYSteps = anchorCoordSteps[1]

            self.anchorCoordX = bandtools400.convertStepsToMeters(anchorCoordSteps[0])
            self.anchorCoordY = bandtools400.convertStepsToMeters(anchorCoordSteps[1])

            print("Set on Steps")

    def __repr__(self):
        return '<Anchor Settings for Anchor #{0}>'.format(self.anchorNumber)
