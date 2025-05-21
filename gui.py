import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ast
from mainProgram import *


def draw_gantt_chart(canvas, processes, start_time):
    canvas.delete("all")
    if not processes or not start_time:
        print("No data to draw Gantt chart.")
        return
    x_scale = 30
    y = 50 #where they are located vertically
    height = 20 #Tool el-bar
    current_x = 0  # Tracks a5r of prev process

    for i, process in enumerate(processes):
        start = int(start_time[i])
        duration = process["burst time"] #duration is the burst time while start is passed stand alone cuz it is dictionary ejntry
        end = start + duration

        if start > current_x:
            canvas.create_rectangle(
                current_x * x_scale, y,
                start * x_scale, y+ height,
                fill = "lightgray"
            )
            canvas.create_text(
                ((current_x + start) / 2) * x_scale,
                (y + height)/2,
                text = "idle",
                font =("courier", 10,"italic")
            )
            canvas.create_text(
                current_x * x_scale,
                y + height+10,
                text = str(current_x)
            )
        # draws bar , y is unchanged startpoint to end point
        canvas.create_rectangle(
            start * x_scale, y,
            end * x_scale, y + height,
            fill="pink")

        #process name placed in mid of each x scale
        canvas.create_text(
        ((start + end)/2) * x_scale,
        (y+ height)/2,
        text=process["process name"],
        font=("Courier", 10, "bold") )

        #start time 3la start kol bar
        canvas.create_text(
        start * x_scale,
        y + height + 10,  # under bar
        text=str(start)
            )

        #draw end time on last or if next doesn't match ya3ni only draw end time law lazm
        if i == len(processes) - 1 or start_time[i + 1] != end or start > current_x:
            canvas.create_text(
            end * x_scale,
            y + height + 10,
            text=str(end))
        current_x = end


window=Tk()
window.title("Calculate Priority Scheduling (Non-Preemptive)")
window.geometry('925x500+300+200')
window.configure(bg='#fff')
window.resizable(False,False)

page1 = Frame(window, bg='white', width=925, height=500)
page2 = Frame(window, bg='white', width=925, height=500)
page3 = Frame(window, bg='white', width=925, height=500)
page4 = Frame(window, bg='white', width=925, height=500)

for page in (page1, page2, page3,page4):
    page.place(x=0, y=0)

def show_frame(frame):
    frame.tkraise()

total_processes=0;

home_icon=PhotoImage(file="home.png").subsample(2,2)
next_icon=PhotoImage(file="next.png")

#image page 1
photo=PhotoImage(file='osproject (2).png')
label=Label(page1,image=photo,border=0,bg='white').place(x=0,y=70)
frame=Frame(page1,width=400,height=390,bg='#fff')
frame.place(x=480,y=50)
heading=Label(frame,
              text='Priority Scheduling (Non-Preemptive)',
              fg="#FF69B4",
              bg='white',
              font=('Courier',23,'bold'),
              wraplength=400,
              justify='left')
heading.place(x=0,y=50)
#number of process field
def on_enter(e):
    if user.get()=="" or user.get()=="Number Of Processes":
            user.delete(0,'end')
    user.config(fg="#FF69B4")


user=Entry(frame,width=20,fg="#696969",border=0,bg='white',font=('Courier',12,'bold'))
user.place(x=70,y=200)
user.insert(0,'Number Of Processes')
Frame(frame,width=280,height=2,bg='black').place(x=70,y=225)
user.bind("<FocusIn>",on_enter)


message_label = Label(frame, text="", fg="red", bg="white", font=("Courier", 10, "bold"))
message_label.place(x=70, y=230)

#next page1 button
def on_next_from_page1():
    global total_processes
    value=user.get().strip()
    if(value.isdigit() and int(value)>0):
        total_processes=int(value)
        FirstButton.config(state=NORMAL)
        show_frame(page2)
    else:
         FirstButton.config(state=DISABLED)
         message_label.config(text="!Please enter a valid number.", fg="red")




