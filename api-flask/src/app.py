import os

from datetime import datetime
from flask import Flask, current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import click
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)
migrate = Migrate()

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True, nullable=True)
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r})"


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'), nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"Post(id={self.id}, author_id={self.author_id}, title={self.title}, created={self.created}, body={self.body!r})"

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///bank-database.sqlite',
    )
    

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from src.controller import user, post
    app.register_blueprint(user.app)

    return app
