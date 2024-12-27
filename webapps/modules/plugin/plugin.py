


from abc import abstractmethod



class Plugin():

    @abstractmethod
    def endpoints(self):
        pass

