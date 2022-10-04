import curses
import traceback
import time
from main import *
import threading
import _thread




def writeDateTime(win):
    win.move(3, 3)
    # win.clrtoeol()
    win.addstr("Current Date: %s")
    win.move(4, 3)
    # win.clrtoeol()
    win.addstr("Current Time: %s")
    win.refresh()


def openSubWindow(win):
    # create a sub-window and keep it open until
    # user presses the X key
    subwin = win.subwin(10, 60, 10, 10)
    subwin.nodelay(1)  # disable getch() blocking
    subwin.erase()
    subwin.box()
    subwin.addstr(1, 2, "1")
    ## border is ascii char in decimal ##
    # subwin.border(35, 35, 35, 35)
    subwin.bkgdset(' ')
    subwin.refresh()
    subwin.addstr(1, 20, "Check HTTP header date")
    subwin.addstr(8, 20, "Enter X to exit sub-window")
    subwin.addstr(2, 12, "this might take awhile")
    subwin.refresh()
    twrv = threadmanager(target=getnumber) # for testing only
    #twrv = threadmanager(target=get_rss_headerdate)
    twrv.start()
    subwin.addstr(3, 3, "waiting for check: ")
    subwin.refresh()
    while 1:
        inch = subwin.getch()
        if inch != -1:
            try:
                instr = chr(inch)
            except:
                # just ignore non-character input
                pass
            else:
                if instr.upper() == 'X':
                    break
        time.sleep(1)
        threadstatus = twrv.status()
        #threadstatus = False
        #print("inloop")
        if threadstatus is True:
            subwin.addstr(3, 22, "waiting " + str(threadstatus))
            subwin.refresh()
            #print("istrue")
        if threadstatus is False:
            #header_date = str(twrv.join())
            header_date = "ehh"
            subwin.addstr(4, 4, "XML feed last modified date: " + header_date)
            subwin.addstr(3, 22, "waiting " + str(threadstatus))
            subwin.refresh()
            #print("isfalse")


    return subwin

def openSubCWindow(win):
    # create a sub-window and keep it open until
    # user presses the X key
    subwin = win.subwin(10, 60, 10, 10)
    subwin.nodelay(1)  # disable getch() blocking
    subwin.erase()
    subwin.box()
    subwin.addstr(1, 2, "1")
    ## border is ascii char in decimal ##
    # subwin.border(35, 35, 35, 35)
    subwin.bkgdset(' ')
    subwin.refresh()
    subwin.addstr(1, 20, "Sub-C_Window Title")
    subwin.addstr(8, 20, "Enter X to exit sub-window")
    subwin.refresh()
    while 1:
        inch = subwin.getch()
        if inch != -1:
            try:
                instr = chr(inch)
            except:
                # just ignore non-character input
                pass
            else:
                if instr.upper() == 'X':
                    break
        time.sleep(0.2)
    return subwin


def mainScreen(win):
    win.erase()
    y, x = win.getmaxyx()
    win.border(124, 124, 45, 95)

    win.move(1, 40)
    win.addstr("Input Data Monitor")
    win.move(2, 38)
    win.addstr("Screen size Y: {0} X: {1}".format(y, x))
    ### Example of calling function to print text ###
    writeDateTime(win)

    win.move(15, 4)
    win.addstr("Enter X to exit")
    win.move(16, 4)
    win.addstr("1 to check header date || ")
    win.addstr("2 to configure paths || ")
    win.addstr("3 to download torrent files || ")
    win.refresh()


def mainloop(win):
    win.nodelay(1)  # disable getch() blocking
    # draw the main display template
    mainScreen(win)

    # run until the user wants to quit
    while 1:
        # check for keyboard input
        inch = win.getch()
        # getch() will return -1 if no character is available
        if inch != -1:
            # see if inch is really a character
            try:
                instr = str(chr(inch))
            except:
                # just ignore non-character input
                pass
            else:
                if instr.upper() == 'X':
                    break
                if instr.upper() == 'C':
                    subwin = openSubCWindow(win)
                    # simple way to restore underlying main screan
                    # call this to refresh when window size changes (should be in a loop?)
                    break
                if instr.upper() == '1':
                    subwin = openSubWindow(win)
                    # simple way to restore underlying main screan
                    # call this to refresh when window size changes (should be in a loop?)
                    mainScreen(win)
                if instr.upper() == 'Z':
                    subwin = opentestwindow(win)
                    mainScreen(win)
        writeDateTime(win)
        ## time-delay should not be part of the main control loop ##
        ## this causes a delay in UI response ##
        time.sleep(0.5)


def startup():
    # borrowed the idea of using a try-except wrapper around the
    # initialization from David Mertz.
    try:
        # Initialize curses
        stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        mainloop(stdscr)  # Enter the main loop

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()

        curses.endwin()  # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()  # Print the exception


if __name__ == '__main__':
    startup()
