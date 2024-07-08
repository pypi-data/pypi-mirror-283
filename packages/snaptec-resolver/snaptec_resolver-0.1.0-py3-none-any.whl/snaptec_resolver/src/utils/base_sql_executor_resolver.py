
class BaseSQLExecutorResolver:
    def __init__(self) -> None:
        self._post_init()

    def _post_init(self):
        # Action after init the class
        print(f' Resolver {self.__class__.__name__} created')

    def _before_init(self):
        # preprocess step 1
        pass

    def _init(self):
        # step 1
        pass

    def _after_init(self):
        # postprocess step 1
        pass

    def _before_connect_to_database(self):
        # preprocess step 2
        pass

    def _connect_to_database(self):
        # step 2
        pass

    def _after_connect_to_database(self):
        # postprocess step 2
        pass

    def _before_get_data(self):
        # preprocess step 3
        pass

    def _get_data(self):
        # step 3
        pass

    def _after_get_data(self):
        # postprocess step 3
        pass

    def _before_format_result(self):
        # preprocess step 4
        pass

    def _format_result(self):
        # step 4
        pass

    def _after_format_result(self):
        # postprocess step 4
        pass
    

    def template_method(self):
        # Step 1: Init
        self._before_init()
        self._init()
        self._after_init()
        # Step 2: Connect to databases
        self._before_connect_to_database()
        self._connect_to_database()
        self._after_connect_to_database()
        # Step 3: Get data
        self._before_get_data()
        self._get_data()
        self._after_get_data()
        # Step 4: Format result
        self._before_format_result()
        self._format_result()
        self._after_format_result()
