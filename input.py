import os
import sys
import termios
import atexit
from select import select


class KBHit:

    def __init__(self):
        # Save the terminal settings
        self._fd = sys.stdin.fileno()
        self._new_term = termios.tcgetattr(self._fd)
        self._old_term = termios.tcgetattr(self._fd)

        # New terminal setting unbuffered
        self._new_term[3] = (self._new_term[3] & ~
                            termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self._fd, termios.TCSAFLUSH, self._new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        termios.tcsetattr(self._fd, termios.TCSAFLUSH, self._old_term)

    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''
        return sys.stdin.read(1)

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []

    def flush(self):
        '''
        Clears input buffer
        '''

        termios.tcflush(sys.stdin, termios.TCIOFLUSH)