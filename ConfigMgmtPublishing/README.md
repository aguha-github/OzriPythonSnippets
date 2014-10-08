Configuration Management & Publishing Automation
================================================

This example shows how we can use automate the publishing of ArcGIS for Server map services based on map document changes being committed to a version control system.

This example uses **Mercurial** to store the map documents, and uses three named branches called **development**, **testing**, and **production**.  Changes are made to the *development* branch, and then after basic testing the service is published in testing by merging the change into the *testing* branch in Mercurial.

Mercurial has been configured with a commit hook which sends a request to **Jenkins** to kick off a build process to publish the map service.

Jenkins has been configured with three jobs - each one publishes a different branch of the repository to a different folder in ArcGIS for Server.

ArcGIS for Server has been configured with three folders called **development**, **testing**, and **production**, which relate to the three Mercurial branches, and three Jenkins jobs.

The Python scripts publish services based on the map documents found in the branch in Mercurial.  The standard publishing functions in ArcGIS are used to perform this action - **CreateMapSDDraft**, **AnalyzeForSD**, **StageService_server**, **UploadServiceDefinition_server**.

The .sddraft file is altered to configure the antialias settings, using a custom class that manages the sddraft file.  Internally the sddraft file is an xml structure which uses **cElementTree to read and manipulate it.