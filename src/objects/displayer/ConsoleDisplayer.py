from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug, Style
import os

def clear_console():
    """Clears the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

@singleton
class DisplayManager:
    def __init__(self, console_width=50, total_lines=8):
        self.console_width = console_width
        self.total_lines = total_lines

    def show(self, content, mode="text"):
        """Clears the console and displays content in the specified mode."""
        clear_console()
        if mode == "text":
            self._display_content(f"[Display]> {content}")
        elif mode == "image":
            self._display_image(content)
        elif mode == "table":
            self._display_table(content)
        else:
            Debug.LogError("Invalid display type")

    def _display_image(self, content):
        lines = ["Image :", content]
        
        self._display_content(lines)

    def _display_content(self, content):
        """Displays content (string or list of strings) centered within the total lines, with separators."""
        
        if isinstance(content, str):
            content = [content]  # Convert single string to a list

        # Calculate available lines for content
        lines_available = self.total_lines - 2
        
        # Calculate starting line for content
        start_line = max(0, (lines_available - len(content)) // 2) 

        Debug.LogSeparator("-")
        
        # Print empty lines before content
        for _ in range(start_line):
            self._display_centered_text("")

        # Print the content lines
        for line in content:
            self._display_centered_text(line)

        # Print empty lines after content
        for _ in range(start_line + len(content) +1, self.total_lines - 1):
            self._display_centered_text("")
        
        Debug.LogSeparator("-")

    def _display_table(self, content):
        """Displays a table within the total lines, with separators."""
        
        title = ""
        
        table_content = content
        
        if " ~ " in content:
            title = content.split(" ~ ")[0]
            table_content = content.split(" ~ ")[1]
            
            
        rows = table_content.split("|")
        table = [[row.strip() for row in rows[i:i+2] if row.strip()] 
                for i in range(0, len(rows), 2)]
        col_widths = [max(len(str(row[j])) if j < len(row) else 0 
                        for row in table) 
                    for j in range(2)]  # Calculate column widths
            
        
        lines = []
        if title != "":
            lines.append(title)
            
        # Format table rows
        for row in table:
            line = f"| {row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}} |" if len(row) == 2 else f"| {row[0]:<{col_widths[0]}} |"
            lines.append(line)
            
        self._display_content(lines)

    def _display_centered_text(self, text):
        """Displays text centered in the console with optional color."""
        padding = (self.console_width - len(text)) // 2
        Debug.LogColor(" " * padding + text, Style.PURPLE)
      

    def exit(self):
        pass

    def get_ip_address(self):
        pass