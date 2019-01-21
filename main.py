import logging
import os
import sys
import click
from scraper import parse_json
from searchParams import SearchParams


@click.command()
@click.option('--searchquery', default=None, help='Query to be searched on twitter')
@click.option('--username', default=None, help='User to search for')
@click.option('--since', default=None, help='Start date in the format yyyy-mm-dd (e.g: 2017-08-25)')
@click.option('--until', default=None, help='End date in the format yyyy-mm-dd (e.g 2019-01-20)')
@click.option('--language', default='en', help='Tweet language to search for')
@click.option('--maxcount', default=0, help='Max number of tweets you want to grab')
@click.option('--proxy', default=None, help='Proxy ip to use')
@click.option('--op', default='op.csv', help='Output file to save the tweets (default: op.csv)')
@click.option('--log', default='def_log.log', help='Log file name to log search index (default: def_log.log)')
def arg_parser(searchquery, username, since, until, language, maxcount, proxy, op, log):
    """
    Python based Twitter Scraper. \n
    Provide search parameters when running this script. \n
    Example: python main.py --searchquery notpetya --since 2017-06-07 --until 2017-07-15 --op notpetya.csv --log test.log
    """
    search_parameters = SearchParams()
    search_parameters.set_search_query(searchquery)
    search_parameters.set_user_name(username)
    search_parameters.set_since_date(since)
    search_parameters.set_until_date(until)
    search_parameters.set_language(language)
    search_parameters.set_max_retrieval_count(maxcount)
    search_parameters.set_proxy(proxy)
    search_parameters.set_op(op)
    search_parameters.set_log_file_name(log)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=search_parameters.log_file_name,
                        filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    search_parameters.set_logger(logging)

    with open(search_parameters.op, 'a+') as f:
        if os.stat(search_parameters.op).st_size == 0:
            f.write('uuid;tweet_id;user_name;screen_name;tweet;date_time;retweet_count;fav_count;link\n')

    parse_json(search_parameters)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print('Python 3 not found. Please install Python 3.x and try again')
    else:
        arg_parser(sys.argv[1:])
