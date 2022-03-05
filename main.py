
import src.update_localdb as update
import src.result as result

def main():

    update.store_newdata_local_db()
    result.produce_new_csv()

if __name__ == "__main__":
    main()
