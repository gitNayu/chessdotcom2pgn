#!/usr/bin/env python3

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

API = 'https://api.chess.com/pub/player/{}/games/archives'

def request(url):
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'ChessCom-PGN-Exporter/1.0'}
    )

    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def get_header(pgn, name):
    match = re.search(
        rf'^\[{re.escape(name)}\s+"(.*?)"\]',
        pgn,
        re.MULTILINE
    )

    return match.group(1) if match else 'unknown'

def safe_filename(value):
    return re.sub(r'[^\w.-]', '_', value)


def split_games(pgn):
    games = re.split(
        r'(?m)(?=^\[Event\s)',
        pgn.strip()
    )

    return [game.strip() for game in games if game.strip()]

def export_games(username, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    archives = json.loads(
        request(API.format(username))
    )['archives']

    total = 0

    for archive_url in archives:
        print(f'Downloading: {archive_url}')

        pgn_url = archive_url + '/pgn'
        pgn_data = request(pgn_url)

        games = split_games(pgn_data)

        for game in games:
            date = get_header(game, 'UTCDate')
            time_str = get_header(game, 'UTCTime')
            white = get_header(game, 'White')
            black = get_header(game, 'Black')
            result = get_header(game, 'Result')

            opponent = (
                black if white.lower() == username.lower()
                else white
            )

            filename = (
                f'{date}_{time_str}_vs_{safe_filename(opponent)}'
                f'_{safe_filename(result)}.pgn'
            )

            filename = filename.replace(':', '-')
            output_file = output_dir / filename

            # Avoid overwriting files with identical names.
            counter = 1

            while output_file.exists():
                output_file = output_dir / (
                    f'{Path(filename).stem}_{counter}.pgn'
                )
                counter += 1

            output_file.write_text(
                game + '\n',
                encoding='utf-8'
            )

            total += 1

        time.sleep(1)

    print('\nExport complete!')
    print(f'Games exported: {total}')
    print(f'Output directory: {output_dir.resolve()}')

def main():
    parser = argparse.ArgumentParser(
        description='Export Chess.com games as individual PGN files.'
    )

    parser.add_argument(
        'username',
        nargs='?',
        help='Chess.com username'
    )

    parser.add_argument(
        '-o', '--output',
        default='chesscom_games',
        help='Output directory (default: chesscom_games)'
    )

    args = parser.parse_args()

    username = args.username

    if not username:
        username = input('Chess.com username: ').strip()

    if not username:
        parser.error('Username cannot be empty.')

    try:
        export_games(username, Path(args.output))
    except Exception as error:
        parser.exit(1, f'Error: {error}\n')

if __name__ == '__main__':
    main()