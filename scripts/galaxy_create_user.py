import argparse
import re
import sys

import bioblend.galaxy

def parse_args(args):
    parser = argparse.ArgumentParser(description="Create Galaxy user")

    parser.add_argument("api", help="Galaxy API key")
    parser.add_argument("galaxy_user", type=arg_user, help="Galaxy user e-mail")
    parser.add_argument("galaxy_password", type=arg_password, help="Galaxy user password")
    parser.add_argument("--url", help="Galaxy URL", default="http://127.0.0.1:80")

    args = parser.parse_args(args)
    return args

def arg_user(user):
    try:
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user).group(0)
    except:
        raise argparse.ArgumentTypeError("galaxy_user is not a valid e-mail address")

def arg_password(password):
    try:
        return re.match(r"^\S{6,}$", password).group(0)
    except:
        raise argparse.ArgumentTypeError("incorrect password (min 6 chars)")

def create_user(args):
    args = parse_args(args)

    try:
        galaxy = bioblend.galaxy.GalaxyInstance(args.url, args.api)
        galaxy.users.create_local_user(args.galaxy_user.split("@")[0].lower(), args.galaxy_user, args.galaxy_password)
        sys.exit(0)
    except Exception as err:
        print("Error creating user: {}".format(err))
        sys.exit(1)

if __name__ == "__main__":
    create_user(sys.argv[1:])
