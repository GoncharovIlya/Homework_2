import pytest

def test_simple():
    mylist = [1,2,3,4,5]
    assert 1 in mylist

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def set_age(self, new_age: int):
        if type(new_age) == int:
            self.age = new_age
            return
        raise ValueError

    def __repr__(self):
        return f'Person{self.name, self.age}'
    
@pytest.fixture
def people():
    person = Person('Ivan', 30)
    return person

def test_create_person(people):
    """Проверка создания персоны"""
    assert people.name =='Ivan'
    assert people.age == 30

def test_set_age(people):
    assert people.age == 30
    people.set_age(50)
    assert people.age == 50