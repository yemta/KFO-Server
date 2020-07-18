import os

from server import database
from server.constants import TargetType
from server.exceptions import ClientError, ArgumentError, AreaError

from . import mod_only

__all__ = [
    'ooc_cmd_bg',
    'ooc_cmd_status',
    'ooc_cmd_area',
    'ooc_cmd_getarea',
    'ooc_cmd_getareas',
    'ooc_cmd_area_lock',
    'ooc_cmd_area_spectate',
    'ooc_cmd_area_unlock',
    'ooc_cmd_invite',
    'ooc_cmd_uninvite',
    'ooc_cmd_area_kick',
    'ooc_cmd_getafk',
    # Hub system [TO BE MOVED]
    'ooc_cmd_save_hub',
    'ooc_cmd_load_hub',
    'ooc_cmd_list_hubs',
    # Area Creation system
    'ooc_cmd_area_create',
    'ooc_cmd_area_remove',
    'ooc_cmd_area_rename',
    'ooc_cmd_area_swap',
    'ooc_cmd_area_pref',
    # Area links system
    'ooc_cmd_area_link',
    'ooc_cmd_area_unlink',
]


def ooc_cmd_bg(client, arg):
    """
    Set the background of a room.
    Usage: /bg <background>
    """
    if len(arg) == 0:
        raise ArgumentError('You must specify a name. Use /bg <background>.')
    if not client.is_mod and client.area.bg_lock == "true":
        raise AreaError("This area's background is locked")
    try:
        client.area.change_background(arg)
    except AreaError:
        raise
    client.area.broadcast_ooc(
        f'{client.char_name} changed the background to {arg}.')
    database.log_room('bg', client, client.area, message=arg)


def ooc_cmd_status(client, arg):
    """
    Show or modify the current status of a room.
    Usage: /status <idle|rp|casing|looking-for-players|lfp|recess|gaming>
    """
    if len(arg) == 0:
        client.send_ooc(f'Current status: {client.area.status}')
    else:
        try:
            client.area.change_status(arg)
            client.area.broadcast_ooc('{} changed status to {}.'.format(
                client.char_name, client.area.status))
            database.log_room('status', client, client.area, message=arg)
        except AreaError:
            raise


def ooc_cmd_area(client, arg):
    """
    List areas, or go to another area/room.
    Usage: /area [id] or /area [name]
    """
    args = arg.split()
    if len(args) == 0:
        client.send_area_list()
        return

    try:
        area = client.server.area_manager.get_area_by_id(int(args[0]))
    except:
        try:
            area = client.server.area_manager.get_area_by_name(arg)
        except:
            try:
                area = client.server.area_manager.get_area_by_abbreviation(args[0])
            except ValueError:
                raise ArgumentError('Area ID must be a name or a number.')
            except (AreaError, ClientError):
                raise
    client.change_area(area)


def ooc_cmd_getarea(client, arg):
    """
    Show information about the current area.
    Usage: /getarea
    """
    client.send_area_info(client.area.id, False)


def ooc_cmd_getareas(client, arg):
    """
    Show information about all areas.
    Usage: /getareas
    """
    client.send_area_info(-1, False)


def ooc_cmd_getafk(client, arg):
    """
    Show currently AFK-ing players in the current area or in all areas.
    Usage: /getafk [all]
    """
    if arg == 'all':
        arg = -1
    elif len(arg) == 0:
        arg = client.area.id
    else:
        raise ArgumentError('There is only one optional argument [all].')
    client.send_area_info(arg, False, afk_check=True)


def ooc_cmd_area_lock(client, arg):
    """
    Prevent users from joining the current area.
    Usage: /area_lock
    """
    if not client.area.locking_allowed:
        client.send_ooc('Area locking is disabled in this area.')
    elif client.area.is_locked == client.area.Locked.LOCKED:
        client.send_ooc('Area is already locked.')
    elif client in client.area.owners:
        client.area.lock()
    else:
        raise ClientError('Only CM can lock the area.')


def ooc_cmd_area_spectate(client, arg):
    """
    Allow users to join the current area, but only as spectators.
    Usage: /area_spectate
    """
    if not client.area.locking_allowed:
        client.send_ooc('Area locking is disabled in this area.')
    elif client.area.is_locked == client.area.Locked.SPECTATABLE:
        client.send_ooc('Area is already spectatable.')
    elif client in client.area.owners:
        client.area.spectator()
    else:
        raise ClientError('Only CM can make the area spectatable.')


def ooc_cmd_area_unlock(client, arg):
    """
    Allow anyone to freely join the current area.
    Usage: /area_unlock
    """
    if client.area.is_locked == client.area.Locked.FREE:
        raise ClientError('Area is already unlocked.')
    elif not client in client.area.owners:
        raise ClientError('Only CM can unlock area.')
    client.area.unlock()
    client.send_ooc('Area is unlocked.')


