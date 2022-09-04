from pykson import *
import random
import uuid
import os
import math

characters = list()

class Character(JsonObject):
    #Properties
    name = StringField()

    hitpoints = IntegerField()
    
    strength = IntegerField()
    agility = IntegerField()
    perserverance = IntegerField()
    intelligence = IntegerField()
    wisdom = IntegerField()
    charisma = IntegerField()
    mentality = IntegerField()

    strength_bonus = IntegerField()
    agility_bonus = IntegerField()
    perserverance_bonus = IntegerField()
    intelligence_bonus = IntegerField()
    wisdom_bonus = IntegerField()
    charisma_bonus = IntegerField()
    mentality_bonus = IntegerField()
    
    practice_bonus_keys = ListField(str)
    practice_bonus_values = ListField(str)

    inventory = ListField(str)
    skills = ListField(str)

    def __repr__(self):
        return f"Character({self.name}, strength={self.strength}, {self.inventory})"

    def delete(self):
        global characters
        print(characters)
        characters.remove(self)
        print(characters)
        
        if not os.path.exists('characterdata'):
            os.mkdir('characterdata')
        
        filename = "characterdata/" + self.name + ".json"
        if os.path.exists(filename):
            os.remove(filename)
        

    def addItem(self, item):
        try:
            self.inventory.append(item)
        except AttributeError:
            self.inventory = [item]

    def removeItem(self, index):
        self.inventory.pop(index)

    def addSkill(self, skill):
        try:
            self.skills.append(skill)
        except AttributeError:
            self.skills = [skill]

    def removeSkill(self, index):
        self.skills.pop(index)

    def addPractice(self, description, value):
        try:
            self.practice_bonus_keys.append(description)
            self.practice_bonus_values.append(value)
        except AttributeError:
            self.practice_bonus_keys = [description]
            self.practice_bonus_values = [value]

    def removePractice(self, index):
        self.practice_bonus_keys.pop(index)
        self.practice_bonus_values.pop(index)

    def initCharacterWithRandomProperties(self):
        self.strength = random.randint(1, 20)
        self.agility = random.randint(1, 20)
        self.perserverance = random.randint(1, 20)
        self.intelligence = random.randint(1, 20)
        self.wisdom = random.randint(1, 20)
        self.charisma = random.randint(1, 20)
        self.mentality = random.randint(1, 20)
    
        self.practice_bonus_keys = list()
        self.practice_bonus_values = list()

        self.inventory = list()
        self.skills = list()

    def getAttributesDisplayString(self):
        strength_bonus = calculateBonus(self.strength)
        agility_bonus = calculateBonus(self.agility)
        perserverance_bonus = calculateBonus(self.perserverance)
        intelligence_bonus = calculateBonus(self.intelligence)
        wisdom_bonus = calculateBonus(self.wisdom)
        charisma_bonus = calculateBonus(self.charisma)
        mentality_bonus = calculateBonus(self.mentality)
        return f"""
```
Spielername: {self.name}
Hitpoints: {self.hitpoints}
-----
--- Attribute ---
Stärke (STR): {self.strength} --- Bonus: {strength_bonus}
Geschicklichkeit (GES): {self.agility} --- Bonus: {agility_bonus}
Konstitution (KON): {self.perserverance} --- Bonus: {perserverance_bonus}
Intelligenz (INT): {self.intelligence} --- Bonus: {intelligence_bonus}
Weisheit (WIS): {self.wisdom} --- Bonus: {wisdom_bonus}
Charisma (CHA): {self.charisma} --- Bonus: {charisma_bonus}
Mentality (MTL): {self.mentality} --- Bonus: {mentality_bonus}
-----
```"""

    def getPracticeBonusDisplayString(self):
        stringbuild = "```\n"
        stringbuild += "Übungsboni\n"
        for i in range(len(self.practice_bonus_keys)):
            stringbuild += str(i) + ": " + self.practice_bonus_keys[i] + " - " + self.practice_bonus_values[i] + "\n"
        stringbuild += "```"
        return stringbuild

    def getInventoryDisplayString(self):
        stringbuild = "```\n"
        stringbuild += "Inventar\n"
        for i in range(len(self.inventory)):
            stringbuild += str(i) + ": " + self.inventory[i] + "\n"
        stringbuild += "```"
        return stringbuild

    def getSkillsDisplayString(self):
        stringbuild = "```\n"
        stringbuild += "Skills\n"
        for i in range(len(self.skills)):
            stringbuild += str(i) + ": " + self.skills[i] + "\n"
        stringbuild += "```"
        return stringbuild

    def getDisplayString(self):
        return self.getAttributesDisplayString() + self.getPracticeBonusDisplayString() + self.getInventoryDisplayString() + self.getSkillsDisplayString()

    def getAsJson(self):
        return Pykson().to_json(self)

    def saveCharacterToFile(self):
        if not os.path.exists('characterdata'):
            os.mkdir('characterdata')
        
        filename = "characterdata/" + self.name + ".json"
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, "w") as file:
            file.write(self.getAsJson())