FirstButton=Button(frame,text=" Next ",pady=7,border=0,width=100,
                             highlightthickness=0,fg="white",bg="#FF69B4",
                                    font=("Courier", 14, "bold"),
                             command=on_next_from_page1,image=next_icon,compound=RIGHT)
FirstButton.place(x=280,y=330)
FirstButton.config(activebackground="#D1006F")
FirstButton.config(activeforeground="white")
FirstButton.image=next_icon
#check the input page1
def on_user_typing(event):
    value = user.get().strip()
    if   value=="":
         message_label.config(text="")

    elif  value.isdigit() and int(value)>0:
           message_label.config(text=f"\u2713 {value} is allowable number. ", fg="green")
           FirstButton.config(state=NORMAL)
    else:
        message_label.config(text="!Please enter a valid number.", fg="red")

user.bind("<KeyRelease>",on_user_typing )


#page 2
#image
photo2=PhotoImage(file='page2.png')
label2=Label(page2,image=photo2,border=0,bg='white').place(x=0,y=0)
frame2=Frame(page2,width=600,height=450,bg='#fff')
frame2.place(x=380,y=20)
heading2=Label(frame2,
              text='Enter Arrival & Burst Time for Each Process',
              fg="#FF69B4",
              bg='white',
              font=('Courier',23,'bold'),
              wraplength=550,
              justify='left')
heading2.place(x=0,y=15)

current_process=1
arrival_time=[]
burst_time=[]
priority_time=[]


#process دي ثابته مش بتسمح للuser to enter value
processnumbermassage =Label(frame2,
              text='Process number',
              fg="#000000",
              bg='white',
              font=('Courier',15,'bold'),
              wraplength=400,
              justify='left')
processnumbermassage.place(x=10,y=120)
processnumbermassage=Entry(frame2,width=25,fg="#FF69B4",border=1,bg='white',font=('Courier',12,'bold'))
processnumbermassage.place(x=60,y=150)
processnumbermassage.insert(0,f'P{current_process}')
processnumbermassage.config(state=DISABLED)
processnumbermassage.config(disabledforeground="#FF69B4")
processnumbermassage.config(disabledbackground='white')


#if field is Empty and go to next field
def on_leave_Arrival_Time(event):
    valueArrival = ArrivalTimeMassage.get().strip()
    if valueArrival == "":
        message_label_Arrival.config(text="!Please enter a valid number.", fg="red")
    elif not valueArrival.isdigit():
        message_label_Arrival.config(text="!Please enter a valid number.", fg="red")
    else:
        message_label_Arrival.config(text="")

def on_leave_Burst_Time(event) :

    valueBurst = BurstTimeMassage.get().strip()
    if valueBurst == "":
        message_label_Burst.config(text="!Please enter a valid number.", fg="red")
    elif not valueBurst.isdigit():
        message_label_Burst.config(text="!Please enter a valid number.", fg="red")
    else:
        message_label_Burst.config(text="")


#enter arrival time
ArrivalTimeMassage =Label(frame2,
              text='ArrivalTime',
              fg="#000000",
              bg='white',
              font=('Courier',15,'bold'),
              wraplength=400,
              justify='left')
ArrivalTimeMassage.place(x=10,y=180)

ArrivalTimeMassage=Entry(frame2,width=25,fg="#FF69B4",border=1,bg='white',font=('Courier',12,'bold'))
ArrivalTimeMassage.place(x=60,y=210)


ArrivalTimeMassage.bind("<FocusOut>",on_leave_Arrival_Time)



# enter burst time
BurstTimeMassage =Label(frame2,
              text='BurstTime',
              fg="#000000",
              bg='white',
              font=('Courier',15,'bold'),
              wraplength=400,
              justify='left')
BurstTimeMassage.place(x=10,y=250)

BurstTimeMassage=Entry(frame2,width=25,fg="#FF69B4",border=1,bg='white',font=('Courier',12,'bold'))
BurstTimeMassage.place(x=60,y=280)
BurstTimeMassage.bind("<FocusOut>",on_leave_Burst_Time)

