import shlex

from server import database
from server.constants import TargetType
from server.exceptions import ClientError, ArgumentError, AreaError

from . import mod_only

__all__ = [
    "ooc_cmd_bg",
    "ooc_cmd_bgs",
    "ooc_cmd_status",
    "ooc_cmd_allow_blankposting",
    "ooc_cmd_allow_showname",
    "ooc_cmd_allow_iniswap",
    "ooc_cmd_area",
    "ooc_cmd_area_visible",
    "ooc_cmd_autogetarea",
    "ooc_cmd_getarea",
    "ooc_cmd_getareas",
    "ooc_cmd_getafk",
    "ooc_cmd_invite",
    "ooc_cmd_uninvite",
    "ooc_cmd_area_kick",
    "ooc_cmd_pos_lock",
    "ooc_cmd_pos_lock_clear",
    #"ooc_cmd_knock",
    #"ooc_cmd_peek",
    "ooc_cmd_max_players",
    "ooc_cmd_desc",
    "ooc_cmd_edit_ambience",
    "ooc_cmd_lights",
    "ooc_cmd_link",
    "ooc_cmd_removelink",
    "ooc_cmd_update",
]


def ooc_cmd_bg(client, arg):
    """
    Set the background of an area.
    Usage: /bg <background>
    """
    if len(arg) == 0:
        pos_lock = ""
        if len(client.area.pos_lock) > 0:
            pos = ", ".join(str(lpos) for lpos in client.area.pos_lock)
            pos_lock = f"\nAvailable positions: {pos}."
        client.send_ooc(
            f"Current background is {client.area.background}.{pos_lock}")
        return
    if client not in client.area.owners and not client.is_mod and client.area.bg_lock:
        raise AreaError("This area's background is locked!")
    if client.area.cannot_ic_interact(client):
        raise AreaError("You are not on the area's invite list!")
    if (
        not client.is_mod
        and not (client in client.area.owners)
        and client.char_id == -1
    ):
        raise ClientError("You may not do that while spectating!")
    if client.area.dark and not client.is_mod and not (client in client.area.owners):
        raise ClientError("You must be authorized to do that.")
    try:
        client.area.change_background(arg)
    except AreaError:
        raise
    client.area.broadcast_ooc(
        f"{client.char_name} changed the background to {arg}.")
    database.log_area("bg", client, client.area, message=arg)


def ooc_cmd_bgs(client, arg):
    """
    Display the server's available backgrounds.
    Usage: /bgs
    """
    msg = "Available backgrounds:"
    msg += "\n" + "; ".join(client.server.backgrounds)
    client.send_ooc(msg)


def ooc_cmd_status(client, arg):
    """
    Show or modify the current status of an area.
    Usage: /status <idle|rp|casing|looking-for-players|lfp|recess|gaming|standby|building>
    """
    if not client.area.area_manager.arup_enabled:
        raise AreaError("This hub does not use the /status system.")
    if len(arg) == 0:
        client.send_ooc(f"Current status: {client.area.status}")
    else:
        if (
            not client.area.can_change_status
            and not client.is_mod
            and client not in client.area.owners
        ):
            raise AreaError(
                "This area's status cannot be changed by anyone who's not a CM or mod!"
            )
        if client.area.cannot_ic_interact(client):
            raise AreaError("You are not on the area's invite list!")
        if (
            not client.is_mod
            and client not in client.area.owners
            and client.char_id == -1
        ):
            raise ClientError("You may not do that while spectating!")
        try:
            client.area.change_status(arg)
            client.area.broadcast_ooc(
                "{} changed status to {}.".format(
                    client.char_name, client.area.status)
            )
            database.log_area("status", client, client.area, message=arg)
        except AreaError:
            raise


