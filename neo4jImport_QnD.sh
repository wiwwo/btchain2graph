sudo rm -rf /var/lib/neo4j/data/databases/blckchain.db
sudo neo4j-import --into /var/lib/neo4j/data/databases/blckchain.db \
      --nodes /media/sf_E_DRIVE/btchain2graph/output/blocks_nodes.csv.gz \
      --nodes /media/sf_E_DRIVE/btchain2graph/output/addresses_nodes.csv.gz \
      --relationships /media/sf_E_DRIVE/btchain2graph/output/blockchain_rels.csv.gz \
      --relationships /media/sf_E_DRIVE/btchain2graph/output/transactions_rels.csv.gz
sudo chown -R neo4j.neo4j /var/lib/neo4j/data/databases/blckchain.db/
sudo service neo4j restart

