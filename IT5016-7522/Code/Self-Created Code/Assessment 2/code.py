import os
import csv

# Ticket data for example output to put inside of a csv file.
tickets_data = [
    {
        'Ticket Number': 2001,
        'Staff Name': 'Inna',
        'Staff ID': 'INNAM',
        'Email': 'inna@whitecliffe.co.nz',
        'Description': 'My monitor stopped working',
        'Response': 'Not Yet Provided',
        'Status': 'Open'
    },
    {
        'Ticket Number': 2002,
        'Staff Name': 'Maria',
        'Staff ID': 'MARIAH',
        'Email': 'maria@whitecliffe.co.nz',
        'Description': 'Request for a videocamera to conduct webinars',
        'Response': 'Not Yet Provided',
        'Status': 'Open'
    },
    {
        'Ticket Number': 2003,
        'Staff Name': 'John',
        'Staff ID': 'JOHNS',
        'Email': 'john@whitecliffe.co.nz',
        'Description': 'Password change',
        'Response': 'New password generated: JOJoh',
        'Status': 'Closed'
    }
]

# Above data gets placed into a .CSV file if file doesn't already exist, to retain any/all changes and data of the database. 
filename = 'database.csv'
with open(filename, 'w', newline='') as file:
    database = csv.DictWriter(file, fieldnames=['Ticket Number', 'Staff Name', 'Staff ID', 'Email', 'Description', 'Response', 'Status'])
    database.writeheader()
    database.writerows(tickets_data)

print(f"Ticket Database created: {filename}.")


