from  pyinfra.api import FactBase

class IpAdress(FactBase):
    '''
    Returns the value of the ip adress of the host
    '''

    def command(self):
        return """
        if su -c 'swapon --show' | read REPLY; then
            echo "True"
        else
            echo "False"
        fi
        """

    def process(self, output):
        return "True" in output