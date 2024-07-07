from __future__ import annotations

import random
import re
from random import randint as _randint
from typing import Optional as _Optional, Any

from entyty import _AbstractEntity as AbstractEntity

import getch
import pymunk
from pymunk import Vec2d

from dicepy import Roll as _Roll
from dicepy import Die as _Die
from .character import *
from CharObj import Armory, Goods, Weapon, Armor, ItemStack
from CharActor._charactor.dicts import load_dict

from CharActor import log

_ability_rolls = _Roll.ability_rolls

_LEVELS = load_dict('levels')

d20 = _Die.d20()
CARDINAL_DIRECTIONS = {
        "East":  list(range(337, 360)) + list(range(23)) + [0],
        "North-East": range(22, 68),
        "North":  range(67, 113),
        "North-West": range(112, 158),
        "West":  range(157, 203),
        "South-West": range(202, 248),
        "South":  range(247, 293),
        "South-East": range(292, 338)
}

def get_direction(pointa: tuple[int, int] | type(Vec2d), pointb: tuple[int, int] | type(Vec2d)):
    if isinstance(pointa, tuple):
        pointa = Vec2d(*pointa)
    if isinstance(pointb, tuple):
        pointb = Vec2d(*pointb)
    angle_degrees = (pointb - pointa).angle_degrees
    angle_degrees = round(angle_degrees)
    angle_degrees %= 360

    return [direction for direction, angle_range in CARDINAL_DIRECTIONS.items() if angle_degrees in angle_range][0]




