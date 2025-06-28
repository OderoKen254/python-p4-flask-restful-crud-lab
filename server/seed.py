#!/usr/bin/env python3

from app import app
from models import db, Plant


with app.app_context():

    # Clear existing data
    Plant.query.delete()

     # Seed data with is_in_stock included
    plants = [
        Plant(
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50,
            is_in_stock=True
        ),
        Plant(
            name="Fiddle Leaf Fig",
            image="./images/fiddle-leaf-fig.jpg",
            price=25.00,
            is_in_stock=False
        ),
        Plant(
            name="Monstera",
            image="./images/monstera.jpg",
            price=30.00,
            is_in_stock=True
        ),
        Plant(
            name="ZZ Plant",
            image="./images/zz-plant.jpg",
            price=22.00,
            is_in_stock=False
        )
    ]

    db.session.add_all(plants)
    db.session.commit()
    print("✅ Database seeded with plant data!")

