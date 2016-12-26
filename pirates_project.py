from Pirates import *
import math

def do_turn(game):
    handle_pirates(game)
    handle_drones(game)
    
    
def handle_pirates(game):
    my_pirates=game.get_my_living_pirates()
    not_my_islands=game.get_neutral_islands()+game.get_enemy_islands()
    for pirate in my_pirates:
        if len(game.get_enemy_living_drones())>=5: # if there are drones
            if pirate.id<=2:
                role_capture(pirate,game)
            #elif pirate.id==2:
            #    role_attack(pirate,game)
            else:
                role_defend(pirate,game)
        
        elif len(not_my_islands)>0: # if i dont own some islands
            if pirate.id<=2:
                role_capture(pirate,game)
           
            else:
                if pirate.distance(closest_island(pirate,game))<=4:
                    role_capture(pirate,game)
                else:
                    role_attack(pirate,game)
        else:
            role_attack(pirate,game)
            
        
def handle_drones(game):
    my_drones= game.get_my_living_drones()
    for drone in my_drones:
        move_drone(drone,game.get_my_cities()[0],game)
        
def move_pirate(pirate,destination,game):
    directions = game.get_sail_options(pirate, destination) 
    if game.get_turn()%2==0 and len(directions)>1:
        game.set_sail(pirate, directions[1])
    else:
        if len(directions)==3:
            game.set_sail(pirate,directions[2])
        else:
            game.set_sail(pirate,directions[0])

def enemy_pirate_in_row(row,game):
    enemy_pirates=game.get_enemy_living_pirates()
    for pirate in enemy_pirates:
        if math.fabs(pirate.location.row-row)<=3:
            return True
    return False
    
def enemy_pirate_in_col(col,game):
    enemy_pirates=game.get_enemy_living_pirates()
    for pirate in enemy_pirates:
        if math.fabs(pirate.location.col-col)<=3:
            return True
    return False


            
def move_drone(drone,destination,game):
    side=check_side(game)
    directions = game.get_sail_options(drone, destination)
    if len(directions)==1:
        game.set_sail(drone,directions[0])
    else:
        if enemy_pirate_in_row(drone.location.row,game) and not enemy_pirate_in_col(drone.location.col,game):
            game.set_sail(drone,directions[0])
        else:
            game.set_sail(drone,directions[1])
        
def get_weakest_pirate(pirates_list,game):
    enemy_pirate=pirates_list[0]
    small_health=enemy_pirate.current_health
    for pirate in pirates_list:
        temp_health=pirate.current_health
        if temp_health<small_health:
            small_health=temp_health
            enemy_pirate=pirate
    return enemy_pirate

def get_weakest_enemy_pirate_in_range(pirate,game):
    enemy_pirates_list=[]
    for enemy_pirate in game.get_enemy_living_pirates():
        if pirate.in_attack_range(enemy_pirate):
            enemy_pirates_list.append(enemy_pirate)
    if len(enemy_pirates_list)==0:
        return None
    return get_weakest_pirate(enemy_pirates_list,game)
            
def get_drone_in_range(pirate,game):
    enemy_drones=game.get_enemy_living_drones()
    for drone in enemy_drones:
        if pirate.in_attack_range(drone):
            return drone
    return None
def try_attack(pirate, game):
    enemy_pirate=get_weakest_enemy_pirate_in_range(pirate,game)
    if not enemy_pirate is None:
        game.attack(pirate,enemy_pirate)
        return True
    enemy_drone=get_drone_in_range(pirate,game)
    if not enemy_drone is None:
        game.attack(pirate,enemy_drone)
        return True
    return False


def check_side(game):
    my_location=game.get_all_my_pirates()[0].initial_location
    enemy_location=game.get_all_enemy_pirates()[0].initial_location
    if my_location.col>enemy_location.col:
        return 'right'
    return 'left'

    
def first_island(game):
    side=check_side(game)
    if side=='right':
        return game.get_all_islands()[2]
    return game.get_all_islands()[1]
    
def closest_island(pirate,game):
    all_islands=game.get_neutral_islands()+game.get_enemy_islands()
    if len(all_islands)==0:
        return None
    if len(all_islands)==1:
        return all_islands[0]
    island=all_islands[0]
    smallest_distance=pirate.distance(island)
    for i in range(1,len(all_islands)):
        temp=pirate.distance(all_islands[i])
        if temp<smallest_distance:
            smallest_distance=temp
            island=all_islands[i]
    return island
            
def closest_enemy(pirate,game):
    enemy_pirates=game.get_enemy_living_pirates()
    if len(enemy_pirates)==0:
        return None
    if len(enemy_pirates)==1:
        return enemy_pirates[0]
    enemy=enemy_pirates[0]
    smallest_distance=pirate.distance(enemy)
    for i in range(1,len(enemy_pirates)):
        temp=pirate.distance(enemy_pirates[i])
        if temp<smallest_distance:
            smallest_distance=temp
            enemy=enemy_pirates[i]
    return enemy

def closest_drone(pirate,game):
    enemy_drones=game.get_enemy_living_drones()
    if len(enemy_drones)==0:
        return None
    if len(enemy_drones)==1:
        return enemy_drones[0]
    drone=enemy_drones[0]
    smallest_distance=pirate.distance(drone)
    for i in range(1,len(enemy_drones)):
        temp=pirate.distance(enemy_drones[i])
        if temp<smallest_distance:
            smallest_distance=temp
            drone=enemy_drones[i]
    return drone
    
            
def role_capture(pirate,game):
    island=first_island(game)
    if game.get_turn()<20 and island not in game.get_my_islands() and pirate.id==0:
        move_pirate(pirate,island,game)
    elif len(game.get_neutral_islands()+game.get_enemy_islands())==0:
        role_attack(pirate,game)
    else:
        if not try_attack(pirate,game):
            move_pirate(pirate,closest_island(pirate,game),game)

def role_attack(pirate,game):
    if not try_attack(pirate,game):
        if len(game.get_enemy_living_pirates())>0:
            move_pirate(pirate,closest_enemy(pirate,game),game)
        else:
            move_pirate(pirate,game.get_all_enemy_pirates()[0].initial_location,game)
  
def role_defend(pirate,game):
    if not try_attack(pirate,game):
        move_pirate(pirate,closest_drone(pirate,game),game)
  
                
def role_protect_city(pirate,game):
    if not try_attack(pirate,game):
        if pirate.distance(game.get_enemy_cities()[0])>4:
            move_pirate(game.get_enemy_cities()[0])
        else:
            if len(game.get_enemy_living_drones())>0:
                move_pirate(closest_drone(pirate,game))
            
