from json.decoder import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import json
import string
import random


window = Tk() # instantiate of a window
window.geometry("600x400") #dimensions of the window
window.title("Password Manager") 
window.config(background="#F7672D")

#Declaration of some objects
site_text=StringVar()
password_text=StringVar()
uname_text=StringVar()

#function to copy password into your clipboard
def copy_button():

    if password_text.get()=="":
        messagebox.showerror("Error","Nothing to Copy")

    clip = Tk()
    clip.withdraw()
    clip.clipboard_clear()
    clip.clipboard_append(password_text.get())  
    clip.destroy()

#function to generate password of length 15
def generate():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = 15

	# shuffling the characters
    random.shuffle(characters)
	
	# picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

	# shuffling the resultant password
    random.shuffle(password)
    password_text.set("".join(password))

#function to save data into a JSON file
def Save():
    name=site_text.get()
    password=password_text.get()
    uname=uname_text.get()

#Error message
    if password=="" or name=="" or uname=="":
        messagebox.showerror("Error","Site or password field cannot be empty")
    
    else:
        
        password_dict={
            "Site": name,
            "Username" : uname,
            "Password": password
        }

 
        with open("pass.json","r+") as jfile:
            try:
                data=json.load(jfile)
                data["Details"].append(password_dict)
                jfile.seek(0)
                json.dump(data,jfile,indent=2)
            except JSONDecodeError:
                pass

        site_text.set("")
        password_text.set("")
        uname_text.set("")

        #save into json file


#Function for Opening a new window to create password
def Create_fun():
    # Toplevel object which will be treated as a new window
    newWindow = Toplevel(window)
    newWindow.title("Create your stuff")
    newWindow.geometry("600x400")
    newWindow.config(background="#F7672D")

    Label(newWindow,
    text ="Create a new password").grid(row=0,column=1,pady=10)

    Label(newWindow,text="Enter Site name : ").grid(row=1,pady=10)
    site_entry = Entry(newWindow,textvariable = site_text).grid(row=1,column=2)

    Label(newWindow,text="Enter Username : ").grid(row=2,pady=10)
    uname_entry=Entry(newWindow,textvariable=uname_text).grid(row=2,column=2)
 
    Label(newWindow,text="Enter password : ").grid(row=3,pady=10)
    pasword_entry=Entry(newWindow,textvariable=password_text,state=DISABLED).grid(row=3,column=2)

    Button(newWindow,text="Generate a password " , command=generate,fg="#00FF00",bg="black").grid(row=4,column=1,pady=10)
    Button(newWindow,text="Save",command=Save,fg="#00FF00",bg="black").grid(row=5,column=1,pady=10)

#Function for Opening a new window to save your pasts password
def Save_fun():
 
    newWindow = Toplevel(window)
    newWindow.title("Store your stuff")
    newWindow.geometry("600x400")
    newWindow.config(background="#F7672D")
    Label(newWindow,
    text ="Store your passwords").grid(row=0,column=1,pady=10)

    Label(newWindow,text="Enter Site name : ").grid(row=1,pady=10)
    site_entry = Entry(newWindow,textvariable = site_text,width=20).grid(row=1,column=2) 

    Label(newWindow,text="Enter Username : ").grid(row=2,pady=10)
    uname_entry=Entry(newWindow,textvariable=uname_text).grid(row=2,column=2)

    Label(newWindow,text="Enter password : ").grid(row=3,pady=10)
    pasword_entry=Entry(newWindow,textvariable=password_text,width=20).grid(row=3,column=2)

    Button(newWindow,text="Save",command=Save,fg="#00FF00",bg="black",pady=10).grid(row=4,column=1)
    
#Function for Opening a new window to show password of a particular website
def Show_fun():
    newWindow=Toplevel(window)
    newWindow.title("Show your stuff")
    newWindow.geometry("600x400")
    newWindow.config(background="#F7672D")
    Label(newWindow,text="Show passwords").grid(row=0,column=1,pady=10)

    Label(newWindow,text="Site name : ").grid(row=1,pady=10)
    #List box to choose a site
    lbox=Listbox(newWindow)
    lbox.grid(row=1,column=2) 
    
    #storing the site name in a list
    sites=[]
    with open("pass.json","r+") as jfile:
            try:
                data=json.load(jfile)
                for i in data['Details']:
                    sites.append(i["Site"])

            except JSONDecodeError:
                pass

#inserting the website's name into the ListBox
    for i in sites:
        lbox.insert(lbox.size(),i)

    lbox.config(height=lbox.size())

#Function to show username and password when a selecting a particular website
    def Show():
        Selected=lbox.get(lbox.curselection())
        with open("pass.json","r+") as jfile:
                try:
                    data=json.load(jfile)
                    for i in data['Details']:
                        if Selected==i["Site"]:
                            password_text.set(i["Password"])
                            uname_text.set(i["Username"])
                except JSONDecodeError:
                    pass
    
    #site_entry = Entry(newWindow,textvariable = site_text,width=20,state=DISABLED).grid(row=1,column=2) 

    Label(newWindow,text="Username : ").grid(row=2,pady=10)
    uname_entry=Entry(newWindow,textvariable=uname_text,state=DISABLED).grid(row=2,column=2)

    Label(newWindow,text="Password : ").grid(row=3,pady=10)
    pasword_entry=Entry(newWindow,textvariable=password_text,width=20,state=DISABLED).grid(row=3,column=2)

    Button(newWindow,text="Show",command=Show,fg="#00FF00",bg="black",pady=10).grid(row=4,column=1,pady=10)
    Button(newWindow,text="Copy Pasword",command=copy_button,fg="#00FF00",bg="black",pady=10).grid(row=5,column=1,pady=10)


#Stuff for Main Window  
Label(window,text="PASSWORD MANAGER",font=(20)).pack(pady=10)

create =Button(window,text="Create",command=Create_fun,fg="#00FF00",bg="black") #remove parenthis of function after placing it
create.pack(pady=10)

   
save=Button(window,text="Save",command=Save_fun,fg="#00FF00",bg="black")
save.pack(pady=10)

#.place(cordinates) for placing in specific coordinates
show=Button(window,text="Get Password",command=Show_fun,fg="#00FF00",bg="black")
show.pack(pady=10)


window.mainloop() # place window on screen and listen to events

