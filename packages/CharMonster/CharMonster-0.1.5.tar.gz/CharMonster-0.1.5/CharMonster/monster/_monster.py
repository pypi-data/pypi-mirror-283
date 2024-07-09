from sys import argv
from typing import Type
from entyty import _AbstractEntity as AbstractEntity
import dicepy
import CharActor as ca
from CharActor._charactor.actor._actor.character.attributes import ability
import pymunk

from ..dicts import load_dict

_MONSTERS = load_dict('monsters')

class BaseMonster(AbstractEntity):
    _monster_name:      Type[str] = None
    _level:             Type[int] = None
    _hitpoints:         Type[int] = None
    _hp:                Type[int] = None
    _ability_scores:    Type[dict]= None
    _abilities:         Type[dict]= None
    _Strength:          Type[int] = None
    _Strength_mod:      Type[int] = None
    _Dexterity:         Type[int] = None
    _Dexterity_mod:     Type[int] = None
    _Constitution:      Type[int] = None
    _Constitution_mod:  Type[int] = None
    _Intelligence:      Type[int] = None
    _Intelligence_mod:  Type[int] = None
    _Wisdom:            Type[int] = None
    _Wisdom_mod:        Type[int] = None
    _Charisma:          Type[int] = None
    _Charisma_mod:      Type[int] = None
    _armor_class:       Type[int] = None
    _attack_bonus:      Type[int] = None
    _saving_throws:     Type[dict]= None
    _fortitude:         Type[int] = None
    _reflex:            Type[int] = None
    _will:              Type[int] = None
    _damage:            Type[dict]= None
    _dmg_dice:          Type[int] = None
    _dmg_dice_value:    Type[int] = None
    _initiative:        Type[int] = None
    _speed:             Type[dict]= None
    _size:              Type[str] = None
    _type:              Type[str] = None
    _subtype:           Type[str] = None
    _alignment:         Type[str] = None
    _special_abilities: Type[dict]= None
    _description:       Type[str] = None
    _dice_set:          Type[dicepy.Dice.DiceSet] = None
    _grid:              Type[any] = None
    _grid_entity:       Type[any] = None
    _target:            Type[any] = None
                  
    def __init__(
        self,
        monster_name:       Type[str] = None,
        level:              Type[int] = None,
        hitpoints:          Type[int] = None,
        ability_scores:     Type[dict] = None,
        armor_class:        Type[int] = None,
        attack_bonus:       Type[int] = None,
        saving_throws:      Type[dict] = None,
        damage:             Type[dict] = None,
        initiative:         Type[int] = None,
        speed:              Type[dict] = None,
        size:               Type[str] = None,
        monster_type:       Type[str] = None,
        subtype:            Type[str] = None,
        alignment:          Type[str] = None,
        special_abilities:  Type[dict] = None,
        description:        Type[str] = None,
        *argv, **kwargs
    ):
        self.monster_name = monster_name
        self.level = level
        self.hitpoints = hitpoints
        self._abilities = {}
        self._initial_ability_scores = ability_scores
        self.ability_scores = ability_scores
        self.armor_class = armor_class
        self.attack_bonus = attack_bonus
        self.saving_throws = saving_throws
        self.dice_set = dicepy.Dice.DiceSet()
        self.damage = damage
        self.initiative = initiative
        self.speed = speed
        self.size = size
        self.monster_type = monster_type 
        self.subtype = subtype
        self.alignment = alignment
        self.special_abilities = special_abilities
        self.description = description
        if kwargs.get('grid', None) is not None:
            from entyty import GridEntity
            self._grid = kwargs['grid']
            self.grid_entity = GridEntity(self.grid, self.monster_name, self)
               
    @property
    def monster_name(self):
        return self._monster_name
    
    @monster_name.setter
    def monster_name(self, monster_name):
        self._monster_name = monster_name
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, level):
        self._level = level
    
    @property
    def hitpoints(self):
        return self._hitpoints
    
    @hitpoints.setter
    def hitpoints(self, hitpoints):
        self._hitpoints = hitpoints
        self.hp = hitpoints
        
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, hp):
        self._hp = hp
    
    @property
    def ability_scores(self):
        return self._ability_scores
    
    @ability_scores.setter
    def ability_scores(self, ability_scores):
        self._ability_scores = ability_scores
        if ability_scores is None:
            return
        self._add_abilities()
                
    @property
    def Strength(self):
        return self._Strength
    
    @Strength.setter
    def Strength(self, Strength):
        self._Strength = Strength
       
    @property
    def Dexterity(self):
        return self._Dexterity
    
    @Dexterity.setter
    def Dexterity(self, Dexterity):
        self._Dexterity = Dexterity
        
    @property
    def Constitution(self):
        return self._Constitution
    
    @Constitution.setter
    def Constitution(self, Constitution):
        self._Constitution = Constitution
           
    @property
    def Intelligence(self):
        return self._Intelligence
    
    @Intelligence.setter
    def Intelligence(self, Intelligence):
        self._Intelligence = Intelligence
       
    @property
    def Wisdom(self):
        return self._Wisdom
    
    @Wisdom.setter
    def Wisdom(self, Wisdom):
        self._Wisdom = Wisdom
       
    @property
    def Charisma(self):
        return self._Charisma
    
    @Charisma.setter
    def Charisma(self, Charisma):
        self._Charisma = Charisma
        
    @property
    def armor_class(self):
        return self._armor_class
    
    @armor_class.setter
    def armor_class(self, armor_class):
        self._armor_class = armor_class
    
    @property
    def attack_bonus(self):
        return self._attack_bonus
    
    @attack_bonus.setter
    def attack_bonus(self, attack_bonus):
        self._attack_bonus = attack_bonus
    
    @property
    def saving_throws(self):
        return self._saving_throws
    
    @saving_throws.setter
    def saving_throws(self, saving_throws):
        self._saving_throws = saving_throws
        if saving_throws is None:
            return
        for key, value in saving_throws.items():
            if key == 'fortitude':
                self._fortitude = value
            elif key == 'reflex':
                self._reflex = value
            elif key == 'will':
                self._will = value
                
    @property
    def fortitude(self):
        return self._fortitude
    
    @property
    def reflex(self):
        return self._reflex
    
    @property
    def will(self):
        return self._will
    
    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, damage):
        if damage is None:
            return
        for key, value in damage.items():
            if key == 'number_of_dice':
                self._dmg_dice = value
            elif key == 'dice_value':
                self._dmg_dice_value = value
        die = getattr(self.dice_set, f'd{self._dmg_dice_value}')
        self._damage = (self._dmg_dice, die)
        
    @property
    def dmg_dice(self):
        return self._dmg_dice
    
    @property
    def dmg_dice_value(self):
        return self._dmg_dice_value
    
    @property
    def initiative(self):
        return self._initiative
    
    @initiative.setter
    def initiative(self, initiative):
        self._initiative = initiative
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def monster_type(self):
        return self._monster_type
    
    @monster_type.setter
    def monster_type(self, monster_type):
        self._monster_type = monster_type
    
    @property
    def subtype(self):
        return self._subtype
    
    @subtype.setter
    def subtype(self, subtype):
        self._subtype = subtype
    
    @property
    def alignment(self):
        return self._alignment
    
    @alignment.setter
    def alignment(self, alignment):
        self._alignment = alignment
    
    @property
    def special_abilities(self):
        return self._special_abilities
    
    @special_abilities.setter
    def special_abilities(self, special_abilities):
        self._special_abilities = special_abilities
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description
        
    @property
    def dice_set(self):
        return self._dice_set
    
    @dice_set.setter
    def dice_set(self, dice_set):
        self._dice_set = dice_set
        
    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        self._grid = grid
        
    @property
    def grid_entity(self):
        return self._grid_entity
    
    @grid_entity.setter
    def grid_entity(self, grid_entity):
        self._grid_entity = grid_entity
        self._create_properties()

    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, target):
        self._target = target
        
