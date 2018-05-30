from Tkinter import *
from Voice_Command import Voice_Command
from IR_Transceiver import IR_Transceiver

DEVICE_ID = 'ENTER DEVICE TOKEN HERE'
ACCESS_TOKEN = 'ENTER ACCESS TOKEN HERE'

def main(device_id, access_token):
    # Object definitions
    ir_transceiver = IR_Transceiver(device_id, access_token)
    voice_command = Voice_Command(ir_transceiver)
    
    # GUI - Window
    root = Tk()
    
    # GUI - Variables
    _ir_code = StringVar()
    _command = StringVar()

    # GUI - Event Methods
    def getIR():
        ir_code = ir_transceiver.getIR()
        _ir_code.set(ir_code)

    def addCommand(command, ir_code):
        if voice_command.addCommand(command, ir_code):
            lst_Commands.insert(END, command.strip())

    def delCommand(selection):
        try:
            # Get selected command
            index = int(selection[0])
            i = 0
            for key in voice_command.commandList:
                if index == i:
                    command = key
                    break
                i += 1
            # Delete command
            if voice_command.removeCommand(command):
                # Clear list
                lst_Commands.delete(0, END)
                # Populate list
                for key in voice_command.commandList:
                    lst_Commands.insert(END, key)
        except:
            return

    # GUI - Widgets
    lbl_KnownCommands = Label(root, text="Known Commands:")
    lbl_KnownCommands.grid(row=0, column=0, columnspan=3, sticky='W')

    lst_Commands = Listbox(root, width=45)
    lst_Commands.grid(row=1, column=0, columnspan=3, sticky='WE')

    lbl_NewCommand = Label(root, text="New Command:")
    lbl_NewCommand.grid(row=2, column=0, columnspan=2, sticky='W')

    lbl_IR_Code = Label(root, text="IR Code:")
    lbl_IR_Code.grid(row=2, column=2, sticky='W')

    txt_Command = Entry(root, textvariable=_command)
    txt_Command.grid(row=3, column=0, columnspan=2, sticky='WE')

    lbl_IRCode = Label(root, textvariable=_ir_code)
    lbl_IRCode.grid(row=3, column=3, sticky='WE')

    btn_GetIR = Button(root, text='Get IR Code', command=getIR, width=12)
    btn_GetIR.grid(row=4, column=0)  

    btn_AddCommand = Button(root, text="Add Command", command=lambda:addCommand(_command.get(), _ir_code.get()), width=12)
    btn_AddCommand.grid(row=4, column=1)

    btn_DelCommand = Button(root, text="Del Selected", command=lambda:delCommand(lst_Commands.curselection()), width=12)
    btn_DelCommand.grid(row=4, column=2)

    for key in voice_command.commandList:
        lst_Commands.insert(END, key)

    mainloop()

if __name__ == "__main__":
    main(DEVICE_ID, ACCESS_TOKEN)
