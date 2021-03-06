<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Comedibot</h3>

  <p align="center">
    The meme bot that's personal. 
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=Nkprrm17Rbs">View Demo</a>
    ·
    <a href="https://github.com/sunset-developer/ComediBot/issues">Report Bug</a>
    ·
    <a href="https://github.com/sunset-developer/ComediBot/pulls">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Commands](#Commands)
  * [Meme](#meme)
  * [Goof](#goof)
  * [Administrative](#administrative)
   * [Misc](#misc)
* [Roles](#roles)


## Commands
Argument Key: ```[Required] (Optional)```

Command Preifx: ```$``` (Is subject to change)

### Meme
  
* ```$submit [trigger] [meme]```
  - ```trigger``` is a word or a phrase that comedibot looks for.
  - ```meme``` is the phrase that comedibot responds with when triggered
  
* ```$submitnsfw [trigger] [meme]```
  - Has same behavior as the submit command, however only is triggered in nsfw channels.
    
* ```$delete [trigger]```
  - Deletes a meme that you submitted.
  
* ```$get [trigger]```
  - Retreives all memes associated with trigger with authors.
  
### Goof

* ```$submitgoof [mention] [quote]```
  - ```mention``` is a reference to a user, for example @sunsetdev.
  - ```quote``` is the idiotic thing your friend said or did.
  
* ```$deletegoof [mention] [quote]```
  - Deletes a goof that you submitted.
  
* ```$getgoof [mention]```
  - Retreives all of the goof's associated with this mention with timestamp.
 
### Administrative

* ```$genroles```
  - Generates roles needed for permissions. Roles may need to be configured by adminstrators.
  
* ```$fdelete [trigger] (mention)```
  - Forcefully deletes a meme by any user.
  - ```mention``` is an optional paramater for when you want to delete a meme told by a specific user.
  - Leaving mention blank will delete all memes with associated trigger.

* ```$fdeletegoof [mention] [quote]```
  - Forcefully deletes the goof of any user.
  
### Misc

* ```$help``` - Displays help menu.
  
## Roles

* ```Comedian``` role allows for users to execute commands.
* ```Audience``` allows for the triggering of memes.

The absence of a role in a server will default to allow all.
