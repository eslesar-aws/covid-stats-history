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