@mod_only(area_owners=True)
def ooc_cmd_allow_blankposting(client, arg):
    """
    Toggle whether or not in-character messages purely consisting of spaces are allowed.
    Usage: /allow_blankposting
    """
    client.area.blankposting_allowed = not client.area.blankposting_allowed
    answer = 'allowed' if client.area.blankposting_allowed else 'forbidden'
    client.area.broadcast_ooc(
        '{} [{}] has set blankposting in the area to {}.'.format(
            client.char_name, client.id, answer))
    database.log_area('blankposting', client, client.area, message=client.area.blankposting_allowed)


@mod_only()
def ooc_cmd_allow_showname(client, arg):
    """
    Toggle whether or not users can use shownames in the current area.
    Usage: /allow_showname
    """
    client.area.showname_changes_allowed = not client.area.showname_changes_allowed
    answer = 'allowed' if client.area.showname_changes_allowed else 'forbidden'
    client.area.broadcast_ooc(
        '{} [{}] has set showname usage in the area to {}.'.format(
            client.char_name, client.id, answer))
    database.log_area('shownames', client, client.area, message=client.area.showname_changes_allowed)


@mod_only()
def ooc_cmd_allow_iniswap(client, arg):
    """
    Toggle whether or not users are allowed to swap INI files in character
    folders to allow playing as a character other than the one chosen in
    the character list.
    Usage: /allow_iniswap
    """
    client.area.iniswap_allowed = not client.area.iniswap_allowed
    answer = 'allowed' if client.area.iniswap_allowed else 'forbidden'
    client.send_ooc(f'Iniswap is {answer}.')
    database.log_area('iniswap', client, client.area, message=client.area.iniswap_allowed)


def ooc_cmd_area(client, arg):
    """
    List areas, or go to another area.
    Usage: /area [id] or /area [name]
    """
    if arg == "":
        client.send_area_list(
            full=client.is_mod or client in client.area.owners)
        return

    try:
        for area in client.area.area_manager.areas:
            a = arg.split(" ")[0]
            aid = a.strip("[]")
            if (
                (
                    a.startswith("[")
                    and a.endswith("]")
                    and aid.isdigit()
                    and area.id == int(aid)
                )
                or area.name.lower() == arg.lower()
                or area.abbreviation == arg
                or (arg.isdigit() and area.id == int(arg))
            ):
                client.change_area(area)
                return
        raise AreaError("Targeted area not found!")
    except ValueError:
        raise ArgumentError(
            "Area ID must be a name, abbreviation or a number.")
    except (AreaError, ClientError):
        raise


def ooc_cmd_area_visible(client, arg):
    """
    Display only linked and non-hidden areas. Useful to GMs.
    Usage: /area_visible
    """
    if arg != "":
        raise ArgumentError("This command takes no arguments!")
    client.send_area_list(full=False)


def ooc_cmd_autogetarea(client, arg):
    """
    Automatically /getarea whenever you enter a new area
    Usage: /autogetarea
    """
    client.autogetarea = not client.autogetarea
    toggle = "enabled" if client.autogetarea else "disabled"
    client.send_ooc(
        f"You have {toggle} automatic /getarea."
    )


def ooc_cmd_getarea(client, arg):
    """
    Show information about the current area, or target area id with sufficient permissions.
    Usage: /getarea [id]
    """
    aid = client.area.id
    if arg.strip().isnumeric():
        area = client.area.area_manager.get_area_by_id(int(arg))
        aid = int(arg)
    client.send_area_info(aid)


def ooc_cmd_getareas(client, arg):
    """
    Show information about all areas.
    Usage: /getareas
    """
    client.send_areas_clients()


def ooc_cmd_getafk(client, arg):
    """
    Show currently AFK-ing players in the current area or in all areas.
    Usage: /getafk [all]
    """
    if arg == "all":
        arg = -1
    elif len(arg) == 0:
        arg = client.area.id
    else:
        raise ArgumentError("There is only one optional argument [all].")
    client.send_area_info(arg, afk_check=True)


