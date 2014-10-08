import arcpy, sys, os, ntpath
import map_config_mgmt_cfg as cfg
from sddraft import SDDraft


def main():
    # get the environment name and repository path from the command line args
    environment_name = sys.argv[1]
    repository_path = sys.argv[2]

    publish_map_documents(environment_name, repository_path) # publish the maps in the repository to ags
    
# publishes the map documents in the repository (in the "MXD" directory)
def publish_map_documents(environment_name, repository_path):
    map_documents_path = os.path.join(repository_path, "MXD")
    map_documents = filter(lambda f: f.lower().endswith('.mxd'), os.listdir(map_documents_path)) # filter to get the MXDs
    map_documents = map(lambda m: os.path.join(map_documents_path, m), map_documents) # map the full path onto the file names

    # publish the map documents
    for map_document in map_documents:
        publish_service(environment_name, map_document)

# publishes a single map document as a service
def publish_service(ags_folder, map_document):

    map_document_file_name = ntpath.basename(map_document)

    # build up a name for the service, the sddraft file name, and the sd file name
    sd_draft_path = map_document.replace('.mxd', '.sddraft')
    sd = map_document.replace('.mxd', '.sd')
    service_name = os.path.splitext(map_document_file_name)[0]

    # create the SDDraft file
    arcpy.mapping.CreateMapSDDraft(map_document, sd_draft_path, service_name, 'ARCGIS_SERVER', cfg.AGS_CONN, True, None, '', '')

    # alter some of the settings in the SDDraft
    sddraft = SDDraft.load(sd_draft_path)
    sddraft.set_property('antialiasingMode', 'Fast')
    sddraft.set_property('textAntialiasingMode', 'Force')
    sddraft.set_manifest_type('esriServiceDefinitionType_Replacement')
    sddraft.save()
    del sddraft

    # analyse the service
    analysis = arcpy.mapping.AnalyzeForSD(sd_draft_path)

    # check for analysis errors, if there are none publish the service
    if analysis['errors'] == {}:
        arcpy.StageService_server(sd_draft_path, sd)
        arcpy.UploadServiceDefinition_server(sd, cfg.AGS_CONN, service_name, "default", "EXISTING", ags_folder, "STARTED")
        print "Service successfully published"
        sys.exit(0)
        
    else: 
        for key in ('messages', 'warnings', 'errors'):
            print '----' + key.upper() + '---'
            vars = analysis[key]
            for ((message, code), layerlist) in vars.iteritems():
                print '    ', message, ' (CODE %i)' % code
                print '       applies to:',
                for layer in layerlist:
                    print layer.name,
                print

        print
        print "Service could not be published because errors were found during analysis"
        sys.exit(1)


if __name__ == '__main__':
    main()