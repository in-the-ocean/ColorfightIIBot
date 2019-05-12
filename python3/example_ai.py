from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

ASSUMING_TIME = 6
MAX_VALUE = 3

def attackable():
    home = (-1,-1)
    attackable = {}
    for mine in game.me.cells.keys():
        if game.game_map[mine].building.name == "home":
            home = mine
        for surround in mine.get_surrounding_cardinals():
            if game.game_map[surround].owner != game.uid:
                attackable[surround] = game.game_map[surround] 
    
    return [home,attackable] 

def attack_basic(pos):
    dis = nearest_enemy(pos)
    if dis == 0:
        income = ASSUMING_TIME*30*(gold_val*game.game_map[pos].natural_gold+energy_val*game.game_map[pos].natural_energy)
    else:
        income = ASSUMING_TIME*(16-dis)*(gold_val*game.game_map[pos].natural_gold+energy_val*game.game_map[pos].natural_energy)
    if game.game_map[pos].building.name == "gold":
        extra = [50,150,350][game.game_map[pos].building.level -1] * gold_val
    elif game.game_map[pos].building.name == "home":
        extra = game.users[game.game_map[pos].owner].gold/3 * gold_val
    else:
        extra = 0
    print("income",pos,income)
    return income+extra
    
def attack_tax(pos):
    tax = cell_num//100
    dis = nearest_enemy(pos)
    if dis == 0:
        tax_amount = (gold_val+energy_val)*ASSUMING_TIME*20*tax
    else:
        tax_amount = (gold_val+energy_val)*ASSUMING_TIME*tax*(16-dis)
    print("tax:", pos,tax_amount)
    return tax_amount

def home_lost(home_pos):
    dis = nearest_enemy(home_pos)
    if dis == 0:
        return me.gold/3/30/ASSUMING_TIME
    return me.gold/3/dis/ASSUMING_TIME
    
def total_attack_cost(pos):
    home_lose = home_lost(home_pos)*(game.game_map[pos].attack_cost/me.energy)
    return energy_val*game.game_map[pos].attack_cost

def attack_eval(pos):
    return attack_basic(pos)-attack_tax(pos)-total_attack_cost(pos)

def attack_dict(attackable):
    evaluation = {}
    for cell in attackable.keys():
        evaluation[cell] = attack_eval(cell)
    return evaluation

def nearest_enemy(pos):
    for dis in range(1,16):
        for x in range(dis):
            y = dis - x;
            temp_x = pos.x+x
            temp_y = pos.y+y
            if temp_x< 30 and temp_x>= 0 and temp_y <30 and temp_y >= 0: 
                c = game.game_map[(temp_x,temp_y)]
                if c.owner != 0 and c.owner != game.uid:
                    return dis
            y = -y
            temp_x = pos.x+x
            temp_y = pos.y+y
            if temp_x< 30 and temp_x>= 0 and temp_y <30 and temp_y >= 0: 
                c = game.game_map[(temp_x,temp_y)]
                if c.owner != 0 and c.owner != game.uid:
                    return dis
            x = -x
            temp_x = pos.x+x
            temp_y = pos.y+y
            if temp_x< 30 and temp_x>= 0 and temp_y <30 and temp_y >= 0: 
                c = game.game_map[(temp_x,temp_y)]
                if c.owner != 0 and c.owner!= game.uid:
                    return dis
            y = -y
            temp_x = pos.x+x
            temp_y = pos.y+y
            if temp_x< 30 and temp_x>= 0 and temp_y <30 and temp_y >= 0: 
                c = game.game_map[(temp_x,temp_y)]
                if c.owner != 0 and c.owner!= game.uid:
                    return dis
    return 0

def build_type(pos):
    cell = game.game_map[pos]
    if cell.natural_gold >= cell.natural_energy:
        return BLD_GOLD_MINE 
    else :
        return BLD_ENERGY_WELL

def build_gain(pos):
    cell = game.game_map[pos]
    dis = nearest_enemy(pos)
    tax = building_num//100
    if cell.natural_gold>=(cell.natural_energy-1):
        if dis == 0:
            tax_amount = (gold_val+energy_val)*ASSUMING_TIME*20*tax
            income = ASSUMING_TIME*30*(gold_val*cell.natural_gold)
        else:
            tax_amount = (gold_val+energy_val)*ASSUMING_TIME*tax*(16-dis)
            income = ASSUMING_TIME*(16-dis)*(gold_val*cell.natural_gold)
    else:
        if dis == 0:
            tax_amount = (gold_val+energy_val)*ASSUMING_TIME*20*tax
            income = ASSUMING_TIME*30*(energy_val*cell.natural_energy)
        else:
            tax_amount = (gold_val+energy_val)*ASSUMING_TIME*tax*(16-dis)
            income = ASSUMING_TIME*(16-dis)*(energy_val*cell.natural_energy)
    return income-tax_amount

