from dotenv import load_dotenv

from database.populate import run

load_dotenv()

if __name__ == "__main__":
    run()
