from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class OpportunityStage(enum.Enum):
    NEW = "New"
    QUALIFIED = "Qualified"
    PROPOSAL = "Proposal"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    customer = relationship("Customer", back_populates="contacts")

Customer.contacts = relationship("Contact", order_by=Contact.id, back_populates="customer")

class Opportunity(Base):
    __tablename__ = 'opportunities'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stage = Column(Enum(OpportunityStage), default=OpportunityStage.NEW)
    customer = relationship("Customer", back_populates="opportunities")

Customer.opportunities = relationship("Opportunity", order_by=Opportunity.id, back_populates="customer")

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    type = Column(String, nullable=False)  # e.g., call, meeting, email
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    customer = relationship("Customer", back_populates="interactions")

Customer.interactions = relationship("Interaction", order_by=Interaction.id, back_populates="customer")

# Create engine and session
engine = create_engine('sqlite:///crm.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
