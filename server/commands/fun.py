from server import database
from server.constants import TargetType
from server.exceptions import ClientError, ArgumentError

from . import mod_only

__all__ = [
    "ooc_cmd_disemvowel",
    "ooc_cmd_undisemvowel",
    "ooc_cmd_shake",
    "ooc_cmd_unshake",
    "ooc_cmd_gimp",
    "ooc_cmd_ungimp",
    "ooc_cmd_washhands",
    "ooc_cmd_rainbow",
    "ooc_cmd_emoji",
    "ooc_cmd_dank",
]


@mod_only()
def ooc_cmd_disemvowel(client, arg):
    """
    Remove all vowels from a user's IC chat.
    Usage: /disemvowel <id>
    """
    if len(arg) == 0:
        raise ArgumentError("You must specify a target.")
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False
        )
    except Exception:
        raise ArgumentError("You must specify a target. Use /disemvowel <id>.")
    if targets:
        for c in targets:
            database.log_area("disemvowel", client, client.area, target=c)
            c.disemvowel = True
        client.send_ooc(f"Disemvowelled {len(targets)} existing client(s).")
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_undisemvowel(client, arg):
    """
    Give back the freedom of vowels to a user.
    Usage: /undisemvowel <id>
    """
    if len(arg) == 0:
        raise ArgumentError("You must specify a target.")
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False
        )
    except Exception:
        raise ArgumentError(
            "You must specify a target. Use /undisemvowel <id>.")
    if targets:
        for c in targets:
            database.log_area("undisemvowel", client, client.area, target=c)
            c.disemvowel = False
        client.send_ooc(f"Undisemvowelled {len(targets)} existing client(s).")
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_shake(client, arg):
    """
    Scramble the words in a user's IC chat.
    Usage: /shake <id>
    """
    if len(arg) == 0:
        raise ArgumentError("You must specify a target.")
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False
        )
    except Exception:
        raise ArgumentError("You must specify a target. Use /shake <id>.")
    if targets:
        for c in targets:
            database.log_area("shake", client, client.area, target=c)
            c.shaken = True
        client.send_ooc(f"Shook {len(targets)} existing client(s).")
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_unshake(client, arg):
    """
    Give back the freedom of coherent grammar to a user.
    Usage: /unshake <id>
    """
    if len(arg) == 0:
        raise ArgumentError("You must specify a target.")
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False
        )
    except Exception:
        raise ArgumentError("You must specify a target. Use /unshake <id>.")
    if targets:
        for c in targets:
            database.log_area("unshake", client, client.area, target=c)
            c.shaken = False
        client.send_ooc(f"Unshook {len(targets)} existing client(s).")
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_gimp(client, arg):
    """
    Replace a user's message with a random message from a list.
    Usage: /gimp <id>
    """
    if len(arg) == 0:
        raise ArgumentError('You must specify a target ID.')
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False)
    except Exception:
        raise ArgumentError('You must specify a target. Use /gimp <id>.')
    if targets:
        for c in targets:
            database.log_misc('gimp', client, target=c, data=client.area.abbreviation)
            c.gimp = True
        client.send_ooc(f'Gimped {len(targets)} existing client(s).')
    else:
        client.send_ooc('No targets found.')

@mod_only()
def ooc_cmd_ungimp(client, arg):
    """
    Allow the user to send their own messages again.
    Usage: /ungimp <id>
    """
    if len(arg) == 0:
        raise ArgumentError('You must specify a target ID.')
    try:
        targets = client.server.client_manager.get_targets(
            client, TargetType.ID, int(arg), False)
    except Exception:
        raise ArgumentError('You must specify a target. Use /ungimp <id>.')
    if targets:
        for c in targets:
            database.log_misc('ungimp', client, target=c, data=client.area.abbreviation)
            c.gimp = False
        client.send_ooc(f'Ungimped {len(targets)} existing client(s).')
    else:
        client.send_ooc('No targets found.')


def ooc_cmd_washhands(client, arg):
    """
    Stay safe!
    Usage: /washhands
    """
    client.send_ooc('You washed your hands!')


def ooc_cmd_rainbow(client, arg):
    """
    Activate or Deactivate rainbow text.
    Usage: /rainbow
    """
    if client.rainbow:
        client.rainbow = False
        client.send_ooc("Rainbow Mode DEACTIVATED.")
    else:
        client.rainbow = True
        client.send_ooc(f"Rainbow Mode ACTIVATED.")

def ooc_cmd_emoji(client, arg):
    """
    Activate or Deactivate emoji mode.
    Usage: /emoji
    """
    if client.dank:
        client.dank = False
        client.send_ooc("Emoji Mode DEACTIVATED.")
    else:
        client.dank = True
        client.send_ooc(f"Emoji Mode ACTIVATED.")

@mod_only()
def ooc_cmd_dank(client, arg):
    """
    Activate or Deactivate full dank mode for the area.
    Warning: this is an absolute God-defying clusterfuck of a mess.
    Usage: /dank
    """
    from server import commands
    targets = [c for c in client.area.clients]
    ann = "bussin"
    drip = "https://cdn.discordapp.com/attachments/657301457086840837/1090753556237266954/Official_Goku_Drip_Theme_-_Ultra_Dripstinct.mp3"

    for c in targets:
        if c.dank:
            c.dank = False
        else:
            c.dank = True

    if client.dank:
        ann = f"AREA {client.area.id} DRIP STATUS:\nGOATED WITH THE SAUCE"
        client.area.play_music(drip, "0", 0, "Hypebeast Goku", 0)
        
        client.area.evi_list.add_evidence(client, "Goku's Drip", 
                                          "MS#chat#-#Hatch#Gunshot##wit#et-gunshot-2#0#29#1#0#0#0#0#0# #-1###0&0#0#0#0#0#0#-^(b)Gunshot^(a)Gunshot^#-^(b)Gunshot^(a)Gunshot^#-^(b)Gunshot^(a)Gunshot^#0#||#%", 
                                          "JFAMoney.png", "all")      
        client.area.broadcast_evidence_list()
        commands.call(client, "demo", "Goku's Drip")
        c.used_showname_command = True
        c.showname = f"HYPEBEAST-{c.char_name.upper()}"
        
        client.send_ooc("Dank Mode ACTIVATED.")
    else:
        ann = f"AREA {client.area.id} DRIP STATUS:\nNONE, COMPLETELY DRY"
        client.area.play_music("[Misc] Record Scratch", "0", 0, "Regular Goku", 0)

        commands.call(client, "evidence_remove", "Goku's Drip")
        client.area.broadcast_evidence_list()
        c.used_showname_command = False
        c.showname = ""
        
        client.send_ooc(f"Dank Mode DEACTIVATED.")

    client.server.send_all_cmd_pred(
        "CT",
        client.server.config["hostname"],
        f"==== ALERT ====\r\n{ann}\r\n=================",
        "1",
    )
