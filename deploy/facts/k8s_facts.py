from  pyinfra.api import FactBase

class K8sInitialized(FactBase):
    '''
    Returns a boolean indicating whether cluster is nitialized or not.
    '''

    def command(self):
        return """
        (kubectl get nodes > /dev/null 2>&1) &&  echo 'cluster initialized'
        """

    def process(self, output):
        return any(["initialized" in el for el in output])