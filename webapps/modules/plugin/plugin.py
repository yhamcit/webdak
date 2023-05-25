


from abc import abstractproperty



class Plugin():

    @abstractproperty
    def endpoints(self):
        pass

