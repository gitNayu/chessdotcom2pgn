# chessdotcom2pgn
A simple Python script to export your Chess.com game history as individual PGN files.

## Usage

### Interactive mode

Run the script without arguments:
```
python3 export.py
```

You will be prompted to enter your Chess.com username.

### Command-line mode
Provide your username directly:
```
python3 export.py nayu0chess
```

#### Custom output directory
Use -o or --output to specify where the PGN files should be saved:
```
python3 export.py nayu0chess -o games
```

If no output directory is specified, files are saved in chesscom_games/.

## Output
Each game is saved as an individual PGN file.

Example directory structure:
<br> chesscom_games/
<br> ├── 2026.11.08_12-30-15_vs_opponent1_1-0.pgn
<br> ├── 2026.11.08_12-45-22_vs_opponent2_0-1.pgn
<br> ├── 2026.11.08_13-02-10_vs_opponent3_1_2-1_2.pgn
<br> └── ...

Filenames follow this format:
DATE_TIME_vs_OPPONENT_RESULT.pgn

If two games produce the same filename, a numerical suffix is automatically added to prevent overwriting.
