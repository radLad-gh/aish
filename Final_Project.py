# Justice Smith
# COP2930/Arup Guha
# 4.20.20
# Final Project

import ast
import sys
import time

COMMANDS = {'enter', 'examine', 'inventory', 'help', 'whereami', 'edit', 'exits', 'define', 'refresh', 'inspect'}

LOCATIONS = {
    "banquet": {"maze"},
    "maze": {"grate"},
    "grate": {"spiderroom", "bull"},
    "spiderroom": {"mirrorhall", "grate"},
    "mirrorhall": {"keyroom"},
    "keyroom": {"grate"},
    "bull": {"home"},
    "home": {None},
}

# I switched the movement system from being based around checking what items were in the bag to qualify user for a room
# to a series of counters that creates a predetermined adventure/not truly open world. It allows me to set item receipt/
# discard to be dependent on visits to the rooms, which triggered different narrative based on visit count.
visited = {
    "banquet": 0,
    "maze": 0,
    "grate": 0,
    "spiderroom": 0,
    "mirrorhall": 0,
    "keyroom": 0,
    "bull": 0,
    "home": 0,
}

# Found these dictionaries to be a nice narrative holder, especially with the auto indents.
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
            You are the child of the great King Aegeus. 
            
            You have volunteered to end the culling of your brethren. As divine punishment for killing a Cretan decades 
            ago, every nine years, seven Athenian boys and seven Athenian girls are taken as tribute and left to die as 
            feed for the great beast of the Labyrinth, the Minotaur. 
            
            As you stand at the entrance of the Maze, smooth stone walls rising up 40 feet on each side, you worry about 
            being unable to find your way through. You happen to spot a worn post by the entrance to the maze and 
            wonder what its use could be. It strikes you that perhaps you can use the clew of yarn in your bag. 
            You take it out and pull on it, testing its strength. Though it stretches a bit, it doesn't break, even
            with a mighty pull. You tie one end of the clew to the post, unraveling it as you and the other Athenians 
            start your way through the maze. 
            
            The stone walls hold no warmth, and as night falls, neither do you. You fear sleep, as you are certain
            it will lead to your demise by some creature of the Labyrinth. It was never mentioned in the myths that
            many monsters would come to call the Labyrinth home, wandering into it and remaining trapped or seeking it 
            out in the hopes of partaking in some of the tribute that would wander in periodically. Oh, and they would 
            eat each other. Times are tough, ya know? 
            
            You know that you have to move quickly so as to take advantage of the food, or else your strength will fail
            you before you reach the Minotaur. So you pick up your pace, albeit as quietly as possible, hoping the 
            mysterious woman's string can give you a way back. 
            
            After moving through the labyrinth for what felt like hours, you come upon a door, the first you've seen,
            with gold leaf inlaid in its surface. It is strange in its composition, being both very rugged in 
            construction yet gaudy in decoration. 
            ''',
        "grate":
            '''
            You staggered into this open room, tired and seeing nothing but the turns, left, right, left, right, 
            spinning through your weary mind. You've tied off to the post, closed the door behind you and now, leaning
            on that same door on whose sturdy construction you now rely to give you the rest you need, you sleep. You 
            have determined that will the grate locked, and you leaning on the entrance to the maze, you have time to 
            recuperate some of the energy you lost, partly through the emotional toll but mostly from the physical toll 
            of traversing the maze. 
            
            Z
            ZZ
            ZZZ
            ZZZZ
            ZZZZZ
            ZZZZZZ
            ZZZZZ
            ZZZZ
            ZZZ
            ZZ
            Z
            
            You wake up stiff, your sleep having been full of the things you hoped to escape for but a few minutes.
            Beast-men of lore, monsters you'd only heard told in stories to scare children, now they returned to 
            frighten you in your most helpless, vulnerable time, sleep. As you stretch and shake off the last wisps of
            dreams that cling to your mind, your gaze sharpens, returning to your task. You look around the room, 
            seeking progress, and your eyes fall upon a door across the grate. You approach the door, knowing that your
            path leads through it.
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
            ''',
        "mirrorhall":
            '''
            At first you are simply intrigued by this technology. You marvel at the craftsmanship, having thought it 
            impossible, or at least unheard of to create mirrors of this size. Upon examination of the mirrors, however,
            a small feeling of something being slightly off arises in the pit of your stomach. 
            
            The bare stone ceiling and floor yield no further clues so you are certain that the answer lies in these 
            gods-forsaken mirrors. You walk back and forth in front of them, seeking even the slightest information, 
            when you notice something on a mirror across the room. The trim on the sandals of the Theseus in the mirror 
            across the room is blue, while your own have a red trim. You only notice because these are your lucky 
            sandals, given to you on your 18th birthday when you also received your sword. You examine the mirror, 
            noting that nothing else seems to be out of place, then turn to the mirror next to it, looking for 
            something, anything. On that mirror, you notice that THAT version of you has a different sword at his side. 
            You know not what magic is on these mirrors, for they are not static, just different versions. The version
            of you in the mirror mimics your every move, with slight changes in each as far as clothes, mannerism, 
            aesthetic. 
            
            You step back now, hoping to gain some greater knowledge about the mirrors. At this point, however, your 
            mind has fixated on finding the flaws in reflection. The next mirror you lay eyes on, however, doesn't seem 
            to have one. You pore over it, looking for any tiny difference, but find none. Considering the nature of the
            room, you are sure that either you are missing the fault in the image or there is none. But, tired of the 
            games, you choose to destroy that mirror, hoping to reveal something more. 
            
            You crack the pommel of your sword on the surface of the mirror, causing the shards to fall and reveal a
            door. The door is small, creating an opening only large enough for one person to sidle in sideways. 
            ''',
        "keyroom":
            '''
            Knowing that there must be a way to find the right key, you persist in combing through the piles and
            piles of keys. There seems to be no difference to any of them, really, as far as uniqueness. They're just...
            plain old keys. Your eyes are swimming with keys, they're just blending together at this point. You've 
            looked in drawers, on hooks, under papers, underfoot, overhead, and nothing. You looked for a way out but 
            the only way in or out of this room appears to be the way you came in, through the mirror hall. As your hand
            passes over what feels like the millionth key, you see it. 
            
            A sun. 
            
            You fly toward it, not wanting to lose sight of it among the other nondescript keys around it. You're not 
            even sure how you were able to spot it but the key has a tiny sun engraved on the head. Almost scratched on,
            it appears to be fresh, as you can clearly distinguish the shiny metal from the scratched sun as newer than 
            the age of the surrounding unscratched metal. You are sure this is the key. Now, to use it on the right 
            lock. 
            
                Where to now, champion?
            ''',
        "bull":
            '''
            Taking a look around the room in what little light you have, you see this place almost as a cell. It is 
            cold, damp, simply a stone box with one way in and one way out. In fact, it seems almost reminiscent of the
            dungeons you heard of that are used in France called oubliettes. In these dungeons, there is a steep slope 
            down to a hole that connects the dungeon cell to the outside, creating a simple yet inescapable prison.
            
            As you stand there, in the flickering light of the torch, you wonder how you came to this moment. This 
            beast, how did he come to be here? 
                What is his story? 
                    Is this true Justice? 
                        Is this vengeance? 
                            Is the bull even to blame? 
                            
            You don't know the answers to these and other questions but for the moment, you know that  your people are 
            dying and that the Minotaur will surely kill you upon waking. With those two thoughts in mind, you know that
            certain decisions need be made by those with not enough time.  
            
            ''',
        "home":
            '''
            Home is...bittersweet. How can you celebrate knowing that your oversight caused the death of your father?
            Or that dozens of young Athenian boys and girls had been sent to slaughter before you made it to the 
            labyrinth to end the slaughter? These things and others turned the golds, whites, and purples of your 
            celebratory return into muted grays. You wanted to be joyful, like your citizens, even to revel in your own 
            victory, but alas, too much blood had been spilt in recent affairs for you to be ignorant of the loss of 
            life. 
            
            But for now, we drink and make merry. For the lives saved. 
            ''',

    }
}
short_descriptions = {
    "locations": {
        "banquet":
            '''
            You and your fellow kinsmen find yourselves in a magnificent hall set for 14, with
            a packed second floor overlooking yours while you dine. As your compatriots
            sit down, their hunger gets the best of them and they tear into the food. At the 
            end of the hall, an open door marked 'maze' stands agape like the mouth of a massive 
            ocean beast. The rest seem to pay no mind to the looming entrance. 
            
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
            The only door that leads forward is barely visible past the thick web that blocks your vision, not to 
            mention the literal creeping carpet of spiders covering every surface. This is surely an intentional 
            obstacle to whatever is beyond and, knowing by now that the Labyrinth was intentionally designed, you are
            sure that there is something to help you and ultimately, your people, beyond that door. But as you step 
            forward, the spiders too move forward, signalling your inability to pass. But how will you express that
            you mean them no harm?
            
                What say ye, adventurer?
            ''',
        "mirrorhall":
            '''
            Emboldened by the semblance of immunity the clew offered, you grab and pull that gleaming brass door handle,
            What you find behind the door is even wilder than the room you just overcame. 
            
            All you see is you. 
            Hundreds of 'you's.
            
            As you slowly step forward, you realize that these are nothing like the handmirrors you've seen maidens use 
            back home. These are monolithic versions, and too many of them to count. You consider using the pommel of 
            your sword to simply beat through them all and pass but are sure the noise will call a, if not the, beast.
            
                Your move, adventurer.
            
            ''',
        "keyroom":
            '''
            What you find before you is, quite simply, a workshop. Equipped with benches and tools of all kinds, this is
            like any workshop you'd find at home. 
            
            Except for one thing. Every possible surface is covered in keys of all kinds. Metal keys of all types of 
            metals and forms, wooden keys mixed among them.  You had neither the time nor the energy to pick the right 
            one from the milieu so moved to the nearest chair, swept the keys off, and sat to think. You realize that 
            you barely took time to notice anything about the lock affixing the grate door. Perhaps that would be a 
            good place to start.
            
                Where to now, adventurer?
                
            ''',
        "bull":
            '''
            You pull open the lock, remove it from the grate and carefully pull the grate open, revealing a hole with a
            ladder. The darkness in the hole is thick, like the thickest air you've ever felt slipping over your skin, 
            bringing with it hair-raising chills. As you pass down through the opening of the whole, it feels like the 
            Earth itself is swallowing you whole. 
            
            After what seems like an eternity of hand-over-hand down the ladder, your foot touches ground. And just as 
            it touches ground, a torch on a wall near you lights. The faint flickering glow of the torch plays along the
            stone floor, revealing just steps from the bottom of the ladder that same beast that terrorized your people 
            for so long, sleeping. 
            
            The Minotaur, head of a bull, body of a man, lies before you. 
            
            Though your journey was long, and your body is weary, you slowly unsheath your sword from its hiding place
            and thrust it home through the evil Beast. As the Beast falls limp, the remaining torches on the wall 
            illuminate, showing piles of bones stacked against the wall on every side, likely the bones of those who 
            came before you but were unlucky enough to encounter the Bull-man while he was awake. You stand, wiping off 
            your blade and preparing for the return home. No longer will your people be slaughtered by this beast. 
            
                Ready to go home, hero?
            ''',
        "home":
            '''
            You follow your string back through the maze, carrying nought but your sword, the head/neck of the Minotaur,
            and what is left of your life. You manage to escape and take a vessel back to your home in Athens but forget
            to raise a white sail to let Athens know of your victory and instead have the black sail you left with 
            hoisted. Your father, seeing the black sail and thinking his son is lost,casts himself off the castle 
            parapets into the sea below. Though you return as the new Ruler of Athens, Minotaur head trophy in tow, 
            you do so at great cost, having lost both those who went with you as well as your own father, the King of 
            Athens. 
            ''',

    },
    "things": {
        "clew":
            '''
            The ball is of the softest material you've ever felt. She tells you it's made from a special silk,
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
        "lock":
            '''
            You take the lock in your hand, noting its weight first, then its design. Heavy and minimalistic, the lock 
            is efficient and effective. You feel a slight bump on the back, prompting you to turn the lock over. A 
            small door sits on the back, with a point hinge holding it down. You slide the little door to the side on 
            the back of the lock revealing a small sun engraved on it. 
            '''
    }
}
alt_descriptions = {
    "locations": {
        "maze":
            '''
            With your mission to save your people at the forefront of your mind, you forsake but the minimum food 
            you think it will take to provide you the energy to fell the mighty beast and you set off for the maze.
            As you make your way through its twists and turns, you find no rhyme or reason to them, growing at
            first increasingly anxious for your companions who have by now all separated, with that anxiety then 
            turning to fear as you begin to hear the various screams from near and far signalling the deaths of those 
            from your homeland. 
            
            As you round yet another corner, you hear it. 
            A low chuff.
            
            The beast before is like nothing you could have imagined(as none return to tell the tale).
            With the body of a man and the head of a bull, he is a massive, hulking representation of both.
            Standing well over seven feet tall and composed of pure muscle, skin covered in what you assume
            is the blood of your kinsmen, he appears as a monster before you.
            
            As he bellows and charges, the distance between you seems much shorter than when you round the corner. 
            Perhaps that is the magic of the labyrinth. Regardless, you attempt to draw your weapon, barely getting
            it out of its sheath when the beast is upon you. In one fell swoop, the beast brings down its mighty
            fist and ends your tale. 
            ''',
        "grate4clew":
            '''
            You return to the room with the grate, wondering if there was something you were supposed to find in the 
            maze to help you vanquish the spiders. Nothing comes to mind. As you pace, you know that your time is 
            running out. 
 
            Sweeping your gaze around the room, you wonder if there is anything in that room itself capable of helping 
            you. The grate, the lock, the door, the post, the clew...wait.
            
            That string was unlike any other you'd ever encountered, fine like a web yet stronger than any man could 
            pull. Perhaps this is why that woman game you the clew, in the hopes that you'd hold on to it and have it \
            when you needed it the most. 
            
            You untie the silk from the post and bring it with you as you head back toward the spider room. 
            
                Onward, champion?
            ''',
        "spiderroom":
            '''
            You return to the room of spiders with yarn in hand, hoping for a miracle. Little did you know that this 
            simple string was crafted by the creator of the Labyrinth itself and passed down to your admirer to aid in
            your salvation. 
            
            Even as you enter the room, you notice the change. All the spiders, upon closer examination,
            are cutting their own webs and recrafting them to create a walkway through the room to the door. The sea of 
            spiders makes short work of the rearranging of furniture and in mere minutes you are able to continue to the 
            door at the other end of the hall. 
            
            You still step cautiously, keenly aware of the size of those pincers on that one over there, but make your
            way across the room. 
            
                And now, sword-swinger?
            ''',
        "grateWkey":
            '''
            Returning to the grate room, key in hand, you start to feel a swell of anticipatory energy. This is it.
            The moment on which your kingdom and countrymen are resting their hopes. You take out the key and fit it 
            to the lock. Despite the rust and ruggedness, there is clearly magic afoot. The locks are too smooth,
            the rooms too carefully crafted, to be accidental. There is surely a creator, a hand, someone behind the 
            curtain, directing the show. As you turn the key, the click of the lock seems to echo throughout the room,
            thunderously loud. The lock springs open.
            
                Into the deep, hero? 
            ''',
    }
}


