import sqlite3

conn = sqlite3.connect('pharma.db')

c = conn.cursor()

print("welcome to the pharmacy")
answer = input("are you registered or not? Yes/No:")

if answer == "Yes":
    your_id = int(input("please enter your id:"))
    c.execute("SELECT * FROM customers WHERE id =(?)", (your_id,))
    obj = c.fetchall()
    print(obj)
    conn.commit

    while not obj:
        try_again = int(input("your id is wrong...try again:"))

    question = input("would u like to buy smth? Yes/No:")

    if question == "Yes":
        med = input("what would u like to buy:")
        if med == 'aspirin':
            exe = c.execute(
                "SELECT price FROM medicines WHERE meds LIKE 'aspirin%'")
            object = exe.fetchall()
            print(object)
            print("your bill will be " + str(object) +
                  "...please head over to the counter and get your " + med)
        elif med == 'brufen':
            exe = c.execute(
                "SELECT price FROM medicines WHERE meds LIKE 'brufen%'")
            object = exe.fetchall()
            print(object)
            print("your bill will be " + str(object) +
                  "...please head over to the counter and get your " + med)
        elif med == 'panadol':
            exe = c.execute(
                "SELECT price FROM medicines WHERE meds LIKE 'panadol%'")
            object = exe.fetchall()
            print(object)

            print("your bill will be " + str(object) +
                  "...please head over to the counter and get your " + med)

        quantity = int(input("How much " + med + " would u like to buy:"))
        
    elif question == "No":
        print("Thank you for coming")


elif answer == "No":
    register = input("would u like to register? Yes/No:")
    if register == "Yes":
        id = int(input("Please enter your id:"))
        name = input("enter your name:")
        c.execute("INSERT INTO customers VALUES(?,?)", (name, id))
        print("congratulations! you are registered")
    else:
        print("Thank you for coming")


conn.commit()
conn.close()
