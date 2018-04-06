import wx,re
FILE = '../DFDCharacters.txt'
with open(FILE,"r",encoding="utf8") as f:
    lines = f.readlines()

current_row_id = 0
page_breaks = []

column_breaks = []

re_current_row_id = re.compile(r'\+Page=([0-9]+)')
re_col_no = re.compile(r'\+Column=([0-9]+)')

def current_page_col(lines, row_num):
    page = 0
    col = 0
    for i in range(0, row_num+1):
        line = lines[i].rstrip()
        if line.startswith('+Page'):
            if (re_current_row_id.match(line)):
                page = int(re_current_row_id.match(line).group(1))
            else:
                page += 1
            col = 0
        elif line.startswith('+Column'):
            if (re_col_no.match(line)):
                col = int(re_col_no.match(line).group(1))
            else:
                col += 1
    return (page,col)

def create_preview(lines,limit):
    
    results = {}
    def add(page_id, col_id, row ,line):
        nonlocal results
        if ((page_id,col_id) not in results):
            results[(page_id,col_id)] = []
        if (not line.startswith('+Page') and not line.startswith('+Column')):
            results[(page_id,col_id)].append((row,line.rstrip()))

    page = 0
    col = 0
    for i in range(0, len(lines)):
        line = lines[i].rstrip()
        if line.startswith('+Page'):
            if (re_current_row_id.match(line)):
                page = int(re_current_row_id.match(line).group(1))
            else:
                page += 1
            col = 0
        elif line.startswith('+Column'):
            if (re_col_no.match(line)):
                col = int(re_col_no.match(line).group(1))
            else:
                col += 1
        add(page,col,i,line)
        if i > limit:
            break
    return results

def display_text(lines, start_line, length):
    i = start_line
    ls = []
    while (i<-1 and (len(ls)<length)):
        i = i+1
        ls.append((i, ''))
    while (i<len(lines)-1 and (len(ls)<length)):
        i = i+1
        #if (lines[i].rstrip().startswith('+Page') or lines[i].rstrip().startswith('+Column')):
        #    pass
        #else:
        ls.append((i,lines[i].rstrip()))

    return ls

def display_centre(lines, current_line, wrap=10):
    ls = display_text(lines, current_line-10, 2*wrap+1)
    
    result = ''
    for line in ls:
        if (line[0]==current_line):
            startlen = (len(result))
            result+='%04d>> %s\n'% (line[0],line[1]) 
            endlen = (len(result))
        else:
            result+='%04d:  %s\n'% (line[0],line[1]) 
    return (result,startlen,endlen)

def insert_page_break(lines, row):
    lines.insert(row+1,'+Page\n')

def insert_col_break(lines, row):
    lines.insert(row+1,'+Column\n')

def delete_row(lines,row):
    if (row in range(len(lines))):
        if (lines[row].startswith('+Page') or lines[row].startswith('+Column')):
            del lines[row]

