from httpx import HTTPStatusError
from argparse import ArgumentParser, Namespace

from user_settings import UserSettings
from client import Client


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="""Get coordinates of a given address.
                                               Receive suggestions for quicker data input.""",
                            add_help=False,
                            epilog='Press Ctrl+C or Ctrl+Z to exit program')
    parser.add_argument('-h', action='help',
                        help='Run program with no arguments to get started',
                        )
    parser.add_argument('-l', '--language', metavar='en/ru', type=str, help='Changes suggestions language')
    parser.add_argument('-k', '--key', metavar='api_key', type=str, help='Sets new api_key')
    parser.add_argument('-s', '--secret', metavar='secret_key', type=str, help='Sets new secret key')
    parser.add_argument('-b', '--base_url', metavar='base_url', type=str, help='Sets new base_url')

    return parser.parse_args()


def main():

    args = parse_arguments()

    while True:

        try:
            client = Client(args)
            settings = UserSettings()

            settings.create_table()
            client.check_settings(settings)

            lang, base, api, secret = settings.get_user_settings()
            if (api, secret) == (None, None) or (not api) or (not secret):  # at first start there are no keys in DB
                raise TypeError

            proposed_address = input("Enter address to get coordinates\n")
            if proposed_address:
                result = client.get_suggestions(proposed_address, api, secret, language=lang)

                if not result:
                    continue

            option = int(input("Choose an option\n"))
            if option <= 0:  # avoiding negative indices
                raise IndexError
            chosen_suggestion = result[option - 1]['value']

            final = client.get_coordinates(chosen_suggestion, api, secret)
            if final[1] and final[2]:
                print(f"Coordinates for {final[0]} are:\n Lat {final[1]} Long {final[2]}")
            else:
                print(f"Unable to get coordinates for {final[0]}")  # processing results with no coordinates

        except IndexError:  # if chosen suggestion is out of list's range
            print("There is something wrong with your choice. Try again")
            continue

        except (HTTPStatusError, TypeError):  # if there is no key in DB or if it's wrong
            print('There is something wrong with your api key or secret key.\n'
                  'Try setting a new key using \'-k\' or \'-s\' flags')
            break

        except (KeyboardInterrupt, EOFError):  # Ctrl+C or Ctrl+Z to exit
            print("Program was stopped")
            break

        except ValueError:  # if validation failed
            print("Your key is not valid. Please enter a valid key")
            break


if __name__ == '__main__':
    main()