@mod_only(area_owners=True)
def ooc_cmd_invite(client, arg):
    """
    Allow a particular user to join a locked or speak in spectator-only area.
    ID can be * to invite everyone in the current area.
    Usage: /invite <id>
    """
    if not arg:
        msg = "Current invite list:\n"
        msg += "\n".join(
            [
                f"[{c.id}] {c.char_name}"
                for c in client.server.client_manager.clients
                if c.id in client.area.invite_list
            ]
        )
        msg += "\nUse /invite <id> to invite someone."
        client.send_ooc(msg)
        return

    args = arg.split(" ")

    try:
        if args[0] == "*":
            targets = [
                c
                for c in client.area.clients
                if c != client and c != client.area.owners
            ]
        else:
            targets = client.server.client_manager.get_targets(
                client, TargetType.ID, int(args[0]), False
            )
    except ValueError:
        raise ArgumentError("Area ID must be a number or *.")

    try:
        for c in targets:
            client.area.invite_list.add(c.id)
            client.send_ooc(f"{c.char_name} is invited to your area.")
            c.send_ooc(
                f"You were invited and given access to {client.area.name}.")
            database.log_area("invite", client, client.area, target=c)
    except Exception:
        raise ClientError("You must specify a target. Use /invite <id>")


@mod_only(area_owners=True)
def ooc_cmd_uninvite(client, arg):
    """
    Revoke an invitation for a particular user.
    ID can be * to uninvite everyone in the area.
    Usage: /uninvite <id>
    """
    if not arg:
        raise ClientError("You must specify a target. Use /uninvite <id>")
    args = arg.split(" ")
    try:
        if args[0] == "*":
            targets = [
                c
                for c in client.area.clients
                if c != client and c != client.area.owners
            ]
        else:
            targets = client.server.client_manager.get_targets(
                client, TargetType.ID, int(args[0]), False
            )
    except ValueError:
        raise ArgumentError("Area ID must be a number or *.")

    if targets:
        try:
            for c in targets:
                client.send_ooc(
                    "You have removed {} from the whitelist.".format(
                        c.char_name)
                )
                c.send_ooc("You were removed from the area whitelist.")
                database.log_area("uninvite", client, client.area, target=c)
                client.area.invite_list.discard(c.id)
        except AreaError:
            raise
        except ClientError:
            raise
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_area_kick(client, arg):
    """
    Remove a user from the current area and move them to another area.
    If id is a * char, it will kick everyone but you and CMs from current area to destination.
    If id is **, it will kick everyone including CM's from current area to destination.
    If id is ***, it will kick everyone in the hub to destination.
    If id is afk, it will only kick all the afk people.
    If the destination is not specified, the destination defaults to your current area.
    target_pos is the optional position that everyone should end up in when kicked.
    Usage: /area_kick <id> [destination] [target_pos]
    """
    if not arg:
        raise ClientError(
            "You must specify a target. Use /area_kick <id> [destination] [target_pos]"
        )

    args = shlex.split(arg)

    # Kick everyone but AFKers
    if args[0] == "afk":
        targets = client.server.client_manager.get_targets(
            client, TargetType.AFK, args[0], False
        )
    # Kick everyone but owners
    elif args[0] == "*":
        targets = [
            c
            for c in client.area.clients
            if c != client and c != client.area.owners
        ]
    # Kick everyone in area
    elif args[0] == "**":
        targets = [
            c
            for c in client.area.clients
        ]
    # Kick everyone in hub
    elif args[0] == "***":
        targets = [
            c
            for c in client.area.area_manager.clients
        ]
    else:
        # Try to find by char name first
        targets = client.server.client_manager.get_targets(
            client, TargetType.CHAR_NAME, args[0]
        )
        # If that doesn't work, find by client ID
        if len(targets) == 0 and args[0].isdigit():
            targets = client.server.client_manager.get_targets(
                client, TargetType.ID, int(args[0])
            )
        # If that doesn't work, find by OOC Name
        if len(targets) == 0:
            targets = client.server.client_manager.get_targets(
                client, TargetType.OOC_NAME, args[0]
            )

    if len(targets) == 0:
        client.send_ooc(
            f"No targets found by search term '{args[0]}'."
        )
        return

    try:
        for c in targets:
            # We're a puny CM, we can't do this.
            if (
                not client.is_mod
                and client not in client.area.area_manager.owners
                and c not in client.area.clients
            ):
                raise ArgumentError(
                    "You can't kick someone from another area as a CM!"
                )
            if len(args) == 1:
                area = client.area
            else:
                try:
                    area = client.area.area_manager.get_area_by_id(
                        int(args[1]))
                except AreaError:
                    raise
                if (
                    not client.is_mod
                    and client not in client.area.area_manager.owners
                    and client not in area.owners
                ):
                    raise ArgumentError(
                        "You can't kick someone to an area you don't own as a CM!"
                    )
            target_pos = ""
            old_area = c.area
            if len(args) >= 3:
                target_pos = args[2]
            client.send_ooc(
                f"Attempting to kick [{c.id}] {c.showname} from [{old_area.id}] {old_area.name} to [{area.id}] {area.name}."
            )
            c.set_area(area, target_pos)
            c.send_ooc(
                f"You were kicked from [{old_area.id}] {old_area.name} to [{area.id}] {area.name}."
            )
            database.log_area(
                "area_kick", client, client.area, target=c, message=area.id
            )
            client.area.invite_list.discard(c.id)
    except ValueError:
        raise ArgumentError("Area ID must be a number.")
    except AreaError:
        raise
    except ClientError:
        raise


