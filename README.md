# TEAM 11 SPOTIFY WRAPPER EXPERIENCE #

## Description ##

Spotify Wrapper Experience is a web application built using Django and Spotify API that allows Spotify users to view their listening statistics at any time of the year (no need to wait for Spotify Wrapped!) 

## User Stories To Tackle ##

### BASE USER STORIES ###

Base User Story #1: As a user, I want to be able to view a presentation of the different
aspects of my personal Spotify music listening tastes displayed in colorful and fun ways.
Acceptance criteria:
    ● Able to parse through a Spotify account’s data to generate a detailed and creative
    summary of the user’s music listening habits and tastes
    ● Summary must consist of at least 8 distinct “slides” (transition slides count and are
    encouraged)

    Base User Story #2: As a user, I would like to be able to create and login to an account that
saves my previously generated Spotify wraps.
Acceptance criteria:
    ● Able to create and log into an account associated with your Spotify info
    ● Able to log out of your account
    ● Account information is persistent (exists after exiting the website)
    ● Provide a screen where past Spotify wraps (the entire wrap, not just a summary) can
    be accessed, viewed, and deleted
● Provide a screen where you can delete your account

Base User Story #3: As a user, I would like the UI to be aesthetically-pleasing and responsive.
Acceptance criteria:
    ● UI matches your client TA’s personal design tastes and expectations
    ● UI is not hard-coded for a specific screen resolution, will display correctly on different
    laptop/monitor sizes
    Base User Story #4: As a developer, I would like to avoid security leaks by not hosting secrets
    like API keys on GitHub.
    Acceptance criteria:
    ● No secrets should be committed to GitHub
    ● We recommend storing all secrets in a file that has been added to your .gitignore to
prevent accidental commits

### ADDITIONAL USER STORIES ###

3. As a user, I would like to be able to access the website on my phone with a
well-designed and mobile-friendly UI.
    a. 8 points

4. As a user, I would like to be able to generate and save special and distinct holiday
versions of my Spotify Wrapped on at least 2 specific days of the year (Halloween,
Christmas, etc.)
    a. 3 points


5. As a user, I would like to be able to hear clips from some of my top songs play during
my Spotify Wrapped
    a. 3 points
    b. +1 point for integrating music playback into Duo-Wrapped

6. As a user, I would like to create Spotify Wraps over short, medium, and long terms of
my listening history (each of these options must be distinguishable when saved)
    a. 2 points


7. As a user, I would like fun games embedded into my Spotify Wrapped that quiz me
on my own taste
    a. Base points scale based on game complexity and creativity:
    i. Simple/uncreative games = 2 points
    ● E.g. guess your most listened to musician
    ii. Moderately complex/creative games = 5 points
    ● E.g. guess one of your top songs based on an audio snippet

^^ MAX we are going to go is a moderately creative game. Anything else is a waste of time

10. As a user, I would like to be able to toggle a dark-mode that applies to all UI on the
website.
    a. 2 points
    b. +1 points for adding the ability to swap to another visually distinct theme of
    your choice

11. As a user, I would like to be able to click a button to easily share my Wrapped on
social media like Instagram, LinkedIn, and X (Twitter)
    a. 2 points

13. As a developer, I would like to run my Django website on a hosting service (like
Heroku) so anyone can access my Spotify Wrapped application
    a. 5 points
    b. See the payment disclaimer!

15. As a user, I would like to be able to access a “contact the developers” page where I
can read more about the development team and easily send them feedback.
    a. 1 point

16. As a developer, I would like all functions to have proper documentation so I can
easily understand them at a glance (use docstrings for Python functions and JSDoc
for JavaScript functions)
    a. 1 point

SUM: 29 MAX points we want to get. 8 additional points are buffer to make sure we get an A on this project.


## Features ##

### Spotify Account Data ###
    - Generate a detailed and creative summary of the user’s music listening habits and tastes
    - Summary consists of 8 distinct “slides”

### Account Features ###
    - Able to create and log into an account associated with your Spotify info
    - Able to log out of your account
    - Account information is persistent
    - Provide a screen where past Spotify wraps can be accessed, viewed, and deleted
    - Provide a screen where you can delete your account

### Aesthetically pleasing UI ###
    - UI matches your client TA’s personal design tastes and expectations
    - UI is not hard-coded for a specific screen resolution, will display correctly on different laptop/monitor sizes

### Secutity ###
    -all secrets are in a file that has been added to .gitignore

### Customizability ###
    -tbd