def calculateBonus(p):
    return math.floor(p/2 -5)
    

def updateAllCharactersFromFiles():
    if not os.path.exists('characterdata'):
        return list()

    list_of_characters = list()
    list_of_files = list()
    
    for root, dirs, files in os.walk("characterdata"):
        for file in files:
            list_of_files.append(os.path.join(root,file))
            
    for filename in list_of_files:
        with open(filename) as f:
            json_text = f.read()
            list_of_characters.append(Pykson().from_json(json_text, Character, accept_unknown=True))

    global characters
    characters = list_of_characters

def doesCharacterExist(name):
    updateAllCharactersFromFiles()
    global characters
    for char in characters:
        if name.lower() in char.name.lower():
            return True
    return False
    
    
def getCharacterWithRandomValues(name):
    newCharacter = Character()
    newCharacter.name = name
    newCharacter.initCharacterWithRandomProperties()
    return newCharacter

def parseOperationValue(stringOperand):
    if not "+" in stringOperand and not "-" in stringOperand:
        return None

    if "+" in stringOperand and "-" in stringOperand:
        return None

    if "+" in stringOperand:
        splitChar = "+"
        value = 1
    else:
        splitChar = "-"
        value = -1

    splitOperand = stringOperand.split(splitChar)
    return splitOperand[0], int(splitOperand[1]), value

async def applyOperation(character, operationValue, channel):
    attr = operationValue[0].upper()
    editValue = operationValue[1] * operationValue[2]
    if attr == "STR":
        character.strength += editValue
    elif attr == "GES":
        character.agility += editValue
    elif attr == "KON":
        character.perserverance += editValue
    elif attr == "INT":
        character.intelligence += editValue
    elif attr == "WIS":
        character.wisdom += editValue
    elif attr == "CHA":
        character.charisma += editValue
    elif attr == "MTL":
        character.mentality += editValue
    character.saveCharacterToFile()
    updateAllCharactersFromFiles()
    await sendMessageToChannel(channel, f"```\nDer Wert {attr} von {character.name} wurde um {editValue} angepasst.\n```")
    

async def executeOperationWithChar(character, remainingOperands, channel):
    if len(remainingOperands) == 0:
        await sendMessageToChannel(channel, character.getDisplayString())
        return

    if remainingOperands[0].lower().startswith("inventoryadd "):
        joined = " -".join(remainingOperands)
        joined = joined[len("inventoryadd "):]
        character.addItem(joined)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDas Item "{joined}" wurde dem Character {character.name} ins Inventar gelegt.\n```')
        return

    if remainingOperands[0].lower().startswith("skilladd "):
        joined = " -".join(remainingOperands)
        joined = joined[len("skilladd "):]
        character.addSkill(joined)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDer Skill "{joined}" wurde dem Character {character.name} hinzugefügt.\n```')
        return

    if remainingOperands[0].lower().startswith("practiceadd "):
        if len(remainingOperands) != 2:
            await sendMessageToChannel(channel, f'```\nBitte verwende die korrekte Syntax: !char -<Name> -practiceadd <Beschreibung> -<Wert>\n```')
            return
        desc = remainingOperands[0][len("practiceadd "):]
        level = remainingOperands[1]
        character.addPractice(desc, level)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDer Character {character.name} hat nun den Übungsbonus {desc} mit dem Level {level}.\n```')
        return

    if remainingOperands[0].lower().startswith("inventoryremove "):
        joined = " -".join(remainingOperands)
        joined = joined[len("inventoryremove "):]
        index = int(joined)
        item = character.inventory[index]
        character.removeItem(index)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDas Item "{item}" wurde dem Character {character.name} aus dem Inventar entfernt.\n```')
        return

    if remainingOperands[0].lower().startswith("skillremove "):
        joined = " -".join(remainingOperands)
        joined = joined[len("skillremove "):]
        index = int(joined)
        item = character.skills[index]
        character.removeSkill(index)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDer Skill "{item}" wurde dem Character {character.name} wieder genommen.\n```')
        return

    if remainingOperands[0].lower().startswith("practiceremove "):
        joined = " -".join(remainingOperands)
        joined = joined[len("practiceremove "):]
        index = int(joined)
        desc = character.practice_bonus_keys[index]
        character.removePractice(index)
        character.saveCharacterToFile()
        await sendMessageToChannel(channel, f'```\nDer Übungsbonus "{desc}" wurde dem Character {character.name} wieder genommen.\n```')
        return

    if len(remainingOperands) == 1:
        soleOp = remainingOperands[0].lower()
        if soleOp == "showinv":
            await sendMessageToChannel(channel, character.getInventoryDisplayString())
            return
        elif soleOp == "showskills":
            await sendMessageToChannel(channel, character.getSkillsDisplayString())
            return
        elif soleOp == "showpractice":
            await sendMessageToChannel(channel, character.getPracticeBonusDisplayString())
            return
        elif soleOp == "showattributes":
            await sendMessageToChannel(channel, character.getAttributesDisplayString())
            return
        elif soleOp == "delete":
            await sendMessageToChannel(channel, f'```Diese Aktion kann nicht rückgängig gemacht werden! Bitte verwende "!char -{character.name} -delete -confirm"```')
            return
        else:
            operationValue = parseOperationValue(remainingOperands[0])
            if operationValue == None:
                await sendMessageToChannel(channel, f'```\nDieser Befehl wurde nicht erkannt. Verwende "!char" um eine Übersicht über die Befehle zu bekommen\n```')
                return
            await applyOperation(character, operationValue, channel)
            return
            
    elif len(remainingOperands) == 2:
        if remainingOperands[0] == "delete" and remainingOperands[1] == "confirm":
            character.delete()
            await sendMessageToChannel(channel, f"```\nDer Character {character.name} wurde permanent gelöscht.\n```")
            return
        
async def displayHelp(channel):
    await sendMessageToChannel(channel, """
```
Alle Befehle beginnen mit "!char". Argumente werden durch ein " -" getrennt, also z.B. so: "!char -argument1 -argument2 -Ganz langes Argument"