# TODO: actually finish this command
@mod_only(area_owners=True)
def ooc_cmd_shuffle_pos(client, arg):
    """
    Randomly shuffle the players into a list of pos separated by space or comma.
    If your pos have spaces in them, it must be a comma-separated list like /shuffle_pos pos one, pos two, pos X
    Usage:  /shuffle_pos <pos(s)>
    """
    client.area.pos_lock.clear()
    client.area.broadcast_ooc("Position lock cleared.")


@mod_only(area_owners=True)
def ooc_cmd_pos_lock(client, arg):
    """
    Lock current area's available positions into a list of pos separated by space or comma.
    Use /pos_lock_clear to make the list empty.
    If your pos have spaces in them, it must be a comma-separated list like /pos_lock pos one, pos two, pos X
    If you're locking into a single pos with spaces in it, end it with a comma, like /pos_lock this is a pos,
    Usage:  /pos_lock <pos(s)>
    """
    if client.area.dark:
        if not arg or arg.strip() == "":
            pos = client.area.pos_dark
            client.send_ooc(f"Current darkness pos is {pos}.")
            return
        if not client.is_mod and not (client in client.area.owners):
            raise ClientError("You must be authorized to do that.")
        client.area.pos_dark = arg
        client.area.broadcast_ooc(f"Locked darkness pos into {arg}.")
        return
    if not arg or arg.strip() == "":
        if len(client.area.pos_lock) > 0:
            pos = ", ".join(str(p_lock) for p_lock in client.area.pos_lock)
            client.send_ooc(f"Pos_lock is currently {pos}.")
        else:
            client.send_ooc("No pos lock set.")
        return

    if arg.strip().lower() == "none":
        ooc_cmd_pos_lock_clear(client, arg)
        return

    if not client.is_mod and not (client in client.area.owners):
        raise ClientError("You must be authorized to do that.")

    client.area.pos_lock.clear()
    if "," in arg:
        args = arg.split(",")
    else:
        args = arg.split()
    # remove duplicates while preserving order
    args = sorted(set(args), key=args.index)
    for pos in args:
        pos = pos.strip().lower()
        if pos == "none" or pos == "":
            continue
        client.area.pos_lock.append(pos)

    pos = ", ".join(str(p_lock) for p_lock in client.area.pos_lock)
    client.area.broadcast_ooc(f"Locked pos into {pos}.")
    client.area.send_command(
        "SD", "*".join(client.area.pos_lock)
    )  # set that juicy pos dropdown


@mod_only(area_owners=True)
def ooc_cmd_pos_lock_clear(client, arg):
    """
    Clear the current area's position lock and make all positions available.
    Usage:  /pos_lock_clear
    """
    client.area.pos_lock.clear()
    client.area.broadcast_ooc("Position lock cleared.")


