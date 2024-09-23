import os
import customtkinter
from PIL import Image

from Billgen import PDF, generat_bill_id, generate_qr_code

class ItemFrames(customtkinter.CTkFrame):
    def __init__(self, master, corner_radius=5, item_image_path='', item_name='', item_price='', add_callback=None, remove_callback=None):
        super().__init__(master, corner_radius=corner_radius)

        self.itemName = item_name
        self.itemPrice = int(item_price)

        self.add_callback = add_callback
        self.remove_callback = remove_callback



        self.rowconfigure((0,3), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        self.itemImage = customtkinter.CTkImage(light_image=Image.open(item_image_path), size=(70,70))
        self.itemLable = customtkinter.CTkLabel(self,image=self.itemImage,text='')
        self.itemLable.grid(row=0,pady=5, padx=5, columnspan=2)

        # name section
        self.itemLableName = customtkinter.CTkLabel(self,text=item_name)
        self.itemLableName.grid(row=1,pady=0, padx=0, columnspan=2)

        # price section
        self.itemLablePrice = customtkinter.CTkLabel(self,text=f'{item_price}$',font=('arial', 10, 'bold'))
        self.itemLablePrice.grid(row=2,pady=0, padx=0, columnspan=2)


        self.button = customtkinter.CTkButton(self, text="-", corner_radius=5 , width=50, fg_color='red',command=self.remove_item)
        self.button.grid(row=3,column=0,pady=5, padx=5)
        self.button = customtkinter.CTkButton(self, text="+", corner_radius=5 , width=50, fg_color='green',command=self.add_item)
        self.button.grid(row=3,column=1,pady=5, padx=5)

        # for the buttons we need functions
    def add_item(self):
        if self.add_callback:
            self.add_callback(self.itemName,self.itemPrice)
        
    def remove_item(self):
        if self.remove_callback:
            self.remove_callback(self.itemName, self.itemPrice)


        
class CustomerDetailFrame(customtkinter.CTkFrame):
    def __init__(self,master, lableName=''):
        super().__init__(master)

        self.columnconfigure((0,2),weight=0)
        self.rowconfigure((0,2), weight=1)

        self.customerLable = customtkinter.CTkLabel(self, text=lableName, width=160)
        self.customerLable.grid(row=1, padx=5, columnspan=2)

        self.customerNameEntry = customtkinter.CTkEntry(self,width=200, height=30, border_width=0,fg_color='white', text_color='black')
        self.customerNameEntry.grid(row=1, column=3, pady=5, padx=5)

class ProccedClearButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, proceed_callback, clear_callback):
        super().__init__(master,width=150)

        self.columnconfigure((0,1), weight=0)
        self.rowconfigure(0,weight=0)

        self.generateBill = customtkinter.CTkButton(self, text="Proceed",width=180, command=proceed_callback)
        self.generateBill.grid(row=0, column=0, padx=2, pady=4)

        self.clearBill = customtkinter.CTkButton(self, text="Clear",width=190, command=clear_callback)
        self.clearBill.grid(row=0, column=1, padx=2, pady=4)


