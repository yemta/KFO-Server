# KFO-Server-AOV
**Attorney Online Vidya’s** server code has been updated from _tsuserver3_ to _KFO-Server_, the new standard for python based Attorney Online servers.
While most features remain the same between code bases, there are several changes and new features that we have documented below to help you use them,
as well as general differences between KFO-Server base and our own server.
Note that several of these features may require CM.

## General AOV Changes From KFO-Base / tsuserver3
* **Sneaking / Movement Announcements Removal**
	- For some reason, base KFO-Server _really_ wants everyone else to know when you change areas and announce as such in OOC. 
	- We've deleted this because no one gives a fuck when you move area and it clogs up OOC.
* **Various Emoji Removal**
	- For some other reason, base KFO-Server has emojis in almost every command. We've deleted most of these.
* **Hub System Disabled**
	- The concept of having multiple hubs containing multiple areas. Completely uneccessary and generally turned off, so don't worry about it.
* **DJ and Looping Music**
	- DJ is dead. `/play` now loops by default. Use `/play1` if you want to play a song only once.

# New Server Features
## Minigames
**Note**: These can only be activated if the area's evidence_mod is set to "CT" as they are otherwise disruptive. Ask a mod for help.
* **cs** `<id>`
    - Start a one-on-one "Cross Swords" debate with targeted player!
	- Will automatically pair you with the target
    - Expires in 5 minutes.
    - If there's an ongoing cross-swords already, it will turn into a Scrum Debate (team vs team debate) with you joining the side *against* the `<id>`.
* **pta** `<id>`
    - Start a one-on-one "Panic Talk Action" debate with targeted player!
    - Unlike `/cs`, a Panic Talk Action (PTA) cannot evolve into a Scrum Debate.
    - Expires in 5 minutes.
* **concede** `<id>`
    - Concede a trial minigame and withdraw from either team you're part of.
## Demo / Cutscenes
* **/demo [evidence id]** 
	- "Cutscenes" can effectively be created and played using demo files and evidence.
	- The easiest way to do this is to turn Demo File Logging on in your client's Settings - Logging options.
	- Then, on server, play out your cutscene using your preferred characters. This will create a demo file in your client's "Logs" folder.
	- Open the demo file in a text editor such as Notepad++. From here you can scroll down to see the individual lines relating to each action you performed.
	- These lines basically consist of client commands involving talking IC, animations, backgrounds and effects. You can manipulate these as needed.
	- Copy and paste these lines into the Description of a piece of evidence. Note the following:
	- If playing music, any line starting with "MC#" must be replaced with /play to play music instead. Other commands can be used as well.
	- You must use `%` to end a line. You can also chain to another demo evidence by putting `/demo [next evidence id]` as the last line.
	- When finished, use `/demo [evidence name or ID]` to play the cutscene. Use `/demo` by itself to stop it.
## Case Advert Webhook
* **/need**
	- Sending an advert through `/need` will automatically post it to the AOV Community Server's #Case-Advertising channel.
	- This will also include your current area as well as pinging any roles mentioned in the advert.
	- eg. "/need defense, co-pro, and steno for case!" will ping the discord's Defense, Prosecution and Steno roles.
	- Putting "All roles" in the message will ping all roles.
	- 'Arcade' will be pinged automatically if a `/need` is sent from an Arcade-named area.
## Testimony Commands
**Note: Testimony recording can also be used from IC Chat as a CM - see "In-Character Commands" below.**
* **testimony** `[id]`
    - Display the currently recorded testimony, including statement IDs.
    - Optionally, `id` is a nubmer that can be passed to move to that statement ID.
* **testimony\_start** `<title>`
    - Manually start a testimony with the given title.
* **testimony\_continue**
    - Manually start a testimony with the given title.
* **testimony\_clear**
    - Clear the current testimony.
* **testimony\_remove** `<id>`
    - Remove the statement at index.
* **testimony\_amend** `<id>` `<msg>`
    - Edit the spoken message of the statement at idx.
* **testimony\_swap** `<id>` `<id>`
    - Swap the two statements by id.
* **testimony\_insert** `<id>` `<id>`
    - Insert the targeted statement at idx.
