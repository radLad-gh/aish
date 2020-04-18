import ast
import sys


COMMANDS = {'enter', 'examine', 'inventory', 'help', 'whereami', 'edit', 'exits'}

LOCATIONS = {
    "banquet": {"maze"},
    "maze": {"grate"},
    "grate": {"spider", "bull"},
    "spider": {"mirrors", "grate"},
    "mirrors": {"keyroom"},
    "keyroom": {"grate"},
    "bull": {"home"},
    "home": {None},
}

visited = {
    "banquet": 0,
    "maze": 0,
    "grate": 0,
    "spiderroom": 0,
    "mirrorhall": 0,
    "keyroom": 0,
    "keygrate": 0,
    "bull": 0,
    "home": 0,
}

short_descriptions = {
    "locations": {
        "banquet":
            '''
            You and your fellow kinsmen find yourselves in a magnificent hall set for 14, with
            a packed second floor overlooking the Athenians while you dined. As your compatriots
            sat down, they tore into the food. At the end of the hall, an open door marked 'maze' 
            stands agape like the mouth of a massive ocean beast. The rest seem to pay no mind to
            the looming entrance. 
            
                And you, adventurer?
            ''',
        "maze":
            '''
            Your group wandered through the maze, most unaware of your mission, and fewer unaware of 
            the string you had with you, slowly unfurling behind you all as you made your way through 
            that accursed maze. Some ran off, all were afraid. 
            
            But that's what bravery is, isn't it? 
            That despite fear, despite the odds being stacked against you, you rise to meet that enemy.
            However big, however fearsome...
            
                Care to wander more, adventurer?
            ''',
        "grate":
            '''
            After hours and hours of wall-tracing, you arrive at a strange room with a grate in the 
            center. There is a post at the doorway, and you tie off the clew that guided you this far.
            You approach the grate and peer down into its dark depths. You sense the void that lies
            behind the wrought-iron bars. You grab the bars and pull but the lock holds it fast. You look 
            around and see but a single door before you. The design of the hall, the placement of the 
            grate before the door, the placement of the door itself begs further inquiry. 
            
                Do you choose to go on, adventurer?
            ''',
        "spiderroom":
            '''
            Reaching out for the handle, you notice it. There is a fine web that sits on every square inch 
            of the heavy wooden door. Almost like something out of a fairy tale, the closer you look, the 
            more you discover. When you lift the handle, spiders scurry out from beneath their makeshift cover.
            As the door opens, a scene unlike any you have ever faced sits in front of you. 
            
            What appears to be an enormous dining hall, fit for kings and queens, lies...mostly, unoccupied 
            but clothed from arch to flagstone in dozen of different types of webs. Funnels, nets, balls. 
            And on this thick fog of silk, the thousands of spiders that called that agglomeration of web home. 
            
            There was, however, one problem. Other than the spiders. There was, on the other side of the dining 
            hall, through all the webs, through all the spiders, and all those legs, a door.
            
            A door, with a bright, shiny, untouched door handle. Glinting, almost teasing, from the other side 
            of the room. You know you'll never get through there in one piece or unbitten. There MUST be something
            you can use or have to keep the spiders at bay. But what?
            
                What say ye, adventurer?
            ''',
        "mirrorhall":
            '''
            
            ''',
        "keyroom":
            '''
            
            ''',
        "bull":
            '''
            
            ''',

    },
    "things": {
        "clew":
            '''
            The ball is off the softest material you've ever felt. She tells you it's made from a special silk,
            but says no more. You can tell that, despite the softness of feel, it is incredibly strong.
            
            "Sometimes finding your way back is harder than the journey itself. Hope this helps."
            ''',
        "key":
            '''
            The key, unassuming in appearance, hums slightly, imbued with the magic needed to unlock a magical
            lock. It's a bit rusty, a bit heavy, but overall not noticeably different from the hundreds of other
            keys you could have chosen. 
            ''',
        "bag":
            '''
            The bag given to you by the serving maid is leather, yet of a very high quality. Though you haven't seen
            many examples of such, it seems to be a magical item of some kind. 
            ''',
        "note":
            '''
            The note has but one hand-written line:
            
                Keep to the wall.
            ''',
    }
}
long_descriptions = {
    "locations": {
        "banquet":
            '''
            The tables are laden with the most succulent fruits, meats, and candies. The weary travelers lay waste to 
            the meal, ravenously tearing apart the display, knowing this might be their last meal. So concerned with the 
            food, they don't see the guards at all entrances. How peculiar, that the guards are on the inside of the 
            doors. Shouldn't guards be posted to stop people from coming in, you wonder? 
            
            You realize that this is not a welcoming party, but a fattening routine. 
            
            You and yours are being prepared like foie gras farms as tribute to the Minotaur, filling your stomachs 
            to transfer these delicious foods to the Beast of the Labyrinth. With this morbid realization at the 
            forefront of your mind, you eat in moderation, tempering your hunger with the gravity of the task ahead. 
            
            As you gaze around, a woman on the second floor catches your eye, staring intently at you while you eat. 
            A bit unnerving, but you HAVE all been reduced to fodder for the slaughterhouse. When you meet her gaze, 
            she holds it for a few seconds, then walks away. Shortly after the exchange, when more food is brought 
            out, one of the serving staff slips you a small bag and whispers, "Hide this, it's from her Highness." 
            You feel some sort of ball within, firm but yielding.  
            ''',
        "maze":
            '''
            You are the Child of the great King Aegeus. You have volunteered to end the culling of your brethren. Every 
            nine years, seven Athenian boys and seven Athenian girls are taken as tribute and left to die as feed for 
            the great beast of the Labyrinth, the Minotaur. As you stand at the entrance of the Maze, smooth walls 
            rising up 40 feet on each side, you worry about being unable to find your way through. You happen to spot a
            worn post by the entrance to the maze and wonder what its use could be. It strikes you that perhaps you can
            use the clew of yarn in your bag. You take it out and pull on it, testing its strength. Though it stretches 
            a bit, it doesn't break, even with a mighty pull. You tie one end of the clew to the post, unraveling it as 
            you and the other Athenians start the maze. 
            '''
    }
}
alt_descriptions = {
    "locations": {
        "grate":
            '''
            
            ''',
        "spiderroom":
            '''
            
            ''',
    }
}


