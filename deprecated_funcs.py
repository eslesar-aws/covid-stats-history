# ! deprecated for now !
        # parses the CDC database for relevant titles
        def get_cdc(self):
            # get the text data
            page = requests.get(self.CDC_LINK).text
            # lxml great to use for organzing html
            tree = lxml.html.fromstring(page)
            link = tree.xpath(
                '/html/body/div[6]/main/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/ul[1]/li[1]/a')[0]
            # find the spreadsheet link
            rest = link.attrib['href']
            # download and open the spreadhsset
            r = requests.get(self.CDC_PAPERS + rest)
            with open("articles.xlsx", 'wb') as f:
                f.write(r.content)
            path = Path(Path.cwd() / 'articles.xlsx')
            # read into pandas
            df = pd.read_excel(path)
            # loop over every title
            self.words = ""
            for index, row in df.iterrows():
                curr_match = {}
                curr_title = row['Title']
                # withdrawn is a keyword CDC uses to say the article has been withdrawn
                if 'withdrawn' in curr_title.lower():
                    continue
                # string fixing in title
                if curr_title[0] == '[':
                    curr_title = curr_title[1:-1]
                # run the relevant function (function returns True or False)
                if find_relevant_titles(curr_title, self.KEYPHRASES, self.BAD_KEYWORDS):
                    curr_match["title"] = curr_title
                    try:
                        # if it is in english (python cant tell the difference between the two)
                        print(curr_title)
                        self.words += curr_title + ' '
                        # if it can print -> pull data
                        curr_match['Publisher'] = row['Journal/Publisher']
                    except:
                        continue





# date formatting to get the right  CDC URL ( not used right now)
today = date.today()
d2 = today.strftime("%B %d %Y").split()
if d2[1][0] == '0':
    day = d2[1][1:]
else:
    day = d2[1]
self.DATE = day + d2[0] + d2[2]
yesterday = date.today() - datetime.timedelta(days=1)
d2 = yesterday.strftime("%B %d %Y").split()
if d2[1][0] == '0':
    day = d2[1][1:]
self.DATE_YESTERDAY = day + d2[0] + d2[2]
self.CDC_LINK = 'https://www.cdc.gov/library/researchguides/2019novelcoronavirus/researcharticles.html'
self.params = manual_params
self.CDC_PAPERS = 'https://www.cdc.gov'





# code chunk for text_funcs.py that used word as a medium
if sys.platform.startswith('linux'):
        pass
    
    else:
        word = win32com.client.Dispatch("Word.Application")
        word.visible = 0  # supress errors in console (probably get a lot of errors from images we don't care about)
        pdfs_path = "pdfs/" # folder where the .pdf files are stored
        for i, doc in enumerate(glob.iglob(pdfs_path + "*.pdf")):
            filename = doc.split('\\')[-1]
            in_file = os.path.abspath(doc)
            wb = word.Documents.Open(in_file)
            out_file = os.path.abspath(Path(Path.cwd() / "pdfs" / "curr.docx"))
            wb.SaveAs2(out_file, FileFormat=16) # file format for docx
            wb.Close()
        word.Quit()
        doc = docx.Document(Path(Path.cwd() / "pdfs" / "curr.docx"))  # build path
        full_text = []  # store text
        for para in doc.paragraphs:
            full_text.append(para.text.encode(sys.stdout.encoding, errors='replace'))  # fix encodings and append
        return b'\n'.join(full_text).decode('windows-1252')  # one final decode -> will look different on linux