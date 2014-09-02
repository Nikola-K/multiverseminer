""" This contains a list of all models used by Multiverse Miner"""

from mm import db
from item import Item
from inventory import Inventory 
from flask import jsonify
from datetime import datetime, timedelta
from random import randint
from mm.exceptions import CraftingException


class Character(db.Model):
    """ Character is the actual in-game PC."""
    name = db.Column(db.String(64), primary_key=True, nullable=False)
    account = db.relationship("Account", backref=db.backref("characters", uselist=True), uselist=False )

    constitution = db.Column(db.Integer, default=1, nullable=False)
    dexterity = db.Column(db.Integer, default=1, nullable=False)
    luck = db.Column(db.Integer, default=1, nullable=False)
    perception = db.Column(db.Integer, default=1, nullable=False)
    strength = db.Column(db.Integer, default=1, nullable=False)

    # secondary
    accuracy = db.Column(db.Integer, default=1, nullable=False)
    attackSpeed = db.Column(db.Integer, default=1, nullable=False)
    counter = db.Column(db.Integer, default=1, nullable=False)
    crit_chance = db.Column(db.Integer, default=1, nullable=False)
    crit_percentage = db.Column(db.Integer, default=1, nullable=False)
    defense = db.Column(db.Integer, default=1, nullable=False)
    evasion = db.Column(db.Integer, default=1, nullable=False)
    health = db.Column(db.Integer, default=1, nullable=False)
    loot_luck = db.Column(db.Integer, default=1, nullable=False)
    mining_luck = db.Column(db.Integer, default=1, nullable=False)
    parry = db.Column(db.Integer, default=1, nullable=False)
    regeneration = db.Column(db.Integer, default=1, nullable=False)
    resillience = db.Column(db.Integer, default=1, nullable=False)
    scavenge_luck = db.Column(db.Integer, default=1, nullable=False)
    shipSpeed = db.Column(db.Integer, default=1, nullable=False)

    # experience
    character_experience = db.Column(db.Integer, default=1, nullable=False)
    crafting_experience = db.Column(db.Integer, default=1, nullable=False)
    loot_experience = db.Column(db.Integer, default=1, nullable=False)
    mining_experience = db.Column(db.Integer, default=1, nullable=False)
    scavenging_experience = db.Column(db.Integer, default=1, nullable=False)

    def update_collection(self, collectiontype):
        """ This method will verify the collectiontype is valid,
            then see if it's been long enough to update."""
        curtime = datetime.utcnow()
        waittime = timedelta(0, 5)  # 5 seconds
        collectionlastfield = 'last_'+collectiontype
        successlist = {}
        if hasattr(self.account, collectionlastfield):
            oldtime = getattr(self.account, collectionlastfield)
            if oldtime + waittime < curtime:
                oldtime = curtime
                setattr(self.account, collectionlastfield, oldtime)
                for loot in self.account.planet.loot:
                    chance = loot.droprate * 100000
                    x = randint(0, 10000)
                    print x
                    #app.logger.debug('is %s less than %s for %s?' % (x, chance, loot.item.name))
                    if x <= chance:
                        amount = randint(1, 5)
                        self.adjust_inventory(loot.item, amount)
                        successlist[loot.item.id] = amount
                if successlist:
                    return jsonify(collectiontype=collectiontype,
                                   message="You found something.",
                                   data=successlist,
                                   lastrun=oldtime, result='success')
                else:
                    return jsonify(collectiontype=collectiontype,
                                   message="nothing found.",
                                   data=successlist,
                                   lastrun=oldtime, result='success')
            else:
                return jsonify(collectiontype=collectiontype, message="too soon",
                               lastrun=oldtime, result='success')
        else:
            return jsonify(collectiontype=collectiontype, result='failure',
                           message="Invalid collection type." )


    def craft_item(self, itemid, count=1):
        newitem = Item.query.filter_by(id=itemid)
        # verify it's a valid item
        if newitem.first():
            newitem = newitem.first()
            # verify all ingredients are in inventory.
            if not newitem.ingredients:
                raise CraftingException("%s is a base material and non-craftable." % itemid)

            if not self.has_recipe(itemid):
                raise CraftingException("You don't have the %s recipe!" % itemid)
            for ingredient in newitem.ingredients:
                amount_needed = count * ingredient.amount
                if not self.in_inventory(ingredient.item.id, amount_needed):
                    raise CraftingException("cannot craft %s %s without %s %s"
                                            % (count, itemid, amount_needed, ingredient.item.id))
            # remove items from inventory now that we know all exist
            #app.logger.debug("Crafting %s %s " % (count, itemid))
            for ingredient in newitem.ingredients:
                amount_needed = count * ingredient.amount
                self.adjust_inventory(ingredient.item, -amount_needed)
            self.adjust_inventory(newitem, count)
            return newitem
        else:
            raise CraftingException("Item %s doesn't exist in DB" % itemid)

    def has_recipe(self, itemid):
        """placeholder"""
        for recipe in self.recipebook:
            if recipe.item.id == itemid:
                return True
        return False

    def in_inventory(self, itemid, amount=0):
        """placeholder"""
        for inventory_item in self.inventory:
            if inventory_item.item.id == itemid and inventory_item.amount >= amount:
                return True
        return False

    def adjust_inventory(self, item, amount):
        """placeholder"""
        for inventory_item in self.inventory:
            if inventory_item.item.id == item.id:
                if inventory_item.amount + amount >= 0:
                    inventory_item.amount = inventory_item.amount + amount
                    return inventory_item.amount
                else:
                    raise CraftingException("You need %s %s, but have %s"
                                            % (amount, inventory_item.item.id, inventory_item.amount))
        # Item wasn't found in inventory, create a new inventory item
        if amount > 0:
            inv=Inventory(item=item, item_id=item.id, character=self, character_name=self.name, amount=amount)
            return amount
        raise CraftingException("Item %s not found in inventory??" % item.id)

    # tbd
    # skills
    # gear
    # weapon
    def __repr__(self):
        """ return a tag for the character"""
        return '<Character %r>' % (self.name)

    def __unicode__(self):
        """ return the unicode name """
        return self.name
