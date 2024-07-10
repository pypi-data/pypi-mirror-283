from datetime import datetime
from pdf_crawler.ui import UI
#from ui import UI

def main():
    expiration_date = datetime(2024, 9, 1)

    current_date = datetime.now()

    if current_date < expiration_date:
        app = UI()
        app.run()
    else:
        print("Your Trial has expired!")

if __name__ == "__main__":
    main()
