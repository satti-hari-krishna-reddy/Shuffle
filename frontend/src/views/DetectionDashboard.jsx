import React, { useState, useEffect } from "react";
import { Container, CircularProgress, Typography } from "@mui/material";
import { toast } from "react-toastify";
import Detection from "./Detection";

const getSigmaInfo = (globalUrl, setRuleInfo, setFolderDisabled, setIsTenzirActive, setLoading) => {
  const url = globalUrl + "/api/v1/files/detection/sigma_rules";

  fetch(url, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) =>
      response.json().then((responseJson) => {
        if (responseJson["success"] === false) {
          toast("Failed to get sigma rules");
        } else {
          setRuleInfo(responseJson.sigma_info);
          setFolderDisabled(responseJson.folder_disabled);
          setIsTenzirActive(responseJson.is_tenzir_active);
          setLoading(false);
        }
      })
    )
    .catch((error) => {
      console.log("Error in getting sigma files: ", error);
      toast("An error occurred while fetching sigma rules");
      setLoading(false); 
    });
};

const importStandardsFromUrl = (globalUrl) => {
  const url = "https://github.com/satti-hari-krishna-reddy/shuffle_sigma";
  const folder = "sigma";
  const branch = "main";

  const parsedData = {
    url: url,
    path: folder,
    field_3: branch,
  };

  toast(`Getting files from url ${url}. This may take a while if the repository is large. Please wait...`);
  fetch(globalUrl + "/api/v1/files/download_remote", {
    method: "POST",
    mode: "cors",
    headers: {
      Accept: "application/json",
    },
    body: JSON.stringify(parsedData),
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 200) {
        toast("Successfully loaded files from " + url);
      }

      return response.json();
    })
    .then((responseJson) => {
      if (!responseJson.success) {
        if (responseJson.reason !== undefined) {
          toast("Failed loading: " + responseJson.reason);
        } else {
          toast("Failed loading");
        }
      }
    })
    .catch((error) => {
      toast(error.toString());
    });
};

const DetectionDashBoard = (props) => {
  const { globalUrl } = props;
  const [ruleInfo, setRuleInfo] = useState(null);
  const [, setSelectedRule] = useState(null);
  const [, setFileData] = useState("");
  const [isTenzirActive, setIsTenzirActive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [folderDisabled, setFolderDisabled] = useState(false);

  useEffect(() => {
    getSigmaInfo(globalUrl, setRuleInfo, setFolderDisabled, setIsTenzirActive, setLoading);
  }, [globalUrl]); 

  useEffect(() => {
    if (ruleInfo && ruleInfo.length > 0) {
      openEditBar(ruleInfo[0]);
    } else {
      importStandardsFromUrl(globalUrl);
    }
  }, [ruleInfo]); 

  const openEditBar = (rule) => {
    setSelectedRule(rule);
    getFileContent(rule.file_id);
  };

  const handleSave = (updatedContent) => {
    toast("this will be saved");
  };

  const getFileContent = (file_id) => {
    setFileData("");
    fetch(globalUrl + "/api/v1/files/" + file_id + "/content", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      credentials: "include",
    })
      .then((response) => {
        if (response.status !== 200) {
          console.log("Status not 200 for file :O!");
          return "";
        }
        return response.text();
      })
      .then((respdata) => {
        if (respdata.length === 0) {
          toast("Failed getting file. Is it deleted?");
          return;
        }
        return respdata;
      })
      .then((responseData) => {
        setFileData(responseData);
      })
      .catch((error) => {
        toast(error.toString());
      });
  };

  return (
    <Container style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh" }}>
      {loading ? (
        <>
          <CircularProgress />
          <Typography variant="h6" style={{ marginTop: "1rem" }}>
            Fetching rules, please wait...
          </Typography>
        </>
      ) : ruleInfo !== null ? ( 
        <Detection
          globalUrl={globalUrl}
          ruleInfo={ruleInfo}
          folderDisabled={folderDisabled}
          setFolderDisabled={setFolderDisabled}
          openEditBar={openEditBar}
          isTenzirActive={isTenzirActive}
        />
      ) : (
        <Typography variant="h6">
          No rules found. Please wait while rules are fetched.
        </Typography>
      )}
    </Container>
  );
};

export default DetectionDashBoard;