class BaseActor(AbstractEntity):
    """
    Base class for characters. Inherits from AbstractEntity.

    Attributes:
        _actor_type (str): The type of actor.
        name (str): The name of the actor.
        _age (int): The age of the actor.
        level (int): The level of the actor.
        _initial_ability_scores (dict): The initial ability scores of the actor.
        _role (Role): The role of the actor.
        _race (Race): The race of the actor.
        _background (Background): The background of the actor.
        _alignment (Alignment): The alignment of the actor.
        _abilities (dict): The abilities of the actor.
        _skills (dict): The skills of the actor.
        _experience (int): The experience points of the actor.
        saving_throws (dict): The saving throws of the actor.
        initiative (int): The initiative of the actor.
        skillbook (Skillbook): The skillbook of the actor.
        skill_points (int): The available skill points of the actor.
        armor_class (int): The armor class of the actor.
        inventory (Inventory): The inventory of the actor.
        _traveling (bool): Indicates if the actor is traveling.
        _labels (list): The labels associated with the actor.

    Methods:
        __init__: Initializes the BaseActor instance.
        character_sheet: Returns the character sheet of the actor.
        age: Gets or sets the age of the actor.
        speed: Calculates and returns the speed of the actor.
        experience: Gets or sets the experience points of the actor.
        _on_turn_change: Handles the event when the turn changes for the actor.
        _initialize: Initializes the attributes of the actor.
        _spend_skill_points: Allows the actor to spend skill points to increase skills.
        _build_labels: Builds the labels associated with the actor.
        _set_age: Sets the age of the actor.
        _init_ability_scores: Initializes the ability scores of the actor.
        _add_abilities: Adds the abilities to the actor.
        _determine_saves_and_initiative: Determines the saving throws and initiative of the actor.
        _add_role: Adds the role to the actor.
        _init_hp: Initializes the hit points of the actor.
        _init_skill_points: Initializes the skill points of the actor.
        _add_skills: Adds the skills to the actor.
        _add_race: Adds the race to the actor.
        _add_background: Adds the background to the actor.
        _add_alignment: Adds the alignment to the actor.
        _init_inventory: Initializes the inventory of the actor.
        _add_and_equip_piece: Adds and equips a piece of equipment to the actor.
        _determine_armor_class: Determines the armor class of the actor.
        _on_skill_up: Handles the event when a skill is leveled up.
        _give_xp: Gives experience points to the actor.
        _level_up: Levels up the actor.
        __repr__: Returns a string representation of the actor.
    """
    log('Initializing BaseActor class.')
    AbstractEntity.dispatcher.register_event_type('on_level_up')

    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            race: _Optional[str] = None,
            background: _Optional[str] = None,
            alignment: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs

    ):
        """
        :param actor_type: The type of actor. This is used to determine the type of actor to create.
        :param name: The name of the actor.
        :param role: The role of the actor.
        :param race: The race of the actor.
        :param background: The background of the actor.
        :param alignment: The alignment of the actor.
        :param age: The age of the actor.
        """
        super(BaseActor, self).__init__()
        self._actor_type = actor_type if actor_type is not None else "Base"
        self.name = name if name is not None else "Unnamed"
        self._age = None
        self.level = 1
        self._initial_ability_scores = {}
        self._role = None
        self._race = None
        self._background = None
        self._alignment = None
        self._abilities = {}
        self._skills = {}
        self._experience = 0
        self.saving_throws = {}
        self.initiative = 0
        self.skillbook = Skillbook(self)
        self.skill_points = 0
        self.armor_class = 0
        self.inventory = None
        self.vision = 200
        self._traveling = False
        self._initialize(role, race, background, alignment, age)
        self._is_turn = False

    @property
    def character_sheet(self):
        def of_equipment():
            for piece in self.inventory.equipment._slots.values():
                if piece is not None and not isinstance(piece, Weapon):
                    yield piece

        def of_items():
            for item in self.inventory.items:
                if item is not None and not (isinstance(item, (Weapon, Armor))):
                    yield item

        def tab(tabs=1):
            return '\t'*tabs
        count_of_equipment = of_equipment()
        equipment_count = 0
        for piece in count_of_equipment:
            equipment_count += 1
        count_of_items = of_items()
        item_count = 0
        for item in count_of_items:
            item_count += 1
        items = of_items()
        piece_of_equipment = of_equipment()
        return f"""A level {self.level} {self._alignment} {self._race.title} {self._role.title} {self._background.title} named {self.name}
    
{self.Strength}\tInitiative: {self.initiative}\t\tEquipment:
{self.Dexterity}\tHP: {self.hp}\t\t\t{next(piece_of_equipment) if equipment_count > 0 else ''}\t\t{next(piece_of_equipment) if equipment_count > 1 else ''}\t{next(piece_of_equipment) if equipment_count > 2 else '' }\t\t{next(piece_of_equipment) if equipment_count > 3 else ''}
{self.Constitution}\tAC: {self.armor_class}\t\t\t{next(piece_of_equipment) if equipment_count > 4 else ''}\t\t{next(piece_of_equipment) if equipment_count > 5 else ''}\t{next(piece_of_equipment) if equipment_count > 6 else ''}\t\t{next(piece_of_equipment) if equipment_count > 7 else ''}
{self.Intelligence}\t\t\t\t{next(piece_of_equipment) if equipment_count > 8 else ''}\t\t{next(piece_of_equipment) if equipment_count > 9 else ''}\t{next(piece_of_equipment) if equipment_count > 10 else ''}\t\t{next(piece_of_equipment) if equipment_count > 11 else ''}
{self.Wisdom}\t{'CELL:' if self._grid_entity is not None else tab()} {self.cell_name if self._grid_entity is not None else tab()}\tMain Hand:
{self.Charisma}\t\t\t\t{self.inventory.equipment._slots['MAIN_HAND'] if self.inventory.equipment._slots['MAIN_HAND'] is not None else 'None'}
    
{'Items:' if item_count > 0 else ''}\t\t\t\t{self.inventory.equipment._slots['OFF_HAND'] if self.inventory.equipment._slots['OFF_HAND'] is not None else ''}
{next(items) if item_count > 0 else ''}\t{next(items) if item_count > 1 else ''}\t{next(items) if item_count > 2 else ''}\t{next(items) if item_count > 3 else ''}
{next(items) if item_count > 4 else ''}\t{next(items) if item_count > 5 else ''}\t{next(items) if item_count > 6 else ''}\t{next(items) if item_count > 7 else ''}
    """

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age: _Optional[int] = None):
        if age is not None and self._race.age['maturity'] <= age <= self._race.age['maximum']:
            self._age = age
        elif age is None:
            self._age = _randint(self._race.age['maturity'], self._race.age['maximum'])
        else:
            raise ValueError("Age is outside the acceptable range")

    @property
    def speed(self):
        return 10 + (5*self.Dexterity.modifier) if self.Dexterity.modifier >= 2 else 20

    @property
    def experience(self) -> int:
        return self._experience

    @experience.setter
    def experience(self, experience: int = None):
        if experience is not None:
            self._experience = experience
            if experience >= _LEVELS[str(self.level)]['experience_threshold']:
                self._level_up()

    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        self._grid = grid

    def _on_turn_change(self, actor):
        self._is_turn = self is actor

    def _initialize(self, role: str , race: str, background: str, alignment: str, age: int):
        log('Initializing BaseActor instance.')
        self._add_role(role)
        self._add_race(race)
        self._add_alignment(alignment)
        if background is not None or background != 'custom':
            self._add_background(background)
        self._init_ability_scores()
        self._add_abilities()
        self._add_skills()
        self._init_skill_points()
        self._init_hp()
        self._determine_saves_and_initiative()
        self._set_age(age)
        self._init_inventory()
        self._determine_armor_class()
        if self._actor_type != 'Player':
            self._spend_skill_points()
        else:
            for _ in range(self.skill_points):
                skill = random.choice(list(SKILLS.keys()))
                getattr(self.skillbook, f'{skill.title().replace(" ", "_")}').level += 1
                self.skill_points -= 1

    #        self._build_labels()

    # ... (other parts of your class)

    def __getstate__(self):
        state = self.__dict__.copy()
        for k, v in state.copy().items():
            if k in ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
                     'Warlock', 'Wizard']:
                del state[k]
            if k in ['Human', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Half-Orc', 'Halfling', 'Tiefling']:
                del state[k]
            if k in ['LawfulGood', 'Lawful', 'LawfulEvil', 'Good', 'TrueNeutral', 'Evil',
                     'ChaoticGood', 'Chaotic', 'ChaoticEvil', 'Unaligned']:
                del state[k]
            if k in ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'FolkHero', 'GuildArtisan', 'Hermit',
                     'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin']:
                del state[k]
            if k in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
                del state[k]
            if k in ['_skills', 'inventory', 'skillbook']:
                del state[k]
            if k in ['_role', '_race', '_background', '_alignment']:
                state[k] = v.title
        return state
            
    def __setstate__(self, state):
        self._add_race(state['_race'])
        self._add_role(state['_role'])
        self._add_alignment(state['_alignment'])
        self._add_background(state['_background'])
        self._add_abilities()
        return state
    
    def _spend_skill_points(self):
        log('Spending skill points.')
        while self.skill_points > 0:
            print(f'You have {self.skill_points} skill points available.')
            print('Which skill would you like to increase?')

            # Create a list of skills for menu navigation
            skills_list = list(SKILLS.keys())
            skills_attrs = [skill.title().replace(" ", "_") for skill in skills_list]

            # Initialize cursor position
            cursor_position = 0
            skill_ups = []
            # Display the skills menu
            while True:
                for idx, skill_name in enumerate(skills_list):
                    cursor_indicator = " <--" if idx == cursor_position else ""
                    attr_name = skill_name.title().replace(" ", "_")
                    print(f'{skill_name} ({getattr(self.skillbook, f"{attr_name}").level}){cursor_indicator}')

                # Display add/subtract buttons and selected skill's level
                print("Add (+)")
                print(
                    f"Selected skill: {skills_list[cursor_position]} ("
                    f"{getattr(self.skillbook, f'{skills_attrs[cursor_position]}').level})"
                    )

                # Read key press for navigation
                key = getch.getch()  # For Linux/macOS

                if key == '+':
                    # Increase the skill level if there are available points
                    if self.skill_points > 0:
                        selected_skill = skills_list[cursor_position]
                        getattr(self.skillbook, f'{skills_attrs[cursor_position]}').level += 1
                        if f'{skills_list[cursor_position]}' not in skill_ups:
                            skill_ups.append(f'{skills_list[cursor_position]}')
                        else:
                            skill_ups.remove(f'{skills_list[cursor_position]}')
                            skill_ups.append(f'{skills_list[cursor_position]} +2')
                        self.skill_points -= 1
                elif key == 'w':  # Up arrow (Escape sequence for arrow up)
                    cursor_position = max(0, cursor_position - 1)
                elif key == 's':  # Down arrow (Escape sequence for arrow down)
                    cursor_position = min(len(skills_list) - 1, cursor_position + 1)
                elif key == '\n':  # Enter key
                    # Exit the loop
                    break
                else:
                    print('Invalid input.')

                # Clear the console for better display
                import os
                os.system('clear')

            print(
                f'{skills_list[cursor_position]} increased to '
                f'{getattr(self.skillbook, f"{skills_attrs[cursor_position]}").level}'
                )
        log(f'Skills increased: {skill_ups}')

    def _set_age(self, age: _Optional[int] = None):
        if age is not None and self._race.age['maturity'] <= age <= self._race.age['maximum']:
            log('Provided age value is appropriate for race.')
            setattr(self, 'age', age)
        elif age is None:
            log('No age provided. Rolling for age.')
            setattr(self, 'age', _randint(self._race.age['maturity'], self._race.age['maximum']))
        else:
            raise ValueError("Age is outside the acceptable range")
        log(f'Age set to {self.age}')

    def _init_ability_scores(self):
        initabilityscores = _ability_rolls()
        log(f'Ability scores rolled: {initabilityscores}')
        for ability_name, info in ABILITIES.items():
            if self._role.title in info["Primary"]:
                self._initial_ability_scores[ability_name] = initabilityscores[0]
                initabilityscores.pop(0)
            else:
                self._initial_ability_scores[ability_name] = initabilityscores[-1]
                initabilityscores.pop(-1)

    def _add_abilities(self):
        for ability_name, info in ABILITIES.items():
            ability_class = AbilityFactory.create_ability(self, ability_name)
            if ability_class is not None:
                ability_instance = ability_class
                self._abilities[ability_name] = ability_instance
                setattr(self, ability_name, ability_instance)
        log(f'Abilities set to {self._abilities}')

    def _determine_saves_and_initiative(self):
        log('Determining saving throws and initiative.')
        for save, info in SAVING_THROWS.items():
            ability = info['ability']
            self.saving_throws[save] = self._abilities[ability].modifier
            log(f'{save} save bonus set to {self.saving_throws[save]}')
        self.initiative = self._abilities["Dexterity"].modifier
        log(f'Initiative set to {self.initiative}')

    def _add_role(self, role):
        role_class = RoleFactory.create_role(role)
        if role_class is not None:
            role_instance = role_class(role)
            self._role = role_instance
            self._role._add_special_ability()
            setattr(self, role_instance.title, role_instance)
        log(f'Role set to {self._role.title}')

    def _init_hp(self):
        self.hp = self._role._hit_die.value + self._abilities["Constitution"].modifier
        log(f'Initial health points set to {self.hp}')

    def _init_skill_points(self):
        self.skill_points = self._role.skill_points + self._abilities["Intelligence"].modifier
        log(f'Available skill points set to {self.skill_points}')

    def _add_skills(self):
        log('Adding skills.')
        for skill_name, info in SKILLS.items():
            skill_class = SkillFactory.create_skill(self, skill_name)
            if skill_class is not None:
                skill_instance = skill_class
                self._skills[skill_name] = skill_instance
                attr_name = skill_name.title().replace(" ", "_")
                setattr(self.skillbook, attr_name, skill_instance)
                self.skillbook.update({attr_name: skill_instance})

    def _add_race(self, race):
        race_class = RaceFactory.create_race(race)
        if race_class is not None:
            log(f'Adding race: {race}')
            race_instance = race_class(race)
            self._race = race_instance
            setattr(self, race_instance.title.replace("-", "_"), race_instance)
        log(f'Set race to {self._race.title}')

    def _add_background(self, bckgrnd: str):
        background_instance = BackgroundFactory.background_instances[bckgrnd]
        if background_instance is not None:
            self._background = background_instance
            setattr(self, background_instance.title.replace(" ", ""), background_instance)
            log(f'Set background to {self._background.title}')
            return
        return None
    
    def _add_alignment(self, algnmnt: str):
        alignment_inst = AlignmentFactory.create_alignment(algnmnt)
        if alignment_inst is not None:
            log(f'Adding alignment: {algnmnt}')
            self._alignment = alignment_inst
            if not alignment_inst.title.startswith('True'):
                setattr(self, alignment_inst.title.replace(" ", "").replace('Neutral', ''), alignment_inst)
                return
            setattr(self, alignment_inst.title.replace(" ", ""), alignment_inst)

    def _init_inventory(self):
        log('Initializing inventory.')
        setattr(self, 'inventory', Inventory(self))
        log(f'Adding starting equipment: {self._role._starting_equipment}')
        for item in self._role._starting_equipment + self._background.equipment:
            if isinstance(item, list):
                if item == []:
                    continue
                elif len(item) > 1 and (item[1] in Armory or item[1] in Goods):
                    log(f'Adding {item[0]} {item[1]}')
                    for _ in range(item[0]):
                        self.inventory.add_item(item[1])
                elif not isinstance(item[0], int) and (item[0] in Armory or item[0] in Goods):
                    self.inventory.add_item(item[0])
            elif item in ['Leather Armor', 'Light Leather', 'Scale Mail', 'Chain Mail', 'Plate Mail', 'Tunic']:
                log(f'Building armor set: {item} ')
                for name, piece in Armory._dict.items():
                    set_name = piece.get('set_name')
                    if set_name == item:
                        piece_ = Armory[name]
                        log(f'{piece_.name} found in Armory')
                        self._add_and_equip_piece(piece_)
                        if isinstance(piece_.slot, list):
                            log(f'Adding additional {piece_.name}')
                            piece_ = Armory[name]
                            self._add_and_equip_piece(piece_)
            elif item in Armory:
                log(f'Found {item} in Armory')
                self._add_and_equip_piece(Armory[item])
            elif item in Goods:
                log(f'Found {item} in Goods')
                self.inventory.add_item(item)
            else:
                log(f'Could not find {item} in Armory or Goods')

    # TODO Rename this here and in `_init_inventory`
    def _add_and_equip_piece(self, piece):
        self.inventory.add_item(piece.name)
        self.inventory.equip_item(self.inventory.items[-1])
        log(f'{piece.name} equipped')

    def _determine_armor_class(self):
        ac = self.Dexterity.modifier
        for slot, item in self.inventory.equipment._slots.items():
            if item is not None and item.category == 'ARMOR':
                ac += item.armor_class
        self.armor_class = ac

    def _on_skill_up(self, skill):
        if self.skill_points > 0:
            self.skill_points -= 1
            skill.level += 1

    def _give_xp(self, amount: int = None):
        if amount is not None:
            self.experience += amount

    def _level_up(self):
        self.level += 1

    def __repr__(self):
    #     # return f'A level {self.level}, {self._race.title} {self._role.title} named {self.name}\nLocation: Cell -> {
    #     # self._cell_name}@{self._position}\n\n{self.Strength}\tInitiative: {self.initiative}\n{self.Dexterity}\tHP:
    #     # {self.hp}\n{self.Constitution}\tAC: {self.armor_class}\n{self.Intelligence}\n{self.Wisdom}\n{
    #     # self.Charisma}\n\n'
        return f'{self._race.title}'

    # def _draw(self):
    #     self._shape.draw()
    #     [label.draw() for label in self._labels]

    # def _update(self):
    #     #super()._update()
    #     #self.cell = self._cell
    #     if self.path:
    #         self.move_in_path()
    #     self._reflect()
    #     [label.update() for label in self._labels]

    # @property
    # def role(self):
    #     return self._role

    # @role.setter
    # def role(self, role_name):
    #     role_class = _RoleFactory.create_role(role_name)
    #     if role_class is not None:
    #         self._role = role_class(role_name)
    #         self._role._add_special_ability()