# enter priority
Priority =Label(frame2,
              text='Priority',
              fg="#000000",
              bg='white',
              font=('Courier',15,'bold'),
              wraplength=400,
              justify='left')
Priority.place(x=10,y=320)

Priority=Entry(frame2,width=25,fg="#FF69B4",border=1,bg='white',font=('Courier',12,'bold'))
Priority.place(x=60,y=350)


#شكل ومكان عرض ال ايرور
message_label_Arrival = Label(frame2, text="", fg="red", bg="white", font=("Courier", 10, "bold"))
message_label_Arrival.place(x=60,y=235)
message_label_Burst = Label(frame2, text="", fg="red", bg="white", font=("Courier", 10, "bold"))
message_label_Burst.place(x=60,y=305)
message_label_Priority = Label(frame2, text="", fg="red", bg="white", font=("Courier", 10, "bold"))
message_label_Priority.place(x=60,y=375)

# first make check for any field alone next for all fields
def check_fields(event=None):
    at = ArrivalTimeMassage.get().strip()
    bt = BurstTimeMassage.get().strip()
    p=Priority.get().strip()

    if at == "":
        message_label_Arrival.config(text="")
    elif not at.isdigit():
        message_label_Arrival.config(text="!Please enter a valid number.", fg="red")
    else:
        message_label_Arrival.config(text="")


    if bt == "":
        message_label_Burst.config(text="")
    elif not bt.isdigit():
        message_label_Burst.config(text="!Please enter a valid number.", fg="red")
    else:
        message_label_Burst.config(text="")

    if p == "":
        message_label_Priority.config(text="")
    elif not p.isdigit():
        message_label_Priority.config(text="!Please enter a valid number.", fg="red")
    else:
        message_label_Priority.config(text="")


    # if at.isdigit() and bt.isdigit() and p.isdigit():
    #     secondButton.config(state=NORMAL)
    # else:
    #     secondButton.config(state=DISABLED)

ArrivalTimeMassage.bind("<KeyRelease>", check_fields)
BurstTimeMassage.bind("<KeyRelease>", check_fields)
Priority.bind("<KeyRelease>", check_fields)

#Next page 2 make check for all fields ,next make loop change when enter on button
def next_process():
    global current_process
    at=ArrivalTimeMassage.get().strip()
    bt=BurstTimeMassage.get().strip()
    p=Priority.get().strip()
    valid = True


    if at == "":
        message_label_Arrival.config(text="!Please enter arrival time.", fg="red")
        valid = False
    elif not at.isdigit():
        message_label_Arrival.config(text="!Invalid number.", fg="red")
        valid = False
    else:
        message_label_Arrival.config(text="")


    if bt == "":
        message_label_Burst.config(text="!Please enter burst time.", fg="red")
        valid = False
    elif not bt.isdigit():
        message_label_Burst.config(text="!Invalid number.", fg="red")
        valid = False
    else:
        message_label_Burst.config(text="")


    if p == "":
        message_label_Priority.config(text="!Please enter priority.", fg="red")
        valid = False
    elif not p.isdigit():
        message_label_Priority.config(text="!Invalid number.", fg="red")
        valid = False
    else:
        message_label_Priority.config(text="")

    # لو في خطأ، وقف هنا
    if not valid:
       return
    arrival_time.append(int(at))
    burst_time.append(int(bt))
    priority_time.append(int(p))
    inputTable.insert(parent='', index='end', values=(f'P{current_process}', at, bt,p))
    if current_process <total_processes:
        current_process+=1
        processnumbermassage.config(state=NORMAL)
        processnumbermassage.delete(0,END)
        processnumbermassage.insert(0,f'P{current_process}')
        processnumbermassage.config(state=DISABLED)
        ArrivalTimeMassage.delete(0,END)
        BurstTimeMassage.delete(0,END)
        Priority.delete(0,END)
        ArrivalTimeMassage.focus_set()


    else:
        show_frame(page3)


#button page 2

