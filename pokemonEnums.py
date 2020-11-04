from enum import Enum
from enum import IntEnum


# Enum used to represent pokemon types
class PokemonType(IntEnum):
    Normal = 1
    Fighting = 2
    Flying = 3
    Poison = 4
    Ground = 5
    Rock = 6
    Bug = 7
    Ghost = 8
    Fire = 10
    Water = 11
    Grass = 12
    Electric = 13
    Psychic = 14
    Ice = 15
    Dragon = 16
    Error = 17


# Enum used to represent the category of a pokemon's move
class MoveCategory(Enum):
    Status = 1
    Physical = 2
    Special = 3
    Error = 4


# Enum used to represent the status effect on a pokemon
class PokemonStatusEffect(Enum):
    Error = 0
    Freeze = 1
    Paralysis = 2
    Poison = 3
    BadlyPoisoned = 4
    Sleep = 5
    Bound = 6
    CannotEscape = 7
    Confusion = 8
    Curse = 9
    Embargo = 10
    HealBlock = 11
    Identified = 12
    Infatuation = 13
    Leeched = 14
    Nightmare = 15
    PerishSong = 16
    Taunt = 17
    Telekinesis = 18
    Torment = 19
    AquaRing = 20
    Bracing = 21
    ChargingTurn = 22
    CenterOfAttention = 23
    DefenseCurl = 24
    Rooting = 25
    MagneticLevitation = 26
    Minimize = 27
    Protection = 28
    Recharging = 29
    SemiInvulnerable = 30
    Substitute = 31
    TakingAim = 32
    Withdrawing = 33
    Burn = 34


# Stat modifier map
# part of the attack/defense statistic multiplier system
statModifier = {0: 1, 1: 1.5, 2: 2, 3: 2.5, 4: 3, 5: 3.5, 6: 4, -1: 0.66, -2: 0.5, -3: 0.4, -4: 0.33, -5: 0.28,
                -6: 0.25}