## In-Character Commands
* **/a** `[id(s)]` `[msg]`
    - Put this in the In-Character chat. Use to message other areas you are a CM in.
    - This command can only be used by CMs and above.
    - `[id(s)]` are optional. If ID(s) are not provided (`/a msg`), the message will be broadcast across all owned areas.
    - `[id(s)]` stand for Area ID's that can be viewed using `/area`, or in the A/M area list, so `/a 1 msg` to send message "msg" to area ID 1. If multiple ID's, they must be comma-separated, like so: `/a 1,2,3,4 msg` - send message "msg" to area ID's 1, 2, 3 and 4.
* **/w** `[id(s)]` `[msg]`
    - Put this in the In-Character chat. Used to whisper to other players.
    - This command can be used by anyone, unless `/area_pref can_whisper` is `false`.
    - `[id(s)]` are optional. If ID(s) are not provided (`/w msg`), the message will be broadcast to clients in the current `/pos` only.
    - `[id(s)]` stand for Client ID's that can be viewed using `/getarea`, so `/w 1 msg` to send message "msg" to client with ID 1. The client must be present in the same area. If multiple ID's, they must be comma-separated, like so: `/aw 1,2,3,4 msg` - send message "msg" to Client ID's 1, 2, 3 and 4.
* **Testimony**
    - Begin with a title, like `--title--`, `==title==`, etc.
    - When a CM pressed the "Witness Testimony" button, any message spoken from this point on will be recorded.
        - If anyone that isn't a CM tries to do this, it will not start recording. Use the OOC `/testimony` commands detailed above instead.
    - Once everyone has testified, last one to testify or the CM has to say a single word - `end` to finish recording.
    - Afterwards, next time the CM uses "Cross-Examination" button, the testimony title will be replayed, and the defense can use `>` to progress a statement, `<` to precede a statement, `>5` to go to specific statement 5.
    - You can use `**msg` to amend the current statement.
    - You can use `++msg` to add a new statement after the current one.
## Areas
* **desc** `[desc]`
    - Set an area description that appears to the user any time they enter the area.
		- Could be used to immediately detail the current case format and summary to incoming users.
* **edit\_ambience** `[tog]`
    - Toggle edit mode for setting ambience. Playing music will set it as the area's ambience.
    - tog can be `on`, `off` or empty.
* **lights** `[tog]`
    - Toggle lights for this area. If lights are off, players will not be able to use `/getarea` or see evidence.
    - You can change `/bg`, `/desc` and `/pos_lock` of the area when its dark and it will remember it next time you turn the lights off.
    - tog can be `on`, `off` or empty.
* **follow**
    - Follow targeted character ID if they move area.
* **unfollow**
    - Stop following whoever you are following.
## Casing
**Various evidence features can now be used through OOC commands if preferred, as detailed below.**
* **evidence** `[evi_name/id]`
    - Use `/evidence` to read all evidence in the area.
    - Use `/evidence` `[evi_name/id]` to read specific evidence.
* **evidence_add** `[name]` `[desc]` `[image]`
    - Add a piece of evidence.
    - For sentences with spaces the arg should be surrounded in `""`'s, for example `/evidence_add Chair "It's a chair." chair.png`
* **evidence_remove** `<evi_name/id>`
    - Remove a piece of evidence.
* **evidence_edit** `<evi_name/id>` `[name]` `[desc]` `[image]`
    - Edit a piece of evidence.
    - If you don't want to change something, put an `*` there.
    - For sentences with spaces the arg should be surrounded in `""`'s, for example `/evidence_edit * "It's a chair." chair.png`
* **evi\_swap**  `<id>` `<id>`
    - Swap the positions of two evidence items on the evidence list.
    - The ID of each evidence can be displayed by mousing over it in 2.8 client, or simply its number starting from 1.
* **remote\_listen** `[option]`
    - Change the remote listen logs to either `NONE`, `IC`, `OOC` or `ALL`.
    - It will send you those messages from the areas you are an owner of.
    - Leave blank to see your current option.
## Character
* **player\_move\_delay** `<id>` `[delay]`
    - Set the player's move delay to a value in seconds. Can be negative.
    - Delay must be from `-1800` to `1800` in seconds or empty to check.
    - If only `delay` is provided, you will be setting your own move delay.
