# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import argparse


def delete_all_rows(table):
    """Delete all rows from the table"""

    # TODO(developer): Create the table
    # table = Table(
    #    table_id,
    #    metadata,
    #    Column("user_id", Integer, primary_key=True),
    #    Column("user_name", String(16), nullable=False),
    # )
    # table.create()

    table.insert().execute(
        {"user_id": 1, "user_name": 'ABC'},
        {"user_id": 2, "user_name": 'DEF'}
    )

    result = table.select().execute().fetchall()
    print("Total inserted rows:", len(result))

    # [START sqlalchemy_spanner_delete_all_rows]
    table.delete().execute()

    result = table.select().execute().fetchall()
    print("Total rows:", len(result))
    # [END sqlalchemy_spanner_delete_all_rows]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--table",
        help="Your sqlalchemy table object.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("delete_all_rows", help=delete_all_rows.__doc__)
    args = parser.parse_args()
    if args.command == "delete_all_rows":
        delete_all_rows(args.table)
    else:
        print(f"Command {args.command} did not match expected commands.")