# Pokemon type Effectiveness dictionary for Gen1
# Currently only setup to work through gen 1
# other generations not implemented
# Key is attacking pokemon, Value is defending pokemon
typeEffectiveness = {
    PokemonType.Normal: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                         PokemonType.Grass: 1, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                         PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 1,
                         PokemonType.Rock: 0.5, PokemonType.Ghost: 0, PokemonType.Dragon: 1},

    PokemonType.Fire: {PokemonType.Normal: 1, PokemonType.Fire: 0.5, PokemonType.Water: 0.5, PokemonType.Electric: 1,
                       PokemonType.Grass: 2, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                       PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 2,
                       PokemonType.Rock: 0.5, PokemonType.Ghost: 1, PokemonType.Dragon: 0.5},

    PokemonType.Water: {PokemonType.Normal: 1, PokemonType.Fire: 2, PokemonType.Water: 0.5, PokemonType.Electric: 1,
                        PokemonType.Grass: 0.5, PokemonType.Ice: 2, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                        PokemonType.Ground: 2, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 1,
                        PokemonType.Rock: 2, PokemonType.Ghost: 1, PokemonType.Dragon: 0.5},

    PokemonType.Electric: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 2, PokemonType.Electric: 0.5,
                           PokemonType.Grass: 0.5, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                           PokemonType.Ground: 0, PokemonType.Flying: 2, PokemonType.Psychic: 1, PokemonType.Bug: 1,
                           PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 0.5},

    PokemonType.Grass: {PokemonType.Normal: 1, PokemonType.Fire: 0.5, PokemonType.Water: 2, PokemonType.Electric: 1,
                        PokemonType.Grass: 0.5, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 0.5,
                        PokemonType.Ground: 2, PokemonType.Flying: 0.5, PokemonType.Psychic: 1, PokemonType.Bug: 0.5,
                        PokemonType.Rock: 2, PokemonType.Ghost: 1, PokemonType.Dragon: 0.5},

    PokemonType.Ice: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 0.5, PokemonType.Electric: 1,
                      PokemonType.Grass: 2, PokemonType.Ice: 0.5, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                      PokemonType.Ground: 2, PokemonType.Flying: 2, PokemonType.Psychic: 1, PokemonType.Bug: 1,
                      PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 2},

    PokemonType.Fighting: {PokemonType.Normal: 2, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                           PokemonType.Grass: 1, PokemonType.Ice: 2, PokemonType.Fighting: 1, PokemonType.Poison: 0.5,
                           PokemonType.Ground: 1, PokemonType.Flying: 0.5, PokemonType.Psychic: 0.5,
                           PokemonType.Bug: 0.5,
                           PokemonType.Rock: 2, PokemonType.Ghost: 0, PokemonType.Dragon: 1},

    PokemonType.Poison: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                         PokemonType.Grass: 2, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 0.5,
                         PokemonType.Ground: 0.5, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 2,
                         PokemonType.Rock: 0.5, PokemonType.Ghost: 0.5, PokemonType.Dragon: 1},

    PokemonType.Ground: {PokemonType.Normal: 1, PokemonType.Fire: 2, PokemonType.Water: 1, PokemonType.Electric: 2,
                         PokemonType.Grass: 0.5, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 2,
                         PokemonType.Ground: 2, PokemonType.Flying: 0, PokemonType.Psychic: 1, PokemonType.Bug: 0.5,
                         PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 1},

    PokemonType.Flying: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 0.5,
                         PokemonType.Grass: 2, PokemonType.Ice: 1, PokemonType.Fighting: 2, PokemonType.Poison: 1,
                         PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 2,
                         PokemonType.Rock: 0.5, PokemonType.Ghost: 1, PokemonType.Dragon: 1},

    PokemonType.Psychic: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                          PokemonType.Grass: 1, PokemonType.Ice: 1, PokemonType.Fighting: 2, PokemonType.Poison: 2,
                          PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 0.5, PokemonType.Bug: 1,
                          PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 1},

    PokemonType.Bug: {PokemonType.Normal: 1, PokemonType.Fire: 0.5, PokemonType.Water: 1, PokemonType.Electric: 1,
                      PokemonType.Grass: 2, PokemonType.Ice: 1, PokemonType.Fighting: 0.5, PokemonType.Poison: 2,
                      PokemonType.Ground: 1, PokemonType.Flying: 0.5, PokemonType.Psychic: 2, PokemonType.Bug: 1,
                      PokemonType.Rock: 1, PokemonType.Ghost: 0.5, PokemonType.Dragon: 1},

    PokemonType.Rock: {PokemonType.Normal: 1, PokemonType.Fire: 2, PokemonType.Water: 1, PokemonType.Electric: 1,
                       PokemonType.Grass: 1, PokemonType.Ice: 2, PokemonType.Fighting: 0.5, PokemonType.Poison: 1,
                       PokemonType.Ground: 0.5, PokemonType.Flying: 2, PokemonType.Psychic: 1, PokemonType.Bug: 2,
                       PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 1},

    PokemonType.Ghost: {PokemonType.Normal: 0, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                        PokemonType.Grass: 1, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                        PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 0, PokemonType.Bug: 1,
                        PokemonType.Rock: 1, PokemonType.Ghost: 2, PokemonType.Dragon: 1},

    PokemonType.Dragon: {PokemonType.Normal: 1, PokemonType.Fire: 1, PokemonType.Water: 1, PokemonType.Electric: 1,
                         PokemonType.Grass: 1, PokemonType.Ice: 1, PokemonType.Fighting: 1, PokemonType.Poison: 1,
                         PokemonType.Ground: 1, PokemonType.Flying: 1, PokemonType.Psychic: 1, PokemonType.Bug: 1,
                         PokemonType.Rock: 1, PokemonType.Ghost: 1, PokemonType.Dragon: 2}
}
