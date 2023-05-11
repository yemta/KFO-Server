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

gokudrip = """
wait#280#%
BN#OCCourtSky#%
/play_once https://cdn.discordapp.com/attachments/657301457086840837/1090753556237266954/Official_Goku_Drip_Theme_-_Ultra_Dripstinct.mp3 %
MS#1#-#Phoenix#confident# #def#1#0#0#0#0#0#0#0#0#Phoenix#-1###0<and>0#0#0#0#0#0#-^(b)confident^(a)confident^#-^(b)confident^(a)confident^#-^(b)confident^(a)confident^#0#dbzteleport||dbz-teleport#%
wait#2500#%
BN#OCCourtSky#%
MS#1#hat#Hershel#hat# #pro#1#0#6#0#0#0#1#0#0#Layton#-1###0<and>0#0#0#0#0#0#hat^(b)hat^(a)hat^#hat^(b)hat^(a)hat^#hat^(b)hat^(a)hat^#0#dbzteleport||dbz-teleport#%
wait#2300#%
BN#OCCourtSky#%
MS#1#-#Phoenix_SOJ_Wit#stern# #jud#1#0#0#0#0#0#0#0#0#Phoenix?#-1###0<and>0#0#0#0#0#0#-^(b)stern^(a)stern^#-^(b)stern^(a)stern^#-^(b)stern^(a)stern^#0#dbzteleport||dbz-teleport#%
wait#2300#%
BN#OCCourtSky#%
MS#1#mladytipper#Hershel_Pro#mlady# #wit#1#0#6#0#0#0#0#0#0#Layton?#-1###0<and>0#0#0#0#0#0#mladytipper^(b)mlady^(a)mlady^#mladytipper^(b)mlady^(a)mlady^#mladytipper^(b)mlady^(a)mlady^#0#dbzteleport||dbz-teleport#%
wait#2500#%
BN#OCWhiteRoom#%
MS#0#puzzlewin-layton-pre#Phoenix_PLvsAA#puzzlewin-layton#~~}}}By any means necessary. By any means necessary. By any means necessary. By any means necessary. By any means necessary.#def#1#0#0#1#0#0#0#0#0#HYPEBEAST PHOENIX AND LAYTON#-1###0<and>0#0#0#0#0#0#puzzlewin-layton-pre^(b)puzzlewin-layton^(a)puzzlewin-layton^#puzzlewin-layton-pre^(b)puzzlewin-layton^(a)puzzlewin-layton^#puzzlewin-layton-pre^(b)puzzlewin-layton^(a)puzzlewin-layton^#0#slash||sfx-slash#%
"""

def ooc_cmd_emoji(client, arg):
    """
    Activate or Deactivate emoji mode.
    Usage: /emoji
    """
    if client.emoji:
        client.emoji = False
        client.send_ooc("Emoji Mode DEACTIVATED.")
    else:
        client.emoji = True
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

    for c in targets:
        if not c.emoji:
            c.emoji = True
        if c.dank:
            c.dank = False
            c.emoji = False
        else:
            c.dank = True

    if client.dank:
        ann = f"AREA {client.area.id} DRIP STATUS:\nGOATED WITH THE SAUCE"
        client.area.name = "HYPERBOLIC SWAG CHAMBER"
        client.area.status = "DRIPPED OUT OF THEIR MINDS\n"
        client.area.background = "OCCourtInverted"
        client.area.area_manager.broadcast_area_list()
        client.area.evi_list.add_evidence(client, "Goku's Drip", 
                                          gokudrip, 
                                          "JFAMoney.png", "all")      
        client.area.broadcast_evidence_list()
        commands.call(client, "demo", "Goku's Drip")
        for c in targets:
            c.used_showname_command = True
            c.showname = f"HYPEBEAST-{c.char_name.upper()}"      
        client.send_ooc("Dank Mode ACTIVATED.")
    else:
        ann = f"AREA {client.area.id} DRIP STATUS:\nNONE, COMPLETELY DRY"
        client.area.name = client.area.o_name
        client.area.status = "IDLE"
        client.area.background = client.area.o_background
        client.area.area_manager.broadcast_area_list()
        client.area.play_music("[Misc] Record Scratch", "0", 0, "Reality", 0)
        commands.call(client, "evidence_remove", "Goku's Drip")
        client.area.broadcast_evidence_list()
        client.area.stop_demo()
        for c in targets:
            c.used_showname_command = False
            c.showname = ""     
        client.send_ooc(f"Dank Mode DEACTIVATED.")

    client.server.send_all_cmd_pred(
        "CT",
        client.server.config["hostname"],
        f"==== ALERT ====\r\n{ann}\r\n=================",
        "1",
    )