def ooc_cmd_knock(client, arg):
    """
    Knock on the target area ID to call on their attention to your area.
    Usage:  /knock <id>
    """
    if arg == "":
        raise ArgumentError(
            "Failed to knock: you need to input an accessible area name or ID to knock!"
        )
    if client.blinded:
        raise ClientError("Failed to knock: you are blinded!")
    try:
        area = None
        for _area in client.area.area_manager.areas:
            if (
                _area.name.lower() == arg.lower()
                or _area.abbreviation == arg
                or (arg.isdigit() and _area.id == int(arg))
            ):
                area = _area
                break
        if area is None:
            raise ClientError("Target area not found.")

        allowed = client.is_mod or client in area.owners or client in client.area.owners
        if not allowed and area != client.area:
            if len(client.area.links) > 0:
                if not str(area.id) in client.area.links:
                    raise ClientError(
                        f"Failed to knock on [{area.id}] {area.name}: That area is inaccessible!"
                    )

                if str(area.id) in client.area.links:
                    # Get that link reference
                    link = client.area.links[str(area.id)]

                    # Link requires us to be inside a piece of evidence
                    if (
                        len(link["evidence"]) > 0
                        and client.hidden_in not in link["evidence"]
                    ):
                        raise ClientError(
                            f"Failed to knock on [{area.id}] {area.name}: That area is inaccessible!"
                        )
            if client.area.locked and client.id not in client.area.invite_list:
                raise ClientError(
                    f"Failed to knock on [{area.id}] {area.name}: Current area is locked!"
                )

        area.send_command("RT", "knock")
        if area == client.area:
            area.broadcast_ooc(
                f"💢 [{client.id}] {client.char_name} knocks for attention. 💢"
            )
        else:
            client.area.broadcast_ooc(
                f"[{client.id}] {client.char_name} knocks on [{area.id}] {area.name}."
            )
            area.broadcast_ooc(
                f"💢 Someone is knocking from [{client.area.id}] {client.area.name} 💢"
            )
    except ValueError:
        raise ArgumentError(
            "Failed to knock: you need to input an accessible area name or ID to knock!"
        )
    except (AreaError, ClientError):
        raise


def ooc_cmd_peek(client, arg):
    """
    Peek into an area to see if there's people in it.
    Usage:  /peek <id>
    """
    if arg == "":
        raise ArgumentError(
            "You need to input an accessible area name or ID to peek into it!"
        )
    if client.blinded:
        raise ClientError("You are blinded!")
    try:
        area = None
        for _area in client.area.area_manager.areas:
            if (
                _area.name.lower() == arg.lower()
                or _area.abbreviation == arg
                or (arg.isdigit() and _area.id == int(arg))
            ):
                area = _area
                break
        if area is None:
            raise ClientError("Target area not found.")
        if area == client.area:
            ooc_cmd_getarea(client, "")
            return

        try:
            client.try_access_area(area, True)
            if not area.can_getarea:
                raise ClientError("Can't peek in that area!")
            if area.dark:
                raise ClientError("Area is dark!")
        except ClientError as ex:
            if (
                not client.area.dark
                and not client.sneaking
                and not client.hidden
                and "locked" in str(ex).lower()
            ):
                client.area.broadcast_ooc(
                    f"[{client.id}] {client.char_name} tried to peek into [{area.id}] {area.name} but {str(ex).lower()}"
                )
                # People from within the area have no distinction between peeking and moving inside
                area.broadcast_ooc(
                    f"Someone tried to enter from [{client.area.id}] {client.area.name} but {str(ex).lower()}"
                )
            client.send_ooc(
                f"Failed to peek into [{area.id}] {area.name}: {ex}")
            return
        else:
            sorted_clients = []
            for c in area.clients:
                if not c.hidden and c not in area.owners and not c.is_mod:  # pure IC
                    sorted_clients.append(c)

            _sort = [
                c.char_name for c in sorted(sorted_clients, key=lambda x: x.char_name)
            ]

            # this would be nice to be a separate "make human readable list" func
            if len(_sort) == 2:
                sorted_clients = " and ".join(_sort)
            elif len(_sort) > 2:
                sorted_clients = ", ".join(_sort[:-1])
                sorted_clients = "{} and {}".format(sorted_clients, _sort[-1])
            elif len(_sort) == 1:
                sorted_clients = _sort[0]

            if len(sorted_clients) <= 0:
                sorted_clients = "nobody"

            if not client.sneaking and not client.hidden:
                client.area.broadcast_ooc(
                    f"[{client.id}] {client.char_name} peeks into [{area.id}] {area.name}..."
                )
            else:
                client.send_ooc(
                    f"You silently peek into [{area.id}] {area.name}...")
            client.send_ooc(f"There's {sorted_clients}.")
    except ValueError:
        raise ArgumentError(
            "Failed to peek: you need to input an accessible area name or ID to knock!"
        )
    except (AreaError, ClientError):
        raise


