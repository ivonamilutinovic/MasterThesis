import argparse

from train_wiser.backend.utils.log import get_logger
from train_wiser.backend.utils.prepare_data_for_training import merge_all_race_results
from train_wiser.backend.utils.run_info_utils import count_number_of_data

LOGGER = get_logger(__name__)


def main():
    # TODO: Calling race_results_spiders
    args = parse_command_line_params()

    if args.prepare_data_for_training:
        merge_all_race_results()
        # prepare_data_for_training()
    if args.print_number_of_data:
        number_of_data = count_number_of_data()
        print(f"{number_of_data}")


def parse_command_line_params() -> argparse.Namespace:
    """
    Parse command line arguments
    :return: command line arguments
    """
    return get_parser().parse_args()


def get_parser() -> argparse:
    """ Returns parser of command line arguments """
    parser = argparse.ArgumentParser()

    # General arguments - Optional
    parser.add_argument('--print-number-of-data',
                        action='store_true',
                        help='Prints number of data per race organization')
    parser.add_argument('--prepare-data-for-training',
                        action='store_true')
    return parser


if __name__ == '__main__':
    main()