# pulls needed info from txt file or creates game data for new player
def menu():
    print("-" * 30, "\n")
    print("Welcome to The Labyrinth, adventurer, a text-based adventure maze game by Justice Smith")
    print("-" * 30, "\n")
    print("\nFeel free to type 'help' at any time to check out the reference manual. Enjoy")
    print("-" * 30, "\n")
    print("-" * 30, "\n")
    print("MENU: (Choose a number from the following.)\n")
    print("\t1. New Game\n\t2. Load Game\n\t3. About")

    # foolproof* menu input
    option = (1, 2, 3)
    choice = 0
    while choice not in option:
        while True:
            try:
                choice = int(input("\nPlease enter 1, 2, or 3:\n> "))
                break
            except ValueError:
                choice = int(input("\nEnter only 1, 2, or 3:\n> "))
                break
    if choice == 1:
        player_data = {
            "name": None,
            "inventory": [],
            "current_loc": "banquet",
            "turns": 0,
            "game_over": 0,
            "alive": 1,
        }
        name = input("Hello! It seems this is your first time playing this game. What is your name?\n> ")
        print(f"Welcome, {name}.")
        player_data["name"] = name
        save(player_data)
        return player_data

    elif choice == 2:
        player_data = pull_data()
        return player_data

    elif choice == 3:
        print("This game is cool. Tell your friends or you're a n00b4lyf3.\n")
        input("Press enter to return to the menu.")
        menu()
    else:
        print("That's not a valid response. Try 1, 2, or 3.")


