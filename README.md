# **Discord Rides Bot**

## Description
This is a Discord bot developed for making and announcing ride assignements on a club Discord server.
Members sign up for rides for events through a Google form, and through the usage of the Google Sheets API, the bot uses the information on this spreadsheet to determine the best way to determine rides both going to and returning from the event.

## Commands
Currently these are the commands built into the bot.

***!update_signups*** - removes duplicate entries in the spreadsheets (to account for updated information on a person's ride situation)

***!print_drivers*** - prints all available drivers for the event, going and returning

***!assign_rides_going*** - assigns members to drivers and updates the spreadhseet to show the ride assignments.  If there are not enough drivers, the bot returns an error message.

***!assign_rides_back*** - same as !assign_rides_going but for returning from the event.  Takes into consideration where members live to minimize distance for drivers.

***!announce_rides_going*** - sends an announcement message in the discord server with the ride assignment listed in the spreadsheet

***!announce_rides_returning*** - same as !announce_rides_going but for returning from the event

***!update_areas*** - updates the spreadsheet to show how many people live in the same area.  Used primarily for !assign_rides_back

## Announcements
The bot makes announcement messages for reminders to sign up for rides every week at a specific time. 
It also sends a separate announcmeent message for drivers, where reacting to that message will add them to the list of drivers used for the other commands.