class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)
        filler = wx.BoxSizer(wx.VERTICAL)
        
        pnl_top = wx.Panel(self)
        gs_top = wx.BoxSizer(wx.HORIZONTAL)
        pnl_top.SetSizer(gs_top)
        pnl_centre = wx.Panel(self)
        gs_centre = wx.BoxSizer(wx.HORIZONTAL)
        pnl_centre.SetSizer(gs_centre)
        pnl_bottom = wx.Panel(self)
        gs_bottom =  wx.BoxSizer(wx.HORIZONTAL)
        pnl_bottom.SetSizer(gs_bottom)
        self.SetSizer(filler)
        filler.Add(pnl_top,0,wx.ALIGN_TOP)
        filler.Add(pnl_centre,1,wx.EXPAND)
        filler.Add(pnl_bottom,0,wx.ALIGN_BOTTOM)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, faceName='Noto Sans Mono CJK TC Regular')
        self.status_text = wx.StaticText(pnl_top,size=(500,20),label="sdfsdf")
        self.status_text.SetFont(font)
        gs_top.Add(self.status_text,1,wx.ALIGN_RIGHT)
        # and put some text with a larger bold font on it
        self.text_upcoming = wx.TextCtrl(pnl_centre, value="",style=wx.TE_READONLY | wx.TE_MULTILINE |  wx.TE_RICH2)
        self.text_upcoming.SetFont(font)  
        self.text_1 = wx.TextCtrl(pnl_centre, value="",style=wx.TE_READONLY | wx.TE_MULTILINE|  wx.TE_RICH2)
        self.text_1.SetFont(font)  
        self.text_2 = wx.TextCtrl(pnl_centre, value="",style=wx.TE_READONLY | wx.TE_MULTILINE|  wx.TE_RICH2)
        self.text_2.SetFont(font)  
        self.text_3 = wx.TextCtrl(pnl_centre, value="",style=wx.TE_READONLY | wx.TE_MULTILINE|  wx.TE_RICH2)
        self.text_3.SetFont(font)
        self.text_upcoming.Enable(False)
        self.text_1.Enable(False)
        self.text_2.Enable(False)
        self.text_3.Enable(False)
        
        gs_centre.Add(self.text_upcoming,3, wx.EXPAND)
        gs_centre.Add(self.text_1,2, wx.EXPAND)
        gs_centre.Add(self.text_2,2, wx.EXPAND)
        gs_centre.Add(self.text_3,2, wx.EXPAND)

        btn_up = wx.Button(pnl_bottom, label='UP')
        btn_up.Bind(wx.EVT_BUTTON, self.OnUp)
        btn_up10 = wx.Button(pnl_bottom, label='UP 10')
        btn_up10.Bind(wx.EVT_BUTTON, self.OnUp10)
        btn_down = wx.Button(pnl_bottom, label='DOWN')
        btn_down.Bind(wx.EVT_BUTTON, self.OnDown)
        btn_down10 = wx.Button(pnl_bottom, label='DOWN 10')
        btn_down10.Bind(wx.EVT_BUTTON, self.OnDown10)

        btn_page_break = wx.Button(pnl_bottom, label='+Page')
        btn_page_break.Bind(wx.EVT_BUTTON, self.OnBreakPage)
        btn_col_break = wx.Button(pnl_bottom, label='+Column')
        btn_col_break.Bind(wx.EVT_BUTTON, self.OnBreakCol)
        btn_delete = wx.Button(pnl_bottom, label='Delete')
        btn_delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        btn_save = wx.Button(pnl_bottom, label='Save')
        btn_save.Bind(wx.EVT_BUTTON, self.OnSave)

        gs_bottom.Add(btn_up,0,wx.ALIGN_LEFT)
        gs_bottom.Add(btn_down,0,wx.ALIGN_LEFT)
        gs_bottom.Add((10,20),0,wx.ALIGN_LEFT)
        gs_bottom.Add(btn_up10,0,wx.ALIGN_LEFT)
        gs_bottom.Add(btn_down10,0,wx.ALIGN_LEFT)
        gs_bottom.Add((10,20),0,wx.ALIGN_LEFT)

        gs_bottom.Add(btn_page_break,0,wx.ALIGN_LEFT)
        gs_bottom.Add(btn_col_break,0,wx.ALIGN_LEFT)
        gs_bottom.Add((10,20),0,wx.ALIGN_LEFT)
        gs_bottom.Add(btn_delete,0,wx.ALIGN_LEFT)
        
        gs_bottom.Add((10,20),0,wx.ALIGN_LEFT)
        
        gs_bottom.Add(btn_save,0,wx.ALIGN_LEFT)
        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")
        self._refresh()
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
 
    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print(keycode)
        if keycode == wx.WXK_UP:
            self.OnUp(event)
        elif keycode == wx.WXK_DOWN:
            self.OnDown(event)
        elif keycode == wx.WXK_PAGEUP:
            self.OnUp10(event)
        elif keycode == wx.WXK_PAGEDOWN:
            self.OnDown10(event)
        elif chr(keycode) in ['P','p']:
            self.OnBreakPage(event)
        elif chr(keycode) in ['C','c']:
            self.OnBreakCol(event)
        elif chr(keycode) in ['D','d']:
            self.OnDelete(event)
        elif keycode == wx.WXK_CONTROL_S:
            self.OnSave(event)
        event.Skip()

    def OnDown(self,event):
        global current_row_id
        current_row_id +=1
        self._refresh()
        event.Skip()
    def OnUp(self,event):
        global current_row_id
        current_row_id -=1
        self._refresh()
        event.Skip()

    def OnDown10(self,event):
        global current_row_id
        current_row_id +=10
        self._refresh()
        event.Skip()

    def OnUp10(self,event):
        global current_row_id
        current_row_id -=10
        self._refresh()
        event.Skip()

    def OnBreakPage(self,event):
        global lines,current_row_id
        insert_page_break(lines,current_row_id)
        current_row_id+=1 + 23
        self._refresh()
        event.Skip()

    def OnBreakCol(self,event):
        global lines,current_row_id
        if (self.active_col == 2):
            insert_page_break(lines,current_row_id)
        else:
            insert_col_break(lines,current_row_id)
        current_row_id+=1 + 23
        self._refresh()
        event.Skip()


    def OnDelete(self,event):
        global lines,current_row_id
        delete_row(lines,current_row_id)
        current_row_id -=1
        self._refresh()
        event.Skip()

    def OnSave(self,event):
        global lines
        print('saving...')
        with open(FILE,'w',encoding='utf-8') as f:
            f.writelines(lines)
        event.Skip()

    def _refresh(self):
        global current_row_id
        if (current_row_id >= len(lines)):
            current_row_id = len(lines)-1
        if (current_row_id<0):
            current_row_id = 0
        page_id, col_id = current_page_col(lines,current_row_id)
        self.active_col = col_id
        self.status_text.SetLabel('Current Row= %d, Current Page = %d, Current Col = %d'% (current_row_id,page_id,col_id))
        (text, highlight_start, highlight_end) = display_centre(lines,current_row_id)
        print(highlight_start,highlight_end)
        self.text_upcoming.SetValue(text)
        self.text_upcoming.SetInsertionPoint(0)
        highlight_style = wx.TextAttr(wx.BLACK, wx.YELLOW)
        if (not self.text_upcoming.SetStyle(highlight_start,highlight_end, highlight_style)):
            print('set style error')

        preview = create_preview(lines,current_row_id+500)
        self._update_preview(self.text_1,preview,page_id,0)
        self._update_preview(self.text_2,preview,page_id,1)
        self._update_preview(self.text_3,preview,page_id,2)

    def _update_preview(self,control,preview_text, page_id, col_id):
        global current_row_id
        if (page_id,col_id) in preview_text: 
            value = ''
            startpos = -1
            endpos = -1
            if len(preview_text)> 50:
                preview_text = preview_text[:50]
                preview_text.append(10099595,'...')
            for row_id, line in preview_text[(page_id,col_id)]:
                if (row_id == current_row_id):
                    startpos = len(value)
                    value += (line+'\n')
                    endpos = len(value)
                else:
                    value+=(line+'\n')
            print( startpos,endpos)
            control.SetValue(value) 

            if startpos != -1:
                highlight_style = wx.TextAttr(wx.BLACK, wx.YELLOW)
                if (not control.SetStyle(startpos, endpos,highlight_style)):
                    print('set style error')
        else: 
            control.SetValue("")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()