# This is a pseudo-interface. You can 'initialize' it and terminate it, refreshing state.
def help_util(player_data):
    """
    This utility function returns a list of commands that can be implemented.
    """
    print("Hello. n00b. This is the help office. This is like passing your big brother the controller.\n"
          "Effective, but at what cost? Anyway, there are like... a LOT of commands you can do.\n"
          "Note that \"> define <command>\" can be used to provide further information on any of the commands.\n"
          "Here they are:\n"
          f"\n\t{COMMANDS}\n")
    # No penalty for asking for help
    if player_data["turns"] == 0:
        pass
    else:
        player_data["turns"] -= 1


# This is my getter. Care was taken in being surgical about the selection of functions called in this section.
def get_action(player_data):
    single_kw = ('inventory', 'help', 'whereami', 'edit', 'exits', 'refresh')
    multi_kw = ('define', 'enter', 'examine', 'inspect')
    while True:
        turns = player_data["turns"]
        command = input(f"Turns taken:{turns}\n\n\t> ").lower().split()
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
                        return command
                    else:
                        print("Examine what?")
                elif command[0] == 'inspect':
                    if command[1] in short_descriptions["things"]:
                        return command
                    else:
                        print("Inspect what?")
                else:
                    print("That is not a command string this game understands. Enter 'help' for more information.")
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
                elif command[0] == 'refresh':
                    return command
                else:
                    print("That is not a command string this game understands. Enter 'help' for more information.")
            else:
                print("That is not a command string this game understands. Enter 'help' for more information.")