class BaseCharacter(BaseActor):
    """
    The BaseCharacter class essentially serves as a wrapper for the GridEntity class. It inherits from BaseActor.
    The BaseCharacter class is used to create characters that can be placed on a grid. Although, they can be used
    without a grid as well. The characters created as instances of this class can be controlled by the user or
    controlled by the computer.
    
    Attributes:
        name (str): The name of the character.
        _background (Background): The background of the character.
        _alignment (Alignment): The alignment of the character.
        _grid (Grid): The grid the character is on.
        _grid_entity (GridEntity): The grid entity associated with the character.
        _actions (dict): The actions available to the character.
        _is_turn (bool): Indicates if it is the character's turn.
        _nearby_items (dict): The nearby items visible to the character.
        _target (BaseActor): The target of the character.

    Methods:
        __init__: Initializes the BaseCharacter instance.
        _create_properties: Creates the properties associated with the character.
        end_turn: Ends the character's turn.
        _join_grid: Joins the character to a grid.
        saving_throw: Performs a saving throw for the character.
        _set_target: Sets the target of the character.
        move: Moves the character in a specified direction.
        attack: Performs an attack action for the character.
        pickup: Picks up an item for the character.
        drop: Drops an item for the character.
        _get_distance: Calculates the distance between the character and another actor.
        _is_in_pickup_range: Checks if another actor is within pickup range of the character.
        _is_in_sight: Checks if another actor is within sight range of the character.
        _see_item: Checks if an item is visible to the character.
        look_around: Looks around the character's surroundings.
    """
    log('Initializing BaseCharacter class.')
    AbstractEntity.dispatcher.register_event_type('on_turn_end')
    dispatcher = AbstractEntity.dispatcher
    def __init__(self, name, background: str, alignment: str, grid=None):
        from entyty import GridEntity
        character_class = self.__class__.__name__
        class_list = re.findall('[A-Z][^A-Z]*', character_class)
        if 'Half' in class_list:
            class_list[0] = f'Half-{class_list[1]}'
            class_list.remove(f'{class_list[1]}')
        character_race = class_list[0]
        character_role = class_list[1]
        super().__init__('Player', name, role=character_role, race=character_race, background=background, alignment=alignment)
        if grid is None:
            self._grid = None
            self._grid_entity = None
        else:
            self._grid = grid
            self._grid_entity = GridEntity(grid=grid, name=self.name.upper(), parent=self)
            self._grid_entity.speed = self.speed
            self._create_properties()
        self._actions = {'move':   {i: {'direction': None, 'from': None, 'distance': None, 'to': None} for i in range(self.speed//5)},
                         'attack': {'target': None, 'weapon': None, 'result': None}, 'free': [], 'quick': []}
        self._action_history = []
        self._is_turn = False
        self._nearby_items = {}
        self._nearby_units = {}
        self._nearby_other = {}
        self._target = None
        
    def __json__(self):
        _dict = {}
        for key, value in self.__dict__.copy().items():
            if hasattr(value, '__json__'):
                _dict[key] = value.__json__()
            elif key in [
                'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'Barbarian', 'Bard', 'Cleric', 
                'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard', 'Human', 'Dwarf', 
                'Elf', 'Gnome', 'Half-Elf', 'Half-Orc', 'Halfling', 'Tiefling', 'LawfulGood', 'Lawful', 'LawfulEvil', 'Good', 
                'TrueNeutral', 'Evil', 'ChaoticGood', 'Chaotic', 'ChaoticEvil', 'Unaligned', 'Acolyte', 'Charlatan', 
                'Criminal', 'Entertainer', 'FolkHero', 'GuildArtisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 
                'Soldier', 'Urchin', '_skills', 'inventory', 'skillbook', '_abilities', '_grid', '_grid_entity', '_actions', 
                '_action_history', '_nearby_items', '_nearby_units', '_nearby_other', '_target'
            ]:
                continue
            else:
                _dict[key] = value
        return _dict        

    def _create_properties(self):
        """Called when the character is added to a grid. Creates the relevant properties and makes them accessible to
        the character. Adds the following properties:
        
        grid: The grid the character is on.
        grid_entity: The grid entity associated with the character.
        movements: The movements available to the character.
        movements_remaining: The movements remaining for the character.
        movement_queue: The movement queue for the character.
        cell: The cell the character is in.
        cell_name: The name of the cell the character is in.
        cell_history: The history of the cells the character has been in.
        last_cell: The last cell the character was in.
        x: The x coordinate of the character.
        y: The y coordinate of the character.
        position: The position of the character.
        path: The path the character is following.
        """
        if self._grid_entity is not None:
            setattr(self.__class__, 'grid', property(lambda self: self._grid))
            setattr(self, 'grid', self._grid)
            setattr(self.__class__, 'grid_entity', property(lambda self: self._grid_entity))
            setattr(self, 'grid_entity', self._grid_entity)
            properties = {
                'movements': self.grid_entity.movements,
                'movement_queue': self.grid_entity.movement_queue,
                'movement_energy': self.grid_entity.movement_energy,
                'cell': self.grid_entity.cell,
                'cell_name': self.grid_entity.cell_name,
                'cell_history': self.grid_entity.cell_history,
                'last_cell': self.grid_entity.last_cell,
                'x': self.grid_entity.x,
                'y': self.grid_entity.y,
                'position': pymunk.Vec2d(self.grid_entity.position[0], self.grid_entity.position[1]),
                'path': self.grid_entity.path
            }
            for attr, value in properties.items():
                setattr(self, attr, value)
                setattr(self.__class__, attr, property(lambda self, attr=attr: getattr(self.grid_entity, attr)))
            self._push_handlers(on_turn_end=self.grid_entity.end_turn)
        else:
            for attr in ['movements', 'movement_queue', 'movement_energy', 'cell', 'cell_name', 'cell_history', 'last_cell', 'x', 'y', 'position', 'path']:
                delattr(self, attr)
                
    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        self._grid = grid

    @property
    def actions(self) -> dict[str, dict[str, Any]]:
        return self._actions

    @actions.setter
    def actions(self, actions: _Optional[dict[str, dict[str, Any]]] = None):
        if actions is None:
            if hasattr(self, 'grid_entity') and self.grid_entity is not None:
                actions = {
                    'move': self.grid_entity.actions['move'], 
                    'attack': {'target': None, 'weapon': None, 'result': None}, 
                    'free': [], 'quick': []
                    }
                self._actions = actions
                return
            actions = {'move': {},
                       'attack': {'target': None, 'weapon': None, 'result': None}, 
                       'free': [], 
                       'quick': []}
            self._actions = actions
            return
        self._actions = actions

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._set_target(target)

    def _on_turn_change(self, actor):
        super()._on_turn_change(actor)
        if self is actor:
            self._is_turn = False
        else:
            self.actions = None
            self._is_turn = True

    def end_turn(self):
        self._action_history.append(self.actions)
        if hasattr(self, 'grid_entity'):
            self.grid_entity.end_turn()
        self.actions = None

    def _join_grid(self, grid):
        from entyty import GridEntity
        self._grid = grid
        self._grid_entity = GridEntity(grid=grid, name=self.name.upper(), parent=self)
        self._create_properties()

    def reflex_save(self, dc):
        self.Dexterity.reflex_save(dc)
        
    def fortitude_save(self, dc):
        self.Constitution.fortitude_save(dc)
        
    def will_save(self, dc):
        self.Wisdom.will_save(dc)
        
    def _set_target(self, target):
        self._target = target

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

    # TODO Rename this here and in `move`
    def _extracted_from_move_18(self, direction, FROM):
        move = self.grid_entity.move_in_direction(direction)
        TO = self.cell.designation
        if not move:
            return move
        self.actions['move'] = self.grid_entity.actions['move']
        self._update_nearby()
        return f'{FROM} --> {TO}'
            
    def attack(self):
        # if self.actions['attack'] != {'target': None, 'weapon': None, 'result': None}:
        #     return 'You have already attacked this turn.'
        if self._target is None:
            return 'No target.'
        elif hasattr(self, 'grid') and self.grid is not None and self.grid.get_distance(self.cell_name, self._target.cell_name) > self.inventory.equipment['MAIN_HAND'].weapon_range[0]:
            return 'Target out of range.'
        else:
            log(f'{self.name} and {self.target.name} do not inhabit a grid, so attack is emulated. Combatants are assumed to be within range of each other.')
        result = self._attack_figure()
        print(result)
        self.actions['attack'] = {'target': self._target, 'weapon': self.inventory.equipment['MAIN_HAND'],
                                  'result': result}

    def _attack_figure(self):
        attack_roll = d20.roll()
        if attack_roll == 20:
            damage = sum(
                self.inventory.equipment['MAIN_HAND'].damage[1].roll()
                for _ in range(self.inventory.equipment['MAIN_HAND'].damage[0])
            )
            damage += self.Strength.modifier
            damage *= 2
            self._target.hp -= damage
            return f'Critical hit! {damage} damage dealt.'
        elif attack_roll == 1:
            return 'Critical miss!'
        elif attack_roll + self.Strength.modifier >= self._target.armor_class:
            damage = sum(
                self.inventory.equipment['MAIN_HAND'].damage[1].roll()
                for _ in range(self.inventory.equipment['MAIN_HAND'].damage[0])
            )
            damage += self.Strength.modifier
            self._target.hp -= damage
            return f'{damage} damage dealt.'
        else:
            return 'Miss!'

    def pickup(self, item):
        if self._grid_entity is None:
            self.inventory.pick_up(item)

        elif self._is_turn and self._nearby_items != {}:
            for item in self._nearby_items.values():
                self.inventory.pick_up(item)
                
    def drop(self, item):
        if self._is_turn and item.name in self.inventory:
            self.inventory.drop_item(item.name)

    def _get_distance(self, other):
        return self.grid.get_distance(self.cell_name, other.cell_name, 'units')

    def _is_in_pickup_range(self, other):
        return self._get_distance(other) <= 1

    def _is_in_sight(self, other):
        return self._get_distance(other) <= 20
    
    def _is_in_view(self, other):
        return self._get_distance(other) <= 40

    def _see_item(self, item, direction):
        CARDINAL_DIRECTIONS = ['East', 'North-East', 'North', 'North-West', 'West', 'South-West', 'South', 'South-East']
        direction = direction.split() if len(direction) > 1 else [direction]
        for d in range(len(direction)):
            if direction[d] == 'S':
                direction[d] = 'South'
            elif direction[d] == 'N':
                direction[d] = 'North'
            elif direction[d] == 'E':
                direction[d] = 'East'
            elif direction[d] == 'W':
                direction[d] = 'West'
        direction = '-'.join(direction) if len(direction) > 1 else direction[0]
        dindx = CARDINAL_DIRECTIONS.index(direction)
        Dist = self.grid.get_distance(self.cell_name, item.cell_name, 'cells')
        if not self._is_in_pickup_range(item):
            return f'You see {repr(item)} to the {direction}'
        self._nearby_items[item.name] = item
        From = (dindx + 4) % 8
        view = item.__view__((From, Dist))
        return f'You see {view} at your feet.'



    def _update_nearby(self):
        vision = self.vision//5
        nearby_items = {}
        nearby_units = {}
        for cell in self.grid.get_area(self.cell_name, vision):
            if cell.entry_object['items'] is not None:
                nearby_items |= cell.entry_object['items']
            if cell.entry_unit['players'] is not None:
                nearby_units |= cell.entry_unit['players']
        self._nearby_items = nearby_items
        self._nearby_units = nearby_units

    def look_around(self):
        self._update_nearby()

        directions = {
            self.grid.get_direction(self.cell, item.cell)
            for name, item in self._nearby_items.items()
        }

        if len(self._nearby_items) > 8:
            return 'There are several objects scattered around you,'
        elif len(self._nearby_items) <= 7:
            return {self._see_item(item, direction) for item, direction in zip(self._nearby_items.values(), directions)}

    def look_to(self, direction):
        self._update_nearby()
        items_in_direction = []
        units_in_direction = []
        for item in self._nearby_items.values():
            d = self.grid.get_direction(self.cell, item.cell)
            if '-' in direction:
                ds = direction.split('-')
                ds.append(direction)
                if d in ds:
                    items_in_direction.append(item)
            elif d.startswith(direction) or d.endswith(direction):
                items_in_direction.append(item)
        for unit in self._nearby_units.values():
            d = self.grid.get_direction(self.cell, unit.cell)
            if '-' in direction:
                ds = direction.split('-')
                ds.append(direction)
                if d in ds:
                    units_in_direction.append(unit)
        in_direction = items_in_direction + units_in_direction
        for att in in_direction:
            self._see_item(att, direction)
                    
                
        # for item in self.grid.armory._grid_instances.values():
        #     item_count += 1 if self._is_in_sight(item) else 0
        # for item in self.grid.goods._grid_instances.values():
        #     item_
        #     self._see_item(item)