def menu():
    print("-" * 30, "\n")
    print("Welcome to The Labyrinth, adventurer, a text-based adventure maze game by Justice Smith")
    print("-" * 30, "\n")
    print("\nFeel free to type 'help' at any time to check out the reference manual. Enjoy")
    print("-" * 30, "\n")

    print("-" * 30, "\n")
    print("MENU: (Choose a number from the following.)\n")
    print("\t1. New Game\n\t2. Load Game\n\t3. About")

    options = {1, 2, 3}
    choice = int(input("> "))

    while choice not in options:
        choice = int(input("Choose either 1, 2, or 3 from the menu options.\n> "))

    if choice == 1:
        player_data = {
            "name": None,
            "inventory": [],
            "current_loc": "banquet",
            "turns": 0,
        }
        name = input("Hello! It seems this is your first time playing this game. What is your name?\n> ")
        print(f"Welcome, {name}.")
        player_data["name"] = name
        return player_data

    elif choice == 2:
        player_data = pull_data()
        return player_data

    elif choice == 3:
        print("This game is cool. Tell your friends or you're a n00b4lyf3.\n")
        choice = input("Enter quit to leave the about page.\n> ")
        if choice == "quit":
            menu()
    else:
        print("That's not a valid response. Try 1, 2, or 3.")


def help_util(player_data):
    """
    This utility function returns a list of commands that can be implemented.
    """
    print("Hello. n00b. This is the help office. This is like passing your big brother the controller.\n"
          "Effective, but at what cost? Anyway, there are like... a LOT of commands you can do. Here they are:\n"
          f"\n\t{COMMANDS}\n")

    input("Press enter to continue.")
    start(player_data["current_loc"])