secondButton=Button(frame2,text=" Next ",pady=7,border=0,width=100,
                             highlightthickness=0,fg="white",bg="#FF69B4",
                                 font=("Courier", 14, "bold"),image=next_icon,compound=RIGHT)

secondButton.place(x=400,y=395)
secondButton.config(activebackground="#D1006F")
secondButton.config(activeforeground="white")
secondButton.config(command=next_process)
secondButton.image=next_icon
#
# #button Home هيرجعني للصفحه الرئسيه
def reset_to_home():
     global current_process,arrival_time,burst_time,total_processes
     show_frame(page1)
     user.delete(0,END)
     # user.insert(0,'Number Of Processes')
     # user.config(fg="#696969")
     user.focus_set()
     message_label.config(text="",fg="red")
     message_label_Burst.config(text="",fg="red")
     message_label_Arrival.config(text="",fg="red")
     message_label_Priority.config(text="",fg="red")
     FirstButton.config(state=DISABLED)
     current_process=1
     arrival_time.clear()
     burst_time.clear()
     priority_time.clear()
     total_processes=0
     ArrivalTimeMassage.delete(0, END)
     BurstTimeMassage.delete(0, END)
     Priority.delete(0,END)
     processnumbermassage.config(state=NORMAL)
     processnumbermassage.delete(0, END)
     processnumbermassage.insert(0, f'P1')
     processnumbermassage.config(state=DISABLED)
     for row in inputTable.get_children():
         inputTable.delete(row)


# # button home

returnButton=Button(frame2,text=" Home ",pady=7,border=0,width=100,
                              highlightthickness=0,fg="white",bg="#FF69B4",
                                     font=("Courier", 14, "bold"),image=home_icon,compound=LEFT )
returnButton.place(x=270,y=395)
returnButton.config(activebackground="#D1006F")
returnButton.config(activeforeground="white")
returnButton.config(command=reset_to_home)
returnButton.image = home_icon


heading3 = Label(page3,
                text="Process Input Table",
                fg="#FF69B4",
                bg="white",
                font=("Courier", 26, "bold"),
                wraplength=600,
                justify="left")
heading3.place(x=250, y=30)

frame3=Frame(page3,width=450,height=200,bg='#f8f8f8')
frame3.place(x=120,y=100)
scrollbar = Scrollbar(frame3, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

inputTable=ttk.Treeview(frame3,columns=('process_number','arrival','burst','priority'),
                        show='headings',height= 8  , yscrollcommand=scrollbar.set)
inputTable.heading('process_number',text='Process Number')
inputTable.heading('arrival',text='Arrival Time')
inputTable.heading('burst',text='Burst Time')
inputTable.heading('priority',text='Priority')
inputTable.column('process_number',width=185,anchor=CENTER)
inputTable.column('arrival',width=165,anchor=CENTER)
inputTable.column('burst',width=165,anchor=CENTER)
inputTable.column('priority',width=165,anchor=CENTER)
inputTable.pack(side=LEFT,fill=BOTH,expand=True)
scrollbar.config(command=inputTable.yview)
style=ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="white",
                foreground="#FF69B4",
                rowheight=30,
                font=('Courier', 11,'bold'),
                fieldbackground="white",
                borderwidth=3
                )
style.map("Treeview",
          background=[('selected', '#FFB6C1')],
          foreground=[('selected', 'black')])


style.configure("Treeview.Heading",
                background="white",
                foreground="#a30d5c",
                font=("Courier", 12, "bold")
                )
def next_from_page3():
    show_frame(page4)
    for row in outputTable.get_children():
        outputTable.delete(row)

    processes = [] #stores the inputs for use below
    for i in range(total_processes):
        processes.append({
            "process name": f'P{i + 1}',
            "burst time": burst_time[i],
            "priority": priority_time[i],
            "arrival time": arrival_time[i]
        })
    results = run_PScheduler(processes,total_processes)

    start_times = results['startTime']
    gantt_canvas = Canvas(page4, width=710, height=100, bg="white", highlightthickness=1)
    gantt_canvas.place(x=60, y=410)
    scrollbar_gantt_x = Scrollbar(page4, orient="horizontal", command=gantt_canvas.xview)
    scrollbar_gantt_x.place(x=20, y=390, width=500)
    gantt_canvas.configure(xscrollcommand=scrollbar_gantt_x.set)
