from pprint import pprint

import uvicorn

from fastapi import FastAPI

from config import (
    WEBHOOK_URL,
    WEBHOOK_PATH,
)



def run_wsgi():
    print("Wsgi is running!..")
    # APP
    # app: FastAPI = run_app()
    uvicorn.run(app="app:run_app", host="0.0.0.0", port=8000, reload=True, workers=1)
    print("Wsgi has finished running!..")



def main():
    print("MAIN")
    # init_db(db, DB_FILENAME) <- an extra process locks an sqlite db
    run_wsgi()


if __name__ == "__main__":
    try:
        print("MAIN")
        print("path ", WEBHOOK_PATH, "\nurl", WEBHOOK_URL)
        main()
        # polling_flow()
    except KeyboardInterrupt as e:
        print(e)
