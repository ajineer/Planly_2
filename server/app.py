import sys
import os
from . import create_app

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