class Ticket:
    total_tickets_submitted = 0 # 0 by default, changes based on .csv file
    total_tickets_resolved = 0 # 0 by default, changes based on .csv file

    def __init__(self, ticket_id, staff_name, staff_id, email, description, response=None, status="Open"): # Response is none by default. Status Open by default. 
        self.ticket_id = ticket_id # 2000 + 1 over the last ticket (e.g if last ticket is 2002, next one will be 2003.)
        self.staff_name = staff_name 
        self.staff_id = staff_id # e.g. INNAM, MARIAH, etc. 
        self.email = email # Requires @ to be used or won't submit, code on that below at elif choice == 6. 
        self.description = description # The Issue
        self.response = response if response is not None else "Not Yet Provided"
        self.status = status

    @classmethod
    def load_tickets(cls, filename):
        tickets = []
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticket = Ticket(
                    int(row['Ticket Number']),
                    row['Staff Name'],
                    row['Staff ID'],
                    row['Email'],
                    row['Description'],
                    row.get('Response'),  # No default value for response
                    row.get('Status', 'Open')  # Default to 'Open' if status is not provided
                )
                tickets.append(ticket)
        return tickets

    @classmethod
    def save_tickets(cls, tickets, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Ticket Number', 'Staff Name', 'Staff ID', 'Email', 'Description', 'Response', 'Status'])
            writer.writeheader()
            for ticket in tickets:
                writer.writerow({
                    'Ticket Number': ticket.ticket_id,
                    'Staff Name': ticket.staff_name,
                    'Staff ID': ticket.staff_id,
                    'Email': ticket.email,
                    'Description': ticket.description,
                    'Response': ticket.response,
                    'Status': ticket.status
                })



def respond_to_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket.ticket_id == ticket_id:
            response = input("Enter your response: ")
            ticket.response = response
            ticket.status = "Closed"
            print("Response Submitted. The Ticket is now Closed.")
            return True
    print("TicketID not found.")
    return False


def reopen_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket.ticket_id == ticket_id:
            ticket.status = "Open"
            print("Ticket reopened successfully.")
            return True
    print("TicketID not found.")
    return False


def TicketStats(tickets):
    print("\nStatistics:")
    print(f"Tickets Created: {len(tickets)}")
    print(f"Tickets Resolved: {sum(ticket.status == 'Closed' for ticket in tickets)}")
    print(f"Tickets to Solve: {len(tickets) - sum(ticket.status == 'Closed' for ticket in tickets)}")


def show_tickets(tickets):
    for ticket in tickets:
        print("Ticket Number:", ticket.ticket_id)
        print("Ticket Staff:", ticket.staff_name)
        print("Staff ID:", ticket.staff_id)
        print("Email Address:", ticket.email)
        print("Description:", ticket.description)
        print("Response:", ticket.response)
        print("Ticket Status:", ticket.status)
        print()


def show_main_menu():
    print("\nPlease Choose from the Following:")
    print("1. See Open Tickets")
    print("2. See Closed Tickets")
    print("3. See All Tickets")
    print("4. Respond to Ticket")
    print("5. Reopen Ticket")
    print("6. Create Ticket")
    print("7. Exit")


def main():
    filename = 'database.csv'
    tickets = Ticket.load_tickets(filename)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        TicketStats(tickets)
        show_main_menu()

        choice = input("\nEnter your choice: ")  # Add an extra newline before the prompt

        if choice == '1': # See Open Tickets
            open_tickets = [ticket for ticket in tickets if ticket.status == 'Open']
            show_tickets(open_tickets)
            input("Press Enter to go back.")
        elif choice == '2': # See Closed Tickets          
            closed_tickets = [ticket for ticket in tickets if ticket.status == 'Closed']
            show_tickets(closed_tickets)
            input("Press Enter to go back.")
        elif choice == '3': # See All Tickets
            show_tickets(tickets)
            input("Press Enter to go back.")
        elif choice == '4': # Respond to Ticket
            while True:
                ticket_input = input("Enter ticket number to respond or 'view' to view open tickets: ")
                if ticket_input.lower() == 'view': 
                    open_tickets = [ticket for ticket in tickets if ticket.status == 'Open']
                    show_tickets(open_tickets)
                elif ticket_input.isdigit():
                    ticket_id = int(ticket_input)
                    respond_to_ticket(tickets, ticket_id)
                    Ticket.save_tickets(tickets, filename)  
                    input("Press Enter to go back.")
                    break
        elif choice == '5': # Reopen Ticket
            while True: 
                ticket_input = input("Enter ticket number to reopen or 'view' to view closed tickets: ")
                if ticket_input.lower() == 'view':
                    closed_tickets = [ticket for ticket in tickets if ticket.status == 'Closed']
                    show_tickets(closed_tickets)
                elif ticket_input.isdigit():
                    ticket_id = int(ticket_input)
                    if not reopen_ticket(tickets, ticket_id):
                        continue
                    Ticket.save_tickets(tickets, filename) 
                    input("Press Enter to go back.")
                    break
        elif choice == '6': # Create Ticket
            staff_name = input("Enter Your Name: ")
            staff_id = input("Enter Your StaffID: ")
            while True:
                email = input("Enter Your Business Email: ")
                if "@" in email:
                    break
                else:
                    print("Invalid email address. Please include @ in the email address.")
                    
            description = input("Please enter a description of the issue or question you have: ")
            
            if "password change" in description.lower(): # Generate Password
                new_password = staff_id[:2] + staff_name[:3]
                response = f"Your New Password Is: {new_password}"
                status = "Closed"
            else:
                status = "Open"
                response = ""

            ticket_id = len(tickets) + 2001  # Increment ticket number
            new_ticket = Ticket(ticket_id, staff_name, staff_id, email, description, response, status)
            tickets.append(new_ticket)
            print("Ticket submitted successfully.")
            Ticket.save_tickets(tickets, filename) 
            input("Press Enter to continue...")
        elif choice == '7':
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before exiting
            print("Exiting program.")
            input("Press Enter to continue...")  # Wait for Enter key before exiting
            break
        elif choice == 'easteregg'.lower(): 
            print("""
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⠤⠀⠀⠤⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡆⠈⢠⣾⣷⡄⠁⢰⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠠⠆⠈⠋⠀⠶⠄⠙⠋⠠⠶⠀⠙⠁⠰⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡉⠹⣿⠏⠉⢿⡿⠉⠉⢿⡿⠉⠹⣿⠏⢉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⠀⡿⠀⡇⠸⡇⢸⡇⢸⠇⢸⠀⢿⠀⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣦⣤⣼⣿⣤⣤⣾⣷⣤⣤⣿⣧⣤⣴⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⣤⣤⡤⠀⡀⠠⣤⣤⣤⣤⠄⢀⠀⢤⣤⣤⠄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⠋⣤⣾⣿⣷⡌⠛⠛⢡⣾⣿⣷⣤⠙⠏⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
""")
            input("Press Enter to continue...")  # Wait for Enter key before exiting



if __name__ == "__main__":
    main()
