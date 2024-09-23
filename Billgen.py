from fpdf import FPDF, XPos
import datetime
import qrcode
import qrcode.constants



class PDF(FPDF):
    def header(self):
        
        self.set_y(0)
        self.set_font('helvetica', '', 9)
        self.cell(25,2,'----------------------------------------------------------------------------------------------------------------------', align='C')
        self.ln()
        self.set_y(3)
        self.set_font('helvetica', 'B', 9)
        self.cell(0,2,'Invoice', align='C')
        self.ln(3)

        self.set_font('helvetica', '', 7)
        self.cell(0,2,'The 24/7 Road Stop Center', align='C')
        self.ln(5)
        # adding a line
        
        self.set_line_width(0.01)
        self.line(0,self.get_y(),50,self.get_y())
    
    def footer(self):
        self.set_y(-40)
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(0, 0, 0)
        self.set_font('helvetica','B', 10)
        self.cell(0,0, 'PAID', align='C')
        self.ln(5)
        self.image('qr_code.png', x=15, w=20, h=20)
        self.cell(0,2,'Thank You ! See you again ', align='C')
        self.ln(5)
        self.set_x(0)
        self.set_font('helvetica', 'B', 6)
        self.multi_cell(50,2,'For any kind of help please contact our customer-care number 123-456-789 or mail us at roadstar247@gmail.com ')
        self.ln()
        self.set_x(0)
        self.cell(25,2,'----------------------------------------------------------------------------------------------------------------------', align='C')
        


    def customerInfo(self, name, contact, billId):
        s_pos = self.get_y()
        self.set_y(s_pos+3)
        self.set_x(0)
        # cutomer part
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(0, 0, 0)
        self.cell(15,0,'Customer:', align='L')
        self.set_font('helvetica', '', 8)
        self.cell(0,0,name, align='L')

        # contact part
        self.ln(4)
        self.set_x(0)

        
        self.set_font('helvetica', 'B', 8)
        self.cell(15,0,'Contact:', align='L')
        self.set_font('helvetica', '', 8)
        self.cell(0,0,contact, align='L')

        # bill id part
        self.ln(4)
        self.set_x(0)

        self.set_font('helvetica', 'B', 6)
        self.cell(0,0,billId, align='L')

    def order_info(self,data):
        s_pos = self.get_y()
        self.set_y(s_pos + 5)
        self.set_x(0)
        
        self.set_line_width(0.01)
        self.line(0,s_pos+3,50,s_pos+3)

        self.set_font('helvetica', 'B', 8)
        self.set_text_color(0, 0, 0)
        self.cell(16,0, 'Item', new_x=XPos.RIGHT, align='L')
        self.cell(18,0, 'Amount',new_x=XPos.RIGHT, align='C')        
        self.cell(16,0, 'Price',new_x=XPos.RIGHT, align='R')
        self.ln(5)

        total_item = 0
        total_price = 0

        for item, (amount, price) in data.items():
            item_name, amount, price = item, amount, price
            price = float(price)
            total_item += int(amount)
            total_price += float(price*amount)
            self.set_x(0)
            self.set_font('helvetica', '', 8)
            self.cell(16,0,str(item_name), new_x=XPos.RIGHT, align='L')
            self.cell(18,0, str(amount),new_x=XPos.RIGHT, align='C')        
            self.cell(16,0, f'{price:.2f}',new_x=XPos.RIGHT, align='R')
            self.ln(4)
        
        
        self.set_x(0)
        self.set_line_width(0.01)
        self.line(0,self.get_y(),50,self.get_y())

        self.ln(4)
        self.set_x(0)
        self.cell(16,0, f'Total Items: {total_item} ',new_x=XPos.RIGHT, align='L')
        self.ln(4)
        self.set_x(0)
        self.cell(16,0, f'Total Price: {total_price:.2f} ',new_x=XPos.RIGHT, align='L')

                
#imporant fucntions
def get_time_of_day():

    now = datetime.datetime.now()
    current_hour = now.hour
    if 5 <= current_hour <= 10 :
        return 'MORNING'
    elif 11 <= current_hour <= 13:
        return 'DAY'
    elif 14 <= current_hour <= 16:
        return 'NOON'
    elif 17 <= current_hour <= 19:
        return 'EVENING'
    elif 20 <= current_hour <= 23:
        return 'NIGHT'
    else:
        return 'MIDNIGHT'

def generat_bill_id():
    get_current_hour = get_time_of_day()
    now = datetime.datetime.now()
    bill_id = now.strftime('%Y%m%D%H%M%S')
    
    return f'{get_current_hour}-BILL-{bill_id}'

def generate_qr_code(data, customer_name, contact, billId):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10, border=4)
    qr.add_data(f'-Customer:{customer_name}\n-Contact:{contact}\nItems-Amount-Price\n{data}\n-Bill-ID: {billId}')
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_path = "qr_code.png"
    img.save(img_path)

'''Here is the use case of pdf class'''
# data = {
#     "BURGER":(1,20),
#     "Fries":(2,30),
#     "Cola":(3,30)
# }

# pdf = PDF(orientation='P', unit='mm', format=(50, 110))
# pdf.add_page()
# bill_id = generat_bill_id()
# generate_qr_code(data=data,customer_name='jonny',contact='1234', billId=bill_id)
# pdf.customerInfo('Jonny', '1234',bill_id )
# pdf.order_info(data)

# pdf.output('invoice.pdf')