Befehle:

!char | Zeigt die Hilfe an.
!char -list | Zeigt eine Liste mit allen verfügbaren Characteren an
!char -create -<Name> | Erstellt einen neuen Character mit zufälligen Attributswerten und dem gegebenen Namen
!char -<Name> -delete | Löscht den angegeben Character unwiderruflich
!char -<Name> | Zeigt die vollständige Characterübersicht an
!char -<Name> -showInv | Zeigt das Inventar dieses Characters an
!char -<Name> -showSkills | Zeigt die Skill-Liste dieses Characters an
!char -<Name> -showPractice | Zeigt die Practice Boni dieses Characters an
!char -<Name> -showAttributes | Zeigt die Attribute dieses Characters an
!char -<Name> -inventoryadd <Itembeschreibung> | Fügt ein Item in das Inventar des Spielers ein
!char -<Name> -inventoryremove <Position> | Entfernt das Item an der gegebenen Position 
!char -<Name> -skilladd <Skillbeschreibung> | Fügt ein Skill zum Character hinzu
!char -<Name> -skillremove <Position> | Entfernt den Skill an der angegebenen Position
!char -<Name> -practiceadd <Beschreibung> -<Wert> | Fügt einen Übungsbonus zum Character hinzu
!char -<Name> -practiceremove <Position> | Entfernt einen Übungsbonus wieder

Charaktereigenschaften können mit "!char -<Name> <Kürzel>+-<Wert>" verändert werden, z.B.:
!char -Tobey -STR+2 (Erhöht Stärke um 2)
!char -Tobey -MTL-1 (Verringert Mentality um 1)
Die Kürzel sind in den Characterübersichten aufgeführt.

```
""")

async def sendMessageToChannel(channel, message):
    await channel.send(message)

def getDisplayListOfAllCharacters():
    updateAllCharactersFromFiles()
    global characters
    stringbuild = "```\n"
    stringbuild += "Liste aller verfügbaren Charactere:\n\n"
    for char in characters:
        stringbuild += char.name + "\n"
    stringbuild += "```"
    return stringbuild

async def handleCharacterCommand(message):
    global characters
    arguments = message.content.split(" -")
    arguments.pop(0)
    
    if len(arguments) == 0:
        await displayHelp(message.channel)
        return
    elif len(arguments) == 1:
        if arguments[0] == "list":
            await sendMessageToChannel(message.channel, getDisplayListOfAllCharacters())
            return
    elif len(arguments) == 2:
        if arguments[0] == "create":
            newChar = getCharacterWithRandomValues(arguments[1])
            newChar.saveCharacterToFile()
            characters.append(newChar)
            await sendMessageToChannel(message.channel, f"Der Character {newChar.name} wurde erstellt.")
            await sendMessageToChannel(message.channel, newChar.getDisplayString())
            return
            

    formattedName = arguments[0].strip()
    if doesCharacterExist(formattedName):
        updateAllCharactersFromFiles()

        character = None
        for char2 in characters:
            if formattedName.lower() in char2.name.lower():
                character = char2
    else:
        await sendMessageToChannel(message.channel, "Dieser Character wurde nicht gefunden")
        return

    arguments.pop(0)
    
    await executeOperationWithChar(character, arguments, message.channel)
    

if __name__ == "__main__":

    for i in range(20):
        print(calculateBonus(i))

    
