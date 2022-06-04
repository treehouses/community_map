import sys

import src.database.update_localdb as update
import src.dataset.produce_dataset as dataset
import src.dataset.produce_data_by_duration as duration
import src.build.html as html 

def main():

    if len(sys.argv) == 1:
        update.store_newdata_local_db()
        dataset.produce_new_dataset('data')
        duration.produce()
    else:
        command = sys.argv[1]
        if command == 'build':
            html.build()
        elif command == 'all':
            update.store_newdata_local_db()
            dataset.produce_new_dataset('data')
            duration.produce('all')


if __name__ == "__main__":
    main()
