IS_RELEASE_SERVER = True if input() == "true" else False
DEBUG = True if not IS_RELEASE_SERVER else False