class DisplayOrderedItemFrame(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master, width=150)

        self.cartLabel = customtkinter.CTkLabel(self,text="Orders:",font=('arial',12,'bold'))
        self.cartLabel.grid(row=0, column=0, padx=4, pady=4, stick="w")

        self.addedItems = customtkinter.CTkLabel(self,text="No Items are added", font=('arial',12,'bold'),justify="left")
        self.addedItems.grid(row=1,column=0, pady=0, padx=4, stick="w")

        self.totalPrice = customtkinter.CTkLabel(self, text="Total: 0$",font=('arial',12,'bold'))
        self.totalPrice.grid(row=3, column=0, sticky='w',pady=10, padx=4)

    # function for update the addedItem text and price
    def updateItems(self,items, total_price):
        display_text = "\n".join([f"{item}: {quantity}x {price}" for item, (quantity, price) in items.items()])
        self.addedItems.configure(text=display_text)

        self.totalPrice.configure(text=f"Total: {total_price}$")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.items = {}
        self.total_price = 0


        self.geometry("410x600")
        self.resizable(False, False)
        self.title("Bill Gen App")
        self.grid_columnconfigure((0,5),weight=1)
        # self.grid_rowconfigure((0,10),weight=1)

        self.title = customtkinter.CTkLabel(self, text="RoadStopC", font=('Arial', 30, 'bold'))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(current_dir,'images','burger.png')
        imagePath2 = os.path.join(current_dir,'images','fries.png')
        imagePath3 = os.path.join(current_dir,'images','soda.png')
        


        self.frame = customtkinter.CTkFrame(self,fg_color='transparent' , width=150, height=150)
        self.frame.grid(row=1, column=0, sticky="ew", padx=10)



        # testing custom class
        self.image = ItemFrames(self.frame,item_image_path=imagePath,item_name='Burger', item_price='20',add_callback=self.add_item, remove_callback=self.remove_item)
        self.image.grid(row=0, column=0, padx=5)

        self.image2 = ItemFrames(self.frame,item_image_path=imagePath2, item_name='fries', item_price='20',add_callback=self.add_item, remove_callback=self.remove_item)
        self.image2.grid(row=0, column=2,padx=5)

        self.image3 = ItemFrames(self.frame,item_image_path=imagePath3, item_name='cola', item_price='30',add_callback=self.add_item, remove_callback=self.remove_item)
        self.image3.grid(row=0, column=3,padx=5)



        
        #space for customer name entry
        self.customerSection = customtkinter.CTkFrame(self)
        self.customerSection.grid(row=6, column=0, sticky='w', padx=15, pady=15)

        self.cSection = CustomerDetailFrame(self.customerSection,lableName='Customer Name')
        self.cSection.pack()

        #sapce for customer contact entry
        self.customerContactSection = customtkinter.CTkFrame(self)
        self.customerContactSection.grid(row=7, column=0, pady=4, padx=15, sticky='w')

        self.numberSection = CustomerDetailFrame(self.customerContactSection, lableName='Customer Contact')
        self.numberSection.pack()


        #proceedClearButtonSectio
        self.proceedCbutton = ProccedClearButtonFrame(self, proceed_callback=self.proceedTheOrder, clear_callback=self.clearTheOderSection)
        self.proceedCbutton.grid(row=8, column=0, stick="w", padx=15, pady=10)


        #CurrentOrder DisplaySection 
        self.orderDisplaySection = DisplayOrderedItemFrame(self)
        self.orderDisplaySection.grid(row=9, column=0, stick='ew', padx=15, pady=10)

        # copyright info
        self.copyrightInfo = customtkinter.CTkLabel(self, text="buit with 💖 by 2udu-dev 2024")
        self.copyrightInfo.grid(stick="s")
    

    # function for the callbacks
    def updateItemDisplay(self):
        self.orderDisplaySection.updateItems(self.items, self.total_price)

    def add_item(self,item_name, item_price):
        if item_name in self.items:
            self.items[item_name] = (self.items[item_name][0]+1, item_price)
        else:
            self.items[item_name] = (1, item_price)
        
        self.total_price += item_price

        self.updateItemDisplay()
    
    def remove_item(self, item_name, item_price):
        if item_name in self.items and self.items[item_name][0] > 0:
            self.items[item_name] = (self.items[item_name][0] -1 , item_price)
            self.total_price -= item_price

            # if the item count is zero then we remove the item from the list
            if self.items[item_name][0] == 0:
                del self.items[item_name]
        
        self.updateItemDisplay()
    
    # proceedFunction to process the order
    def proceedTheOrder(self):
        customerName = self.cSection.customerNameEntry.get()
        customerNumber = self.numberSection.customerNameEntry.get()

        if self.items == {} :
            self.orderDisplaySection.addedItems.configure(text="Add Items First")
        elif customerName == "" or customerNumber == "":
            self.orderDisplaySection.addedItems.configure(text="Add Customer Details")
        else:
            # print(f"Order is processing for {customerName} number {customerNumber}")
            # print(self.items)
            pdf = PDF(orientation='P', unit='mm', format=(50, 110))
            pdf.add_page()
            bill_id = generat_bill_id().replace('/','_')
            generate_qr_code(data=self.items,customer_name=customerName,contact=customerNumber, billId=bill_id)
            pdf.customerInfo(customerName, customerNumber,bill_id )
            pdf.order_info(self.items)

            pdf.output(f'{bill_id}_invoice.pdf')
            self.orderDisplaySection.addedItems.configure(text="Bill Generated")

    # clear function to clear the display sectIon 
    def clearTheOderSection(self):
        self.items = {}
        self.total_price = 0
        self.updateItemDisplay()







if __name__ == "__main__":
    app = App()
    app.mainloop()