#the chart
    draw_gantt_chart(gantt_canvas, processes, start_times)
    gantt_canvas.configure(scrollregion=gantt_canvas.bbox("all"))

#each value is approx to the 2nd float digit in txt
    Average_Turnaround_Time.config(
        text=f"Average Turnaround Time = {results['avg turnaround']:.2f}")
    Average_Waiting_Time.config(
        text=f"Average Waiting Time = {results['avg waiting']:.2f}")
    Average_Response_Time.config(
        text=f"Average Response Time = {results['avg response']:.2f}")

#the results are lined from input and output in order
    for p in range (total_processes):
       outputTable.insert('', 'end', values=(
            processes[p]['process name'],
            processes[p]['arrival time'],
            processes[p]['burst time'],
            processes[p]['priority'],
            results['compTime'][p],
            results['tat'][p],
            results['wt'][p],
            results['startTime'][p],
            results['respT'][p]
       ))

#button page 2

ThiredButton=Button(page3,text=" Next ",pady=7,border=0,width=100,
                             highlightthickness=0,fg="white",bg="#FF69B4",
                             font=("Courier", 14, "bold"),command=next_from_page3,
                                 image=next_icon, compound=RIGHT)
ThiredButton.place(x=800,y=420)
ThiredButton.config(activebackground="#D1006F")
ThiredButton.config(activeforeground="white")
ThiredButton.image=next_icon

# #button Home هيرجعني للصفحه الرئسيه
def reset_to_home():
     global current_process,arrival_time,burst_time,total_processes
     show_frame(page1)
     user.delete(0,END)
     user.insert(0,'Number Of Processes')
     user.config(fg="#696969")
     message_label.config(text="",fg="red")
     message_label_Burst.config(text="",fg="red")
     message_label_Arrival.config(text="",fg="red")
     message_label_Priority.config(text="",fg="red")
     FirstButton.config(state=DISABLED)
     current_process=1
     arrival_time.clear()
     burst_time.clear()
     priority_time.clear()
     total_processes=0
     ArrivalTimeMassage.delete(0, END)
     BurstTimeMassage.delete(0, END)
     Priority.delete(0,END)
     processnumbermassage.config(state=NORMAL)
     processnumbermassage.delete(0, END)
     processnumbermassage.insert(0, f'P1')
     processnumbermassage.config(state=DISABLED)
     for row in inputTable.get_children():
         inputTable.delete(row)


# # button home

returnButton=Button(page3,text=" Home ",pady=7,border=0,width=100,
                              highlightthickness=0,fg="white",bg="#FF69B4",
                              font=("Courier", 14, "bold"),image=home_icon,
                              compound=LEFT)
returnButton.place(x=680,y=420)
returnButton.config(activebackground="#D1006F")
returnButton.config(activeforeground="white")
returnButton.config(command=reset_to_home)
returnButton.image = home_icon


heading4 = Label(page4,
                text="Scheduling Output Table",
                fg="#FF69B4",
                bg="white",
                font=("Courier", 26, "bold"),
                wraplength=600,
                justify="left")
heading4.place(x=250, y=30)
frame4=Frame(page4,width=500,height=400,bg='white')
frame4.place(x=20,y=100)


outputTable=ttk.Treeview(frame4,columns=('process_number','arrival','burst',
                                         'priority','Completion Time','Turnaround Time',
                                         'Waiting Time','Start Time','Response Time'),
                                         show='headings',height= 8)

outputTable.heading('process_number',text='Process Number')
outputTable.heading('arrival',text='Arrival Time')
outputTable.heading('burst',text='Burst Time')
outputTable.heading('priority',text='Priority')
outputTable.heading('Completion Time',text='Completion Time')
outputTable.heading('Turnaround Time',text='Turnaround Time')
outputTable.heading('Waiting Time',text='Waiting Time')
outputTable.heading('Start Time',text='Start Time')
outputTable.heading('Response Time',text='Response Time')


