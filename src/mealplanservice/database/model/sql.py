from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Double, Table, Text
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped
from typing import List

Base: DeclarativeBase = declarative_base()

class MealPlan(Base):
    __tablename__ = "mealPlan"
    planID             = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    userID             = Column(Integer, nullable=False)
    startDate          = Column(String(255), nullable=False)
    endDate            = Column(String(255), nullable=False)
    mealsPerDay        = Column(Integer, nullable=False)
    totalCalories      = Column(Integer, nullable=False)
    totalProtein       = Column(float, nullable=False)
    totalCarbohydrates = Column(float, nullable=False)
    totalFat           = Column(float, nullable=False)

class MealPlanRecipes(Base):
    __tablename__ = "mealPlanRecipes"
    planID        = Column(Integer, ForeignKey("mealPlan.planID"))    
    recipeID        = Column(Integer, nullable=False)