def get_action(player_data):
    single_kw = ('inventory', 'help', 'whereami', 'edit', 'exits')
    multi_kw = ('define', 'enter', 'examine', 'inspect')
    while True:
        command = input("\n> ").lower().split()
        if command:
            if command[0] == 'save':
                save(player_data)
                print("Game saved.\n")
            if len(command) == 2:
                if command[0] == 'define':
                    if command[1] in single_kw or command[1] in multi_kw:
                        return command
                    else:
                        print(f"You tried to find info on {command[1]}. That's not a command, "
                              "so I couldn't find more information on that keyword.")
                elif command[0] == 'enter':
                    if command[1] in LOCATIONS:
                        return command
                    else:
                        print("I'm sorry, I don't recognize that direction.")
                elif command[0] == 'examine':
                    if command[1] in long_descriptions["locations"]:
                        return command, player_data
                    else:
                        print("Examine what?")
                elif command[0] == 'inspect':
                    if command[1] in short_descriptions["things"]:
                        return command
                    else:
                        print("Inspect what?")
            elif len(command) == 1:
                if command[0] == 'inventory':
                    return command
                elif command[0] == 'help':
                    return command
                elif command[0] == 'whereami':
                    return command
                elif command[0] == 'edit':
                    return command
                elif command[0] == 'exits':
                    return command
                elif command[0] == 'stats':
                    return command
            else:
                print("I don't understand that instruction. Try another.")


def change_name(player_data):
    """
    This function allow you to change your name in the unfortunate incident that you
    fat-finger the keys. It's a nicety, really. Don't get too attached to a name.
    They're just abstract assignments, after all. Right, player_data["name"]?
    """
    new_name = input("What do you want to change your name to?\n> ")
    player_data["name"] = new_name
    print(f"Your name has now been set to {new_name}.")


def enter(destination, location):
    """
    This is the command that directs the changing of location.
    Your command should be of the form:

        > enter <location-name>

    to go to any of the possible rooms connected to your current location.
    """

    if destination in LOCATIONS[location]:
        start(destination)
        return destination

    else:
        print("You can't go that way.")


def start(location):
    if location in LOCATIONS.keys():
        if location in short_descriptions["locations"]:
            print(short_descriptions["locations"][location])
            visited[location] += 1
            print(visited)
    else:
        print("That's not a place you can go. Try somewhere else.")


def examine(location, player_data):
    """
    This function is specifically meant for calling descriptions of the player's current location.
    Your command should be of the form:

        > examine <location-name>

    to get a description of your current location and trigger events that may be hidden past a perfunctory room
    examination.
    """

    if location in LOCATIONS.keys() and player_data["current_loc"] == location:
        if location in long_descriptions["locations"]:
            print(long_descriptions["locations"][location])
            if location == 'banquet':
                keep('clew', player_data)
            if location == 'maze':
                remove('clew', player_data)
    else:
        print(f"There's not much more to the {location} than a name. Try somewhere else.")


def inspect(item, player_data):
    """
    This function is specifically meant for calling descriptions of an item you currently possesses.
    Your command should be of the form:

        >inspect <item-name>

    to get a description of the item and trigger any events that may be hidden past a perfunctory item examination.
    """

    if item in player_data["inventory"]:
        print(short_descriptions["things"][item])
    elif item == 'bag':
        print(short_descriptions["things"]["bag"])
    elif item in short_descriptions["locations"]:
        print("Try keyword 'examine' instead for locations.")
    else:
        print(f"What {item} are you even talking about?")


def keep(thing, player_data):
    player_data["inventory"].append(thing)


def remove(thing, player_data):
    player_data["inventory"].remove(thing)