@mod_only()
def ooc_cmd_max_players(client, arg):
    """
    Set a max amount of players for current area between -1 and 99.
    Usage: /max_players [num]
    """
    if arg == "":
        client.send_ooc(
            f"Max amount of players for the area is {client.area.max_players}."
        )
        return

    try:
        arg = int(arg)
        if arg < -1 or arg > 99:
            raise ClientError("The min-max values are -1 and 99!")
        client.area.max_players = arg
        client.send_ooc(
            f"New max amount of players for the area is now {client.area.max_players}."
        )
    except ValueError:
        raise ArgumentError(
            "Area ID must be a name, abbreviation or a number.")
    except (AreaError, ClientError):
        raise


@mod_only(area_owners=True)
def ooc_cmd_desc(client, arg):
    """
    Set an area description that appears to the user any time they enter the area.
    Usage: /desc [desc]
    """
    if client.blinded:
        raise ClientError("You are blinded!")
    if len(arg) == 0:
        desc = client.area.desc
        if client.area.dark:
            desc = client.area.desc_dark
        client.send_ooc(f"Description: {desc}")
        database.log_area("desc.request", client, client.area)
    else:
        if client.area.cannot_ic_interact(client):
            raise ClientError("You are not on the area's invite list!")
        if (
            not client.is_mod
            and not (client in client.area.owners)
            and client.char_id == -1
        ):
            raise ClientError("You may not do that while spectating!")
        if client.area.dark:
            if not client.is_mod and not (client in client.area.owners):
                raise ClientError("You must be authorized to do that.")
            client.area.desc_dark = arg.strip()
        else:
            client.area.desc = arg.strip()
        desc = arg[:128]
        if len(arg) > len(desc):
            desc += "... Use /desc to read the rest."
        client.area.broadcast_ooc(
            f"{client.char_name} changed the area description to: {desc}."
        )
        database.log_area("desc.change", client, client.area, message=arg)


@mod_only(area_owners=True)
def ooc_cmd_edit_ambience(client, arg):
    """
    Toggle edit mode for setting ambience. Playing music will set it as the area's ambience.
    tog can be `on`, `off` or empty.
    Usage: /edit_ambience [tog]
    """
    if len(arg.split()) > 1:
        raise ArgumentError(
            "This command can only take one argument ('on' or 'off') or no arguments at all!"
        )
    if arg:
        if arg == "on":
            client.edit_ambience = True
        elif arg == "off":
            client.edit_ambience = False
        else:
            raise ArgumentError("Invalid argument: {}".format(arg))
    else:
        client.edit_ambience = not client.edit_ambience
    stat = "no longer"
    if client.edit_ambience:
        stat = "now"
    client.send_ooc(f"Playing a song will {stat} edit the area's ambience.")


