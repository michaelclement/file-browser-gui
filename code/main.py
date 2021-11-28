import tkinter as tk
from FileBrowser import FileBrowser


def main():
    # /app/mymnt is where the actual FUSE is mounted
    # within the docker environment
    file_browser = FileBrowser(tk.Tk(), '/app/mymnt')
    file_browser.init_root_window()

    # Organize the overall window and add things like
    # the back button & favorites bar
    file_browser.init_navbar()
    file_browser.init_favorites()

    # Initially load the root of the FUSE system and
    # display all files
    file_browser.redraw_window(file_browser.root_dir)

    file_browser.root_window.mainloop()


if __name__ == '__main__':
    main()