@mod_only(area_owners=True)
def ooc_cmd_invite(client, arg):
    """
    Allow a particular user to join a locked or spectator-only area.
    Usage: /invite <id>
    """
    if not arg:
        raise ClientError('You must specify a target. Use /invite <id>')
    elif client.area.is_locked == client.area.Locked.FREE:
        raise ClientError('Area isn\'t locked.')
    try:
        c = client.server.client_manager.get_targets(client, TargetType.ID,
                                                     int(arg), False)[0]
        client.area.invite_list[c.id] = None
        client.send_ooc('{} is invited to your area.'.format(
            c.char_name))
        c.send_ooc(
            f'You were invited and given access to {client.area.name}.')
        database.log_room('invite', client, client.area, target=c)
    except:
        raise ClientError('You must specify a target. Use /invite <id>')


@mod_only(area_owners=True)
def ooc_cmd_uninvite(client, arg):
    """
    Revoke an invitation for a particular user.
    Usage: /uninvite <id>
    """
    if client.area.is_locked == client.area.Locked.FREE:
        raise ClientError('Area isn\'t locked.')
    elif not arg:
        raise ClientError('You must specify a target. Use /uninvite <id>')
    arg = arg.split(' ')
    targets = client.server.client_manager.get_targets(client, TargetType.ID,
                                                       int(arg[0]), True)
    if targets:
        try:
            for c in targets:
                client.send_ooc(
                    "You have removed {} from the whitelist.".format(
                        c.char_name))
                c.send_ooc(
                    "You were removed from the area whitelist.")
                database.log_room('uninvite', client, client.area, target=c)
                if client.area.is_locked != client.area.Locked.FREE:
                    client.area.invite_list.pop(c.id)
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
    Usage: /area_kick <id> [destination]
    """
    if client.area.is_locked == client.area.Locked.FREE:
        raise ClientError('Area isn\'t locked.')
    if not arg:
        raise ClientError(
            'You must specify a target. Use /area_kick <id> [destination #]')
    arg = arg.split(' ')
    if arg[0] == 'afk':
        trgtype = TargetType.AFK
        argi = arg[0]
    else:
        trgtype = TargetType.ID
        argi = int(arg[0])
    targets = client.server.client_manager.get_targets(client, trgtype,
                                                       argi, False)
    if targets:
        try:
            for c in targets:
                if len(arg) == 1:
                    area = client.server.area_manager.get_area_by_id(int(0))
                    output = 0
                else:
                    try:
                        area = client.server.area_manager.get_area_by_id(
                            int(arg[1]))
                        output = arg[1]
                    except AreaError:
                        raise
                client.send_ooc(
                    "Attempting to kick {} to area {}.".format(
                        c.char_name, output))
                c.change_area(area)
                c.send_ooc(
                    f"You were kicked from the area to area {output}.")
                database.log_room('area_kick', client, client.area, target=c, message=output)
                if client.area.is_locked != client.area.Locked.FREE:
                    client.area.invite_list.pop(c.id)
        except AreaError:
            raise
        except ClientError:
            raise
    else:
        client.send_ooc("No targets found.")


@mod_only()
def ooc_cmd_save_hub(client, arg):
    """
    Save the current Hub in the server's storage/hubs/<name>.yaml file.
    Usage: /save_hub <name>
    """
    if len(arg) < 3:
        client.send_ooc("Filename must be at least 3 symbols long!")
        return

    try:
        path = 'storage/hubs'
        num_files = len([f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))])
        if (num_files >= 1000): #yikes
            raise AreaError('Server storage full! Please contact the server host to resolve this issue.')
        arg = f'{path}/{arg}.yaml'
        client.server.area_manager.save_areas(arg)
        client.send_ooc(f'Saving as {arg}...')
    except AreaError:
        raise


@mod_only()
def ooc_cmd_load_hub(client, arg):
    """
    Load Hub data from the server's storage/hubs/<name>.yaml file.
    Usage: /load_hub <name>
    """
    try:
        path = 'storage/hubs'
        arg = f'{path}/{arg}.yaml'
        client.server.area_manager.load_areas(arg)
        client.send_ooc(f'Loading {arg}...')
    except AreaError:
        raise
    


@mod_only()
def ooc_cmd_list_hubs(client, arg):
    """
    Show all the available hubs for loading in the storage/hubs/ folder.
    Usage: /list_hubs
    """
    text = 'Available hubs:'
    for F in os.listdir('storage/hubs/'):
        if F.lower().endswith('.yaml'):
            text += '\n- {}'.format(F[:-5])

    client.send_ooc(text)


@mod_only()
def ooc_cmd_area_create(client, arg):
    """
    Create a new area.
    Usage: /area_create [name]
    """
    area = client.server.area_manager.create_area()
    if arg != '':
        area.name = arg
    client.send_ooc(f'New area created! ({area.name})')


@mod_only()
def ooc_cmd_area_remove(client, arg):
    """
    Remove specified area by Area ID.
    Usage: /area_remove <aid>
    """
    args = arg.split()

    if len(args) == 1:
        try:
            area = client.server.area_manager.get_area_by_id(int(args[0]))
            name = area.name
            client.server.area_manager.remove_area(area)
            client.send_ooc(f'Area {name} removed!')
        except ValueError:
            raise ArgumentError('Area ID must be a number.')
        except (AreaError, ClientError):
            raise
    else:
        raise ArgumentError('Invalid number of arguments. Use /area_remove <aid>.')

@mod_only()
def ooc_cmd_area_rename(client, arg):
    """
    Rename area you are currently in to <name>.
    Usage: /area_rename <name>
    """
    if arg != '':
        try:
            client.area.rename_area(arg)
        except ValueError:
            raise ArgumentError('Area ID must be a number.')
        except (AreaError, ClientError):
            raise
    else:
        raise ArgumentError('Invalid number of arguments. Use /area_rename <name>.')

@mod_only()
def ooc_cmd_area_swap(client, arg):
    """
    Swap areas by Area IDs <aid1> and <aid2>.
    Usage: /area_rename <aid1> <aid2>
    """
    args = arg.split()
    if len(args) != 2:
        raise ClientError("You must specify 2 numbers.")
    try:
        area1 = client.server.area_manager.get_area_by_id(int(args[0]))
        area2 = client.server.area_manager.get_area_by_id(int(args[1]))
        client.server.area_manager.swap_area(area1, area2)
        client.send_ooc(f'Area {area1.name} has been swapped with Area {area2.name}!')
    except ValueError:
        raise ArgumentError('Area IDs must be a number.')
    except (AreaError, ClientError):
        raise

@mod_only(area_owners=True)
def ooc_cmd_area_pref(client, arg):
    """
    Toggle a preference on/off for a hub.
    Usage:  /area_pref - display list of prefs
            /area_pref <pref> - toggle pref on/off
            /area_pref <pref> <on/true|off/false> - set pref to on or off
    """
    cm_allowed = [
        # 'bg_lock',
        'locking_allowed',
        'iniswap_allowed',
        'showname_changes_allowed',
        'shouts_allowed',
        'jukebox',
        'non_int_pres_only',
        'blankposting_allowed',
    ]

    if len(arg) == 0:
        msg = 'Current preferences:'
        for attri in client.area.__dict__.keys():
            value = getattr(client.area, attri)
            if not(type(value) is bool):
                continue
            mod = '[mod] ' if not (attri in cm_allowed) else ''
            msg += f'\n* {mod}{attri}={value}'
        client.send_ooc(msg)
        return

    args = arg.split()
    if len(args) > 2:
        raise ArgumentError("Usage: /area_pref | /area_pref <pref> | /area_pref <pref> <on|off>")

    try:
        attri = getattr(client.area, args[0].lower())
        if not (type(attri) is bool):
            raise ArgumentError("Preference is not a boolean.")
        if not client.is_mod and not (args[0] in cm_allowed):
            raise ClientError("You need to be a mod to modify this preference.")
        tog = not attri
        if len(args) > 1:
            if args[1].lower() in ('on', 'true'):
                tog = True
            elif args[1].lower() in ('off', 'false'):
                tog = False
            else:
                raise ArgumentError("Invalid argument: {}".format(arg))
        client.send_ooc(f'Setting preference {args[0]} to {tog}...')
        setattr(client.area, args[0], tog)
        database.log_room(args[0], client, client.area, message=f'Setting preference to {tog}')
    except ValueError:
        raise ArgumentError('Invalid input.')
    except (AreaError, ClientError):
        raise


@mod_only(area_owners=True)
def ooc_cmd_area_link(client, arg):
    """
    Set up a one-way link from your current area with a targeted area.
    Usage:  /area_link <aid>
    Alternatively, /area_link <aid_from> <aid_to>
    """
    args = arg.split()
    if len(args) <= 0:
        links = ', '.join([f for f in iter(client.area.links)])
        client.send_ooc(f'Current area links are {links}. Use /area_link <aid>')
        return
    try:
        links = []
        for aid in args:
            try:
                target_area = client.server.area_manager.get_area_by_id(int(aid))
            except:
                target_area = client.server.area_manager.get_area_by_abbreviation(aid)
            client.area.link(target_area.id)
            links.append(target_area.id)
        links = ', '.join(links)
        client.send_ooc(f'Area {client.area.name} has been linked with Areas {links}.')
    except ValueError:
        raise ArgumentError('Area IDs must be a number.')
    except (AreaError, ClientError):
        raise


@mod_only(area_owners=True)
def ooc_cmd_area_unlink(client, arg):
    """
    Remove a one-way link from your current area with a targeted area.
    Usage:  /area_unlink <aid>
    Alternatively, /area_unlink <aid_from> <aid_to>
    """
    args = arg.split()
    if len(args) <= 0:
        raise ArgumentError('Invalid number of arguments. Use /area_unlink <aid>')
    try:
        links = []
        for aid in args:
            try:
                target_id = client.server.area_manager.get_area_by_abbreviation(aid).id
            except:
                target_id = int(aid)

            try:
                client.area.unlink(target_id)
                links.append(target_id)
            except:
                continue
        links = ', '.join(links)
        client.send_ooc(f'Area {client.area.name} has been unlinked with Areas {links}.')
    except ValueError:
        raise ArgumentError('Area IDs must be a number.')
    except (AreaError, ClientError):
        raise
