import tkinter as tk
import random
import pymysql.cursors

username = "user1"
score = 100

# Establish a connection to your MySQL database
try: connection = pymysql.connect(host='172.20.128.77',
                            user='karsten',
                            password='123Akademiet',
                            database='users',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

except: print("no connection with MySQL database")

def insert_score(username, score):
    with connection.cursor() as cursor:
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            # Update the score for the existing user
            cursor.execute("UPDATE users SET score = %s WHERE username = %s", (score, username))
        else:
            # Insert a new record for the user
            cursor.execute("INSERT INTO users (username, score) VALUES (%s, %s)", (username, score))
    
    connection.commit()



root = tk.Tk()
root.title("Pyramid with Text Label")
root.configure(bg="white")

canvas = tk.Canvas(root, width=1600, height=1440, bg="white")
canvas.pack()

# Draw the pyramid squares
square_size = 70
border_width = 160
spacing = 20
xFix = 9


num_rows = 7
for row in range(num_rows):
    num_squares = row + 1
    start_x = border_width + (num_rows - row) * (square_size / 2 + spacing) + xFix
    start_y = border_width + row * (square_size + spacing)
    
    for i in range(num_squares):
        x0 = start_x + i * (square_size + spacing)
        y0 = start_y
        x1 = x0 + square_size
        y1 = y0 + square_size
        fill_color = "black" if row == 0 and i == 0 else "white"
        
        canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill=fill_color)

        if row == num_rows - 1:
            label_x = (x0 + x1) / 2
            label_y = y1 + 10
            canvas.create_text(label_x, label_y, text="Label", fill="black")  



def drop_ball():
    global score
    score += 1
    row = 1 # Start from the top row
    col = random.randint(0, row)  # Randomly select a column
    fill_square(row, col)
    try: insert_score(username, score)
    except: print("cant insert score")
    print(score)

def fill_square(row, col):
    if row >= num_rows:
        return  # Stop when reaching the bottom row

    x0 = border_width + row * (square_size / 2 + spacing) + (border_width + spacing) + xFix 
    y0 = border_width + row * (square_size + spacing)
    x1 = x0 + square_size
    y1 = y0 + square_size
    if col >= 0 and col < row + 1:

        if random.choice([True, False]):
            fill_square(row + 1, col - 1)  # Fill the square to the left
        else:
            fill_square(row + 1, col + 1) 
            
        canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="black") # Fill the square to the right
    




button = tk.Button(root, text="Drop Ball", command=drop_ball)
button.place(relx=0.5, rely=0.95, anchor="s")


root.mainloop()
