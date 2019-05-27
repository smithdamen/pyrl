import tcod as libtcod
import textwrap

# store message and color of the text
class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

# holds a list of messages
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # split if needed across multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # remove line if buffer is full
            if len(self.messages) == self.height:
                del self.messages[0]

            # add new line as message object with line and color
            self.messages.append(Message(line, message.color))