class Monster(BaseMonster):
    def __init__(self, entry_number: Type[int] = None, **kwargs):
        if entry_number is not None:
            monster_data = Monster.load_monster(entry_number)
            if kwargs.get('grid', None) is not None:
                monster_data['grid'] = kwargs['grid']
            super().__init__(**monster_data)
        else:
            super().__init__(**kwargs)

    def _create_properties(self):
        properties = {
            'cell': self.grid_entity.cell,
            'cell_name': self.grid_entity.cell_name,
            'cell_history': self.grid_entity.cell_history,
            'last_cell': self.grid_entity.last_cell,
            'x': self.grid_entity.x,
            'y': self.grid_entity.y,
            'position': pymunk.Vec2d(self.grid_entity.position[0], self.grid_entity.position[1]),
            'path': self.grid_entity.path
        }

        def make_getter(attr):
            if attr == 'position':
                return lambda self: pymunk.Vec2d(getattr(self.grid_entity, attr))
            else:
                return lambda self: getattr(self.grid_entity, attr)

        for attr, value in properties.items():
            setattr(Monster, attr, property(make_getter(attr)))

    def _add_abilities(self):
        for ability_name, info in ability.ABILITIES.items():
            ability_class = ability.AbilityFactory.create_ability(self, ability_name)
            if ability_class is not None:
                ability_instance = ability_class
                self._abilities[ability_name] = ability_instance
                setattr(self, ability_name, ability_instance)

    @staticmethod
    def load_monster(entry_number: Type[int] = None):
        return _MONSTERS[str(entry_number)]
    
    def move(self, direction: str = None, cell: object | str = None):
        FROM = self.cell.designation
        if cell is not None:
            if isinstance(cell, str):
                cell = self.grid[cell]    
            self.grid_entity.move(cell, teleport = True)
            return
        if direction is not None and direction in {
            'north_west',
            'north',
            'north_east',
            'east',
            'south_east',
            'south',
            'south_west',
            'west',
        }:
            return self._extracted_from_move_18(direction, FROM)

    def _extracted_from_move_18(self, direction, FROM):
        move = self.grid_entity.move_in_direction(direction)
        TO = self.cell.designation
        if not move:
            return move
        return f'{FROM} --> {TO}'

    def set_target(self, target: object):
        self.target = target
    
    def _attack_figure(self):
        if self.target is None:
            return 'No target.'
        attack_roll = self.dice_set.d20.roll()
        if attack_roll == 20:
            damage = sum(self.damage[1].roll() for _ in range(self.damage[0]))
            damage += self.Strength.modifier
            damage *= 2
            self.target.hp -= damage
            return f'Critical hit! {damage} damage dealt.'
        elif attack_roll == 1:
            return 'Critical miss!'
        elif attack_roll + self.Strength.modifier >= self.target.armor_class:
            damage = sum(self.damage[1].roll() for _ in range(self.damage[0]))
            damage += self.Strength.modifier
            self.target.hp -= damage
            return f'{damage} damage dealt.'
        else:
            return 'Miss!'