* **player\_hide** `<id(s)>`
    - Hide player(s) from `/getarea` and playercounts.
    - If `<id>` is `*`, it will hide everyone in the area excluding yourself and CMs.
* **player\_unhide** `<id(s)>`
    - Unhide player(s) from `/getarea` and playercounts.
    - If `<id>` is `*`, it will unhide everyone in the area excluding yourself and CMs.
* **hide** `<evi_name/id>`
    - Try to hide in the targeted evidence name or ID.
* **unhide**
    - Stop hiding.
* **listen\_pos** `[pos(s)]`
    - Start only listening to your currently occupied pos.
    - All messages outside of that pos will be reflected in the OOC.
    - Optional argument(s) is a list of positions you want to listen to.
* **unlisten\_pos**
    - Undo the effects of `/listen_pos` command so you stop listening to the position(s).
* **chardesc** `[desc/id]`
    - Look at your own character description if no arugments are provided.
    - Look at another person's character description if only ID is provided.
    - Set your own character description if description is provided instead of ID.
        - Do note that the first sentence of your chardesc is displayed during area transfer messages!
    - To set someone else's char desc as an admin/GM, or look at their desc, use `/chardesc_set` or `/chardesc_get`.
* **chardesc\_set** `<id>` `[desc]`
    - Set someone else's character description to desc or clear it.
* **chardesc\_get** `<id>`
    - Get someone else's character description.
* **narrate** `[on|off]`
    - Speak as a Narrator for your next emote, speaking over the current IC visuals.
## Music
* **play** `<name>`
    - `/play` now loops a track by default, otherwise works as normal.
* **play1** `<name>`
    - If you only want to play a track once rather than loop, use this.
* **musiclists**
    - Displays all the available music lists in server storage.
* **musiclist** `[path]`
    - Load a music list from server storage that only you will see. Pass no arguments to reset. `/musiclists` to see available lists.
* **area\_musiclist** `[path]`
    - Load a music list from server storage that can be seen by the whole area. Pass no arguments to reset. `/musiclists` to see available lists.
    - Area list takes priority over client lists.
* **random\_music** `[category]`
    - Play a random track from your current muisc list. If supplied, `[category]` will pick the song from that category.
    - Usage: `/random_music [category]`
## Roleplay
* **Standard Actions**
	- `/roll, /notecard, /coinflip, /8ball` all work as standard, with some minor additions outlined below:
* **notecard** `<message>`
    - Write a notecard that can only be revealed by a CM.
* **notecard\_clear**
    - Clear all notecards as a CM.
* **notecard\_reveal**
    - Reveal all notecards and their owners.
* **notecard\_check**
    - Check all notecards and their owners privately with a message telling others you've done so.
* **vote** `<id>`
    - Cast a vote for a particular user that can only be revealed by a CM.
* **vote\_clear** `[char_folder]`
    - Clear all votes as a CM.
    - Include `[char_folder]` (case-sensitive) to only clear a specific voter.
* **vote\_reveal**
    - Reveal the number of votes, the voters and those with the highest amount of votes.
* **vote\_check**
    - Check the number of votes, the voters and those with the highest amount of votes privately with a message telling others you've done so.
* **timer** `<id> [+/-][time]` OR `<id> start` OR `<id> <pause|stop>` OR `<id> <unset|hide>`
    - Manage a countdown timer in the current area. Note that timer of ID `0` is hub-wide. All other timer ID's are local to area.
    - Anyone can check ongoing timers, their status and time left using `/timer <id>`, so `/timer 0`.
    - `[time]` can be formated as `10m5s` for 10 minutes 5 seconds, `1h30m` for 1 hour 30 minutes, etc.
    - You can optionally add or subtract time, like so: `/timer 0 +5s` to add `5` seconds to timer id `0`.
    - `start` starts the previously set timer, so `/timer 0 start`.
    - `pause` OR `stop` pauses the timer that's currently running, so `/timer 0 pause`.
    - `unset` OR `hide` hides the timer for it to no longer show up, so `/timer 0 hide`.