def build_cost(pos):
    return gold_val*100

def build_eval(pos):
    return build_gain(pos)-build_cost(pos)

def build_dict():
    lst = {}
    for cell in me.cells.keys():
        if game.game_map[cell].building.name == "empty":
            lst[cell] = build_eval(cell)
    return lst


def update_gain(pos):
    cell = game.game_map[pos]
    dis = nearest_enemy(pos)
    if cell.natural_gold>=(cell.natural_energy-1):
        if dis == 0:
            income = ASSUMING_TIME*30*(gold_val*cell.natural_gold)
        else:
            income = ASSUMING_TIME*(16-dis)*(gold_val*cell.natural_gold)
    else:
        if dis == 0:
            income = ASSUMING_TIME*30*(energy_val*cell.natural_energy)
        else:
            income = ASSUMING_TIME*(16-dis)*(energy_val*cell.natural_energy)   
    return income

def update_cost(pos):
    cell = game.game_map[pos]
    return gold_val* [200,400][cell.building.level]

def update_eval(pos):
    return update_gain(pos)-update_cost(pos)

def cal_tax(num):
    return num//100


game = Colorfight()

game.connect(room = 'gold')

# game.register should return True if succeed.
# As no duplicate usernames are allowed, a random integer string is appended
# to the example username. You don't need to do this, change the username
# to your ID.
# You need to set a password. For the example AI, the current time is used
# as the password. You should change it to something that will not change 
# between runs so you can continue the game if disconnected.

cell_num = 0
building_num = 0

if game.register(username = 'name' + str(random.randint(1, 100)), \
        password = str(int(time.time()))):
    while True:
        cmd_list = []
        my_attack_list = []
        game.update_turn()

        if game.me == None:
            continue

        me = game.me
        
        gold_val = (MAX_VALUE-1)/500 *game.turn+1
        energy_val = (1-MAX_VALUE)/500*game.turn + MAX_VALUE
        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.
        cell_tax = cal_tax(cell_num)
        building_tax = cal_tax(building_num)
        attackables = attackable()
        home_pos = attackables[0]
        evaluations = attack_dict(attackables[1])
        max_val = max(evaluations.keys(), key = lambda x: evaluations[x])
        print(evaluations)
        while (game.game_map[max_val].natural_gold>cell_tax or game.game_map[max_val].natural_energy >cell_tax) \
            and game.game_map[max_val].attack_cost<me.energy:
            cmd_list.append(game.attack(max_val,game.game_map[max_val].attack_cost))
            cell_num += 1
            print("We are attacking")
            game.me.energy -= game.game_map[max_val].attack_cost
            del evaluations[max_val] 
            if len(evaluations)== 0:
                break
            max_val = max(evaluations.keys(), key = lambda x: evaluations[x])


        build_evaluation = build_dict()
        if len(build_evaluation)>0:
            max_build = max(build_evaluation.keys(),key = lambda x: build_evaluation[x])
            while  (game.game_map[max_val].natural_gold>building_tax or game.game_map[max_val].natural_energy >building_tax) \
                and me.gold > 100:
                cmd_list.append(game.build(max_build,build_type(max_build)))
                building_num += 1
                print("We build {} on ({},{})".format(build_type(max_build),max_build.x,max_build.y))
                me.gold -= 100
                del build_evaluation[max_build]
                if len(build_evaluation) == 0:
                    break
                max_build = max(build_evaluation.keys(),key = lambda x: build_evaluation[x])


        for cell in game.me.cells.values():
                        # Notice can_update only checks for upper bound. You need to check
            # tech_level by yourself. 
            if cell.building.can_upgrade and \
                    (cell.building.is_home or cell.building.level < me.tech_level) and \
                    cell.building.upgrade_gold < me.gold and \
                    cell.building.upgrade_energy < me.energy:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                me.gold   -= cell.building.upgrade_gold
                me.energy -= cell.building.upgrade_energy
                
       
        result = game.send_cmd(cmd_list)
        print(result)
