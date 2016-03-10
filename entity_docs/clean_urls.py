outfile = open('clean_urls.csv', 'w')

with open('gov_ids.csv', 'r') as f:
    for line in f.readlines():
        cells = line.split(',')
        url = cells[-1]
        if url != "#N/A\r\n":
            print url
            url = url.lower()
            if len(url.split('//')) == 1:
                url = 'http://' + url

            clean_line = ','.join(cells[:-1] + [url])
            outfile.write(','.join([cells[0], url]))
