from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import slate
import pdfminer

# ------------------------------------------------------------------------
# Create map from state -> city -> id
states = ['US', 'DC', 'PR', 'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
id_lookup = {}
for state in states:
    id_lookup[state] = {}

with open('gov_ids with domains.csv', 'r') as f:
    for line in f.readlines():
        cells = line.split(',')
        entity_id = cells[0]
        name = cells[1].lower()
        state = cells[3]
        id_lookup[state][name] = entity_id


# ------------------------------------------------------------------------
# Get all filenames
def get_all_filepaths(dirpath):
    filepaths = []
    paths = os.listdir(dirpath)
    for path in paths:
        fullpath = '/'.join([dirpath, path])
        if os.path.isdir(fullpath):
            filepaths = filepaths + get_all_filepaths(fullpath)
        else:
            filepaths.append(fullpath)

    return filepaths

base_dirs = ['/volumes/Untitled/city budgets batch I',
    '/volumes/Untitled/city budgets batch II',
    '/volumes/Untitled/city budgets batch III',
    '/volumes/Untitled/city budgets batch IV']

filepaths = []
for base_dir in base_dirs:
    filepaths = filepaths + get_all_filepaths(base_dir)


# ------------------------------------------------------------------------
# Upload to S3
access_key_id = "AKIAJW5SG3CRPIGYPETQ"
secret_access_key = "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"
conn = S3Connection(access_key_id, secret_access_key)
bucket = conn.get_bucket('og-data-uploads')

def process_item(entity_id, filepath, name):
    k = Key(bucket)
    # k.key = '/'.join(['development', 'pdfs', entity_id, name])
    k.key = '/'.join(['development', 'pdfs', 'test', name])
    k.set_contents_from_filename(filepath)

def display_name(filepath, year):
    is_budget = False
    is_cafr = False
    is_capital_improvements = False
    with open(filepath, 'r') as f:
        try:
            doc = slate.PDF(f, 'password')
            num_pages = len(doc)
            i = 0
            while i < num_pages and i < 5:
                contents = doc[i][:100]

                if 'capital' in contents.lower():
                    is_capital_improvements = True
                    break
                if 'budget' in contents.lower():
                    is_budget = True
                    break
                if 'comprehensive' in contents.lower():
                    is_cafr = True
                    break
        except:
            pass

    if is_budget:
        return year + ' Budget'
    elif is_cafr:
        return year + ' CAFR'
    elif is_capital_improvements:
        return year + ' Capital Improvements'
    else:
        return year + ' Unknown'


for filepath in filepaths[:100]:
    try:
        split_filename = filepath.split('/')[-1].split('_')
        name = split_filename[0]
        state = split_filename[1]
        year = split_filename[2].split('.')[0]
        entity_id = id_lookup[state][name]
        print entity_id
        process_item(entity_id, filepath, display_name(filepath, year))
    except:
        pass

