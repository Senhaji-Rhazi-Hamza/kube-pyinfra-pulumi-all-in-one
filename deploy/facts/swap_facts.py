from  pyinfra.api import FactBase

class SwapEnabled(FactBase):
    '''
    Returns a boolean indicating whether swap is enabled.
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