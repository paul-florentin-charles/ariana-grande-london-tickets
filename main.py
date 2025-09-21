from ticketmaster_scraper import check_ticketmaster
from axs_scraper import check_axs
from notifier import send_notification

def main():
    """
    Main function to run the scrapers and send notifications.
    """
    print("Starting ticket availability check...")
    tm_available, tm_url = check_ticketmaster()
    axs_available, axs_url = False, "" #check_axs()

    if tm_available or axs_available:
        send_notification(ticketmaster_url=tm_url, axs_url=axs_url)
    else:
        print("No tickets found. No notification sent.")

if __name__ == "__main__":
    main()