@mod_only(area_owners=True)
def ooc_cmd_lights(client, arg):
    """
    Toggle lights for this area. If lights are off, players will not be able to use /getarea or see evidence.
    Players will also be unable to see area movement messages or use /chardesc.
    You can change /bg, /desc and /pos_lock of the area when its dark and it will remember it next time you turn the lights off.
    tog can be `on`, `off` or empty.
    Usage: /lights [tog]
    """
    if len(arg.split()) > 1:
        raise ArgumentError(
            "This command can only take one argument ('on' or 'off') or no arguments at all!"
        )
    if arg:
        if arg == "on":
            client.area.dark = False
        elif arg == "off":
            client.area.dark = True
        else:
            raise ArgumentError("Invalid argument: {}".format(arg))
    else:
        client.area.dark = not client.area.dark
    stat = "no longer"
    bg = client.area.background
    if client.area.dark:
        stat = "now"
        bg = client.area.background_dark
    for c in client.area.clients:
        pos = c.pos
        if c.area.dark:
            pos = client.area.pos_dark
        c.send_command("BN", bg, pos)
    client.send_ooc(f"This area is {stat} dark.")


def ooc_cmd_link(client, arg):
    """
    Show a requested HTML link or a list of links.
    Usage: /link [choice]
    """
    links_list = client.server.misc_data['links']

    if links_list is None:
        raise ClientError('miscdata.yaml is empty. Tell a mod.')
    
    if len(arg) == 0:
        msg = 'Links available (use /link <option>):\n• '
        msg += "\n• ".join(links_list)
        client.send_ooc(msg)
    elif ':' in arg:
        add_link(client, arg)
    else:
        arg = arg.lower()
        choice = arg.capitalize()
        if arg in links_list:
            try:
                if arg == 'update':
                    client.send_ooc(f"Latest Update: {links_list[arg]}")
                else:
                    client.send_ooc(f"{choice}: {links_list[arg]}")
                    database.log_area("link.request", client, client.area, message=arg)
            except:
                raise ClientError('Link has not been set!')
        else:
            raise ArgumentError('Link not found. Use /link to see possible choices.')

@mod_only()
def add_link(client, arg):
    """
    Add a HTML link to list.
    Usage: /link <name>: <url>
    """
    links_list = client.server.misc_data['links']
    max = 10

    args = arg.split(': ')
    args[0] = args[0].lower()
    args[0] = args[0].strip(' ')
    if args[0] in links_list:
        try:
            links_list[args[0]] = args[1]
            client.server.save_miscdata()
            client.send_ooc(f'{args[0]} set!')
            database.log_area(f'link.set "{args[0]}"', client, client.area, message=args[1])
        except:
            raise ArgumentError('Input error, link not set.\nUse /link <name>: [url]')
    else:
        if len(links_list) < max:
            if args[0].isspace() or args[0] == "":
                raise ArgumentError('You must enter a link name.')
            else:
                try:
                    links_list[args[0]] = args[1]
                    client.server.save_miscdata()
                    client.send_ooc(f'Link "{args[0]}" created and set!')
                    database.log_area(f'link.create "{args[0]}"', client, client.area, message=args[1])
                except:
                    raise ArgumentError('Input error, link not set.\nUse /link <choice>: [link]')
        else:
            raise ClientError('Link list is full!')

@mod_only()
def ooc_cmd_removelink(client, arg):
    """
    Remove a specific HTML link from data.
    Usage: /removelink <choice>
    """
    links_list = client.server.misc_data['links']

    if len(arg) == 0:
        raise ArgumentError('You must specify a link to delete.')

    arg = arg.lower()
    if arg in links_list:
        try:
            del links_list[arg]
            client.server.save_miscdata()
            client.send_ooc(f'Deleted link "{arg}".')
            database.log_area('link.delete', client, client.area, message=arg)
        except:
            raise ClientError('Error, link has not been deleted.')
    else:
        raise ArgumentError('Link not found. Use /link to see possible choices.')


def ooc_cmd_update(client, arg):
    """
    See the link to the latest update.
    Usage: /update
    """
    try:
        client.send_ooc('Latest Update: {}'.format(client.server.misc_data['links']['update']))
    except:
        raise ClientError('Update not set!')
