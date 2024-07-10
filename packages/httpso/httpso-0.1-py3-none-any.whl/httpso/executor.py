import json
import subprocess

from .binder import Binder


class Executor:
    def run(self, data):
        # Start the C# executable and communicate via stdin/stdout
        process = subprocess.Popen(
            [Binder().cmdlet()],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # Send data to the C# executable
        stdout, stderr = process.communicate(input=json.dumps(data).encode())

        try:
            # Read the response
            response = json.loads(stdout.decode())
        except:
            raise Exception(stdout)

        return response