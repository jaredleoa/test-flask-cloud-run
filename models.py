class Student:
  def __init__(self, id, name, course, year):
    self.id = id
    self.name = name
    self.course = course
    self.year = year

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'course': self.course,
      'year':self.year
    }