# Convenient utility for user to change the character name should a typo be typed.
def change_name(player_data):
    """
    This function allow you to change your name in the unfortunate incident that you
    fat-finger the keys. It's a nicety, really. Don't get too attached to a name.
    They're just abstract assignments, after all. Right, player_data["name"]?
    """
    new_name = input("What do you want to change your name to?\n> ")
    player_data["name"] = new_name
    print(f"Your name has now been set to {new_name}.")


# User-level utility for changing location
def enter(destination, player_data):
    """
    This is the command that directs the changing of location.
    Your command should be of the form:

        > enter <location-name>

    to go to any of the possible rooms connected to your current location.
    """
    # Stopping bad destinations early
    if destination in LOCATIONS[player_data["current_loc"]]:
        new_loc = start(destination, player_data)
        return new_loc

    else:
        print("You can't go that way.")
        return player_data["current_loc"]


# The heavy lifting behind 'enter' and some other use(menu)
def start(location, player_data):
    if location in LOCATIONS.keys():
        # A classic must-have: the death sequence.
        if location == 'maze' and 'clew' not in player_data["inventory"]:
            print(alt_descriptions["locations"]["maze"])
            input("You enter the void. Press enter to continue.")
            player_data["game_over"] = 1
            player_data["alive"] = 0
        elif location == 'grate':
            # Switched to visit-counter based movement function.
            if visited["grate"] == 0:
                print(short_descriptions["locations"][location])
                visited[location] += 1
                remove('clew', player_data)
                return location
            elif visited["grate"] == 1:
                print(alt_descriptions["locations"]["grate4clew"])
                visited[location] += 1
                keep('clew', player_data)
                return location
            elif visited["grate"] == 2 and visited["keyroom"]  == 1:
                print(short_descriptions["locations"][location])
                print(short_descriptions["things"]["lock"])
                LOCATIONS["grate"] = {'keyroom', 'bull'}
                visited[location] += 1
                return location
            elif visited["grate"] >= 3 and visited["keyroom"] >= 2:
                print(alt_descriptions["locations"]["grateWkey"])
                visited[location] += 1
                remove('key', player_data)
                return location
            else:
                print("What are you doing in here again? Scram!\n\n You are sent scurrying back to your last room.")
                refresh(player_data)
                # Force-resets the player location for errors
                return player_data["current_loc"]
        elif location == 'spiderroom':
            if visited["spiderroom"] == 0:
                print(short_descriptions["locations"][location])
                visited[location] += 1
                return location
            elif visited["spiderroom"] == 1:
                print(alt_descriptions["locations"]["spiderroom"])
                visited[location] += 1
                return location
            else:
                print("Nothing more to see here, no matter how many eyes.")
                return player_data["current_loc"]
        elif location == 'mirrorhall' and visited["grate"] == 1:
            print("You couldn't possibly get through all those spiders.")
            return player_data["current_loc"]
        elif location == 'keyroom':
            if visited["keyroom"] == 0:
                print(short_descriptions["locations"][location])
                visited[location] += 1
                return location
            elif visited["keyroom"] == 1:
                print(long_descriptions["locations"][location])
                visited[location] += 1
                keep('key', player_data)
                return location
            else:
                print("What else could you want in there?")
                return player_data["current_loc"]
        elif location == 'bull' and visited["keyroom"] < 2:
            print("The lock is too strong. You cannot enter.")
            return player_data["current_loc"]
        elif location == 'home':
            print(short_descriptions["locations"][location])
            player_data["game_over"] = 1
            return location
        # All but the above exceptions
        else:
            print(short_descriptions["locations"][location])
            visited[location] += 1
            return location
    else:
        print("That's not a place you can go. Try somewhere else.")


