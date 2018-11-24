import sys
import math

# Save humans, destroy zombies!

LIST_HUMAN_IDS=list()

HUMAN_SAVED_MAP=dict()

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    
    human_count = int(input())
    
    human_map=dict()
    
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]    
        human_map[human_id]=dict(x=human_x, y=human_y)
    
    print(human_map, file=sys.stderr)
    
    zombie_count = int(input())
    
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    # First strategy go directly to humans
    
    if len(LIST_HUMAN_IDS)==0:
        print("Init list of humans...", file=sys.stderr)
        
        ids = list(human_map.keys())
        
        ids.sort()
        
        LIST_HUMAN_IDS = ids
        
        print("Human names {}".format(LIST_HUMAN_IDS), file=sys.stderr)
        
        for hid in LIST_HUMAN_IDS:
            HUMAN_SAVED_MAP[hid]=False
            
    action_done=False
    
    for human_id in LIST_HUMAN_IDS:
        
        print(human_id, file=sys.stderr)
        
        if not HUMAN_SAVED_MAP[human_id]:
        
            human_x = human_map[human_id]["x"]
            human_y = human_map[human_id]["y"]
            
            print((human_x, human_y), file=sys.stderr)
        
            if (x == human_x) and (y == human_y):
                HUMAN_SAVED_MAP[human_id]=True
            else:
                print("{0} {1}".format(human_x, human_y))
                action_done=True
                break
            
    if not action_done:
        print("{0} {1}".format(x, y))

    # Your destination coordinates
    
    # print("0 0")