outputTable.column('process_number',width=165,anchor=CENTER)
outputTable.column('arrival',width=145,anchor=CENTER)
outputTable.column('burst',width=140,anchor=CENTER)
outputTable.column('priority',width=140,anchor=CENTER)
outputTable.column('Completion Time',width=160,anchor=CENTER)
outputTable.column('Turnaround Time',width=175,anchor=CENTER)
outputTable.column('Waiting Time',width=160,anchor=CENTER)
outputTable.column('Start Time',width=160,anchor=CENTER)
outputTable.column('Response Time',width=160,anchor=CENTER)
outputTable.place(x=0, y=0,width=500,height=280)
style_output=ttk.Style()
style_output.theme_use("clam")
style_output.configure("Treeview",
                background="white",
                foreground="#FF69B4",
                rowheight=30,
                font=('Courier', 11,'bold'),
                fieldbackground="white",
                borderwidth=3
                )
style_output.map("Treeview",
          background=[('selected', '#FFB6C1')],
          foreground=[('selected', 'black')])


style_output.configure("Treeview.Heading",
                background="white",
                foreground="#a30d5c",
                font=("Courier", 14, "bold"),

                )

# Scrollbars for output table
scrollbar_output_y = Scrollbar(page4, orient="vertical", command=outputTable.yview)
scrollbar_output_y.place(x=520, y=100, height=280)
scrollbar_output_x = Scrollbar(page4, orient="horizontal", command=outputTable.xview)
scrollbar_output_x.place(x=20, y=370, width=500)
outputTable.configure(yscrollcommand=scrollbar_output_y.set,
                      xscrollcommand=scrollbar_output_x.set)

frame5=Frame(page4,width=400,height=450,bg='white')
frame5.place(x=550,y=150)

#متوسطات labels
Average_Turnaround_Time=Label(frame5,text="",fg='#a30d5c',bg='white'
                              ,font=("Courier", 14, "bold"))
Average_Turnaround_Time.place(x=0,y=0)
Average_Waiting_Time=Label(frame5,text="",fg='#a30d5c',bg='white'
                              ,font=("Courier", 14, "bold"))
Average_Waiting_Time.place(x=0,y=50)
Average_Response_Time=Label(frame5,text="",fg='#a30d5c',bg='white'
                              ,font=("Courier", 14, "bold"))
Average_Response_Time.place(x=0,y=100)

#resetting functions
def reset_to_home():
     global current_process,arrival_time,burst_time,total_processes
     show_frame(page1)
     user.delete(0,END)
     user.insert(0,'Number Of Processes')
     user.config(fg="#696969")
     message_label.config(text="",fg="red")
     message_label_Burst.config(text="",fg="red")
     message_label_Arrival.config(text="",fg="red")
     message_label_Priority.config(text="",fg="red")
     FirstButton.config(state=DISABLED)
     current_process=1
     arrival_time.clear()
     burst_time.clear()
     priority_time.clear()
     total_processes=0
     ArrivalTimeMassage.delete(0, END)
     BurstTimeMassage.delete(0, END)
     Priority.delete(0,END)
     processnumbermassage.config(state=NORMAL)
     processnumbermassage.delete(0, END)
     processnumbermassage.insert(0, f'P1')
     processnumbermassage.config(state=DISABLED)
     for row in inputTable.get_children():
         inputTable.delete(row)


#button home

returnButton=Button(frame5,text=" Exit ",pady=7,border=0,width=100,
                              highlightthickness=0,fg="white",bg="#FF69B4",
                                     font=("Courier", 14, "bold"),image=next_icon,compound=RIGHT   )
returnButton.place(x=220,y=260)
returnButton.config(activebackground="#D1006F")
returnButton.config(activeforeground="white")
returnButton.config(command=reset_to_home)
returnButton.image=next_icon


show_frame(page1)
window.mainloop()




