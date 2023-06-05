if [[ $VIRTUAL_ENV == "" ]]; then
    echo "You need to activate virtualenv first"
    exit 1
fi
echo "Removing old migrations"
rm -f ./optymalizator/optymalizator/__pycache__/*.pyc
rm -f ./optymalizator/optymalizator_app/__pycache__/*.pyc
rm -f ./optymalizator/optymalizator_app/migrations/__pycache__/*.pyc
rm -f ./optymalizator/optymalizator_app/migrations/0001_initial.py
echo "Commenting out urls"
sed -i '21s/^/#/' ./optymalizator/optymalizator/urls.py
sed -i '22s/^/#/' ./optymalizator/optymalizator/urls.py
echo "Dropping database"
sudo -iu postgres psql -c "DROP DATABASE lekidb;"
echo "Creating database"
sudo -iu postgres psql -c "CREATE DATABASE lekidb;"
echo "Granting privileges"
sudo -iu postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE lekidb TO root;"
# echo "Migrating"
python3 ./optymalizator/manage.py makemigrations
python3 ./optymalizator/manage.py migrate
echo "Uncommenting urls"
sed -i '21s/#//' ./optymalizator/optymalizator/urls.py
sed -i '22s/^#//' ./optymalizator/optymalizator/urls.py
# echo "Adding data"
cd database
python3 ./lekrefundowany_upload.py
python3 ./daneoleku_upload.py
python3 ./ctr_database_upload.py
cd ..
