# Unnamed tank game

Shoot, upgrade and get a highscore!

This is my first finished game. I am very happy about it. I feel I incurred on some technical debt, so I decided to stop working on it. But it works!

Check it out at [itch.io](https://alex-pf.itch.io/tank-game)

I used [pygbag](https://github.com/pmp-p/pygbag) to play it in the browser, using a custom template (template.html)

## Controls

While playing:
- use wasd/arrows to move
- aim with mouse
- press space or click to shoot
- press e to auto shoot
- press p to pause

## Run from source

- Clone the repo
- Install the requirements
- run `python main.py`

## Build

The game is built using pygbag.

- run `run.sh` to start the test server, and open http://localhost:8000 from your browser to play the game.
- run `build.sh` to get a game build, uploadable to itch.io, under `build/web.zip`
