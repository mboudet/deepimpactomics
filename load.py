import askoclics

import configparser

from braskolib.datafile import Datafile


def main():

    config = configparser.ConfigParser()
    config.read("deepimpactomics.conf")

    asko_client = askoclics.AskomicsInstance(url=config['askomics']['url'], api_key=config['askomics']['api_key'], proxy_username=config['askomics'].get('proxy_username'), proxy_password=config['askomics'].get('proxy_password'))

    search_folder = config['main']['search_folder']

    datafiles = [
        Datafile(
            pattern="Asko*.txt",
            integration_file="templates/askomics/differential_expression.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="*.gff*",
            integration_file="templates/askomics/differential_expression.json",
            search_folder=search_folder,
            askomics_client=asko_client,
            type="gff"
        ),
        Datafile(
            pattern="condition*.txt",
            integration_file="templates/askomics/condition.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="context*.txt",
            integration_file="templates/askomics/context.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="contrast*.txt",
            integration_file="templates/askomics/contrast.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="Dilution*.txt",
            integration_file="templates/askomics/dilution.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="otu_dil*.txt",
            integration_file="templates/askomics/otu_count.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="otu_mean*.txt",
            integration_file="templates/askomics/otu_count_mean.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="OTUs.txt",
            integration_file="templates/askomics/otus.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="soil*.txt",
            integration_file="templates/askomics/soil.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="Taxons.txt",
            integration_file="templates/askomics/taxon.json",
            search_folder=search_folder,
            askomics_client=asko_client
        ),
        Datafile(
            pattern="tables1.csv",
            integration_file="templates/askomics/physicochemical.json",
            search_folder=search_folder,
            askomics_client=asko_client
        )
    ]

    # Cleanup
    for datafile in datafiles:
        datafile.get_files()
        datafile.cleanup_askomics()
        datafile.upload_files()
        datafile.integrate_files()


if __name__ == "__main__":
    main()
