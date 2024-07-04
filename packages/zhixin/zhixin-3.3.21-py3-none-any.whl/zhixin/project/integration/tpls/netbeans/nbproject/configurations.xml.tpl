<?xml version="1.0" encoding="UTF-8"?>
<configurationDescriptor version="97">
  <logicalFolder name="root" displayName="root" projectFiles="true" kind="ROOT">
    <df root="." name="0">
      <in>zhixin.ini</in>
    </df>
    <logicalFolder name="ExternalFiles"
                   displayName="Important Files"
                   projectFiles="false"
                   kind="IMPORTANT_FILES_FOLDER">
      <itemPath>nbproject/private/launcher.properties</itemPath>
    </logicalFolder>
  </logicalFolder>
  <sourceFolderFilter>^(nbproject|.zx)$</sourceFolderFilter>
  <sourceRootList>
    <Elem>.</Elem>
  </sourceRootList>
  <projectmakefile></projectmakefile>
  <confs>
    <conf name="Default" type="0">
      <toolsSet>
        <compilerSet>default</compilerSet>
        <dependencyChecking>false</dependencyChecking>
        <rebuildPropChanged>false</rebuildPropChanged>
      </toolsSet>
      <codeAssistance>
        <buildAnalyzer>true</buildAnalyzer>
        <includeAdditional>true</includeAdditional>
      </codeAssistance>
      <makefileType>
        <makeTool>
          <buildCommandWorkingDir>.</buildCommandWorkingDir>
          <buildCommand>"{{zhixin_path}}" -f -c netbeans run</buildCommand>
          <cleanCommand>"{{zhixin_path}}" -f -c netbeans run --target clean</cleanCommand>
          <executablePath></executablePath>
          <cTool>
            % cleaned_includes = filter_includes(includes)
            <incDir>
              <pElem>src</pElem>
              % for include in cleaned_includes:
              <pElem>{{include}}</pElem>
              % end
            </incDir>
            <preprocessorList>
              % for define in defines:
                <Elem>{{define}}</Elem>
              % end
            </preprocessorList>
          </cTool>
          <ccTool>
            <incDir>
              <pElem>src</pElem>
              % for include in cleaned_includes:
              <pElem>{{include}}</pElem>
              % end
            </incDir>
            <preprocessorList>
              % for define in defines:
                <Elem>{{define}}</Elem>
              % end
            </preprocessorList>
          </ccTool>
        </makeTool>
        <preBuild>
          <preBuildCommandWorkingDir>.</preBuildCommandWorkingDir>
          <preBuildCommand></preBuildCommand>
        </preBuild>
      </makefileType>
      <item path="zhixin.ini" ex="false" tool="3" flavor2="0">
      </item>
    </conf>
  </confs>
</configurationDescriptor>
