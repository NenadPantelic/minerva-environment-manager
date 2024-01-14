from app import db
from datetime import datetime


class Environment(db.Model):
    __tablename__ = "environment"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    docker_image = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, docker_image):
        self.name = name
        self.docker_image = docker_image

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'docker_image': self.docker_image,
        }