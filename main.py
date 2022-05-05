
import src.database.update_localdb as update
import src.dataset.produce_dataset as dataset
import src.dataset.produce_data_by_duration as duration
import src.build.html as html 

def main():

    update.store_newdata_local_db()
    dataset.produce_new_dataset('treehouses')
    duration.produce()
    html.build()

if __name__ == "__main__":
    main()