# Location-specific
def examine(location, player_data):
    """
    This function is specifically meant for calling descriptions of the player's current location.
    Your command should be of the form:

        > examine <location-name>

    to get a description of your current location and trigger events that may be hidden past a perfunctory room
    examination.
    """
    # You can only examine where you are right now because examine triggers other functions.
    if location in LOCATIONS and player_data["current_loc"] == location:
        if location in long_descriptions["locations"]:
            print(long_descriptions["locations"][location])
            if location == 'banquet':
                keep('clew', player_data)
        elif location in long_descriptions["things"]:
            print("Try keyword 'inspect' instead for items.")
        else:
            print(f"There's not much more to the {location} than a name. Try somewhere else.")
    else:
        print("You can't really examine somewhere you aren't, can you?")


# Item-specific
def inspect(item, player_data):
    """
    This function is specifically meant for calling descriptions of an item you currently possesses.
    Your command should be of the form:

        >inspect <item-name>

    to get a description of the item and trigger any events that may be hidden past a perfunctory item examination.
    """

    if item in player_data["inventory"]:
        if item == 'key' and visited["keyroom"] >= 1:
            print(short_descriptions["things"][item])
        else:
            print(short_descriptions["things"][item])
    elif item == 'bag':
        print(short_descriptions["things"][item])
    elif item == 'lock' and player_data["current_loc"] == 'grate':
        print(short_descriptions["things"][item])
    elif item in short_descriptions["locations"]:
        print("Try keyword 'examine' instead for locations.")
    else:
        print(f"What {item} are you even talking about?")


