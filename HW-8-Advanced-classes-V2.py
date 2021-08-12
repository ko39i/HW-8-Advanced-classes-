from __future__ import annotations
from typing import Dict, Any
from abc import ABC, abstractmethod
import random
import uuid
import time


class Animal(ABC):

    def __init__(self, power: int, speed: int):
        self.id = None
        self.max_power = power
        self.current_power = power
        self.speed = speed

    @abstractmethod
    def eat(self, forest: Forest):
        pass


class Predator(Animal):

    def eat(self, forest: Forest):
        hunting_animal = random.choice(list(forest.animals.values()))
        if hunting_animal.id == self.id:
            print("predator left left without a dinner")
        else:
            print(f"{__class__.__name__}: power = {self.current_power} and speed = {self.speed}"
                  f"starts hunting for {hunting_animal.__class__.__name__}: power =  {hunting_animal.current_power} and speed = {hunting_animal.speed}")
            if self.speed > hunting_animal.speed:
                print("predator caught up")
                if self.current_power > hunting_animal.current_power:
                    print("predator won")
                    Forest.recuperation(self)
                    forest.remove_animal(hunting_animal)
                else:
                    print("predator lost")
                    Forest.an_recuperation(hunting_animal)
                    Forest.an_recuperation(self)
            else:
                print("predator did not caught up")
                Forest.an_recuperation(hunting_animal)
                Forest.an_recuperation(self)


class Herbivorous(Animal):

    def eat(self, forest: Forest):
        Forest.recuperation(self)



AnyAnimal: Any[Herbivorous, Predator]


class Forest:

    def __init__(self):
        self.animals: Dict[str, AnyAnimal] = dict()

    def add_animal(self, animal: AnyAnimal):
        print(f"New animal added", animal)
        self.animals.update({animal.id: animal})

    def remove_animal(self, animal: AnyAnimal):
        print(f"{animal.__class__.__name__} removed")
        self.animals.pop(animal.id)

    def any_predator_left(self):
        for x in list(self.animals.values()):
            if x.__class__.__name__ == 'Predator':
                print(f'{x.__class__.__name__} is in forest')
                if len(list(self.animals.values())) == 1:
                    print(f'Only {x.__class__.__name__} live in forest')
                    return False
                return True
        print(f'Only {x.__class__.__name__} live in forest')
        return False

    def __iter__(self):
        self.num = 0
        self.animal_item = list(self.animals.values())
        return self

    def __next__(self):
        self.num += 1
        if self.num <= len(self.animal_item):
            return self.animal_item[self.num - 1]
        else:
            raise StopIteration

    def recuperation(animal: AnyAnimal):
        print(f"{animal.__class__.__name__}: power = {animal.current_power}")
        if animal.current_power + animal.max_power * 0.5 >= animal.max_power:
            animal.current_power = animal.max_power
        else:
            animal.current_power = round(animal.current_power + animal.max_power * 0.5, 1)
            print(f"{animal.__class__.__name__} ate and recovered power to {animal.current_power}")


    def an_recuperation(animal: AnyAnimal):
        if animal.current_power - animal.max_power * 0.3 <= 0:
            forest.remove_animal(animal)
            print(f"{animal.__class__.__name__} died")
        else:
            animal.current_power = round(animal.current_power - animal.max_power * 0.3, 1)
            print(f"{animal.__class__.__name__} has {animal.current_power} power left after failed")


def animal_generator():
    while True:
        new_animal = random.choice((Herbivorous(random.randrange(25, 100, 1), random.randrange(25, 100, 1)),
                                    Predator(random.randrange(25, 100, 1), random.randrange(25, 100, 1))))
        new_animal.id = uuid.uuid4()
        yield new_animal


if __name__ == "__main__":
    step = 0
    forest = Forest()
    nature = animal_generator()
    for i in range(random.randrange(6, 10, 1)):
        animal = next(nature)
        print(animal.__dict__)
        forest.add_animal(animal)
    while True:
        step += 1
        print(f'\n-----------------------------STEP#{step}------------------------------\n')
        for animal in forest:
            print(f'{forest.num}. {animal.__class__.__name__} --> {animal.__dict__}')
        if not forest.any_predator_left():
            break
        random.choice(list(forest.animals.values())).eat(forest)
        time.sleep(1)