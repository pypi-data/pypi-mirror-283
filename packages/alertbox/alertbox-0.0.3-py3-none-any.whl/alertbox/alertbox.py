def run():
    import time
    import os 

    time.sleep(1)
    os.system('msgboxs.vbs')
    time.sleep(1)
    os.remove('msgboxs.vbs')


def create(title, description, type):
    import os
    import time
    


    files = open('msgboxs.vbs', 'x')
        
    file = open('msgboxs.vbs', 'w')
    file.write(f'x=msgbox("{str(description)}" ,{int(type)}, "{str(title)}")')
    file.close()


def types():
    msg = """0 =OK button only
    1 = OK and Cancel buttons
    2 = Abort, Retry, and Ignore buttons
    3 = Yes, No, and Cancel buttons
    4 = Yes and No buttons
    5 = Retry and Cancel buttons
    16 = Critical Message icon
    32 = Warning Query icon
    48 = Warning Message icon
    64 = Information Message icon
    0 = First button is default
    256 = Second button is default
    512 = Third button is default
    768 = Fourth button is default
    0 = Application modal (the current application will not work until the user responds to the message box)
    4096 = System modal (all applications wont work until the user responds to the message box)
    Change the "0" with any of these numbers above."""

    print(msg)


