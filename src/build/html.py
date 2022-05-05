from src.build.secrets import secrets
from src.build.conf import file_list

def build():
    for name in file_list:

        with open(f'src/build/{name}.html', 'r') as r:
            raw_data = r.read()

        for key, val in secrets.items():
            raw_data = raw_data.replace('{' + key + '}', val)


        html = f"""
        {raw_data}
        """

        with open(f'web/{name}.html', 'w') as w:
            w.write(html)