from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random



fire = Spell("Fire", 25 , 600, "black")
thunder = Spell("hunder", 25 , 600, "black")
blizzard = Spell("Blizzard", 25 , 600, "black")
meteor = Spell("Meteor", 40 , 1200, "black")
quake = Spell("Quake", 12 , 120, "black")

cure = Spell("Cure",25,620,"white")
cura = Spell("Cura",32,1500,"white")
curaga = Spell ("Curaga",50,6000,"white")

potion = Item("Potion","potion","Heals 50 HP",50)
hipotion = Item("Hi-Potion","potion","Heals 100 HP",100)
superpotion = Item("Super Potion","potion","Heals 1000 HP",1000)
elixir = Item("ELixir","elixir","Fully restores HP/MP of one party member",9999)
hielixir = Item("MegaElixir","elixir","Fully restores party's HP/MP",9999)
grenade = Item("Grenade","attack","Deals 500 damage",1000)

player_spells = [fire,thunder,blizzard,meteor,cure,cura]
enemy_spells = [fire,meteor,curaga]
player_items = [{"item":potion,"quantity":15},{"item":hipotion,"quantity":5},{"item":superpotion,"quantity":5},{"item":elixir,"quantity":5},{"item":hielixir,"quantity":5},{"item":grenade,"quantity":5}]
person = Person("Valos:", 3260,132,300,34,player_spells,player_items)
person2 = Person("Vapos:",4160,188,311,34,player_spells,player_items)
person3 = Person("Vamos:",3089,174,288,34,player_spells,player_items)

enemy = Person("Magus:  ",1250,130,560,325,enemy_spells,[])
enemy2 = Person("Pegasus:",11200,701,525,25,enemy_spells,[])
enemy3 = Person("Vagus:  ",1250,130,560,325,enemy_spells,[])
players = [person,person2,person3]
enemies = [enemy,enemy2,enemy3]
running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "Fight" + bcolors.ENDC)
while running:
    print("================================================")
    print("\n")
    print("NAME               HP                                  MP")
    for player in players:
        player.get_stats()
    for  enemy in enemies:
        enemy.get_enemy_stats()

    print("\n") 


    for player in players:
        
        player.choose_action()
        choice = input("    Choose Action :")
        index = int(choice)-1
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ","") +" for", dmg, "points of damage.")
            if enemies[enemy].get_hp()==0:
                print(enemies[enemy].name.replace(" ","") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic :")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]

            magic_dmg = spell.generate_damage()


            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not Enough mp" +bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)
            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg),"HP." +bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                
                print(bcolors.OKBLUE + "\n" + spell.name + " Deals", str(magic_dmg), "Points of damage to "+ enemies[enemy].name.replace(" ","") + bcolors.ENDC)
                if enemies[enemy].get_hp()==0:
                    print(enemies[enemy].name.replace(" ","")+ " has died.")
                    del enemies[enemy]


        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: "))-1
            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]
            
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n"+"Nothing left" + bcolors.ENDC )
                continue
            player.items[item_choice]["quantity"]-=1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN +"\n"+item.name+" heals for ", str(item.prop),"HP" +bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:       
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name +" fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                
                print(bcolors.FAIL + "\n" + item.name  + " deals", str(item.prop), " points of damage to "+ enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp()==0:
                    print(enemies[enemy].name.replace(" ","") + " has died.")
                    del enemies[enemy]

    # if battle is over             
    defeated_enemies = 0
    defeated_players = 0
    
    for player in players:
        if player.get_hp() == 0:
            defeated_players+=1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:        

        print(bcolors.OKGREEN + "You won" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:        
        print(bcolors.FAIL + "You were defeated " + bcolors.ENDC)
        running = False

    print("\n Enemy attack:")                
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:

            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_dmg(enemy_dmg)
            print(enemy.name.replace(" ","")+" attacks "+players[target].name.replace(" ","")+" for" , enemy_dmg)
        elif enemy_choice == 1:
            spell,magic_dmg=enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == 'white':
                enemy.heal(magic_dmg)
                
                print(bcolors.OKBLUE +  spell.name + " heals " + enemy.name + " for", str(magic_dmg),"HP." +bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ","") + "'s " + spell.name + " Deals", str(magic_dmg), "Points of damage to "+ players[target].name.replace(" ","") + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ","") + " has died.")
                    del players[player]

            #print("Enemy Chose",spell," damage is ",magic_dmg)
