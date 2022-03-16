import logging
class NoEngine(Exception):
    """ raise for incalid or none engine"""
    def __init__(self,message = "engine not defined", data = None ,*args,**kwargs):
        super(NoEngine,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))

class SessionFailed(Exception):
    """ raise failed to create session"""
    def __init__(self,message = "session could not be established", data = None ,*args,**kwargs):
        super(SessionFailed,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class UnhandledError(Exception):
    """ raise unhandled error"""
    def __init__(self,message = "unhandled error", data = None ,*args,**kwargs):
        super(UnhandledError,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))

class ValidationError(Exception):
    """ raise validation error"""
    def __init__(self,message = "validation falied", data = None ,*args,**kwargs):
        super(ValidationError,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))

class DataError(Exception):
    """ raise for invalid data or epmty data dictionary"""
    def __init__(self,message = "empty data dictionary", data = None ,*args,**kwargs):
        super(DataError,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class NoDataFound(Exception):
    """ raise record does not exist / no data found"""
    def __init__(self,message = "empty data dictionary", data = None ,*args,**kwargs):
        super(NoDataFound,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class TooManyRows(Exception):
    """ raise record does not exist / no data found"""
    def __init__(self,message = "empty data dictionary", data = None ,*args,**kwargs):
        super(TooManyRows,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class InsertFailed(Exception):
    """ raise insert failed"""
    def __init__(self,message = "insert failed", data = None ,*args,**kwargs):
        self.data = data
        logging.error("{} : {}".format(message,data))
        print(message)
        super(InsertFailed,self).__init__(self,message)



class UpdateFailed(Exception):
    """ raise update failed"""
    def __init__(self,message = "update failed", data = None ,*args,**kwargs):
        super(UpdateFailed,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class DeleteFailed(Exception):
    """ raise insert failed"""
    def __init__(self,message = "delete failed", data = None ,*args,**kwargs):
        super(DeleteFailed,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))


class MergeFailed(Exception):
    """ raise merge failed"""
    def __init__(self,message = "merge failed", data = None ,*args,**kwargs):
        super(MergeFailed,self).__init__(self,message)
        self.data = data
        logging.error("{} : {}".format(message,data))