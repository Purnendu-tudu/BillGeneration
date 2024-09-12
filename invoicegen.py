import os
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from datetime import datetime  # Import datetime module

# Function to take user input for invoice details
def take_user_input():
    customer_name = input("Enter customer name: ")
    customer_phone = input("Enter customer phone number: ")
    customer_email = input("Enter customer email: ")
    customer_address = input("Enter customer address: ")

    items = []
    while True:
        item_name = input("Enter item name (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        item_price = float(input(f"Enter price for {item_name}: "))
        item_qty = int(input(f"Enter quantity for {item_name}: "))
        total_price = item_price * item_qty
        items.append(f"{item_name}: {item_qty} x ${item_price:.2f} = ${total_price:.2f}")

    return customer_name, customer_phone, customer_email, customer_address, items

# Function to display the menu
def display_menu():
    print("\n===== Invoice Generator Menu =====")
    print("1. Generate Invoice")
    print("2. Exit")

# Create PDF document
def generate_invoice(file_path, customer_name, customer_phone, customer_email, customer_address, items):
    # Custom paper size (3.25 inches x 11 inches)
    custom_page_size = (3.25 * inch, 11 * inch)
    
    doc = SimpleDocTemplate(file_path, pagesize=custom_page_size)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    # Get current date
    current_date = datetime.now().strftime("%d %B %Y")
    
    # Title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Paragraph("Fauget Steak House", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Invoice Info
    elements.append(Paragraph("<b>Invoice To :</b>", styles['Normal']))
    elements.append(Paragraph(customer_name, styles['Normal']))
    elements.append(Paragraph(customer_phone, styles['Normal']))
    elements.append(Paragraph(customer_email, styles['Normal']))
    elements.append(Paragraph(customer_address, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(f"Date : {current_date}", styles['Normal']))
    elements.append(Paragraph("Invoice No : #12345", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Display items as plain text
    for item in items:
        elements.append(Paragraph(item, styles['Normal']))
    
    # Total
    total_cost = sum(float(item.split('= $')[1]) for item in items)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Total :</b> ${total_cost:.2f}", styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Bank Info
    elements.append(Paragraph("Bank Info", styles['Normal']))
    elements.append(Paragraph("Bank Name : Fauget", styles['Normal']))
    elements.append(Paragraph("Bank Account : 123-456-7890", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    print(f"PDF invoice generated at {file_path}")

# Main function to handle the user input and menu
def main():
    # Define output directory
    output_dir = 'output'
    
    # Check if output directory exists, create it if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Get input from user
            customer_name, customer_phone, customer_email, customer_address, items = take_user_input()
            
            # Sanitize customer name for file name
            sanitized_name = customer_name.replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_')
            
            # Get current date for file name
            current_date = datetime.now().strftime("%Y%m%d")
            
            # File path for output PDF
            file_name = f"invoice_{sanitized_name}_{current_date}.pdf"
            file_path = os.path.join(output_dir, file_name)
            
            # Generate the invoice PDF
            generate_invoice(file_path, customer_name, customer_phone, customer_email, customer_address, items)
        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