# Hidden utility for adjusting player inventory
def keep(thing, player_data):
    player_data["inventory"].append(thing)


# Hidden utility for adjusting player inventory
def remove(thing, player_data):
    player_data["inventory"].remove(thing)


# Convenient tool for player(thinking about auto printing this under turn count)
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


# Fancy lil thang to print handy docstrings(I pretty much used development of this to learn docstrings)
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


# Streamlined, non variable affecting version of start. Very useful for saving 'visited[""] +=' lines
def refresh(player_data):
    """
    This function provides the player the ability to reprint the current room information.
    Your command should be of the form:

        > refresh

    to print to screen the narrative for the current area.
    """
    cur_loc = player_data["current_loc"]
    print(short_descriptions["locations"][cur_loc])


# Command sorting
def perform_action(command, player_data):
    # print(command); this is a diag line to split the engine.
    if command[0] == 'enter':
        player_data["current_loc"] = enter(command[1], player_data)
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
        elif command[1] == 'refresh':
            print(refresh.__doc__)
        elif command[1] == 'inspect':
            print(inspect.__doc__)
        elif command[1] == 'exits':
            print(exits.__doc__)
    elif command[0] == 'inventory':
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
    elif command[0] == 'refresh':
        refresh(player_data)
    else:
        print("Command not implemented.")


