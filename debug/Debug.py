class Debug:
    debug_mode = True

    @staticmethod
    def log(log):
        if Debug.debug_mode:
            print(log)
