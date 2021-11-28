from datetime import datetime
from pathlib import Path
import tkinter as tk
import shutil
import re
import os


class FileBrowser():
    def __init__(self, root_window, root_dir):
        self.root_window = root_window
        self.root_dir = root_dir
        self.icons = []
        self.file_view_frame = tk.Frame(self.root_window)
        self.favorites = None
        self.sort_mode = 'alpha'
        # colors and whatnot
        self.width = 600
        self.height = 350
        self.fv_width = 170
        self.background = '#605D53'
        self.orange = '#ED832C'
        self.blue = '#48A0C8'
        self.offwhite = '#F2F1F0'
        # navigation stuff
        self.visited_paths = [root_dir]
        self.v_idx = 0
        # for copying files
        self.clipboard = False

    def init_root_window(self):
        """Sets up the basic root window for the application, as well as
        creates instances of the PhotoImage class for every image in
        the assets directory.
        """
        self.root_window.title('Fuse Browser')
        rw_dimensions = f'{self.width}x{self.height}'
        self.root_window.geometry(rw_dimensions)
        self.root_window.configure(background=self.offwhite)
        # Call func to generate all icon photo instances
        self.icons = self.init_icons()

    def init_icons(self):
        """Iterates through all files in the assets dir and creates instances
        of PhotoImage for each.

        @return a dictionary mapping filenames to PhotoImage instances
        """

        all_icons = os.listdir('/app/code/assets/')
        icon_dict = {}

        for icon in all_icons:
            icon_path = '/app/code/assets/' + icon
            icon_dict[icon] = tk.PhotoImage(file=icon_path)
            icon_dict[icon] = icon_dict[icon].subsample(10, 10)

        return icon_dict

    def init_navbar(self):
        """Builds the navbar widget that holds the back/forward buttons."""
        # Back/Fwd Buttons
        navbar_frame = tk.Frame(self.root_window, height=40, bg='#3E3D39',
                                width=self.width)
        navbar_frame.pack(fill=tk.X, side=tk.TOP)

        btn_container = tk.Frame(navbar_frame, height=20, bg='#3E3D39',
                                 width=15)
        btn_container.place(x=15, rely=.5, anchor='w')

        # --- Create the back button
        back_btn = tk.Button(btn_container, bg=self.background, width=1,
                             height=1, text=' < ', fg=self.offwhite, highlightthickness=0, bd=0)
        back_btn.bind('<Button-1>', self.retreat)
        back_btn.pack(side=tk.LEFT)

        # --- Create the forward button
        fwd_btn = tk.Button(btn_container, bg=self.background, width=1,
                            height=1, text=' > ', fg=self.offwhite, highlightthickness=0, bd=0)
        fwd_btn.bind('<Button-1>', self.advance)
        fwd_btn.pack(side=tk.LEFT, padx=2)

        # --- Create the 'new folder' button
        dir_btn = tk.Button(btn_container, bg=self.background, bd=0,
                            relief=tk.FLAT, highlightthickness=0, height=25,
                            width=25, image=self.icons['new_folder_icon.png'])
        dir_btn.bind('<Button-1>', self.init_folder_dialog)
        dir_btn.pack(anchor='w', side=tk.LEFT, padx=15)

        # --- Create the new file (just creates empty txt file)
        new_file_btn = tk.Button(btn_container, bg=self.background, bd=0,
                                 relief=tk.FLAT, highlightthickness=0, height=25,
                                 width=25, image=self.icons['new_txt_file.png'])
        new_file_btn.bind('<Button-1>', lambda e: self.create_file())
        new_file_btn.pack(anchor='w', side=tk.LEFT, padx=0)

    def init_rename_dialog(self, path):
        """Opens a dialog window that prompts the user to provide a new
        file/dir name for the rename operation.

        @param path: the absolute path of the file/dir to be renamed 
        """

        pwd = self.visited_paths[self.v_idx]
        bare_filename = re.search('(/)([^/]+)$', path).group(2)

        # Popup to hold prompt
        popup = tk.Toplevel(self.root_window, bg=self.offwhite)
        popup.title('Rename ' + "'" + bare_filename + "'")
        popup.geometry('300x150')

        # Text box to collect new folder name
        entry = tk.Entry(popup, width=30, bg=self.offwhite,
                         bd=0, relief=tk.FLAT)
        entry.pack(pady=40)

        # Container to hold the create/cancel buttons
        btn_container = tk.Frame(popup, height=50, bg=self.offwhite,
                                 width=100)
        btn_container.place(relx=.5, rely=.5, anchor='n')

        cancel_btn = tk.Button(btn_container, text='Cancel',
                               bd=0, relief=tk.FLAT, bg=self.offwhite,
                               highlightthickness=0, command=(
                                   popup.destroy
                               ))
        cancel_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(btn_container, text='Rename',
                             bd=0, relief=tk.FLAT, bg=self.blue, fg=self.offwhite,
                             activebackground=self.offwhite,
                             highlightthickness=0, command=(
                                 lambda: self.rename_file(
                                     popup, path, pwd + '/' + entry.get()
                                 )
                             ))
        save_btn.pack(anchor='e', side=tk.RIGHT, padx=5)

    def init_folder_dialog(self, e):
        """Opens a dialog window that prompts the user for a dir name.

        @param e: the click event that initiated this dialog
        """
        # Popup to hold prompt
        popup = tk.Toplevel(self.root_window, bg=self.offwhite)
        popup.title('New folder')
        popup.geometry('300x150')

        # Text box to collect new folder name
        entry = tk.Entry(popup, width=30, bg=self.offwhite,
                         bd=0, relief=tk.FLAT)
        entry.pack(pady=40)

        # Container to hold the create/cancel buttons
        btn_container = tk.Frame(popup, height=50, bg=self.offwhite,
                                 width=100)
        btn_container.place(relx=.5, rely=.5, anchor='n')

        cancel_btn = tk.Button(btn_container, text="Cancel",
                               bd=0, relief=tk.FLAT, bg=self.offwhite,
                               highlightthickness=0, command=(
                                   popup.destroy
                               ))
        cancel_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(btn_container, text="Create folder",
                             bd=0, relief=tk.FLAT, bg=self.blue, fg=self.offwhite,
                             activebackground=self.offwhite,
                             highlightthickness=0, command=(
                                 lambda: self.create_folder(
                                     '/' + entry.get(), popup)
                             ))
        save_btn.pack(anchor='e', side=tk.RIGHT, padx=5)

    def init_info_dialog(self, path, reading=False, writing=False):
        """Multipurpose dialog window. Handles displaying the contents
        of a standard file, showing metadata for files and dirs, or
        editing the text of a standard file.

        @param path: the absolute path of the file or dir we want to
        inspect
        @param reading: boolean that determines if we want to view the
        text content of a file
        @param writing: boolean that determines if we want to edit the
        text content of a file
        """
        popup = tk.Toplevel(self.root_window, bg=self.offwhite)
        popup.title('File info')
        popup.geometry('300x150')

        if reading or writing:
            # Print the text content to window and bail
            popup.geometry('500x350')
            content = ''
            with open(path, 'r') as inf:
                for l in inf:
                    content += (l)
            if reading:
                file_content = tk.Label(popup, fg=self.background,
                                        bg=self.offwhite, text=(content),
                                        wraplength=450, justify=tk.LEFT,
                                        width=450, anchor='w'
                                        )
                file_content.pack(pady=5, padx=15)
            else:
                # Editable file text
                entry = tk.Text(popup, width=450, height=250,
                                bg=self.offwhite, bd=0, relief=tk.FLAT)
                entry.insert(tk.END, content)
                entry.pack()

                # Container to hold the create/cancel buttons
                btn_container = tk.Frame(popup, height=50, bg=self.offwhite,
                                         width=100)
                btn_container.place(relx=.5, y=300, anchor='n')

                cancel_btn = tk.Button(btn_container, text='Cancel',
                                       bd=0, relief=tk.FLAT, bg=self.offwhite,
                                       highlightthickness=0, command=(
                                           popup.destroy
                                       ))
                cancel_btn.pack(side=tk.LEFT, padx=5)

                save_btn = tk.Button(btn_container, text='Save',
                                     bd=0, relief=tk.FLAT, bg=self.blue,
                                     fg=self.offwhite,
                                     activebackground=self.offwhite,
                                     highlightthickness=0, command=(
                                         lambda: self.write_file(
                                             path, entry.get(
                                                 '1.0', tk.END), popup
                                         )
                                     ))
                save_btn.pack(anchor='e', side=tk.RIGHT, padx=5)
            return  # we don't need to see metadata when reading or writing

        info_label = tk.Label(popup, fg=self.background,
                              bg=self.offwhite, text=('Full name: ' + path),
                              wraplength=270, justify=tk.LEFT,
                              width=100, anchor='w'
                              )
        info_label.pack(pady=5, padx=15)

        ftype = 'File'
        if os.path.isdir(path):
            ftype = 'Directory'
            fcount = tk.Label(popup, fg=self.background,
                              bg=self.offwhite, text=(
                                  'Item count: ' + str(len(os.listdir(path)))
                              ),
                              wraplength=270, justify=tk.LEFT,
                              width=100, anchor='w'
                              )
            fcount.pack(pady=5, padx=15)

            isfav = tk.Label(popup, fg=self.background,
                             bg=self.offwhite, text=('Is favorite: ' + str(
                                 self.is_favorite(path))),
                             wraplength=270, justify=tk.LEFT,
                             width=100, anchor='w'
                             )
            isfav.pack(pady=5, padx=15)

        filetype = tk.Label(popup, fg=self.background,
                            bg=self.offwhite, text=('Filetype: ' + ftype),
                            wraplength=270, justify=tk.LEFT,
                            width=100, anchor='w'
                            )
        filetype.pack(pady=5, padx=15)

    def init_favorites(self):
        """Builds the favorites sidebar widget that holds links to various
        file locations.
        """

        fv_frame = tk.Frame(self.root_window, bg=self.background,
                            width=self.fv_width)
        fv_frame.pack(anchor='w', fill=tk.Y, side=tk.LEFT)
        fv_content = tk.Frame(fv_frame, bg=self.background,
                              width=(self.fv_width - 30), bd=0)
        fv_content.pack(anchor='n', fill=tk.Y, expand=True, side=tk.TOP,
                        padx=15, pady=15)
        fv_label = tk.Label(fv_content, fg=self.background, bg=self.offwhite,
                            text='Favorites', width=10, anchor='w')
        fv_label.pack(fill=tk.X)
        fv_listbox = tk.Listbox(fv_content, bg=self.background, selectmode=tk.SINGLE,
                                bd=0, fg=self.offwhite, relief=tk.FLAT, selectbackground=self.blue,
                                selectforeground=self.offwhite,
                                highlightthickness=0, activestyle='none')
        fv_listbox.bind('<<ListboxSelect>>', self.read_favorite)
        fv_listbox.insert(tk.END, self.root_dir)
        fv_listbox.pack(pady=5)

        self.favorites = fv_listbox

    def init_file_display(self):
        """Builds a Frame widget that will hold all the file icons.

        @return a TK Frame
        """

        # Create the frame
        # TODO: add scrolling
        fd_frame = tk.Frame(self.root_window, bg=self.offwhite, pady=10,
                            padx=15)
        fd_frame.pack(anchor='w', fill=tk.BOTH, expand=True)

        return fd_frame

    def set_sort_mode(self, mode):
        self.sort_mode = mode
        self.redraw_window()

    def write_file(self, path, content, popup):
        """Write arbitrary content to an arbitrary file.

        @param path: the absolute path of the file to write
        @param content: the content to put into the target file
        @param popup: the dialog window that called this func
        """
        with open(path, 'w') as inf:
            inf.write(content)

        popup.destroy()

    def rename_file(self, popup, old_path, new_path):
        """Handles renaming a file/dir and associated cleanup.

        @param popup: the dialog that called this function
        @param old_path: the absolute path of the file to be renamed
        @param new_path: the absolute path of the newly renamed file
        """
        popup.destroy()
        os.rename(old_path, new_path)

        # Update its name in the favorites bar
        if self.is_favorite(old_path):
            self.remove_favorite(old_path)
            self.add_favorite(new_path)

        # Update any references to its children in the favorites bar
        for entry in enumerate(self.favorites.get(0, tk.END)):
            if entry[1].startswith(old_path):
                new_entry = entry[1].replace(old_path, new_path, 1)
                self.remove_favorite(entry[1])
                self.add_favorite(new_entry)

        self.redraw_window()

    def sort_files(self, files):
        if self.sort_mode == 'az':
            return sorted(files)
        else:
            return reversed(sorted(files))

    def is_favorite(self, path):
        try:
            idx = self.favorites.get(0, tk.END).index(path)
            if idx >= 0:
                return True
            else:
                return False
        except:
            return False

    def add_favorite(self, path):
        if not self.is_favorite(path):
            self.favorites.insert(tk.END, path)

    def remove_favorite(self, path):
        """Remove a dir from the favorites bar.

        @param path: either string of full path of favorite to remove
        or tuple containing the favorites listbox index position of 
        said favorite AND a string of the full favorite path.

        ex: '/my/favorite/path' OR (0, 'my/favorite/path)
        """
        idx = False
        if isinstance(path, str):
            idx = self.favorites.get(0, tk.END).index(path)
        else:
            idx = path[0]

        self.favorites.delete(idx)

    def read_favorite(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        pwd = self.visited_paths[self.v_idx]
        if value != pwd:
            self.move(value)

    def update_selected_favorite(self, path):
        if self.is_favorite(path):
            idx = self.favorites.get(0, tk.END).index(path)
            self.favorites.selection_clear(0, tk.END)
            self.favorites.selection_set(idx)
            self.favorites.activate(idx)
        else:
            self.favorites.selection_clear(0, tk.END)

    def browser_context_open(self, event):
        menu = tk.Menu(self.root_window, tearoff=0, cursor='hand2')

        pwd = self.visited_paths[self.v_idx]

        menu.add_command(label='Information',
                         command=(lambda: self.init_info_dialog(pwd)))

        sort_menu = tk.Menu(menu, tearoff=0, cursor='hand2')
        sort_menu.add_command(label='A-Z',
                command=(lambda: self.set_sort_mode('az')))
        sort_menu.add_command(label='Z-A',
                command=(lambda: self.set_sort_mode('za')))
        menu.add_cascade(label='Sort by', menu=sort_menu)

        if not self.is_favorite(pwd):
            menu.add_command(label='Add to Favorites',
                             command=(lambda: self.add_favorite(pwd)))
        elif self.is_favorite(pwd) and pwd != self.root_dir:
            menu.add_command(label='Remove from Favorites',
                             command=(lambda: self.remove_favorite(pwd)))

        if self.clipboard:
            menu.add_command(label='Paste',
                             command=(lambda dest=(
                                 self.visited_paths[
                                     self.v_idx
                                 ]
                             ): self.copy(self.clipboard, dest)))

        menu.tk_popup(event.x_root, event.y_root)

    def file_context_open(self, event, path):
        menu = tk.Menu(self.root_window, tearoff=0, cursor='hand2')

        menu.add_command(label='Information',
                         command=(lambda: self.init_info_dialog(path)))

        menu.add_command(label='Rename',
                         command=(lambda: self.init_rename_dialog(path)))

        menu.add_command(label='Edit content',
                         command=(lambda: self.init_info_dialog(path, writing=True)))

        menu.add_command(label='Copy',
                         command=(lambda: self.save_to_clipboard(path)))

        menu.add_command(label='Delete',
                         command=(lambda: self.delete_file(path)))

        if os.path.isdir(path) and not self.is_favorite(path):
            menu.add_command(label='Add to Favorites',
                             command=(lambda: self.add_favorite(path)))
        if self.is_favorite(path):
            menu.add_command(label='Remove from Favorites',
                             command=(lambda: self.remove_favorite(path)))

        menu.tk_popup(event.x_root, event.y_root)

    def copy(self, src, dest):
        bare_filename = re.search('(/)([^/]+)$', src).group(2)
        pwd = self.visited_paths[self.v_idx]
        new_dest = pwd + '/' + bare_filename
        if os.path.isdir(src):
            shutil.copytree(src, new_dest, dirs_exist_ok=True)
        else:
            shutil.copy(src, dest)
        self.redraw_window()

    def delete_file(self, path):
        if self.clipboard and self.clipboard.startswith(path):
            self.clipboard = False

        if os.path.isdir(path):
            shutil.rmtree(path)
            # This prevents the back/fwd buttons from
            # remembering this path:
            for path_tuple in enumerate(self.visited_paths):
                if path_tuple[1] == path:
                    self.visited_paths.remove(path)
                    # If we're sitting at the edge of the array,
                    # back up to accomodate the new, shorter array
                    if self.v_idx > len(self.visited_paths) - 1:
                        self.v_idx -= 1

            # Remove it or any children from favorites
            del_list = []
            for entry in enumerate(self.favorites.get(0, tk.END)):
                if entry[1].startswith(path) or entry[1] == path:
                    del_list.append(entry[1])
            for l in del_list:
                self.remove_favorite(l)

            # Redraw the screen now that we've lost a file
            self.redraw_window()
        else:
            os.remove(path)
            # Redraw the screen now that we've lost a file
            self.redraw_window()

    def save_to_clipboard(self, txt):
        self.clipboard = txt

    def create_file(self):
        pwd = self.visited_paths[self.v_idx]
        timestamp = datetime.now().strftime('%H%M%S%f')
        Path(pwd + '/blank_' + timestamp + '.txt').touch()
        self.redraw_window()

    def create_folder(self, dirname, dialog):
        pwd = self.visited_paths[self.v_idx]
        # Create a new folder
        os.mkdir(pwd + dirname)
        # Redraw the screen with new folder added
        self.redraw_window()
        # Dismiss the dialog
        dialog.destroy()

    def retreat(self, event):
        """This function handles moving the user 'back' in the file tree
        when the Back button is clicked.

        @param event: the click event that triggered this call
        """

        if self.v_idx > 0:
            self.v_idx -= 1
            self.redraw_window()

    def advance(self, event):
        """This function handles moving the user 'forward' in the file tree
        when the Forward button is clicked.

        @param event: the click event that triggered this call
        """

        if self.v_idx < len(self.visited_paths) - 1:
            self.v_idx += 1
            self.redraw_window()

    def move(self, path):
        """Navigates into a directory. This is triggered by clicking on a 
        folder. Handles clearing out the paths that would have been 
        accessible by clicking the 'forward' button since they're invalid now.

        @param path: the absolute path to navigate to
        """

        # clicking on a file clears out what could
        # have been accessed by the 'forward' button:
        self.visited_paths = self.visited_paths[:self.v_idx + 1]
        self.visited_paths.append(path)
        self.v_idx += 1  # the last item in the array
        if self.v_idx < len(self.visited_paths):
            self.redraw_window()
        else:
            # ? Maybe fixes a bug where the index gets out of step
            self.v_idx -= 1

    def trunc_txt(self, text, length):
        if len(text) > length:
            return text[:length-5] + '...'
        else:
            return text

    def redraw_window(self, path=False):
        """Gets the current list of files to display and paints them to the
        screen.

        @param path: the absolute path of the directory we wish to draw
        """

        # default to pwd
        if not path:
            path = self.visited_paths[self.v_idx]

        try:
            fuse_files = self.sort_files(os.listdir(path))
        except(FileNotFoundError):
            return

        self.root_window.title(path)

        self.file_view_frame.destroy()
        self.file_view_frame = self.init_file_display()

        self.file_view_frame.bind('<Button-3>', (lambda event:
                                                 self.browser_context_open(event))
                                  )

        self.update_selected_favorite(path)

        # Add all files to screen
        cur_row = 0
        cur_col = 0
        for item in fuse_files:
            file_frame = tk.Frame(self.file_view_frame,
                                  bg=self.offwhite)
            file_frame.grid(row=cur_row, column=cur_col, padx=5)

            file_img = self.icons['txt_icon.png']
            item_path = path + '/' + item
            item_click = None

            if os.path.isdir(item_path):
                file_img = self.icons['folder_icon.png']
                # Since it's a dir, clicking should open
                # it and display contained files
                item_click = (lambda e, p=item_path:
                              self.move(p))
            else:
                item_click = (lambda e, p=item_path:
                              # read the file (only works for text)
                              self.init_info_dialog(p,
                                                    reading=True)
                              )

            file_item = tk.Button(file_frame, image=file_img,
                                  bg=self.offwhite, compound=tk.LEFT,
                                  bd=0, relief=tk.FLAT, highlightthickness=0
                                  )

            file_item.bind('<Double-Button-1>', item_click)
            file_item.bind('<Button-3>', (lambda e, p=item_path:
                                          self.file_context_open(e, p))
                           )
            file_item.pack()

            file_label = tk.Label(file_frame,
                                  text=self.trunc_txt(item, 10),
                                  fg=self.background, bg=self.offwhite)
            file_label.pack()

            # Update grid position to automatically
            # wrap files to the next line
            cur_col += 1
            # files are roughly 90px wide:
            max_col = ((self.width - self.fv_width) // 90)
            if cur_col % max_col == 0:
                cur_row += 1
                cur_col = 0