# Could be more useful in game expansion; note use of ast.literal, it's pretty handy
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
    choice = input("Would you like to restart ?\n(Y/N)> ").strip().lower()
    if choice == "y":
        print("Alright, let's try this again.")
        for i in range(50):
            print(i * "  " + "    ~.")
            print(i * "  " + "    /|")
            print(i * "  " + "   / |")
            print(i * "  " + "  /__|__")
            print(i * "  " + "\\--------/")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            time.sleep(.15)
        # Resetting room visit counts
        for k in visited:
            visited[k] = 0

        game()

    elif choice == "n":
        print("Alright. Well, hope to see you soon! Goodbye.")
        sys.exit()
    while choice not in options:
        choice = input("\nYou seem to have entered an invalid response. Try \"Y\" for 'yes' or \"N\" for 'no'.")


def inventory(player_data):
    """
    This function shows the contents of the player's inventory.
    Your command should be of the form:

        > inventory

    to get a single line output showing your current inventory.
    """
    i = player_data["inventory"]
    print(f"In your magical bag, you have: \n{i}.")


def play(player_data):
    alive = True
    game_over = False
    location = player_data["current_loc"]
    start(location, player_data)

    while not game_over:
        try:
            command = get_action(player_data)
            perform_action(command, player_data)
            player_data["turns"] += 1
            print(visited)
            if player_data["game_over"] == 1:
                game_over = True
            if player_data["alive"] == 0:
                alive = False
        except ValueError:
            print("Ooh, that's a nasty error. Let's try to avoid that one.")
    if not alive:
        death()
    else:
        turns = player_data["turns"]
        print(f"Congrats, you beat the game! It took you {turns} turns.")


def game():
    # I split the game into two parts: data-pulling and game execution with data pulled.
    player_data = menu()
    play(player_data)


game()
