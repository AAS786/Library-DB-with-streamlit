import streamlit as st
import mysql.connector
import pandas as pd
import datetime

# ================= Database Connection ======================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",   # change if needed
        password="root",   # change if needed
        database="library"
    )

# ================= CRUD Functions ======================
def add_member(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO library VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)
    conn.commit()
    conn.close()

def fetch_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM library")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_member(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE library SET 
        Member=%s,ID=%s,FirstName=%s,LastName=%s,Address1=%s,
        Address2=%s,PostId=%s,Mobile=%s,BookID=%s,BookTitle=%s,
        Author=%s,DateBorrowed=%s,DateDue=%s,DaysonBook=%s,
        LateReturnFine=%s,DateOverDue=%s,finalPrice=%s
        WHERE PRN_No=%s
    """, data)
    conn.commit()
    conn.close()

def delete_member(prn_no):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library WHERE PRN_No=%s", (prn_no,))
    conn.commit()
    conn.close()

# ================= Streamlit App ======================
st.title("📚 Library Management System (Streamlit + MySQL)")

menu = ["Add Member", "View Members", "Update Member", "Delete Member"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Member":
    st.subheader("➕ Add New Member")

    member = st.selectbox("Member Type", ["Admin Staff", "Student", "Lecturer"])
    prn = st.text_input("PRN No")
    id_no = st.text_input("ID No")
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    address1 = st.text_input("Address 1")
    address2 = st.text_input("Address 2")
    postal = st.text_input("Postal Code")
    mobile = st.text_input("Mobile")
    bookid = st.text_input("Book ID")
    booktitle = st.text_input("Book Title")
    author = st.text_input("Author")
    date_borrowed = st.date_input("Date Borrowed", datetime.date.today())
    date_due = st.date_input("Date Due", datetime.date.today() + datetime.timedelta(days=15))
    days_on_book = st.number_input("Days on Book", min_value=1, max_value=60, value=15)
    fine = st.text_input("Late Return Fine", "Rs.25")
    overdue = st.text_input("Date Overdue", "NO")
    price = st.text_input("Final Price")

    if st.button("Save Member"):
        data = (member, prn, id_no, firstname, lastname, address1, address2,
                postal, mobile, bookid, booktitle, author,
                str(date_borrowed), str(date_due), days_on_book,
                fine, overdue, price)
        add_member(data)
        st.success("✅ Member added successfully!")

elif choice == "View Members":
    st.subheader("📖 View All Members")
    rows = fetch_data()
    df = pd.DataFrame(rows, columns=["MemberType","PRN","ID","FirstName","LastName",
                                     "Address1","Address2","PostID","Mobile",
                                     "BookID","BookTitle","Author",
                                     "DateBorrowed","DateDue","DaysOnBook",
                                     "LateReturnFine","DateOverdue","FinalPrice"])
    st.dataframe(df)

elif choice == "Update Member":
    st.subheader("✏️ Update Member")
    prn_to_update = st.text_input("Enter PRN No to Update")
    if st.button("Load Data"):
        rows = fetch_data()
        df = pd.DataFrame(rows, columns=["MemberType","PRN","ID","FirstName","LastName",
                                         "Address1","Address2","PostID","Mobile",
                                         "BookID","BookTitle","Author",
                                         "DateBorrowed","DateDue","DaysOnBook",
                                         "LateReturnFine","DateOverdue","FinalPrice"])
        member_data = df[df["PRN"] == prn_to_update]
        st.write(member_data)

    # You can extend with editable inputs + update_member()

elif choice == "Delete Member":
    st.subheader("🗑️ Delete Member")
    prn_to_delete = st.text_input("Enter PRN No to Delete")
    if st.button("Delete"):
        delete_member(prn_to_delete)
        st.success("❌ Member deleted successfully!")
