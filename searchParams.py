class SearchParams:
    def __init__(self):
        self.max_retrieval_count = 0
        self.search_query = None
        self.account_name = None
        self.since_date = None
        self.until_date = None
        self.language = None
        self.proxy = None
        self.op = None
        self.logging = None
        self.log_file_name = None
        # Get log file name from logger:     print(logging.root.handlers[0].baseFilename)

    def set_max_retrieval_count(self, max_retrieval_count):
        self.max_retrieval_count = max_retrieval_count

    def set_search_query(self, search_query):
        self.search_query = search_query

    def set_user_name(self, account_name):
        self.account_name = account_name

    def set_since_date(self, since_date):
        self.since_date = since_date

    def set_until_date(self, until_date):
        self.until_date = until_date

    def set_language(self, language):
        self.language = language

    def set_proxy(self, proxy):
        self.proxy = proxy

    def set_op(self, op):
        self.op = op

    def set_log_file_name(self, log_file_name):
        self.log_file_name = log_file_name

    def set_logger(self, logger):
        self.logging = logger
