from abc import ABC, abstractmethod
import uuid
import random

class IDGenerator(ABC):

  @abstractmethod
  def get_id(self):
    pass

class AlphaNumericIDGenerator(IDGenerator):
  def get_id(self):
    return str(uuid.uuid1())

class NumericIDGenerator(IDGenerator):
  def get_id(self):
    return random.randint(10000, 100000000000)