def whereami(player_data):
    """
    This function is a tool for the player to recall their current location, for purposes of using that name
    as a command keyword for other functions.
    Your command should be of the form:

        > whereami

    to get a short line telling you where you are.
    """

    cur_loc = player_data["current_loc"]
    print(f"You are currently in {cur_loc}")


def exits(player_data):
    """
    This function returns the exits available for 'entering' from your current location.
    You command should be of the form:

        > exits

    to get a list of the location keywords usable with the 'enter' command.
    """
    exit_options = LOCATIONS[player_data["current_loc"]]
    print(f"Hm. It seems the exits available to you are: {exit_options}")


def define():
    """
    I made this function special for you just so I could put documentation
    telling you you're not a funny guy for putting 'define define'. Go slay
    the Minotaur or something.
    """


def stats(player_data):
    """
    This function shows the current player data that will be written
    to the save file should the player decide to save.
    Your command should be of the form:

        > stats

    to get a single line output showing your current game stats if a new game
    and your accumulated stats if you are returning from a previous game.
    """
    print(player_data)


def perform_action(command, player_data):
    if len(command) == 2:
        if command[0] == 'enter':
            player_data["current_loc"] = enter(command[1], player_data["current_loc"])
        elif command[0] == 'inspect':
            inspect(command[1], player_data)
        elif command[0] == 'examine':
            examine(command[1], player_data)
        elif command[0] == 'define':
            if command[1] == 'help':
                print(help_util.__doc__)
            elif command[1] == 'edit':
                print(change_name.__doc__)
            elif command[1] == 'save':
                print(save.__doc__)
            elif command[1] == 'enter':
                print(enter.__doc__)
            elif command[1] == 'examine':
                print(examine.__doc__)
            elif command[1] == 'inventory':
                print(inventory.__doc__)
            elif command[1] == 'define':
                print(define.__doc__)
    elif len(command) == 1:
        if command[0] == 'inventory':
            inventory(player_data)
        elif command[0] == 'help':
            help_util(player_data)
        elif command[0] == 'whereami':
            whereami(player_data)
        elif command[0] == 'edit':
            change_name(player_data)
        elif command[0] == 'keep':
            player_data["inventory"].append(command[1])
        elif command[0] == 'remove':
            player_data["inventory"].remove(command[1])
        elif command[0] == 'exits':
            exits(player_data)
        elif command[0] == 'stats':
            stats(player_data)
    else:
        print("Command not implemented.")


def save(player_data):
    """
    This function saves the current gamestate, including player name, inventory contents and current room.
    Your command should be of the form:

        > save

    to save the current game to the player_data.txt file.
    """

    with open("player_data.txt", "w") as f:
        print(player_data, file=f)


def pull_data():
    cur_file = open("player_data.txt", "r+")
    contents = cur_file.read()
    pulled_data = ast.literal_eval(contents)
    cur_file.close()
    return pulled_data


def death():
    print("Sadly, you died. So sad. I'm crying.\n")
    options = ["Y", "N"]
    choice = input("Would you like to restart from your last save point?\n(Y/N)> ")
    if choice == "Y":
        print("Alright, let's try this again.")
        for i in range(100):
            print("-" * 50, "\n")
        play(player_data=pull_data())

    elif choice == "N":
        print("Alright. Well, hope to see you soon! Goodbye.")
        sys.exit()
    while choice not in options:
        choice = input("You seem to have entered an invalid response. Try \"Y\" for 'yes' or \"N\" for 'no'.")


def inventory(player_data):
    i = player_data["inventory"]
    print(f"In your magical bag, you have: \n{i}.")


def play(player_data):
    alive = True
    game_over = False
    location = player_data["current_loc"]
    start(location)

    while not game_over:
        command = get_action(player_data)
        perform_action(command, player_data)
        player_data["turns"] += 1

    if not alive:
        death()
    else:
        turns = player_data["turns"]
        print(f"Congrats, you beat the game! It took you {turns} turns.")


def game():
    player_data = menu()
    play(player_data)


game()
